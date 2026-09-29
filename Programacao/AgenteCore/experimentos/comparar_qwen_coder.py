#!/usr/bin/env python3
# ! Alteração de IA - Revisar: comparativo qwen2.5:7b × qwen2.5-coder:7b em todas as fases medidas
# (29/09/2026; pedido do Eric na ficha 4: "análise comparativa profunda ... pode ser que em alguns
# cenários o coder seja mais interessante"). Lê os registros oficiais (2-A no Ryzen, 2-B e Fase 3 na
# máquina-alvo, ponte de versão, decisão) e grava comparativo_qwen_coder.json (registro) e
# comparativo_qwen_coder.md (blocos `<!-- tabela:cq_… -->` que o Memorial cola; --check regera e
# compara). Inclui o confronto direto caso a caso (McNemar exato) na Fase 3 e na 2-B, que os resumos
# oficiais não trazem, e a tabela "onde o Coder vence" com toda célula em que ele fica à frente.
# ! Motivo: regra do projeto — nenhum número digitado à mão: a análise comparativa (documento do
# Memorial) só pode citar o que sai daqui. O confronto caso a caso é o que responde se a vantagem do
# Coder em algumas células é diferença real ou ruído: dois modelos com o mesmo acerto médio podem
# acertar casos diferentes, e é isso que o McNemar pareado mede.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python comparar_qwen_coder.py [--check]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import avaliar
import caminhos
import taxonomia

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

A, B = "qwen2.5:7b", "qwen2.5-coder:7b"
EXP = Path(__file__).resolve().parent
RES = caminhos.RESULTADOS
F3 = caminhos.fase3("fase3")
SAIDA_JSON = F3["raiz"] / "comparativo_qwen_coder.json"
SAIDA_MD = F3["raiz"] / "comparativo_qwen_coder.md"
CLASSES = {str(k): (v.get("id", str(k)) if isinstance(v, dict) else str(v)) for k, v in taxonomia.CLASSES.items()}
NIVEIS = {"1": "fácil", "2": "médio", "3": "difícil"}


