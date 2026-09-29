#!/usr/bin/env python3
# ! Alteração de IA - Revisar: curadoria da biblioteca L1 do qwen2.5:7b (29/09/2026; ficha 2 de
# pendencias.md, opção (a) decidida pelo Eric). Dois passos: --listar escreve a planilha de
# curadoria com as 40 edições aceitas na época 1, na ordem em que entraram, já com os 10 vereditos
# da planilha oficial de revisão e as outras 30 em branco; --curar refaz a biblioteca a partir da
# epoca-0 reaplicando só as edições cujo veredito não está na lista --remover (padrão: Errada),
# depois de conferir que reaplicar TODAS reproduz o hash oficial da epoca-1, e grava a cópia curada
# com curadoria.json (o que saiu, com o motivo, e o hash antes/depois).
# ! Motivo: a decisão 52 escolheu a L1, mas a revisão leu só 10 das 40 edições dessa época e achou
# 3 erradas; levar a L1 como está para a Fase 4 é levar notas erradas que o agente vai seguir. As
# edições foram gravadas só por acréscimo, então a forma segura de tirar uma é NÃO reaplicá-la: a
# biblioteca curada é reconstruída do zero com a mesma função (aplicar_edicao) e na mesma ordem
# que a bateria usou — e a conferência do hash prova que a reconstrução é fiel antes de qualquer
# edição ser retirada. O snapshot oficial da epoca-1 não é tocado.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python curar_biblioteca.py --listar
  RESULTADOS_DIR=resultados_alvo python curar_biblioteca.py --curar --destino ../biblioteca_producao
  (--modelo qwen2.5:7b --epoca 1 são os padrões; --remover Errada,Parcial tira também as parciais)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import biblioteca as bib
import caminhos
import evolucao_biblioteca as evo
import executar_fase3
import validar_banco

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

VEREDITOS = ("Correta", "Parcial", "Errada")
CABECALHO = "| # | Caso | Verbete | Operação | Texto | Motivo | Avaliação | Comentário | Origem |"
SEPARADOR = "|---|---|---|---|---|---|---|---|---|"


# ------------------------------------------------------------------ leitura dos registros

def edicoes_aceitas(c3: dict, modelo: str, epoca: int) -> list[dict]:
    """As edições aceitas na época, na ordem em que entraram na biblioteca (ordem do JSONL de
    propostas, e dentro de cada rodada a ordem das decisões)."""
    arq = c3["raiz"] / executar_fase3._slug(modelo) / f"propostas__E{epoca}.jsonl"
    saida = []
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        r = json.loads(linha)
        for d in r.get("decisoes", []):
            if d.get("aceita") and d.get("edicao"):
                saida.append({**d["edicao"], "motivo_validador": d.get("motivo")})
    return saida


def _celulas(linha: str) -> list[str]:
    s = linha.strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") else s
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def _chave(caso: str, verbete: str, operacao: str, texto: str) -> tuple:
    t = re.sub(r"[\s\\]+", "", texto or "")[:60].lower()
    return (caso.strip(), verbete.strip(), operacao.strip(), t)


def vereditos_da_planilha(arquivo: Path, epoca: int) -> dict[tuple, tuple[str, str]]:
    """{(caso, verbete, operação, texto) -> (Avaliação, Comentário)} das linhas da época pedida na
    planilha oficial revisao_edicoes__<slug>.md (colunas # | Época | Caso | Verbete | Operação |
    Texto | Motivo | Avaliação | Comentário)."""
    saida = {}
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|"):
            continue
        c = _celulas(linha)
        if len(c) < 9 or not c[0].isdigit() or c[1] != str(epoca):
            continue
        saida[_chave(c[2], c[3], c[4], c[5])] = (c[7], c[8])
    return saida


def vereditos_da_curadoria(arquivo: Path) -> dict[int, tuple[str, str, str]]:
    """{número da edição -> (Avaliação, Comentário, Origem)} da planilha de curadoria."""
    saida = {}
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|"):
            continue
        c = _celulas(linha)
        if len(c) < 9 or not c[0].isdigit():
            continue
        saida[int(c[0])] = (c[6], c[7], c[8])
    return saida


def _esc(texto: str) -> str:
    return " ".join(str(texto or "").split()).replace("|", "\\|")


