#!/usr/bin/env python3
# ! Alteração de IA - Revisar: validação automática de tudo que a Fase 2-B consome antes de
# gastar horas de CPU: os 90 casos contra a taxonomia, a biblioteca (esquema, referências,
# cobertura, sobreposição com casos) e a qualidade da recuperação contra o gabarito.
# ! Motivo: taxonomia.validar_caso existia mas nunca rodava sozinha; e a biblioteca é texto
# escrito à mão, onde um caminho de arquivo inventado ou um verbete que copia um caso não
# seria notado sem checagem. A avaliação de recuperação roda OFFLINE (sem inferência), o que
# permite testar k e o embedding denso sem custo de LLM. Também gera o INDICE.md humano.
import argparse
import math
import sys
from pathlib import Path

import biblioteca as bib
import recuperacao as rec
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from taxonomia import validar_caso

TODOS = CASOS + CASOS_EXTRA


def validar_casos() -> int:
    erros = 0
    ids = [c["id"] for c in TODOS]
    for dup in {i for i in ids if ids.count(i) > 1}:
        print(f"  caso com id repetido: {dup}")
        erros += 1
    for c in TODOS:
        for p in validar_caso(c):
            print(f"  {c['id']}: {p}")
            erros += 1
    return erros


def _cosseno(a: list[float], b: list[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    den = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return num / den if den else 0.0


def pontuador_embedding(verbetes: list[dict], modelo: str):
    """Ordena verbetes por cosseno entre o embedding da consulta do caso e o de cada
    verbete (pelo /api/embed do Ollama). Só para a ablação de recuperação."""
    import cliente_ollama as oll
    residentes = [m["nome"] for m in oll.residentes()]
    if any(not n.startswith(modelo.split(":")[0]) for n in residentes):
        sys.exit(f"outro modelo residente ({residentes}) — rode a ablação de embedding "
                 "depois da bateria (um modelo por vez)")
    vetores = [oll.embed(modelo, rec._texto_indexavel(v)) for v in verbetes]

    def pontuar(caso):
        q = oll.embed(modelo, " ".join(rec.sinais_do_caso(caso)["consulta"]))
        ordem = sorted(zip(verbetes, vetores), key=lambda vv: (-_cosseno(q, vv[1]), vv[0]["id"]))
        return [v for v, _ in ordem]
    return pontuar


def escrever_indice(verbetes: list[dict]) -> Path:
    linhas = [
        "<!-- ! Alteração de IA - Revisar: índice humano da biblioteca, GERADO por",
        "     validar_banco.py --indice a partir do frontmatter dos verbetes; não editar à mão.",
        "     ! Motivo: o modelo recebe os verbetes renderizados, não este arquivo — ele existe",
        "     para quem revisa a biblioteca enxergar cobertura e tipos num lugar só. -->",
        "", "# Índice da biblioteca base", "",
        f"{len(verbetes)} verbetes. {bib.resumo(verbetes)}", "",
        "| Pasta | Id | Título | Tipo | Causas |", "|---|---|---|---|---|",
    ]
    for v in sorted(verbetes, key=lambda v: (v["pasta"], v["id"])):
        m = v["meta"]
        causas = [m["causa_raiz"]] if m.get("causa_raiz") else m.get("causas_relacionadas", [])
        linhas.append(f"| {v['pasta']} | `{v['id']}` | {m.get('titulo', '')} | {m.get('tipo', '')} "
                      f"| {', '.join(causas)} |")
    destino = bib.BASE / "INDICE.md"
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return destino


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--embedding", metavar="MODELO",
                    help="também avalia a recuperação por embedding denso (ex.: embeddinggemma:300m)")
    ap.add_argument("--indice", action="store_true", help="regrava base_conhecimento/INDICE.md")
    args = ap.parse_args()

    print("== casos ==")
    e_casos = validar_casos()
    print(f"  {len(TODOS)} casos, {e_casos} problema(s)")

    print("\n== biblioteca ==")
    verbetes = bib.carregar()
    print(f"  {bib.resumo(verbetes)}")
    probs = bib.validar(verbetes, TODOS)
    for p in probs:
        print("  -", p)
    print(f"  {len(probs)} problema(s)")

    # As duas variantes são reportadas de propósito: a diferença entre elas é o ganho dos
    # sinais calculados em código, e entra no Memorial como resultado.
    for rotulo, usar in (("só texto do sintoma", False), ("texto + sinais em código", True)):
        rec.USAR_SINAIS_DETERMINISTICOS = usar
        print(f"\n== recuperação BM25: {rotulo} ==")
        r = rec.avaliar_recuperacao(verbetes, TODOS)
        print("  " + "  ".join(f"{k}={v}" for k, v in r.items() if k != "posicao_por_caso"))
        fora = sorted(((p or 99, cid) for cid, p in r["posicao_por_caso"].items()),
                      reverse=True)[:8]
        print("  piores (posição do verbete de ouro):",
              ", ".join(f"{cid}:{p}" for p, cid in fora))
    rec.USAR_SINAIS_DETERMINISTICOS = True

    if args.embedding:
        print(f"\n== recuperação por embedding ({args.embedding}) ==")
        r2 = rec.avaliar_recuperacao(verbetes, TODOS,
                                     pontuador=pontuador_embedding(verbetes, args.embedding))
        print("  " + "  ".join(f"{k}={v}" for k, v in r2.items() if k != "posicao_por_caso"))

    if args.indice:
        print(f"\nINDICE.md regravado em {escrever_indice(verbetes)}")

    if e_casos or probs:
        sys.exit(1)
    print("\ntudo válido")


if __name__ == "__main__":
    main()