def ler(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def pick(lista: list[dict], **cond) -> dict | None:
    for x in lista:
        if all(x.get(k) == v for k, v in cond.items()):
            return x
    return None


def _num(x, chave):
    return None if x is None else x.get(chave)


def delta(a, b):
    return None if a is None or b is None else round(b - a, 1)


def mcnemar(b: int, c: int) -> float:
    try:
        return round(float(avaliar.mcnemar_exato(b, c)), 4)
    except TypeError:
        r = avaliar.mcnemar_exato(b, c)
        return round(float(r[0] if isinstance(r, (list, tuple)) else r), 4)


# ------------------------------------------------------------------ blocos de dados

def bloco_2a(m2a: dict) -> list[dict]:
    """Fase 2-A (máquina de desenvolvimento, Ryzen): acerto por estratégia de prompt."""
    linhas = []
    for est in ("linear", "compilador", "dominio"):
        xa, xb = pick(m2a["por_modelo_estrategia"], modelo=A, estrategia=est), pick(m2a["por_modelo_estrategia"], modelo=B, estrategia=est)
        linhas.append({"contexto": f"2-A · estratégia {est}", "n": _num(xa, "n"), "acerto_A": _num(xa, "causa_correta_pct"),
                       "acerto_B": _num(xb, "causa_correta_pct"), "delta": delta(_num(xa, "causa_correta_pct"), _num(xb, "causa_correta_pct")),
                       "s_A": _num(xa, "segundos_mediana"), "s_B": _num(xb, "segundos_mediana"),
                       "fmt_err_A": _num(xa, "formato_ok_conteudo_errado_pct"), "fmt_err_B": _num(xb, "formato_ok_conteudo_errado_pct")})
    return linhas


def bloco_2b_condicoes(m2b: dict) -> list[dict]:
    linhas = []
    for cond in ("A0", "A1", "A2", "A3", "A4", "A5"):
        xa, xb = pick(m2b["por_modelo_condicao"], modelo=A, condicao=cond), pick(m2b["por_modelo_condicao"], modelo=B, condicao=cond)
        if not xa and not xb:
            continue
        ca, cb = pick(m2b["comparacoes"], modelo=A, condicao=cond), pick(m2b["comparacoes"], modelo=B, condicao=cond)
        linhas.append({"contexto": f"2-B · {cond}", "n": _num(xa, "n"), "acerto_A": _num(xa, "causa_correta_pct"), "acerto_B": _num(xb, "causa_correta_pct"),
                       "delta": delta(_num(xa, "causa_correta_pct"), _num(xb, "causa_correta_pct")),
                       "s_A": _num(xa, "segundos_mediana"), "s_B": _num(xb, "segundos_mediana"),
                       "fmt_err_A": _num(xa, "formato_ok_conteudo_errado_pct"), "fmt_err_B": _num(xb, "formato_ok_conteudo_errado_pct"),
                       "vs_A0_A": None if not ca else f'{fd(ca["delta_pp"])} (p = {f(ca["p_mcnemar"], 4)})',
                       "vs_A0_B": None if not cb else f'{fd(cb["delta_pp"])} (p = {f(cb["p_mcnemar"], 4)})'})
    return linhas


def bloco_por_dimensao(lista: list[dict], dim: str, nomes: dict, **fixo) -> list[dict]:
    linhas = []
    for chave in sorted(nomes, key=int):
        xa = pick(lista, modelo=A, **{dim: int(chave)}, **fixo)
        xb = pick(lista, modelo=B, **{dim: int(chave)}, **fixo)
        if not xa and not xb:
            continue
        linhas.append({dim: f"{chave} {nomes[chave]}", "n": _num(xa, "n"), "acerto_A": _num(xa, "causa_correta_pct"),
                       "acerto_B": _num(xb, "causa_correta_pct"), "delta": delta(_num(xa, "causa_correta_pct"), _num(xb, "causa_correta_pct"))})
    return linhas


def bloco_f3_versoes(f3: dict) -> list[dict]:
    linhas = []
    for part, rot in (("avaliacao", "36 de avaliação"), ("aprendizado", "54 de aprendizado"), ("todos", "90")):
        for L in (0, 1, 2, 3):
            xa = pick(f3["por_modelo_biblioteca_particao"], modelo=A, biblioteca_epoca=L, particao=part)
            xb = pick(f3["por_modelo_biblioteca_particao"], modelo=B, biblioteca_epoca=L, particao=part)
            linhas.append({"contexto": f"F3 · L{L} · {rot}", "n": _num(xa, "n"),
                           "acerto_A": _num(xa, "causa_correta_pct"), "acerto_B": _num(xb, "causa_correta_pct"),
                           "delta": delta(_num(xa, "causa_correta_pct"), _num(xb, "causa_correta_pct")),
                           "bal_A": _num(xa, "acuracia_balanceada_pct"), "bal_B": _num(xb, "acuracia_balanceada_pct"),
                           "delta_bal": delta(_num(xa, "acuracia_balanceada_pct"), _num(xb, "acuracia_balanceada_pct")),
                           "s_A": _num(xa, "segundos_mediana"), "s_B": _num(xb, "segundos_mediana"),
                           "fmt_err_A": _num(xa, "formato_ok_conteudo_errado_pct"), "fmt_err_B": _num(xb, "formato_ok_conteudo_errado_pct")})
    return linhas


def confronto_direto_f3(av: list[dict]) -> list[dict]:
    """Caso a caso, mesma versão da biblioteca: b = só o Coder acertou, c = só o qwen2.5:7b acertou."""
    por = defaultdict(dict)
    for r in av:
        if r["modelo"] in (A, B) and not r.get("erro_infra"):
            por[(r["biblioteca_epoca"], r["caso"])][r["modelo"]] = (bool(r["causa_correta"]), r["particao"])
    linhas = []
    for L in (0, 1, 2, 3):
        for part, rot in (("avaliacao", "36 de avaliação"), ("todos", "90")):
            b = c = ambos = nenhum = 0
            for (l, caso), d in por.items():
                if l != L or A not in d or B not in d:
                    continue
                if part != "todos" and d[A][1] != part:
                    continue
                oa, ob = d[A][0], d[B][0]
                b += (ob and not oa); c += (oa and not ob); ambos += (oa and ob); nenhum += (not oa and not ob)
            n = b + c + ambos + nenhum
            linhas.append({"contexto": f"F3 · L{L} · {rot}", "n": n, "ambos": ambos, "nenhum": nenhum,
                           "so_coder": b, "so_qwen": c, "delta_pp": round(100 * (b - c) / n, 1) if n else None,
                           "p_mcnemar": mcnemar(b, c) if (b + c) else 1.0})
    return linhas


def confronto_direto_2b(av2b) -> list[dict]:
    """Mesma leitura na Fase 2-B, se avaliacao.json trouxer registros por caso com modelo, condição e acerto."""
    regs = av2b if isinstance(av2b, list) else (av2b.get("registros") if isinstance(av2b, dict) else None)
    if not regs or not isinstance(regs[0], dict) or not {"modelo", "caso", "condicao", "causa_correta"} <= set(regs[0]):
        return []
    por = defaultdict(dict)
    for r in regs:
        if r["modelo"] in (A, B) and not r.get("erro_infra"):
            por[(r["condicao"], r["caso"])][r["modelo"]] = bool(r["causa_correta"])
    linhas = []
    for cond in ("A0", "A1", "A2", "A3", "A4", "A5"):
        b = c = ambos = nenhum = 0
        for (cd, caso), d in por.items():
            if cd != cond or A not in d or B not in d:
                continue
            oa, ob = d[A], d[B]
            b += (ob and not oa); c += (oa and not ob); ambos += (oa and ob); nenhum += (not oa and not ob)
        n = b + c + ambos + nenhum
        if n:
            linhas.append({"contexto": f"2-B · {cond}", "n": n, "ambos": ambos, "nenhum": nenhum, "so_coder": b, "so_qwen": c,
                           "delta_pp": round(100 * (b - c) / n, 1), "p_mcnemar": mcnemar(b, c) if (b + c) else 1.0})
    return linhas


def bloco_f3_documentacao(f3: dict) -> list[dict]:
    linhas = []
    for E in (1, 2, 3):
        xa, xb = pick(f3["documentacao"], modelo=A, epoca=E), pick(f3["documentacao"], modelo=B, epoca=E)
        linhas.append({"epoca": E, "propostas_A": _num(xa, "n_propostas"), "aceitas_A": _num(xa, "n_aceitas"), "aceitas_pct_A": _num(xa, "aceitas_pct"),
                       "propostas_B": _num(xb, "n_propostas"), "aceitas_B": _num(xb, "n_aceitas"), "aceitas_pct_B": _num(xb, "aceitas_pct"),
                       "tokens_A": _num(xa, "tokens_md_estimados_acrescentados"), "tokens_B": _num(xb, "tokens_md_estimados_acrescentados"),
                       "verbetes_A": (xa or {}).get("biblioteca", {}).get("n_verbetes"), "verbetes_B": (xb or {}).get("biblioteca", {}).get("n_verbetes")})
    rej = {}
    for m in (A, B):
        cnt = Counter()
        for x in f3["documentacao"]:
            if x["modelo"] == m:
                cnt.update(x["motivos_rejeicao"])
        rej[m] = [[k, v] for k, v in cnt.most_common(6)]  # listas, não tuplas: o --check compara com o JSON relido
    return linhas, rej


def bloco_revisao(f3: dict) -> list[dict]:
    linhas = []
    for op in ("nota", "retificacao", "novo_verbete"):
        xa, xb = pick(f3["revisao_humana"], modelo=A, operacao=op), pick(f3["revisao_humana"], modelo=B, operacao=op)
        linhas.append({"operacao": op, **{f"{k}_A": _num(xa, k) for k in ("Correta", "Parcial", "Errada")},
                       **{f"{k}_B": _num(xb, k) for k in ("Correta", "Parcial", "Errada")}})
    return linhas


def bloco_recuperacao(f3: dict) -> list[dict]:
    linhas = []
    for L in (0, 1, 2, 3):
        xa, xb = pick(f3["recuperacao"], modelo=A, biblioteca_epoca=L), pick(f3["recuperacao"], modelo=B, biblioteca_epoca=L)
        linhas.append({"L": L, "hit3_90_A": (xa or {}).get("todos", {}).get("hit@3"), "hit3_90_B": (xb or {}).get("todos", {}).get("hit@3"),
                       "hit3_36_A": (xa or {}).get("avaliacao", {}).get("hit@3"), "hit3_36_B": (xb or {}).get("avaliacao", {}).get("hit@3"),
                       "verbetes_A": _num(xa, "n_verbetes"), "verbetes_B": _num(xb, "n_verbetes")})
    return linhas


def bloco_flips(f3: dict) -> list[dict]:
    linhas = []
    for tr in ("L0→L1", "L1→L2", "L2→L3"):
        for part, rot in (("avaliacao", "36"), ("todos", "90")):
            xa, xb = pick(f3["flips"], modelo=A, transicao=tr, particao=part), pick(f3["flips"], modelo=B, transicao=tr, particao=part)
            linhas.append({"transicao": f"{tr} · {rot}", "autoenv_A": _num(xa, "autoenvenenamento_pct"), "autoenv_B": _num(xb, "autoenvenenamento_pct"),
                           "certo_errado_A": _num(xa, "certo_para_errado"), "errado_certo_A": _num(xa, "errado_para_certo"),
                           "certo_errado_B": _num(xb, "certo_para_errado"), "errado_certo_B": _num(xb, "errado_para_certo")})
    return linhas


def bloco_decisao(d: dict) -> dict:
    rk = [{"pos": i + 1, "modelo": x["modelo"], "L": x["biblioteca_epoca"], "bal_36": x["acuracia_balanceada_36"], "acerto_36": x["acerto_36"],
           "s_36": x["segundos_mediana_36"], "autoenv_max_36": x["autoenvenenamento_max_36"], "risco": x.get("risco"), "vetado": x["vetado"]}
          for i, x in enumerate(d["regra_36"]["ranking"]) if x["modelo"] in (A, B)]
    boot = {}
    for conj in ("nos_36", "nos_90"):
        boot[conj] = {f'{x["modelo"]}/L{x["biblioteca_epoca"]}': {"p_top1": x["p_top1"], "ic": x["ic95_bootstrap"]}
                      for x in d["bootstrap"][conj]["combos"] if x["modelo"] in (A, B)}
    pareto = [f'{x["modelo"]}/L{x["biblioteca_epoca"]}' for x in d["pareto"]["nao_dominados"] if x["modelo"] in (A, B)]
    escore = [{"modelo": x["modelo"], "L": x["biblioteca_epoca"], "score": x["score"]} for x in d["escore_ponderado"]["linhas"] if x["modelo"] in (A, B)]
    estab = {m: d["estabilidade_ranking"]["top1_por_modelo"].get(m) for m in (A, B)}
    ponte = [{"modelo": x["modelo"], "acerto_36": x["acerto_pct"], "bal_36": x["acuracia_balanceada_pct"], "b": x["pareado_vs_f3"]["b"],
              "c": x["pareado_vs_f3"]["c"], "p": x["pareado_vs_f3"]["p_mcnemar"]}
             for x in d["tres_b"].get("fase3b_ponte", {}).get("linhas", []) if x["modelo"] in (A, B)]
    return {"ranking_36": rk, "bootstrap": boot, "pareto_nao_dominados": pareto, "escore": escore,
            "estabilidade_top1": estab, "total_rankings": d["estabilidade_ranking"]["total_rankings"], "ponte": ponte}


def bloco_entre_fases(c: dict) -> list[dict]:
    linhas = []
    for conj, chave in (("36", "nos_36_avaliacao"), ("90", "nos_90")):
        for col in ("2A_linear_ryzen", "2B_A0", "2B_A2", "2B_A3", "F3_L0", "F3_L1", "F3_L2", "F3_L3", "F3_melhor"):
            va, vb = c["por_modelo"][A][chave].get(col), c["por_modelo"][B][chave].get(col)
            if not isinstance(va, dict) and not isinstance(vb, dict):
                continue
            ga = (va or {}).get("acerto_pct") if isinstance(va, dict) else None
            gb = (vb or {}).get("acerto_pct") if isinstance(vb, dict) else None
            linhas.append({"contexto": f"{col} · nos {conj}", "acerto_A": ga, "acerto_B": gb, "delta": delta(ga, gb),
                           "bal_A": (va or {}).get("acuracia_balanceada_pct") if isinstance(va, dict) else None,
                           "bal_B": (vb or {}).get("acuracia_balanceada_pct") if isinstance(vb, dict) else None})
    riscos = {m: {"adesao_cega_2B_A5_pct": c["por_modelo"][m].get("adesao_cega_2B_A5_pct"), "teto_2B_A3_pct": c["por_modelo"][m].get("teto_2B_A3_pct"),
                  "tentativas_de_decorar_F3": c["por_modelo"][m].get("tentativas_de_decorar_F3"), "autoenvenenamento_F3": c["por_modelo"][m].get("autoenvenenamento_F3")}
              for m in (A, B)}
    return linhas, riscos


def onde_o_coder_vence(dado: dict) -> list[dict]:
    """Toda célula de acerto (ou acurácia balanceada) em que B > A, com a diferença e o n."""
    out = []
    for bloco, rot in (("fase2a", "acerto"), ("fase2b_condicoes", "acerto"), ("fase3_versoes", "acerto"), ("entre_fases", "acerto")):
        for l in dado[bloco]:
            if l.get("delta") is not None and l["delta"] > 0:
                out.append({"onde": l.get("contexto"), "metrica": rot, "A": l["acerto_A"], "B": l["acerto_B"], "delta": l["delta"], "n": l.get("n")})
    for l in dado["fase3_versoes"]:
        if l.get("delta_bal") is not None and l["delta_bal"] > 0:
            out.append({"onde": l["contexto"], "metrica": "acurácia balanceada", "A": l["bal_A"], "B": l["bal_B"], "delta": l["delta_bal"], "n": l.get("n")})
    for nome in ("fase2b_classe_A2", "fase2b_nivel_A2", "fase3_classe_L0", "fase3_classe_L1", "fase3_classe_melhor", "fase3_nivel_L0", "fase3_nivel_L1"):
        for l in dado[nome]:
            if l.get("delta") is not None and l["delta"] > 0:
                dim = l.get("classe") or l.get("nivel")
                out.append({"onde": f"{nome.replace('_', ' ')} · {dim}", "metrica": "acerto", "A": l["acerto_A"], "B": l["acerto_B"], "delta": l["delta"], "n": l.get("n")})
    for l in dado["confronto_f3"] + dado["confronto_2b"]:
        if l["so_coder"] > l["so_qwen"]:
            out.append({"onde": l["contexto"] + " (confronto direto)", "metrica": "casos só o Coder acertou − só o qwen acertou",
                        "A": l["so_qwen"], "B": l["so_coder"], "delta": l["delta_pp"], "n": l["n"], "p": l["p_mcnemar"]})
    return out


def montar() -> dict:
    m2a = ler(EXP / "resumo_metricas.json")
    m2b = ler(RES / "resumo_metricas.json")
    av2b = ler(RES / "avaliacao.json") if (RES / "avaliacao.json").exists() else None
    f3 = ler(F3["raiz"] / "resumo_fase3.json")
    av3 = ler(F3["raiz"] / "avaliacao_fase3.json")
    c = ler(F3["raiz"] / "comparacao_fases.json")
    d = ler(F3["raiz"] / "decisao_modelo.json")
    ined = RES / "fase3b_ineditos" / "resumo_fase3.json"
    ined_modelos = ler(ined)["metadados"].get("modelos") if ined.exists() else None
    doc, rej = bloco_f3_documentacao(f3)
    entre, riscos = bloco_entre_fases(c)
    melhor = {m: max((x for x in f3["por_modelo_biblioteca_particao"] if x["modelo"] == m and x["particao"] == "avaliacao"),
                     key=lambda x: (x["acuracia_balanceada_pct"], -x["biblioteca_epoca"]))["biblioteca_epoca"] for m in (A, B)}
    dado = {
        "metadados": {"gerado_em": datetime.now().isoformat(timespec="seconds"), "A": A, "B": B,
                      "fontes": {"2a": "resumo_metricas.json (Ryzen)", "2b": "resultados_alvo/resumo_metricas.json (+ avaliacao.json)",
                                 "f3": "resultados_alvo/fase3/resumo_fase3.json + avaliacao_fase3.json", "comparacao": "comparacao_fases.json",
                                 "decisao": "decisao_modelo.json", "ineditos": str(ined.relative_to(RES)) if ined.exists() else None},
                      "melhor_L_nos_36": melhor, "ineditos_modelos": ined_modelos,
                      "f3_gerado_em": f3["metadados"]["gerado_em"], "decisao_gerado_em": d["metadados"]["gerado_em"]},
        "fase2a": bloco_2a(m2a),
        "fase2a_classe": bloco_por_dimensao(m2a["por_modelo_classe"], "classe", CLASSES),
        "fase2b_condicoes": bloco_2b_condicoes(m2b),
        "fase2b_classe_A2": bloco_por_dimensao(m2b["por_modelo_condicao_classe"], "classe", CLASSES, condicao="A2"),
        "fase2b_nivel_A2": bloco_por_dimensao(m2b["por_modelo_condicao_nivel"], "nivel", NIVEIS, condicao="A2"),
        "confronto_2b": confronto_direto_2b(av2b),
        "fase3_versoes": bloco_f3_versoes(f3),
        "fase3_classe_L0": bloco_por_dimensao(f3["por_modelo_biblioteca_classe"], "classe", CLASSES, biblioteca_epoca=0, particao="todos"),
        "fase3_classe_L1": bloco_por_dimensao(f3["por_modelo_biblioteca_classe"], "classe", CLASSES, biblioteca_epoca=1, particao="todos"),
        "fase3_classe_melhor": [],
        "fase3_nivel_L0": bloco_por_dimensao(f3["por_modelo_biblioteca_nivel"], "nivel", NIVEIS, biblioteca_epoca=0, particao="todos"),
        "fase3_nivel_L1": bloco_por_dimensao(f3["por_modelo_biblioteca_nivel"], "nivel", NIVEIS, biblioteca_epoca=1, particao="todos"),
        "confronto_f3": confronto_direto_f3(av3),
        "fase3_documentacao": doc, "fase3_rejeicoes": rej,
        "fase3_revisao": bloco_revisao(f3), "fase3_recuperacao": bloco_recuperacao(f3), "fase3_flips": bloco_flips(f3),
        "entre_fases": entre, "riscos_entre_fases": riscos, "decisao": bloco_decisao(d),
    }
    # melhor versão de cada um (nos 36) comparada por classe nos 90
    la, lb = melhor[A], melhor[B]
    linhas = []
    for chave in sorted(CLASSES, key=int):
        xa = pick(f3["por_modelo_biblioteca_classe"], modelo=A, classe=int(chave), biblioteca_epoca=la, particao="todos")
        xb = pick(f3["por_modelo_biblioteca_classe"], modelo=B, classe=int(chave), biblioteca_epoca=lb, particao="todos")
        linhas.append({"classe": f"{chave} {CLASSES[chave]}", "n": _num(xa, "n"), "acerto_A": _num(xa, "causa_correta_pct"),
                       "acerto_B": _num(xb, "causa_correta_pct"), "delta": delta(_num(xa, "causa_correta_pct"), _num(xb, "causa_correta_pct"))})
    dado["fase3_classe_melhor"] = linhas
    dado["onde_o_coder_vence"] = onde_o_coder_vence(dado)
    return dado


# ------------------------------------------------------------------ markdown (blocos colados no Memorial)

def f(v, casas=1) -> str:
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "sim" if v else "não"
    if isinstance(v, float):
        return f"{v:.{casas}f}".replace(".", ",")
    return str(v)


def fd(v) -> str:
    return "—" if v is None else (f"{v:+.1f}".replace(".", ",") + " pp")


def tab(nome: str, cab: list[str], linhas: list[list[str]]) -> str:
    corpo = "\n".join("| " + " | ".join(l) + " |" for l in linhas)
    return f"<!-- tabela:{nome} -->\n| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + f"\n{corpo}\n<!-- /tabela:{nome} -->"


def render(dado: dict) -> str:
    m = dado["metadados"]
    a, b = "qwen2.5:7b", "coder:7b"
    blocos = []
    blocos.append(tab("cq_fase2a", ["Fase 2-A (Ryzen) · estratégia", "n", f"acerto {a}", f"acerto {b}", "Δ (coder − qwen)", f"s/caso {a}", f"s/caso {b}"],
                      [[l["contexto"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"]), f(l["s_A"]), f(l["s_B"])] for l in dado["fase2a"]]))
    blocos.append(tab("cq_fase2a_classe", ["Fase 2-A · classe (3 estratégias)", "n", a, b, "Δ"],
                      [[l["classe"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"])] for l in dado["fase2a_classe"]]))
    blocos.append(tab("cq_fase2b", ["Fase 2-B (i5) · condição", "n", f"acerto {a}", f"acerto {b}", "Δ", f"contra A0 {a}", f"contra A0 {b}", f"forma ok/conteúdo errado {a}", f"… {b}", f"s/caso {a}", f"s/caso {b}"],
                      [[l["contexto"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"]), f(l["vs_A0_A"]), f(l["vs_A0_B"]),
                        f(l["fmt_err_A"]) + "%", f(l["fmt_err_B"]) + "%", f(l["s_A"]), f(l["s_B"])] for l in dado["fase2b_condicoes"]]))
    blocos.append(tab("cq_fase2b_classe", ["Fase 2-B · A2 · classe", "n", a, b, "Δ"],
                      [[l["classe"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"])] for l in dado["fase2b_classe_A2"]]))
    blocos.append(tab("cq_fase2b_nivel", ["Fase 2-B · A2 · nível", "n", a, b, "Δ"],
                      [[l["nivel"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"])] for l in dado["fase2b_nivel_A2"]]))
    if dado["confronto_2b"]:
        blocos.append(tab("cq_confronto_2b", ["Fase 2-B · confronto caso a caso", "n", "ambos acertam", "nenhum", "só o Coder", "só o qwen", "Δ", "p (McNemar exato)"],
                          [[l["contexto"], f(l["n"]), f(l["ambos"]), f(l["nenhum"]), f(l["so_coder"]), f(l["so_qwen"]), fd(l["delta_pp"]), f(l["p_mcnemar"], 4)] for l in dado["confronto_2b"]]))
    blocos.append(tab("cq_fase3", ["Fase 3 · versão · conjunto", "n", f"acerto {a}", f"acerto {b}", "Δ acerto", f"balanceada {a}", f"balanceada {b}", "Δ balanceada", f"s/caso {a}", f"s/caso {b}"],
                      [[l["contexto"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"]), f(l["bal_A"]) + "%", f(l["bal_B"]) + "%", fd(l["delta_bal"]),
                        f(l["s_A"]), f(l["s_B"])] for l in dado["fase3_versoes"]]))
    blocos.append(tab("cq_confronto_f3", ["Fase 3 · confronto caso a caso", "n", "ambos acertam", "nenhum", "só o Coder", "só o qwen", "Δ", "p (McNemar exato)"],
                      [[l["contexto"], f(l["n"]), f(l["ambos"]), f(l["nenhum"]), f(l["so_coder"]), f(l["so_qwen"]), fd(l["delta_pp"]), f(l["p_mcnemar"], 4)] for l in dado["confronto_f3"]]))
    for nome, rot in (("fase3_classe_L0", "L0"), ("fase3_classe_L1", "L1"), ("fase3_classe_melhor", f"melhor versão de cada um (qwen L{m['melhor_L_nos_36'][A]}, coder L{m['melhor_L_nos_36'][B]})")):
        blocos.append(tab(f"cq_{nome}", [f"Fase 3 · {rot} · classe (90)", "n", a, b, "Δ"],
                          [[l["classe"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"])] for l in dado[nome]]))
    for nome, rot in (("fase3_nivel_L0", "L0"), ("fase3_nivel_L1", "L1")):
        blocos.append(tab(f"cq_{nome}", [f"Fase 3 · {rot} · nível (90)", "n", a, b, "Δ"],
                          [[l["nivel"], f(l["n"]), f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"])] for l in dado[nome]]))
    blocos.append(tab("cq_documentacao", ["Época", f"propostas {a}", f"aceitas {a}", f"aceitas % {a}", f"propostas {b}", f"aceitas {b}", f"aceitas % {b}", f"tokens acrescentados {a}", f"… {b}", f"verbetes {a}", f"verbetes {b}"],
                      [[f(l["epoca"]), f(l["propostas_A"]), f(l["aceitas_A"]), f(l["aceitas_pct_A"]) + "%", f(l["propostas_B"]), f(l["aceitas_B"]), f(l["aceitas_pct_B"]) + "%",
                        f(l["tokens_A"]), f(l["tokens_B"]), f(l["verbetes_A"]), f(l["verbetes_B"])] for l in dado["fase3_documentacao"]]))
    rej = dado["fase3_rejeicoes"]
    blocos.append(tab("cq_rejeicoes", ["Motivos de rejeição (3 épocas)", a, b],
                      [[k, f(dict(rej[A]).get(k, 0)), f(dict(rej[B]).get(k, 0))] for k in dict.fromkeys([x for x, _ in rej[A]] + [x for x, _ in rej[B]])]))
    blocos.append(tab("cq_revisao", ["Revisão humana das edições aceitas", f"correta {a}", f"parcial {a}", f"errada {a}", f"correta {b}", f"parcial {b}", f"errada {b}"],
                      [[l["operacao"], f(l["Correta_A"]), f(l["Parcial_A"]), f(l["Errada_A"]), f(l["Correta_B"]), f(l["Parcial_B"]), f(l["Errada_B"])] for l in dado["fase3_revisao"]]))
    blocos.append(tab("cq_recuperacao", ["Versão", f"hit@3 nos 90 {a}", f"hit@3 nos 90 {b}", f"hit@3 nos 36 {a}", f"hit@3 nos 36 {b}", f"verbetes {a}", f"verbetes {b}"],
                      [[f"L{l['L']}", f(l["hit3_90_A"]) + "%", f(l["hit3_90_B"]) + "%", f(l["hit3_36_A"]) + "%", f(l["hit3_36_B"]) + "%", f(l["verbetes_A"]), f(l["verbetes_B"])] for l in dado["fase3_recuperacao"]]))
    blocos.append(tab("cq_flips", ["Transição · conjunto", f"✓→✗ {a}", f"✗→✓ {a}", f"autoenvenenamento {a}", f"✓→✗ {b}", f"✗→✓ {b}", f"autoenvenenamento {b}"],
                      [[l["transicao"], f(l["certo_errado_A"]), f(l["errado_certo_A"]), f(l["autoenv_A"]) + "%", f(l["certo_errado_B"]), f(l["errado_certo_B"]), f(l["autoenv_B"]) + "%"] for l in dado["fase3_flips"]]))
    blocos.append(tab("cq_entre_fases", ["Coluna · conjunto", f"acerto {a}", f"acerto {b}", "Δ", f"balanceada {a}", f"balanceada {b}"],
                      [[l["contexto"], f(l["acerto_A"]) + "%", f(l["acerto_B"]) + "%", fd(l["delta"]), f(l["bal_A"]) + "%", f(l["bal_B"]) + "%"] for l in dado["entre_fases"]]))
    r = dado["riscos_entre_fases"]

    def risco(v) -> str:
        if isinstance(v, dict):
            if "total" in v:
                return f(v["total"])
            return " / ".join(f"{k} {f(x)}%" for k, x in v.items())
        return f(v) + ("%" if isinstance(v, (int, float)) else "")
    rot_risco = {"adesao_cega_2B_A5_pct": "adesão cega à documentação errada (2-B A5) — não medida nos dois",
                 "teto_2B_A3_pct": "teto com o verbete de ouro forçado (2-B A3) — não medido nos dois",
                 "tentativas_de_decorar_F3": "tentativas de decorar o caso (Fase 3, total)",
                 "autoenvenenamento_F3": "autoenvenenamento nos 36 por transição (Fase 3)"}
    blocos.append(tab("cq_riscos", ["Risco", a, b],
                      [[rot_risco[k], risco(r[A][k]), risco(r[B][k])] for k in rot_risco]))
    dec = dado["decisao"]
    blocos.append(tab("cq_regra36", ["Posição", "Modelo", "L", "balanceada (36)", "acerto (36)", "s/caso", "autoenv. máx.", "risco", "vetado"],
                      [[f(x["pos"]), x["modelo"], f"L{x['L']}", f(x["bal_36"]) + "%", f(x["acerto_36"]) + "%", f(x["s_36"]), f(x["autoenv_max_36"]) + "%", f(x["risco"], 2), f(x["vetado"])] for x in dec["ranking_36"]]))
    blocos.append(tab("cq_bootstrap", ["Combinação", "P(top-1) nos 36", "IC 95% nos 36", "P(top-1) nos 90", "IC 95% nos 90"],
                      [[k, f(round(v["p_top1"] * 100, 1)) + "%", "–".join(f(x) for x in v["ic"]), f(round(dec["bootstrap"]["nos_90"].get(k, {}).get("p_top1", 0) * 100, 1)) + "%",
                        "–".join(f(x) for x in dec["bootstrap"]["nos_90"].get(k, {}).get("ic", []))] for k, v in dec["bootstrap"]["nos_36"].items()]))
    blocos.append(tab("cq_escore_pareto", ["Combinação", "escore ponderado", "não dominado (Pareto)"],
                      [[f"{x['modelo']}/L{x['L']}", f(x["score"], 4), f(f"{x['modelo']}/L{x['L']}" in dec["pareto_nao_dominados"])] for x in dec["escore"]]))
    blocos.append(tab("cq_ponte", ["Ponte de versão (0.34.1) · nos 36", "acerto", "balanceada", "b (só nova)", "c (só F3)", "p"],
                      [[x["modelo"], f(x["acerto_36"]) + "%", f(x["bal_36"]) + "%", f(x["b"]), f(x["c"]), f(x["p"], 4)] for x in dec["ponte"]]))
    blocos.append(tab("cq_onde_vence", ["Onde o Coder fica à frente", "métrica", a, b, "Δ", "n", "p"],
                      [[l["onde"], l["metrica"], f(l["A"]), f(l["B"]), fd(l["delta"]), f(l.get("n")), f(l.get("p"), 4) if l.get("p") is not None else "—"] for l in dado["onde_o_coder_vence"]]))
    cab = ["<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por comparar_qwen_coder.py a partir dos registros oficiais (--check regera e compara); não editar à mão.",
           "     ! Motivo: nenhum número digitado à mão — o comparativo do Memorial cola estes blocos. -->",
           f"# Comparativo {A} × {B} — gerado em {m['gerado_em'][:10]}", "",
           f"Fontes: {m['fontes']['2a']}; {m['fontes']['2b']}; {m['fontes']['f3']} (gerado em {m['f3_gerado_em']}); {m['fontes']['comparacao']}; "
           f"{m['fontes']['decisao']} (gerado em {m['decisao_gerado_em']}). Melhor versão nos 36: {a} L{m['melhor_L_nos_36'][A]}, {b} L{m['melhor_L_nos_36'][B]}. "
           f"Casos inéditos (28/09): modelos rodados = {m['ineditos_modelos']} — o {B} não rodou lá. Estabilidade de ranking (top-1 em {dec['total_rankings']} cortes): "
           + "; ".join(f"{k}: {v}" for k, v in dec["estabilidade_top1"].items()) + ".", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ colagem no documento do Memorial

DOC_ALVO = EXP.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "comparativo-qwen25-7b-vs-coder-7b.md"
BLOCO_CHEIO_RE = re.compile(r"(<!-- tabela:(cq_[a-z0-9_]+) -->\n.*?\n<!-- /tabela:\2 -->)", re.S)
BLOCO_ALVO_RE = re.compile(r"<!-- tabela:(cq_[a-z0-9_]+) -->\n(?:.*?\n)?<!-- /tabela:\1 -->", re.S)


def blocos_de(md: str) -> dict[str, str]:
    return {m.group(2): m.group(1) for m in BLOCO_CHEIO_RE.finditer(md)}


def colar(doc: Path, md: str) -> tuple[int, bool]:
    """Substitui todo bloco `<!-- tabela:cq_X -->…<!-- /tabela:cq_X -->` do documento (vazio ou não) pelo bloco
    gerado — o inverso do --check; um nome sem bloco gerado interrompe."""
    blocos = blocos_de(md)
    s = doc.read_text(encoding="utf-8")
    faltando = [n for n in BLOCO_ALVO_RE.findall(s) if n not in blocos]
    if faltando:
        raise SystemExit(f"{doc.name}: bloco(s) sem tabela gerada: {faltando}")
    novo, n = BLOCO_ALVO_RE.subn(lambda m: blocos[m.group(1)], s)
    if novo != s:
        doc.write_text(novo, encoding="utf-8", newline="\n")
    return n, novo != s


def conferir_doc(doc: Path, md: str) -> list[str]:
    blocos = blocos_de(md)
    return [n for n, b in blocos_de(doc.read_text(encoding="utf-8")).items() if blocos.get(n) != b]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--colar", action="store_true", help="cola os blocos gerados no documento do Memorial")
    args = ap.parse_args()
    print(caminhos.descricao())
    dado = montar()
    md = render(dado)
    if args.check:
        atual = SAIDA_MD.read_text(encoding="utf-8") if SAIDA_MD.exists() else ""
        antigo = ler(SAIDA_JSON) if SAIDA_JSON.exists() else {}
        sem_data = lambda d: {k: v for k, v in d.items() if k != "metadados"}  # noqa: E731
        ok_json = sem_data(antigo) == sem_data(dado)
        ok_md = atual.split("\n", 3)[-1] == md.split("\n", 3)[-1] if atual else False
        divergentes = conferir_doc(DOC_ALVO, md) if DOC_ALVO.exists() else []
        if ok_json and ok_md and not divergentes:
            print(f"--check: {SAIDA_MD.name}, {SAIDA_JSON.name} e os blocos de {DOC_ALVO.name} batem com os dados atuais")
            return
        print(f"--check: DIFERE (json {'ok' if ok_json else 'difere'}; md {'ok' if ok_md else 'difere'}; "
              f"blocos divergentes no documento: {divergentes})")
        sys.exit(1)
    if args.colar:
        n, mudou = colar(DOC_ALVO, md)
        print(f"{DOC_ALVO.name}: {n} bloco(s) colado(s); mudou: {mudou}")
        return
    SAIDA_JSON.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
    SAIDA_MD.write_text(md, encoding="utf-8", newline="\n")
    print(f"gravado: {SAIDA_JSON.name} e {SAIDA_MD.name} — {len(dado['onde_o_coder_vence'])} célula(s) em que o Coder fica à frente")


if __name__ == "__main__":
    main()
