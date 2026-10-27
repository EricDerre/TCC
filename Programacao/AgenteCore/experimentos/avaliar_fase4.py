#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): a avaliação da corrida 17 (reprodução na
# tela), no molde de analisar_fase3b.py e pre_fase4.py: lê `reproducao.jsonl` e `fora.json` da pasta da corrida,
# resume por classe, por nível e por modo (quantos casos a tela reproduz, regra R1), o custo de um cenário em segundos
# e os tamanhos (árvore antes e depois, corpo, caso ao vivo), e grava `resultados_alvo/fase4/reproducibilidade.{json,md}`
# com os blocos `tb_f4_reproducao_*`, com `--check` e `--colar` como os outros avaliadores.
# ! Motivo: nenhum número do relatório da Fase 4 é digitado à mão (regra do projeto); o que a corrida 17 mede entra
# no roadmap, no relatório da fase e no painel por estes blocos, com a origem de cada número no JSON.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --reproducao --saida fase4_reproducao [--check] [--colar]"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import analisar_fase3b as a3b
import caminhos
import pre_fase4 as pf

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

NOME = "reproducibilidade"
PREFIXO = "tb_f4_reproducao_"
RELATORIO = caminhos.AQUI.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-4-relatorio.md"


def pasta_fase4() -> Path:
    return caminhos.RESULTADOS / "fase4"


def ler(saida: str) -> tuple[list[dict], list[dict]]:
    raiz = caminhos.fase3(saida)["raiz"]
    arq = raiz / "reproducao.jsonl"
    registros = [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()] if arq.exists() else []
    arq_fora = raiz / "fora.json"
    fora = json.loads(arq_fora.read_text(encoding="utf-8")) if arq_fora.exists() else []
    return registros, fora


def _pct(parte: int, total: int) -> float | None:
    return round(100 * parte / total, 1) if total else None


def _mediana(valores: list) -> float | None:
    v = [x for x in valores if isinstance(x, (int, float))]
    return round(statistics.median(v), 3) if v else None


def resumir(registros: list[dict], fora: list[dict], gerado_em: str | None = None, corrida: str | None = None) -> dict:
    """O resumo da reprodução: totais, por classe, por nível, por modo, tempo por cenário e tamanhos."""
    na_tela = len(registros)
    reproduzem = sum(1 for r in registros if r.get("reproduz"))
    casos = na_tela + len(fora)
    classes = sorted({int(r["classe"]) for r in registros} | {int(f["classe"]) for f in fora})
    niveis = sorted({int(r["nivel"]) for r in registros} | {int(f["nivel"]) for f in fora})

    def linha(chave: str, valor: int) -> dict:
        dentro = [r for r in registros if int(r[chave]) == valor]
        de_fora = [f for f in fora if int(f[chave]) == valor]
        rep = sum(1 for r in dentro if r.get("reproduz"))
        return {chave: valor, "casos": len(dentro) + len(de_fora), "na_tela": len(dentro), "reproduzem": rep, "fora": len(de_fora),
                "reproduzem_pct": _pct(rep, len(dentro) + len(de_fora))}

    modos = Counter(r["modo"] for r in registros)
    por_modo = [{"modo": m, "casos": n, "reproduzem": sum(1 for r in registros if r["modo"] == m and r.get("reproduz")),
                 "motivos": sorted({r["motivo"] for r in registros if r["modo"] == m})} for m, n in sorted(modos.items())]
    motivos_fora = Counter(f["motivo"].split(":")[0] for f in fora)
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": corrida,
                          "fonte": "reproducao.jsonl e fora.json gravados por executar_fase4.py --modo reproducao"},
            "resumo": {"casos": casos, "na_tela": na_tela, "reproduzem": reproduzem, "fora": len(fora),
                       "reproduzem_pct": _pct(reproduzem, casos), "reproduzem_dos_na_tela_pct": _pct(reproduzem, na_tela),
                       "roteiro_falhou": sum(1 for r in registros if not r.get("passou_o_roteiro", True)),
                       "com_erro": sum(1 for r in registros if r.get("erro"))},
            "por_classe": [linha("classe", c) for c in classes],
            "por_nivel": [linha("nivel", n) for n in niveis],
            "por_modo": por_modo,
            "fora_por_motivo": [{"motivo": m, "casos": n} for m, n in sorted(motivos_fora.items())],
            "tempo": {"mediana_s": _mediana([r.get("segundos") for r in registros]), "max_s": max([r.get("segundos") or 0 for r in registros], default=None),
                      "soma_s": round(sum(r.get("segundos") or 0 for r in registros), 1), "tempo_api_mediana_ms": _mediana([r.get("tempo_ms") for r in registros])},
            "tamanhos": {"arvore_antes_mediana": _mediana([r.get("arvore_antes") for r in registros]),
                         "arvore_depois_mediana": _mediana([r.get("arvore_depois") for r in registros]),
                         "corpo_chars_mediana": _mediana([r.get("corpo_chars") for r in registros]),
                         "caso_chars_mediana": _mediana([r.get("caso_chars") for r in registros])},
            "casos": [{k: r.get(k) for k in ("id", "classe", "nivel", "causa", "modo", "campo", "cenario", "reproduz", "motivo", "status",
                                               "tempo_ms", "segundos", "arvore_antes", "arvore_depois", "corpo_chars", "caso_chars", "erro")} for r in registros],
            "fora": fora}