# ------------------------------------------------------------------ passo 1: listar

def escrever_planilha(c3: dict, modelo: str, epoca: int, destino: Path) -> tuple[int, int]:
    slug = executar_fase3._slug(modelo)
    edicoes = edicoes_aceitas(c3, modelo, epoca)
    oficial = vereditos_da_planilha(c3["raiz"] / f"revisao_edicoes__{slug}.md", epoca)
    linhas = [
        f"<!-- ! Alteração de IA - Revisar: planilha de CURADORIA da biblioteca L{epoca} do {modelo}, gerada por "
        f"curar_biblioteca.py --listar em {datetime.now().date().isoformat()}: as {len(edicoes)} edições aceitas na "
        f"época {epoca}, na ordem em que entraram; a coluna Origem diz se o veredito veio da planilha oficial de revisão "
        f"(revisao_edicoes__{slug}.md) ou da curadoria.",
        "     ! Motivo: a revisão oficial cobriu uma amostra; para curar a cópia de produção é preciso um veredito por "
        "edição, com o mesmo critério (Correta = verdadeiro sobre o sistema e pertinente; Parcial = vago, recomendação "
        "sem fato novo ou verdade fora de lugar; Errada = afirma o que o código não faz ou atribui a causa a outro "
        "componente). Só as linhas com Avaliação em branco recebem veredito novo; as da planilha oficial não mudam. -->",
        f"# Curadoria da biblioteca L{epoca} — {modelo}",
        "",
        f"Edições aceitas na época {epoca}: {len(edicoes)}. Vereditos já dados na planilha oficial: "
        f"{sum(1 for e in edicoes if _chave(e['caso'], e['verbete'], e['operacao'], e['texto']) in oficial)}. "
        "Política de curadoria (ficha 2, 29/09/2026): sai da cópia de produção toda edição com veredito *Errada*; "
        "*Correta* e *Parcial* ficam.",
        "",
        CABECALHO, SEPARADOR,
    ]
    n_oficial = 0
    for i, e in enumerate(edicoes, 1):
        ver = oficial.get(_chave(e["caso"], e["verbete"], e["operacao"], e["texto"]))
        if ver:
            n_oficial += 1
            aval, coment, origem = ver[0], ver[1], "planilha oficial"
        else:
            aval, coment, origem = "", "", "curadoria"
        linhas.append(f"| {i} | {_esc(e['caso'])} | {_esc(e['verbete'])} | {_esc(e['operacao'])} | {_esc(e['texto'])} | "
                      f"{_esc(e.get('motivo'))} | {_esc(aval)} | {_esc(coment)} | {origem} |")
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8", newline="\n")
    return len(edicoes), n_oficial


# ------------------------------------------------------------------ passo 2: curar

def reconstruir(origem_l0: Path, destino: Path, edicoes: list[dict]) -> str:
    """Copia a epoca-0 para `destino` (que não pode existir), reaplica as edições na ordem dada e
    devolve o hash resultante."""
    evo.copiar_biblioteca(origem_l0, destino)
    for e in edicoes:
        evo.aplicar_edicao(destino, e)
    return evo.hash_biblioteca(destino)


