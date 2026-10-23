#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (22/10/2026) que replica os arquivos rastreados do commit HEAD deste repositório
# na pasta `projeto/` do clone do repositório do orientador (unicid-projeto-software-2026-2/squad-24-projeto), apaga de
# `projeto/` o que saiu daqui, deixa de fora a `.venv` da CobaiaAPI e a `.claude/`, escreve o commit e a contagem no bloco
# SINCRONIZACAO do README do clone e avisa se algum arquivo copiado seria ignorado pelo `.gitignore` do clone. Ensaio por
# padrão; `--aplicar` grava; `--check` devolve 1 fora de sincronia (para as baterias de verificação).
# ! Motivo: o professor orientador pediu o TCC replicado no repositório da disciplina (decisão 72, 22/10/2026), e este
# repositório continua o principal, onde toda alteração sai primeiro. Copiar à mão milhares de arquivos a cada entrega
# erraria (arquivo editado sem commit indo junto, arquivo apagado aqui sobrevivendo lá); o script copia só o que está no
# commit, compara pelo mesmo hash que o git usa (sha1 de "blob <tamanho>\0<conteúdo>") e o Eric revisa, commita e dá push
# no clone. A `.venv` fica de fora porque estava rastreada por engano até a ficha 22 (sai do rastreio no commit do Eric, decisão 74) e só funciona
# nesta máquina; a `.claude/` porque é configuração do Claude Code com caminhos daqui.
"""Replica o commit HEAD deste repositório em `<clone do orientador>/projeto/`.

Uso (a partir da raiz do repositório principal):
    python ferramentas/sincronizar_orientador.py            # ensaio: só lista o que mudaria
    python ferramentas/sincronizar_orientador.py --aplicar  # copia, apaga o que saiu e atualiza o README do clone
    python ferramentas/sincronizar_orientador.py --check    # 0 em sincronia, 1 fora de sincronia, 2 erro de uso
Opções: --origem (padrão: a raiz deste repositório), --destino (padrão: ../squad-24-projeto), --tudo (lista tudo).
Depois de --aplicar, no clone: git add -A && git commit -m "Sincroniza com o commit <hash> do principal" && git push
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

SUBPASTA = "projeto"
EXCLUSOES = ("Programacao/CobaiaAPI/.venv/", ".claude/")
INICIO = "<!-- SINCRONIZACAO:START -->"
FIM = "<!-- SINCRONIZACAO:END -->"
LIMITE_LISTA = 15


class ErroDeUso(Exception):
    """Origem ou destino inválidos: o chamador decide como avisar."""


@dataclass
class Relatorio:
    commit: str = ""
    data: str = ""
    sujo: bool = False
    aplicado: bool = False
    novos: list[str] = field(default_factory=list)
    alterados: list[str] = field(default_factory=list)
    removidos: list[str] = field(default_factory=list)
    iguais: int = 0
    excluidos: list[str] = field(default_factory=list)
    ignorados_no_destino: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    @property
    def em_sincronia(self) -> bool:
        return not (self.novos or self.alterados or self.removidos)


def git(pasta: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(pasta), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def hash_blob(dados: bytes) -> str:
    """O mesmo hash que o git dá a um arquivo: sha1 de "blob <tamanho>\\0" seguido do conteúdo."""
    h = hashlib.sha1(b"blob %d\0" % len(dados))
    h.update(dados)
    return h.hexdigest()


def hash_arquivo(caminho: Path) -> str | None:
    if not caminho.is_file():
        return None
    return hash_blob(caminho.read_bytes())


def excluido(caminho: str) -> bool:
    return caminho.startswith(EXCLUSOES)


def listar_rastreados(origem: Path, relatorio: Relatorio) -> list[tuple[str, str]]:
    """Pares (caminho, sha) dos blobs do commit HEAD, já sem as exclusões; submódulo e link simbólico viram aviso."""
    pares: list[tuple[str, str]] = []
    for item in git(origem, "ls-tree", "-r", "-z", "HEAD").split("\0"):
        if not item:
            continue
        meta, caminho = item.split("\t", 1)
        modo, tipo, sha = meta.split()
        if excluido(caminho):
            relatorio.excluidos.append(caminho)
            continue
        if tipo != "blob" or modo == "120000":
            relatorio.avisos.append(f"{caminho}: {tipo} de modo {modo} não é copiado (submódulo ou link simbólico)")
            continue
        pares.append((caminho, sha))
    return pares


def escrever_blobs(origem: Path, alvo: Path, pares: list[tuple[str, str]]) -> None:
    """Grava cada blob em alvo/<caminho>, lendo todos de um único `git cat-file --batch`."""
    if not pares:
        return
    proc = subprocess.Popen(["git", "-C", str(origem), "cat-file", "--batch"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert proc.stdin is not None and proc.stdout is not None
    entrada = "".join(sha + "\n" for _, sha in pares).encode("ascii")

    def alimentar() -> None:  # escreve a lista numa thread para o git não travar com a saída cheia
        proc.stdin.write(entrada)
        proc.stdin.close()

    threading.Thread(target=alimentar, daemon=True).start()
    for caminho, sha in pares:
        cabecalho = proc.stdout.readline().decode("ascii").split()
        if len(cabecalho) != 3 or cabecalho[0] != sha:
            raise RuntimeError(f"resposta inesperada do git cat-file para {caminho}: {cabecalho}")
        tamanho = int(cabecalho[2])
        dados = proc.stdout.read(tamanho)
        proc.stdout.read(1)  # quebra de linha que fecha cada objeto
        if len(dados) != tamanho:
            raise RuntimeError(f"{caminho}: esperados {tamanho} bytes, lidos {len(dados)}")
        destino = alvo / caminho
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(dados)
    proc.stdout.close()
    proc.wait()


def remover(alvo: Path, caminhos: list[str]) -> None:
    for rel in caminhos:
        (alvo / rel).unlink()
    pastas = sorted((p for p in alvo.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True)
    for pasta in pastas:  # de baixo para cima; rmdir só apaga pasta vazia
        try:
            pasta.rmdir()
        except OSError:
            pass


def ignorados_pelo_clone(destino: Path, caminhos: list[str]) -> list[str]:
    """Caminhos (relativos a projeto/) que o .gitignore do clone ignoraria; `--no-index` olha só as regras, não o índice."""
    if not caminhos:
        return []
    entrada = "".join(f"{SUBPASTA}/{c}\0" for c in caminhos).encode("utf-8")
    proc = subprocess.run(["git", "-C", str(destino), "check-ignore", "--no-index", "--stdin", "-z"],
                          input=entrada, capture_output=True)
    if proc.returncode not in (0, 1):  # 0: algum ignorado; 1: nenhum
        raise RuntimeError(proc.stderr.decode("utf-8", "replace").strip())
    prefixo = SUBPASTA + "/"
    return sorted(item[len(prefixo):] for item in proc.stdout.decode("utf-8").split("\0") if item.startswith(prefixo))


def atualizar_readme(destino: Path, relatorio: Relatorio, total: int) -> None:
    readme = destino / "README.md"
    if not readme.is_file():
        relatorio.avisos.append("README.md do clone não encontrado; bloco SINCRONIZACAO não atualizado")
        return
    texto = readme.read_bytes().decode("utf-8")
    if INICIO not in texto or FIM not in texto:
        relatorio.avisos.append(f"README.md do clone sem os marcadores {INICIO} e {FIM}; bloco SINCRONIZACAO não atualizado")
        return
    quebra = "\r\n" if "\r\n" in texto else "\n"
    hoje = date.today().strftime("%d/%m/%Y")
    linha = (f"Ultima sincronizacao: commit `{relatorio.commit}` do repositorio principal (EricDerre/TCC), "
             f"de {relatorio.data}, aplicada em {hoje}: {total} arquivos em `{SUBPASTA}/`.")
    antes, resto = texto.split(INICIO, 1)
    _, depois = resto.split(FIM, 1)
    readme.write_bytes((antes + INICIO + quebra + linha + quebra + FIM + depois).encode("utf-8"))


def sincronizar(origem: Path, destino: Path, aplicar: bool) -> Relatorio:
    origem, destino = Path(origem).resolve(), Path(destino).resolve()
    if not (origem / ".git").exists():
        raise ErroDeUso(f"origem sem .git: {origem}")
    if not (destino / ".git").exists():
        raise ErroDeUso(f"destino não é um clone git: {destino}")
    rel = Relatorio()
    rel.commit = git(origem, "rev-parse", "--short", "HEAD").strip()
    rel.data = git(origem, "log", "-1", "--date=format:%d/%m/%Y", "--format=%cd", "HEAD").strip()
    rel.sujo = bool(git(origem, "status", "--porcelain").strip())
    pares = listar_rastreados(origem, rel)
    alvo = destino / SUBPASTA
    pendentes: list[tuple[str, str]] = []
    for caminho, sha in pares:
        atual = hash_arquivo(alvo / caminho)
        if atual == sha:
            rel.iguais += 1
            continue
        (rel.novos if atual is None else rel.alterados).append(caminho)
        pendentes.append((caminho, sha))
    conhecidos = {caminho for caminho, _ in pares}
    if alvo.is_dir():
        rel.removidos = sorted(p.relative_to(alvo).as_posix() for p in alvo.rglob("*")
                               if p.is_file() and p.relative_to(alvo).as_posix() not in conhecidos)
    rel.novos.sort()
    rel.alterados.sort()
    rel.excluidos.sort()
    if aplicar:
        escrever_blobs(origem, alvo, pendentes)
        remover(alvo, rel.removidos)
        rel.ignorados_no_destino = ignorados_pelo_clone(destino, sorted(conhecidos))
        atualizar_readme(destino, rel, len(pares))
        rel.aplicado = True
    return rel


def listar(titulo: str, itens: list[str], tudo: bool) -> None:
    if not itens:
        return
    mostrados = itens if tudo else itens[:LIMITE_LISTA]
    print(f"  {titulo} ({len(itens)}):")
    for item in mostrados:
        print(f"    {item}")
    if len(itens) > len(mostrados):
        print(f"    ... e mais {len(itens) - len(mostrados)} (use --tudo para ver todos)")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raiz = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--origem", type=Path, default=raiz, help="raiz do repositório principal (padrão: este)")
    ap.add_argument("--destino", type=Path, default=raiz.parent / "squad-24-projeto",
                    help="clone do repositório do orientador (padrão: ../squad-24-projeto)")
    modo = ap.add_mutually_exclusive_group()
    modo.add_argument("--aplicar", action="store_true", help="grava no clone (sem isso é só ensaio)")
    modo.add_argument("--check", action="store_true", help="sai com 1 se a cópia estiver fora de sincronia")
    ap.add_argument("--tudo", action="store_true", help="lista todos os arquivos de cada categoria")
    args = ap.parse_args(argv)
    try:
        rel = sincronizar(args.origem, args.destino, aplicar=args.aplicar)
    except ErroDeUso as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    print(f"Origem: {Path(args.origem).resolve()} (commit {rel.commit} de {rel.data})")
    if rel.sujo:
        print("  aviso: o principal tem alterações sem commit ou arquivos fora do git; a cópia reflete só o commit.")
    print(f"Destino: {Path(args.destino).resolve() / SUBPASTA}")
    rastreados = rel.iguais + len(rel.novos) + len(rel.alterados)
    print(f"Rastreados no commit: {rastreados} | excluídos: {len(rel.excluidos)} ({', '.join(EXCLUSOES)})")
    print(f"Novos: {len(rel.novos)} | alterados: {len(rel.alterados)} | removidos: {len(rel.removidos)} | iguais: {rel.iguais}")
    listar("novos", rel.novos, args.tudo)
    listar("alterados", rel.alterados, args.tudo)
    listar("removidos", rel.removidos, args.tudo)
    for aviso in rel.avisos:
        print(f"  aviso: {aviso}")
    if rel.ignorados_no_destino:
        print(f"  aviso: {len(rel.ignorados_no_destino)} arquivo(s) copiado(s) que o .gitignore do clone ignora "
              "(só entram no commit com git add -f):")
        listar("ignorados", rel.ignorados_no_destino, args.tudo)
    if rel.aplicado:
        print(f"Aplicado: `{SUBPASTA}/` corresponde ao commit {rel.commit} do principal. "
              "No clone: git add -A && git commit && git push")
    elif rel.em_sincronia:
        print(f"Em sincronia: `{SUBPASTA}/` corresponde ao commit {rel.commit} do principal.")
    elif args.check:
        print("Fora de sincronia: rode com --aplicar para copiar.")
        return 1
    else:
        print("Ensaio: nada foi gravado; rode com --aplicar para copiar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
