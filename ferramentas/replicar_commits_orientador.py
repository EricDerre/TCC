#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (03/11/2026) que replica, um a um, os commits do repositório principal que o
# clone do orientador (unicid-projeto-software-2026-2/squad-24-projeto) ainda não tem: lê no bloco SINCRONIZACAO do
# README do clone qual foi o último commit copiado, lista com `git rev-list` os commits do principal depois dele, e, para
# cada um, chama `sincronizar_orientador.sincronizar(..., commit=<hash>)` para regravar `projeto/` como estava naquele
# commit e, com `--aplicar`, faz `git add -A` e `git commit` no clone com a mesma mensagem, a data de autoria original e
# uma linha final dizendo de que commit do principal a réplica veio. Ensaio por padrão (só lista); o push continua do Eric.
# ! Motivo: o Eric pediu em 03/11/2026 "replicar os commits que fizemos no principal para lá também" (decisão 84): o clone
# estava na cópia de 22/10 (`362db9bf`) e o principal tinha cinco commits depois dela; um commit só por sincronização,
# como a rotina da decisão 72 previa, esconderia no histórico do orientador a sequência de entregas (fechamento da
# Pré-Fase 4, início da Fase 4, corridas). O script roda os comandos git só com `--aplicar`, na mão do Eric, porque a
# regra do projeto é que o commit é dele; sem a opção, nada é gravado.
"""Replica commit a commit o repositório principal no clone do orientador.

Uso (na raiz do repositório principal):
    python ferramentas/replicar_commits_orientador.py            # ensaio: lista os commits que faltam e o que cada um mudaria
    python ferramentas/replicar_commits_orientador.py --aplicar  # copia cada commit em projeto/ e commita no clone
Opções: --origem (padrão: este repositório), --destino (padrão: ../squad-24-projeto),
        --desde <hash> (padrão: o commit do bloco SINCRONIZACAO do README do clone), --ate <ref> (padrão: HEAD).
Depois de --aplicar, no clone: git push
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sincronizar_orientador as so

RAIZ = Path(__file__).resolve().parent.parent
RODAPE = "Réplica do commit {hash} do repositório principal (EricDerre/TCC), de {data}."


def git(pasta: Path, *args: str, env: dict | None = None) -> str:
    return subprocess.run(["git", "-C", str(pasta), *args], check=True, capture_output=True, text=True,
                          encoding="utf-8", env=env).stdout


def ultimo_copiado(destino: Path) -> str:
    """O hash gravado por sincronizar_orientador.py no README do clone (linha "Ultima sincronizacao: commit `x`")."""
    readme = destino / "README.md"
    if not readme.is_file():
        raise so.ErroDeUso(f"README.md não encontrado em {destino}")
    texto = readme.read_text(encoding="utf-8")
    m = re.search(rf"{re.escape(so.INICIO)}.*?commit `([0-9a-f]{{7,40}})`", texto, re.DOTALL)
    if not m:
        raise so.ErroDeUso("o README do clone não tem a linha 'Ultima sincronizacao: commit `...`'; use --desde")
    return m.group(1)


def commits_que_faltam(origem: Path, desde: str, ate: str) -> list[str]:
    """Hashes completos, do mais antigo ao mais novo, na linha principal (`--first-parent`) entre `desde` e `ate`."""
    try:
        git(origem, "cat-file", "-e", f"{desde}^{{commit}}")
    except subprocess.CalledProcessError as erro:
        raise so.ErroDeUso(f"commit {desde} não existe no principal") from erro
    saida = git(origem, "rev-list", "--reverse", "--first-parent", f"{desde}..{ate}")
    return [h for h in saida.split() if h]


def mensagem_da_replica(origem: Path, commit: str) -> tuple[str, str, str]:
    corpo = git(origem, "log", "-1", "--format=%B", commit).strip()
    data = git(origem, "log", "-1", "--date=format:%d/%m/%Y", "--format=%ad", commit).strip()
    data_autor = git(origem, "log", "-1", "--format=%aI", commit).strip()
    curto = git(origem, "rev-parse", "--short", commit).strip()
    return corpo + "\n\n" + RODAPE.format(hash=curto, data=data), data_autor, curto


def replicar(origem: Path, destino: Path, desde: str | None, ate: str, aplicar: bool) -> int:
    origem, destino = Path(origem).resolve(), Path(destino).resolve()
    if not (destino / ".git").exists():
        raise so.ErroDeUso(f"destino não é um clone git: {destino}")
    desde = desde or ultimo_copiado(destino)
    if aplicar and git(destino, "status", "--porcelain").strip():
        raise so.ErroDeUso("o clone tem alterações sem commit; commite ou descarte antes de replicar")
    faltam = commits_que_faltam(origem, desde, ate)
    print(f"Clone: {destino} (último commit copiado: {desde[:8]})")
    if not faltam:
        print("Nada a replicar: o clone já tem todos os commits do principal.")
        return 0
    print(f"{len(faltam)} commit(s) a replicar, do mais antigo ao mais novo:")
    for n, commit in enumerate(faltam, 1):
        mensagem, data_autor, curto = mensagem_da_replica(origem, commit)
        assunto = mensagem.split("\n", 1)[0]
        rel = so.sincronizar(origem, destino, aplicar=aplicar, commit=commit)
        print(f"  {n}. {curto} ({rel.data}) {assunto}")
        print(f"     novos: {len(rel.novos)} | alterados: {len(rel.alterados)} | removidos: {len(rel.removidos)} | iguais: {rel.iguais}")
        for aviso in rel.avisos:
            print(f"     aviso: {aviso}")
        if rel.ignorados_no_destino:
            print(f"     aviso: {len(rel.ignorados_no_destino)} arquivo(s) que o .gitignore do clone ignora (entram só com git add -f)")
        if not aplicar:
            continue
        git(destino, "add", "-A", "--", so.SUBPASTA, "README.md")
        if not git(destino, "status", "--porcelain").strip():
            print("     nada mudou no clone com este commit (só arquivos excluídos da cópia); commit não criado")
            continue
        env = dict(os.environ, GIT_AUTHOR_DATE=data_autor)
        git(destino, "commit", "-q", "-m", mensagem, env=env)
        print(f"     commit criado no clone: {git(destino, 'rev-parse', '--short', 'HEAD').strip()}")
    if aplicar:
        print(f"Pronto. No clone: git -C \"{destino}\" push")
    else:
        print("Ensaio: nada foi gravado nem commitado; rode com --aplicar para replicar (os commits saem com o seu usuário do git).")
    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--origem", type=Path, default=RAIZ)
    ap.add_argument("--destino", type=Path, default=RAIZ.parent / "squad-24-projeto")
    ap.add_argument("--desde", default=None, help="hash do último commit já copiado (padrão: o do README do clone)")
    ap.add_argument("--ate", default="HEAD", help="último commit a replicar (padrão: HEAD)")
    ap.add_argument("--aplicar", action="store_true", help="grava e commita no clone (sem isso é só ensaio)")
    args = ap.parse_args(argv)
    try:
        return replicar(args.origem, args.destino, args.desde, args.ate, args.aplicar)
    except so.ErroDeUso as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as erro:
        print(f"erro do git: {erro.stderr or erro}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