def curar(c3: dict, modelo: str, epoca: int, planilha: Path, destino: Path, remover: tuple[str, ...]) -> dict:
    slug = executar_fase3._slug(modelo)
    raiz_l0 = c3["bibliotecas"] / slug / "epoca-0"
    raiz_ln = c3["bibliotecas"] / slug / f"epoca-{epoca}"
    hash_oficial = json.loads((raiz_ln / "fechamento.json").read_text(encoding="utf-8"))["hash"]
    edicoes = edicoes_aceitas(c3, modelo, epoca)
    vereditos = vereditos_da_curadoria(planilha)
    faltam = [i for i in range(1, len(edicoes) + 1) if not vereditos.get(i, ("",))[0]]
    if faltam:
        raise SystemExit(f"{len(faltam)} edição(ões) sem veredito na planilha: {faltam[:10]}")
    invalidos = {i: v[0] for i, v in vereditos.items() if v[0] not in VEREDITOS}
    if invalidos:
        raise SystemExit(f"veredito fora de Correta/Parcial/Errada: {invalidos}")

    with tempfile.TemporaryDirectory() as tmp:
        h = reconstruir(raiz_l0, Path(tmp) / "todas", edicoes)
    if h != hash_oficial:
        raise SystemExit(f"reaplicar todas as {len(edicoes)} edições dá hash {h}, e o oficial da epoca-{epoca} é "
                         f"{hash_oficial} — a reconstrução não é fiel; nada foi gravado")
    print(f"conferido: reaplicar as {len(edicoes)} edições reproduz o hash oficial da epoca-{epoca} ({hash_oficial})")

    if destino.exists():
        raise SystemExit(f"destino já existe: {destino} — apague-o antes (nada é sobrescrito)")
    mantidas = [e for i, e in enumerate(edicoes, 1) if vereditos[i][0] not in remover]
    removidas = [{"numero": i, "caso": e["caso"], "verbete": e["verbete"], "operacao": e["operacao"],
                  "texto": e["texto"], "avaliacao": vereditos[i][0], "comentario": vereditos[i][1],
                  "origem_do_veredito": vereditos[i][2]}
                 for i, e in enumerate(edicoes, 1) if vereditos[i][0] in remover]
    hash_curada = reconstruir(raiz_l0, destino, mantidas)
    verbetes = bib.carregar(destino)
    validar_banco.escrever_indice(verbetes, destino)
    fechamento = evo.fechar_snapshot(destino, epoca, modelo, aceitas_na_epoca=len(mantidas))
    registro = {
        "_comentario": ("! Alteração de IA - Revisar: registro da curadoria, gravado por curar_biblioteca.py --curar junto "
                        "com a cópia de produção da biblioteca (reconstruída da epoca-0 sem as edições reprovadas). "
                        "! Motivo: diz de que snapshot a cópia veio, o que saiu e por quê, e os dois hashes — sem isso a "
                        "pasta seria uma biblioteca sem origem rastreável; o fechamento.json ao lado é o do próprio "
                        "evolucao_biblioteca (formato congelado da Fase 3, sem campo de comentário)."),
        "origem": f"{raiz_ln.relative_to(caminhos.RESULTADOS.parent)}".replace("\\", "/"),
        "modelo": modelo, "epoca": epoca, "hash_oficial": hash_oficial, "hash_curada": hash_curada,
        "politica": {"remover": list(remover)}, "planilha": planilha.name,
        "edicoes_na_epoca": len(edicoes), "mantidas": len(mantidas), "removidas": removidas,
        "n_verbetes": fechamento["n_verbetes"], "curado_em": datetime.now().isoformat(timespec="seconds"),
    }
    (destino / "curadoria.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    return registro


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modelo", default="qwen2.5:7b")
    ap.add_argument("--epoca", type=int, default=1)
    ap.add_argument("--saida", default="fase3", help="pasta da corrida oficial (caminhos.fase3)")
    ap.add_argument("--listar", action="store_true", help="escreve a planilha de curadoria")
    ap.add_argument("--curar", action="store_true", help="reconstrói a biblioteca curada em --destino")
    ap.add_argument("--destino", default=None, help="pasta da cópia curada (não pode existir)")
    ap.add_argument("--remover", default="Errada", help="vereditos que saem, separados por vírgula")
    args = ap.parse_args()
    c3 = caminhos.fase3(args.saida)
    slug = executar_fase3._slug(args.modelo)
    planilha = c3["raiz"] / f"curadoria_L{args.epoca}__{slug}.md"
    print(caminhos.descricao())
    if args.listar:
        n, n_of = escrever_planilha(c3, args.modelo, args.epoca, planilha)
        print(f"planilha gravada: {planilha} — {n} edições, {n_of} com veredito da planilha oficial, {n - n_of} a revisar")
    if args.curar:
        if not args.destino:
            raise SystemExit("--curar exige --destino")
        remover = tuple(x.strip() for x in args.remover.split(",") if x.strip())
        r = curar(c3, args.modelo, args.epoca, planilha, Path(args.destino).resolve(), remover)
        print(f"curada: {args.destino} — hash {r['hash_curada']} (oficial {r['hash_oficial']}); "
              f"{r['mantidas']} edições mantidas, {len(r['removidas'])} removidas; {r['n_verbetes']} verbetes")
    if not (args.listar or args.curar):
        ap.print_help()


if __name__ == "__main__":
    main()