def render(dado: dict) -> str:
    f = a3b.f
    r = dado["resumo"]

    def n(v) -> str:
        return "não medido" if v is None else (f(v) if isinstance(v, float) else str(v))

    blocos = [
        a3b.tab("tb_f4_reproducao_resumo", ["Casos de avaliação", "Com tela e modo", "Reproduzem na tela", "Fora (sem tela, sem modo ou pelo harness)",
                                            "Reproduzem (% dos casos)", "Reproduzem (% dos com tela)", "Roteiro falhou", "Com erro do harness"],
                [[str(r["casos"]), str(r["na_tela"]), str(r["reproduzem"]), str(r["fora"]), n(r["reproduzem_pct"]), n(r["reproduzem_dos_na_tela_pct"]),
                  str(r["roteiro_falhou"]), str(r["com_erro"])]]),
        a3b.tab("tb_f4_reproducao_por_classe", ["Classe", "Casos", "Com tela e modo", "Reproduzem", "Fora", "Reproduzem (%)"],
                [[str(x["classe"]), str(x["casos"]), str(x["na_tela"]), str(x["reproduzem"]), str(x["fora"]), n(x["reproduzem_pct"])] for x in dado["por_classe"]]),
        a3b.tab("tb_f4_reproducao_por_nivel", ["Nível", "Casos", "Com tela e modo", "Reproduzem", "Fora", "Reproduzem (%)"],
                [[str(x["nivel"]), str(x["casos"]), str(x["na_tela"]), str(x["reproduzem"]), str(x["fora"]), n(x["reproduzem_pct"])] for x in dado["por_nivel"]]),
        a3b.tab("tb_f4_reproducao_por_modo", ["Modo de injeção", "Casos", "Reproduzem", "Motivos registrados"],
                [[f"`{x['modo']}`", str(x["casos"]), str(x["reproduzem"]), "; ".join(x["motivos"])] for x in dado["por_modo"]]),
        a3b.tab("tb_f4_reproducao_custo", ["Tempo por cenário (mediana, s)", "Tempo por cenário (máximo, s)", "Tempo total dos cenários (s)",
                                           "Tempo da chamada à API (mediana, ms)", "Árvore antes da poda (mediana, nós)", "Árvore depois (mediana, linhas)",
                                           "Corpo HTTP (mediana, caracteres)", "Caso ao vivo (mediana, caracteres)"],
                [[n(dado["tempo"]["mediana_s"]), n(dado["tempo"]["max_s"]), n(dado["tempo"]["soma_s"]), n(dado["tempo"]["tempo_api_mediana_ms"]),
                  n(dado["tamanhos"]["arvore_antes_mediana"]), n(dado["tamanhos"]["arvore_depois_mediana"]), n(dado["tamanhos"]["corpo_chars_mediana"]),
                  n(dado["tamanhos"]["caso_chars_mediana"])]]),
        a3b.tab("tb_f4_reproducao_casos", ["Caso", "Classe", "Nível", "Causa", "Modo", "Campo", "Cenário", "Reproduz", "Motivo", "Status", "Segundos"],
                [[f"`{c['id']}`", str(c["classe"]), str(c["nivel"]), f"`{c['causa']}`", f"`{c['modo']}`", f"`{c['campo']}`" if c.get("campo") else "",
                  c["cenario"], "sim" if c["reproduz"] else "não", c["motivo"], n(c.get("status")), n(c.get("segundos"))] for c in dado["casos"]]),
        a3b.tab("tb_f4_reproducao_fora", ["Caso", "Classe", "Nível", "Causa", "Por que ficou fora"],
                [[f"`{x['id']}`", str(x["classe"]), str(x["nivel"]), f"`{x['causa']}`", x["motivo"]] for x in dado["fora"]]),
    ]
    cab = pf.cabecalho("Reprodução dos casos na tela (corrida 17)", "avaliar_fase4.py", "reproducao.jsonl e fora.json da corrida",
                       dado["metadados"]["gerado_em"][:10])
    cab += ["", "Um caso reproduz na tela quando a chamada à CobaiaAPI sai do normal (status, corpo, contrato ou tempo acima do orçamento) "
                "ou quando uma conferência do roteiro falha (regra R1 do plano aprovado). Os casos fora são os de rota sem página "
                "(pedidos), os de causa sem modo de injeção e os de quebra de localizador, que o harness arma (ficha 29).", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reproducao", action="store_true", help="avalia a corrida 17 (reprodução na tela)")
    ap.add_argument("--saida", default="fase4_reproducao")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--colar", action="store_true")
    args = ap.parse_args()
    print(caminhos.descricao())
    if not args.reproducao:
        ap.error("informe --reproducao")
    registros, fora = ler(args.saida)
    if not registros and not fora:
        print(f"sem reproducao.jsonl em {caminhos.fase3(args.saida)['raiz']}")
        return 2
    dado = resumir(registros, fora, corrida=args.saida)
    return pf.fechar(NOME, dado, render(dado), PREFIXO, check=args.check, colar=args.colar, pasta=pasta_fase4(), doc=RELATORIO)


if __name__ == "__main__":
    sys.exit(main())
