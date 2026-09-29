#!/usr/bin/env python3
# ! Alteração de IA - Revisar: gerador do painel interativo dos testes (28/09/2026, pedido do Eric):
# lê os registros oficiais (resumo_fase3.json, comparacao_fases.json, decisao_modelo.json, os
# resumos das Fases 2-A/2-B, os 29 blocos de tabelas_relatorio.md e as figuras SVG 01–18) e grava
# um HTML único e autossuficiente, com gráficos Chart.js (carregado do CDN) e as figuras oficiais
# embutidas; --check regera e compara.
# ! Motivo: o Eric pediu "um dashboard com o relatório detalhado dos testes, com gráficos e
# números, com a explicação e a avaliação de cada modelo, detalhado porém sumarizado". A regra do
# projeto é nenhum número digitado à mão: todo valor do painel sai dos JSON pela mesma origem
# das tabelas do Memorial, e o --check acusa qualquer edição manual do HTML.
# ! Alteração de IA - Revisar: na noite de 28/09/2026 o painel dos testes virou o PAINEL DO PROJETO
# (Documentacao/dashboard/painel-do-projeto.html): ganhou as abas Início (estado por fase, o que
# depende do Eric, corridas), Pendências (um cartão por ficha de pendencias.md, com filtro) e Roadmap
# (faixa de fases e cartões de corrida com o comando pronto, lidos de roadmap.md), antes das abas dos
# testes, que não mudaram; a leitura dos dois .md fica em painel_textos.py.
# ! Motivo: o Eric pediu um relatório visual por pergunta das pendências ("ler no .md é bem ruim"),
# um relatório do roadmap e "tudo num único relatório / página web, um dashboard completo do
# projeto, que dá para acessar de qualquer lugar" — o arquivo publicado no claude.ai passa a ser
# este. O nome do arquivo mudou porque o conteúdo deixou de ser só a Fase 3.
"""Uso: python ferramentas/gerar_dashboard.py [--check] [--saida Documentacao/dashboard/painel-do-projeto.html]"""
from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import painel_textos as pt

RAIZ = Path(__file__).resolve().parent.parent
EXP = RAIZ / "Programacao" / "AgenteCore" / "experimentos"
F3 = EXP / "resultados_alvo" / "fase3"
MEMORIAL = RAIZ / "Documentacao" / "memorial"
SAIDA_PADRAO = RAIZ / "Documentacao" / "dashboard" / "painel-do-projeto.html"

MODELOS_F3 = ["qwen2.5:7b", "granite4.2:8b", "qwen2.5-coder:7b", "qwen2.5-coder:3b"]
CORES = {"qwen2.5:7b": "#2f5d8a", "granite4.2:8b": "#9a6b2f", "qwen2.5-coder:7b": "#3b8a6e",
         "qwen2.5-coder:3b": "#8a3f63", "phi4-mini:3.8b": "#6f6f6f", "qwen2.5-coder:1.5b": "#a8a8a8",
         "qwen2.5-coder:1.5b-instruct-fp16": "#c2c2c2", "qwen2.5-coder:1.5b-instruct-q8_0": "#b5b5b5"}
CLASSES = {1: "léxica", 2: "sintática", 3: "semântica", 4: "tradução", 5: "runtime", 6: "efeito"}
NIVEIS = {1: "fácil", 2: "médio", 3: "difícil"}
CONDICOES_2B = {"A0": "A0 — sem documentação", "A1": "A1 — biblioteca inteira no prompt",
                "A2": "A2 — recuperação (k = 3)", "A3": "A3 — verbete de ouro no prompt (teto)",
                "A4": "A4 — verbete distrator", "A5": "A5 — verbete errado (adversarial)"}
FIGURAS = {
    "01": "Fase 2-A · acerto por modelo", "02": "Fase 2-A · acerto por estratégia de prompt",
    "03": "Fase 2-A · acerto por classe", "04": "Fase 2-A · acerto por nível",
    "05": "Fase 2-A · custo × acerto", "06": "Fase 2-A · formato válido com conteúdo errado",
    "07": "Fase 2-B · biblioteca por modelo (A0 → A2)", "08": "Fase 2-B · ablações: ouro, distrator, adversarial",
    "09": "Fase 2-B · prefill × acerto", "10": "Fase 2-B · quantização e trocas de rótulo",
    "11": "Fase 2-B · ancoragem e recuperação", "12": "Fase 3 · acerto por época",
    "13": "Fase 3 · recuperação por época", "14": "Fase 3 · propostas por motivo de rejeição",
    "15": "Fase 3 · crescimento da biblioteca", "16": "Comparação entre as três fases",
    "17": "Custo × acerto nas três fases", "18": "Decisão · fronteira de Pareto",
}


# ------------------------------------------------------------------ leitura

def ler_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def blocos_tabelas(p: Path) -> dict[str, str]:
    texto = p.read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in re.finditer(r"<!-- tabela:([a-z0-9_]+) -->\n(.*?)\n<!-- /tabela:\1 -->", texto, re.S)}


def figuras_b64() -> dict[str, str]:
    out = {}
    for p in sorted((EXP / "resultados_alvo" / "graficos").glob("*.svg")):
        num = p.name[:2]
        if num in FIGURAS:
            out[num] = "data:image/svg+xml;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    return out


# ------------------------------------------------------------------ markdown -> html

def _inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md_para_html(md: str) -> str:
    """Converte um bloco de tabelas_relatorio.md (tabelas, ### títulos, _notas_, - listas) em HTML."""
    linhas = md.strip("\n").split("\n")
    saida, i = [], 0
    while i < len(linhas):
        l = linhas[i]
        if l.startswith("|"):
            tab = []
            while i < len(linhas) and linhas[i].startswith("|"):
                tab.append(linhas[i]); i += 1
            saida.append(_tabela(tab))
            continue
        if l.startswith("### "):
            saida.append(f"<h4>{_inline(l[4:])}</h4>")
        elif l.startswith("- "):
            itens = []
            while i < len(linhas) and linhas[i].startswith("- "):
                itens.append(f"<li>{_inline(linhas[i][2:])}</li>"); i += 1
            saida.append("<ul>" + "".join(itens) + "</ul>")
            continue
        elif l.strip().startswith("_") and l.strip().endswith("_"):
            saida.append(f'<p class="nota">{_inline(l.strip()[1:-1])}</p>')
        elif l.strip():
            saida.append(f"<p>{_inline(l)}</p>")
        i += 1
    return "\n".join(saida)


def _tabela(linhas: list[str]) -> str:
    def celulas(l: str) -> list[str]:
        return [c.strip() for c in l.strip().strip("|").split("|")]
    cab = celulas(linhas[0])
    corpo = [celulas(l) for l in linhas[2:] if not re.match(r"^\|\s*-", l)]
    th = "".join(f"<th>{_inline(c)}</th>" for c in cab)
    trs = []
    for r in corpo:
        tds = "".join(f'<td{" class=num" if _e_numero(c) else ""}>{_inline(c)}</td>' for c in r)
        trs.append(f"<tr>{tds}</tr>")
    return f'<div class="tabela"><table><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def _e_numero(c: str) -> bool:
    return bool(re.match(r"^\**[\d.,]+%?\**", c.strip())) or c.strip() in {"—", "-"}


# ------------------------------------------------------------------ dados para os gráficos

def pct(v) -> float | None:
    return None if v is None else round(float(v), 1)


def montar_dados(r: dict, c: dict, d: dict, m2b: dict, m2a: dict) -> dict:
    dados: dict = {"modelos": MODELOS_F3, "cores": CORES}
    curvas = defaultdict(lambda: defaultdict(dict))
    custo = defaultdict(dict)
    for x in r["por_modelo_biblioteca_particao"]:
        p = {"avaliacao": "36", "aprendizado": "54", "todos": "90"}[x["particao"]]
        curvas[p][x["modelo"]][str(x["biblioteca_epoca"])] = {
            "balanceada": pct(x["acuracia_balanceada_pct"]), "acerto": pct(x["causa_correta_pct"]),
            "ic": x["causa_correta_ic95"], "segundos": x["segundos_mediana"]}
        if x["particao"] == "todos":
            custo[x["modelo"]][str(x["biblioteca_epoca"])] = {
                "segundos": x["segundos_mediana"], "p95": x.get("segundos_p95"),
                "prefill_s": round((x.get("prefill_ms_mediana") or 0) / 1000, 1),
                "geracao_s": round((x.get("geracao_ms_mediana") or 0) / 1000, 1),
                "tokens_saida": x["tokens_saida_medio"], "tokens_entrada": x.get("tokens_entrada_mediana")}
    dados["curvas"] = curvas
    dados["custo"] = custo
    classes = defaultdict(lambda: defaultdict(dict))
    for x in r["por_modelo_biblioteca_classe"]:
        if x["particao"] == "todos":
            classes[x["modelo"]][str(x["classe"])][str(x["biblioteca_epoca"])] = pct(x["causa_correta_pct"])
    dados["classes"] = classes
    niveis = defaultdict(lambda: defaultdict(dict))
    for x in r["por_modelo_biblioteca_nivel"]:
        if x["particao"] == "todos":
            niveis[x["modelo"]][str(x["nivel"])][str(x["biblioteca_epoca"])] = pct(x["causa_correta_pct"])
    dados["niveis"] = niveis
    dados["pareado"] = [x for x in r["pareado_vs_L0"]]
    dados["flips"] = [x for x in r["flips"]]
    dados["mde"] = r["efeito_minimo_detectavel"]
    rec = defaultdict(dict)
    for x in r["recuperacao"]:
        rec[x["modelo"]][str(x["biblioteca_epoca"])] = {
            "hit3_90": x["todos"]["hit@3"], "hit3_36": x["avaliacao"]["hit@3"], "mrr_90": x["todos"]["mrr"],
            "hit1_90": x["todos"]["hit@1"], "hit5_90": x["todos"]["hit@5"],
            "verbetes": x["n_verbetes"], "novos": x["n_verbetes_novos"], "tokens": x["tokens_estimados"]}
    dados["recuperacao"] = rec
    doc = defaultdict(dict)
    rej = defaultdict(lambda: defaultdict(int))
    for x in r["documentacao"]:
        doc[x["modelo"]][str(x["epoca"])] = {
            "propostas": x["n_propostas"], "aceitas": x["n_aceitas"], "aceitas_pct": x["aceitas_pct"],
            "por_operacao": x["por_operacao"], "tokens": x["tokens_md_estimados_acrescentados"],
            "verbetes": x["biblioteca"]["n_verbetes"], "truncadas": x["n_respostas_truncadas"]}
        for k, v in x["motivos_rejeicao"].items():
            rej[x["modelo"]][k] += v
    dados["documentacao"] = doc
    dados["rejeicoes"] = {m: {k: v for k, v in sorted(rej[m].items(), key=lambda kv: -kv[1]) if v} for m in rej}
    fases = {}
    for m, blocos in c["por_modelo"].items():
        fases[m] = {}
        for conj, chave in (("36", "nos_36_avaliacao"), ("90", "nos_90")):
            fases[m][conj] = {col: (None if not isinstance(v, dict) else {"balanceada": pct(v.get("acuracia_balanceada_pct")),
                                                                          "acerto": pct(v.get("acerto_pct")), "segundos": v.get("segundos_mediana")})
                              for col, v in blocos[chave].items()}
        fases[m]["adesao_cega_A5"] = blocos.get("adesao_cega_2B_A5_pct")
        fases[m]["teto_A3"] = blocos.get("teto_2B_A3_pct")
    dados["fases"] = fases
    dados["pareamentos"] = c["pareamentos"]
    dados["casos_alterados"] = c["metadados"]["casos_alterados_na_fase3"]
    dados["regra36"] = d["regra_36"]["ranking"]
    dados["vencedor"] = d["regra_36"]["vencedor"]
    dados["licencas"] = d["regra_36"]["licencas"]
    dados["bootstrap"] = {conj: {f'{x["modelo"]}/L{x["biblioteca_epoca"]}': {"p": x["p_top1"], "ic": x["ic95_bootstrap"]}
                                 for x in d["bootstrap"][conj]["combos"]} for conj in ("nos_36", "nos_90")}
    dados["bootstrap_meta"] = {"n": d["bootstrap"]["n_bootstrap"], "semente": d["bootstrap"]["semente"]}
    dados["estabilidade"] = {"top1": d["estabilidade_ranking"]["top1_por_modelo"], "total": d["estabilidade_ranking"]["total_rankings"]}
    dados["pareto"] = {"nao_dominados": [f'{x["modelo"]}/L{x["biblioteca_epoca"]}' for x in d["pareto"]["nao_dominados"]],
                       "candidatos": d["pareto"]["candidatos_considerados"]}
    dados["escore"] = {"pesos": d["escore_ponderado"]["pesos"], "linhas": d["escore_ponderado"]["linhas"]}
    dados["sensibilidade"] = {k: v["mudancas_de_vencedor"] for k, v in d["sensibilidade"].items()}
    dados["tres_b"] = d["tres_b"]
    dados["revisao"] = d["revisao_humana"]["por_modelo"]
    dados["cochran"] = r["cochran_q"]
    dados["meta"] = {"resumo_gerado_em": r["metadados"]["gerado_em"], "n_diagnosticos": r["metadados"]["n_diagnosticos"],
                     "n_propostas": r["metadados"]["n_propostas"], "decisao_gerado_em": d["metadados"]["gerado_em"],
                     "comparacao_gerado_em": c["metadados"]["gerado_em"],
                     "erros_infra": sum(x["erros_infra"] for x in r["por_modelo_biblioteca_particao"] if x["particao"] == "todos"),
                     "limiar_veto": d["metadados"]["pesos"]["limiar_autoenvenenamento_pct"]}
    f2b = defaultdict(dict)
    for x in m2b["por_modelo_condicao"]:
        f2b[x["modelo"]][x["condicao"]] = {"acerto": pct(x["causa_correta_pct"]), "n": x["n"], "segundos": x["segundos_mediana"],
                                          "formato_ok_errado": pct(x["formato_ok_conteudo_errado_pct"])}
    dados["f2b"] = f2b
    f2a = defaultdict(dict)
    for x in m2a["por_modelo_estrategia"]:
        f2a[x["modelo"]][x["estrategia"]] = {"acerto": pct(x["causa_correta_pct"]), "n": x["n"], "segundos": x["segundos_mediana"]}
    dados["f2a"] = f2a
    return dados


# ------------------------------------------------------------------ textos (parametrizados pelos dados)

def fmt(v, casas=1) -> str:
    if v is None:
        return "—"
    s = f"{v:.{casas}f}".replace(".", ",")
    return s


def melhor_l(dados: dict, modelo: str, conj: str = "36") -> tuple[int, float]:
    cur = dados["curvas"][conj][modelo]
    melhor = max(sorted(cur.keys()), key=lambda L: (cur[L]["balanceada"], -int(L)))
    return int(melhor), cur[melhor]["balanceada"]


def texto_vereditos(dados: dict) -> dict[str, dict]:
    """Veredito por modelo: números lidos dos JSON; a leitura qualitativa é a da análise decisória §8.1."""
    v = {}
    venc = dados["vencedor"]
    for m in MODELOS_F3:
        L, bal = melhor_l(dados, m)
        rank = [x for x in dados["regra36"] if x["modelo"] == m]
        top = rank[0]
        p36 = dados["bootstrap"]["nos_36"].get(f"{m}/L{L}", {}).get("p")
        aceitas = sum(e["aceitas"] for e in dados["documentacao"].get(m, {}).values())
        propostas = sum(e["propostas"] for e in dados["documentacao"].get(m, {}).values())
        rev = dados["revisao"].get(m)
        v[m] = {"melhor_L": L, "balanceada": bal, "acerto": top["acerto_36"], "segundos": top["segundos_mediana_36"],
                "autoenv": top["autoenvenenamento_max_36"], "p_top1": p36, "aceitas": aceitas, "propostas": propostas,
                "revisao": rev, "licenca": dados["licencas"].get(m, "?"), "vencedor": m == venc["modelo"],
                "risco": top.get("risco")}
    return v


LEITURA = {
    "qwen2.5:7b": ("Vencedor da regra pré-registrada", "Único modelo que escreveu na biblioteca no formato exigido e ganhou com ela: o pico é a época 1 (L1), depois regride. As notas aceitas são em maioria redundantes ou erradas na revisão humana; o ganho veio da forma (notas e cabeçalhos no contexto), não da verdade do conteúdo — por isso a cópia L1 pede curadoria antes da Fase 4."),
    "granite4.2:8b": ("O melhor sem edição; fora do padrão", "Igual em L0..L3 porque não conseguiu documentar: todas as propostas foram barradas pelo teto de texto do validador. É o mais estável entre cortes e o melhor sem biblioteca editada, mas fica abaixo do vencedor com L1, é o mais caro por diagnóstico e o único que a máquina-alvo não sustenta com folga (sem ponte de versão, fora da 3-B)."),
    "qwen2.5-coder:7b": ("Segundo escritor, sem ganho nos 36", "Escreve no formato e teve edições aceitas, mas nos 36 casos de avaliação só ganha em L3 e regride nos 90 depois de L1; é dominado no Pareto (mais lento sem ser mais certeiro). Segue como leitor na troca cruzada da 3-B."),
    "qwen2.5-coder:3b": ("O mais barato; 20 pontos abaixo", "Não dominado no Pareto só pelo custo. Omite o texto em boa parte das propostas (rejeições por bloco malformado), adere cegamente a documentação errada na condição A5 da 2-B e está sob a Qwen Research License (uso não comercial). Segue como leitor nos testes da 3-B."),
}

HIPOTESES = [
    ("H1", "Nos 36 de avaliação, acerto com L3 > L0 nos modelos de 7–8B (McNemar exato, α = 0,05)."),
    ("H2", "O ganho concentra-se nas classes em que a recuperação é fraca (tradução), via aumento do hit@3 da biblioteca do modelo."),
    ("H3", "Nos 54 de aprendizado o ganho é maior que nos 36; a diferença quantifica a memorização."),
    ("H4", "A taxa de aceitação das propostas cresce com o porte; o 3B tem mais rejeições por formato."),
    ("H5", "Autoenvenenamento (casos certos em L(n) que viram errados em L(n+1), nos 36) fica abaixo de 10%; se superar o ganho, o modelo é vetado."),
    ("H6", "A curva não é monótona: reportar o melhor L e o L3, nunca só o último."),
]


def vereditos_hipoteses(dados: dict) -> list[dict]:
    par = {(x["modelo"], x["biblioteca_epoca"], x["particao"]): x for x in dados["pareado"]}
    def p(m, L, part="avaliacao"):
        x = par[(m, L, part)]
        return f'{m}: Δ {fmt(x["delta_pp"])} pp (b/c {x["b"]}/{x["c"]}, p = {fmt(x["p_mcnemar"], 4)})'
    h1 = "; ".join(p(m, 3) for m in ("qwen2.5:7b", "qwen2.5-coder:7b", "granite4.2:8b"))
    mde36 = next(x["delta_pp"] for x in dados["mde"] if x["n"] == 36)
    rec = dados["recuperacao"]["qwen2.5:7b"]
    trad = dados["classes"]["qwen2.5:7b"]["4"]
    h2 = (f'hit@3 nos 90 do qwen2.5:7b: {fmt(rec["0"]["hit3_90"])} (L0) → {fmt(rec["1"]["hit3_90"])} (L1) → {fmt(rec["3"]["hit3_90"])} (L3): '
          f'a biblioteca maior não melhora o recuperador; a classe tradução vai de {fmt(trad["0"])}% (L0) a {fmt(trad["3"])}% (L3) nos 90.')
    w36, w54 = par[("qwen2.5:7b", 1, "avaliacao")], par[("qwen2.5:7b", 1, "aprendizado")]
    h3 = f'qwen2.5:7b em L1: Δ {fmt(w36["delta_pp"])} pp nos 36 contra Δ {fmt(w54["delta_pp"])} pp nos 54 — o ganho é maior onde o modelo nunca viu a causa correta.'
    doc = dados["documentacao"]
    h4 = "aceitação na época 1: " + "; ".join(f'{m} {fmt(doc[m]["1"]["aceitas_pct"])}%' for m in MODELOS_F3 if "1" in doc.get(m, {})) + \
         f'; rejeições por bloco malformado no 3B: {dados["rejeicoes"].get("qwen2.5-coder:3b", {}).get("bloco_malformado", 0)}.'
    autoenv = max((x["autoenvenenamento_pct"], x["modelo"], x["transicao"]) for x in dados["flips"] if x["particao"] == "avaliacao")
    h5 = f'autoenvenenamento máximo nos 36: {fmt(autoenv[0])}% ({autoenv[1]}, {autoenv[2]}), abaixo do teto de {fmt(dados["meta"]["limiar_veto"])}%; nenhum veto.'
    cur = dados["curvas"]["36"]["qwen2.5:7b"]
    h6 = "qwen2.5:7b nos 36 (acurácia balanceada): " + " → ".join(f'{fmt(cur[L]["balanceada"])}% (L{L})' for L in "0123")
    return [
        {"h": "H1", "veredito": "Não confirmada", "cor": "ruim", "ev": f"{h1}. Nenhum p < 0,05 com efeito mínimo detectável de {fmt(mde36)} pp nos 36."},
        {"h": "H2", "veredito": "Não", "cor": "ruim", "ev": h2},
        {"h": "H3", "veredito": "Não; no vencedor, invertida", "cor": "ruim", "ev": h3},
        {"h": "H4", "veredito": "Parcial", "cor": "meio", "ev": h4 + " O 3B tem mais rejeições por formato, mas a aceitação não cresce com o porte: o maior modelo teve 0%."},
        {"h": "H5", "veredito": "Sim", "cor": "bom", "ev": h5},
        {"h": "H6", "veredito": "Sim", "cor": "bom", "ev": h6 + ". O pico é L1, não L3."},
    ]


# ------------------------------------------------------------------ página

CSS = r"""
:root{--bg:#f6f4ee;--bg2:#fdfcf9;--ink:#1f2328;--ink2:#4c545c;--linha:#d8d3c7;--acento:#2f5d8a;--acento2:#dbe7f3;
--bom:#2e7d4f;--meio:#b7791f;--ruim:#b3392b;--sombra:0 1px 2px rgba(20,25,30,.06),0 8px 24px rgba(20,25,30,.06);
--fd:"Source Serif 4",Georgia,"Times New Roman",serif;--fb:"IBM Plex Sans","Segoe UI",Roboto,Arial,sans-serif;--fm:"IBM Plex Mono",Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15181c;--bg2:#1d2126;--ink:#e8e6df;--ink2:#a8adb4;--linha:#333a42;--acento:#7fb0e0;--acento2:#243342;--bom:#5cc48a;--meio:#e0a84a;--ruim:#e46b5c;--sombra:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35)}}
:root[data-theme=dark]{--bg:#15181c;--bg2:#1d2126;--ink:#e8e6df;--ink2:#a8adb4;--linha:#333a42;--acento:#7fb0e0;--acento2:#243342;--bom:#5cc48a;--meio:#e0a84a;--ruim:#e46b5c;--sombra:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 var(--fb)}
.topo{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg2);border-bottom:1px solid var(--linha);box-shadow:var(--sombra)}
.topo .in{max-width:1200px;margin:0 auto;padding:10px 16px;display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}
.marca{font:600 18px/1.2 var(--fd);letter-spacing:.01em}.marca small{display:block;font:12px var(--fb);color:var(--ink2)}
nav{display:flex;flex-wrap:wrap;gap:4px}nav button{border:1px solid transparent;background:none;color:var(--ink2);font:500 13px var(--fb);padding:6px 10px;border-radius:6px;cursor:pointer}
nav button:hover{background:var(--acento2)}nav button[aria-selected=true]{color:var(--acento);border-color:var(--acento);background:var(--acento2)}
nav button:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
main{max-width:1200px;margin:0 auto;padding:22px 16px 64px}section[hidden]{display:none}
h1{font:600 30px/1.15 var(--fd);margin:0 0 6px;text-wrap:balance}h2{font:600 22px/1.2 var(--fd);margin:34px 0 10px;text-wrap:balance}
h3{font:600 17px/1.25 var(--fd);margin:24px 0 8px}h4{font:600 14px var(--fb);margin:14px 0 6px;color:var(--ink2);text-transform:uppercase;letter-spacing:.04em}
p{max-width:78ch;margin:8px 0}p.nota,.nota{color:var(--ink2);font-size:13px}.lead{font-size:17px;color:var(--ink)}
code{font:13px var(--fm);background:var(--acento2);padding:1px 4px;border-radius:4px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:18px 0}
.kpi{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px}
.kpi b{display:block;font:600 26px/1.1 var(--fd);font-variant-numeric:tabular-nums}.kpi span{font-size:12px;color:var(--ink2);text-transform:uppercase;letter-spacing:.04em}
.kpi small{display:block;color:var(--ink2);font-size:12px;margin-top:4px}
.grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.card{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:16px 18px;box-shadow:var(--sombra)}
.card.venc{border-color:var(--acento);box-shadow:0 0 0 2px var(--acento2)}
.card h3{margin:0 0 2px;display:flex;align-items:center;gap:8px}.dot{width:12px;height:12px;border-radius:50%;display:inline-block}
.tag{display:inline-block;font:600 11px var(--fb);letter-spacing:.04em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background:var(--acento2);color:var(--acento)}
.tag.bom{background:color-mix(in srgb,var(--bom) 18%,transparent);color:var(--bom)}.tag.meio{background:color-mix(in srgb,var(--meio) 18%,transparent);color:var(--meio)}.tag.ruim{background:color-mix(in srgb,var(--ruim) 16%,transparent);color:var(--ruim)}
.fatos{display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;margin:10px 0;font-size:13px}.fatos div{display:flex;justify-content:space-between;gap:8px;border-bottom:1px dotted var(--linha);padding:3px 0}
.fatos b{font-variant-numeric:tabular-nums;font-family:var(--fm);font-weight:500}
.chart{position:relative;height:340px;background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:12px}.chart.alto{height:420px}.chart.baixo{height:200px}
.controles{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin:10px 0;font-size:13px}
select{font:13px var(--fb);color:var(--ink);background:var(--bg2);border:1px solid var(--linha);border-radius:6px;padding:4px 8px}
.tabela{overflow-x:auto;margin:10px 0;border:1px solid var(--linha);border-radius:8px;background:var(--bg2)}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:6px 10px;border-bottom:1px solid var(--linha);text-align:left;vertical-align:top}
th{background:var(--acento2);font-weight:600;white-space:nowrap}td.num{font-family:var(--fm);font-variant-numeric:tabular-nums;white-space:nowrap}tbody tr:last-child td{border-bottom:0}
.heat td.num{text-align:center}
figure{margin:14px 0;background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:10px}figure img{max-width:100%;display:block;margin:0 auto;background:#fff;border-radius:6px}
figcaption{font-size:13px;color:var(--ink2);margin-top:8px}
details{border:1px solid var(--linha);border-radius:8px;padding:8px 12px;margin:10px 0;background:var(--bg2)}summary{cursor:pointer;font-weight:600}
.hip{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;align-items:start}.hip .h{font:600 15px var(--fm)}
.rodape{margin-top:40px;font-size:12px;color:var(--ink2);border-top:1px solid var(--linha);padding-top:12px}
nav .grupo{font:600 11px var(--fb);text-transform:uppercase;letter-spacing:.06em;color:var(--ink2);padding:6px 2px 6px 10px}
.chip{display:inline-block;font:600 11px var(--fb);letter-spacing:.04em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background:var(--acento2);color:var(--acento);white-space:nowrap;vertical-align:middle}
.chip.aberta,.chip.andamento{background:color-mix(in srgb,var(--meio) 18%,transparent);color:var(--meio)}
.chip.fechada,.chip.feita,.chip.concluida{background:color-mix(in srgb,var(--bom) 18%,transparent);color:var(--bom)}
.chip.rodando{background:color-mix(in srgb,var(--acento) 22%,transparent);color:var(--acento)}
.chip.pendente,.chip.aguarda,.chip.nao_iniciada,.chip.outro{background:color-mix(in srgb,var(--ink2) 14%,transparent);color:var(--ink2)}
.chip.opcional{background:transparent;border:1px dashed var(--linha);color:var(--ink2)}
.chip.quem,.chip.data{background:transparent;border:1px solid var(--linha);color:var(--ink2);text-transform:none;letter-spacing:0}
.fases{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(210px,100%),1fr));gap:10px;margin:14px 0}
.fase{background:var(--bg2);border:1px solid var(--linha);border-top:4px solid var(--ink2);border-radius:10px;padding:12px 14px}
.fase.concluida{border-top-color:var(--bom)}.fase.andamento{border-top-color:var(--meio)}.fase.nao_iniciada{border-top-color:var(--linha)}
.fase b{display:block;font:600 15px/1.25 var(--fd);margin-bottom:6px}.fase small{display:block;color:var(--ink2);font-size:12px;margin-top:8px}.fase p{font-size:13px;margin:6px 0 0}
.lista-eric,.lista-corridas{padding-left:22px}.lista-eric li,.lista-corridas li{margin:8px 0}.lista-eric a{color:var(--acento);font-weight:600;text-decoration:none}.lista-eric a:hover{text-decoration:underline}
.numero{display:inline-block;font:600 12px/1.4 var(--fm);background:var(--acento);color:var(--bg2);border-radius:6px;padding:1px 7px;vertical-align:middle}
.filtros{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}.filtros button{border:1px solid var(--linha);background:var(--bg2);color:var(--ink2);font:500 13px var(--fb);padding:6px 12px;border-radius:999px;cursor:pointer}
.filtros button[aria-pressed=true]{border-color:var(--acento);color:var(--acento);background:var(--acento2)}.filtros button:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
.ficha,.corrida{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:16px 18px;margin:12px 0;box-shadow:var(--sombra)}
.ficha.fechada{border-style:dashed;box-shadow:none}.ficha.realce{outline:3px solid var(--acento);outline-offset:2px}
.ficha header,.corrida header{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin-bottom:8px}.ficha h3,.corrida h3{margin:0;flex:1 1 260px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.fc{margin:10px 0}.fc h4{margin:0 0 3px}.fc p{margin:0;max-width:90ch}.opcoes{margin:4px 0 0;padding-left:22px}.opcoes li{margin:3px 0}
.fc.decisao{border-left:3px solid var(--meio);padding-left:12px}.fc.decisao.tomada{border-left-color:var(--bom)}
.corridas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(360px,100%),1fr));gap:14px}.corrida{margin:0}
.fatos2{display:grid;grid-template-columns:1fr;gap:4px;font-size:13px}.fatos2 div{display:grid;grid-template-columns:130px 1fr;gap:8px;border-bottom:1px dotted var(--linha);padding:4px 0}.fatos2 span{color:var(--ink2)}.fatos2 b{font-weight:500}
.cmd{position:relative;margin-top:10px}.cmd pre{margin:0;background:var(--acento2);border-radius:6px;padding:10px 74px 10px 12px;font:12px/1.5 var(--fm);white-space:pre-wrap;word-break:break-all;overflow-x:auto}
.cmd button{position:absolute;top:6px;right:6px;border:1px solid var(--linha);background:var(--bg2);color:var(--ink2);font:500 12px var(--fb);padding:3px 8px;border-radius:6px;cursor:pointer}
.ref{font-family:var(--fm);font-size:13px;color:var(--acento)}
main ol,main ul{padding-left:22px}
@media (max-width:640px){.fatos2 div{grid-template-columns:1fr}.cmd pre{padding-right:12px}.cmd button{position:static;margin-top:6px}}
@media (max-width:640px){.fatos{grid-template-columns:1fr}.chart{height:280px}h1{font-size:24px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = r"""
const D = window.DADOS;
const cor = m => D.cores[m] || '#888';
const abas = [...document.querySelectorAll('nav button')];
function mostrar(id){document.querySelectorAll('main > section').forEach(s => s.hidden = s.id !== id);
  abas.forEach(b => b.setAttribute('aria-selected', b.dataset.alvo === id));
  try{history.replaceState(null,'','#'+id)}catch(e){} window.scrollTo({top:0});
  desenhar(id);}
abas.forEach(b => b.addEventListener('click', () => mostrar(b.dataset.alvo)));
const feitos = new Set();
Chart.defaults.font.family = getComputedStyle(document.body).getPropertyValue('--fb');
Chart.defaults.color = getComputedStyle(document.body).getPropertyValue('--ink2').trim();
Chart.defaults.borderColor = getComputedStyle(document.body).getPropertyValue('--linha').trim();
function grafico(id, cfg){const el = document.getElementById(id); if(!el) return; if(el._chart) el._chart.destroy(); el._chart = new Chart(el, cfg);}
const Ls = ['0','1','2','3'];
function linhaCurvas(){
  const conj = document.getElementById('sel-conj').value, met = document.getElementById('sel-met').value;
  grafico('g-curvas', {type:'line', data:{labels: Ls.map(l => 'L'+l), datasets: D.modelos.map(m => ({label:m, data: Ls.map(l => (D.curvas[conj][m][l]||{})[met]), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='balanceada'?'acurácia balanceada (%)':'acerto (%)'}, suggestedMin:60, suggestedMax:95}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function barrasFases(){
  const conj = document.getElementById('sel-fases').value; const cols = ['2A_linear_ryzen','2B_A0','2B_A2','F3_L0','F3_L1','F3_L2','F3_L3'];
  const rot = {'2A_linear_ryzen':'2-A (Ryzen)','2B_A0':'2-B A0','2B_A2':'2-B A2','F3_L0':'F3 L0','F3_L1':'F3 L1','F3_L2':'F3 L2','F3_L3':'F3 L3'};
  const mods = Object.keys(D.fases).filter(m => D.fases[m][conj]['2B_A0']);
  grafico('g-fases', {type:'bar', data:{labels: cols.map(c => rot[c]), datasets: mods.map(m => ({label:m, data: cols.map(c => (D.fases[m][conj][c]||{}).balanceada ?? null), backgroundColor:cor(m)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'acurácia balanceada (%)'}, min:0, max:100}}}});
}
function pareto(){
  const pts = D.regra36.map(x => ({x:x.segundos_mediana_36, y:x.acuracia_balanceada_36, m:x.modelo, L:x.biblioteca_epoca, r:x.risco, nd: D.pareto.nao_dominados.includes(x.modelo+'/L'+x.biblioteca_epoca)}));
  grafico('g-pareto', {type:'scatter', data:{datasets: D.modelos.map(m => ({label:m, data: pts.filter(p => p.m===m), backgroundColor: cor(m), pointRadius: c => (c.raw && c.raw.nd) ? 9 : 5, pointStyle: c => (c.raw && c.raw.nd) ? 'rectRot' : 'circle'}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{title:{display:true,text:'segundos por diagnóstico (mediana, 36)'}}, y:{title:{display:true,text:'acurácia balanceada (36, %)'}, suggestedMin:60, suggestedMax:95}},
      plugins:{tooltip:{callbacks:{label: c => `${c.raw.m} L${c.raw.L}: ${c.raw.y}% · ${c.raw.x} s · risco ${c.raw.r}${c.raw.nd?' · não dominado':''}`}}}}});
}
function bootstrap(){
  const conj = document.getElementById('sel-boot').value; const ent = Object.entries(D.bootstrap[conj]).filter(([k,v]) => v.p >= 0.005).sort((a,b) => b[1].p - a[1].p);
  grafico('g-boot', {type:'bar', data:{labels: ent.map(e => e[0]), datasets:[{label:'P(top-1)', data: ent.map(e => Math.round(e[1].p*1000)/10), backgroundColor: ent.map(e => cor(e[0].split('/')[0]))}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{title:{display:true,text:'% das réplicas em que é o melhor'}, min:0, max:100}}, plugins:{legend:{display:false}, tooltip:{callbacks:{label: c => c.formattedValue+'% · IC 95% ['+D.bootstrap[conj][c.label].ic.join('–')+']'}}}}});
}
function documentacao(){
  const eps = ['1','2','3'];
  grafico('g-doc', {type:'bar', data:{labels: eps.map(e => 'Época '+e), datasets: D.modelos.map(m => ({label:m, data: eps.map(e => (D.documentacao[m]||{})[e]?.aceitas ?? 0), backgroundColor:cor(m)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'edições aceitas'}, beginAtZero:true}}, plugins:{tooltip:{callbacks:{afterLabel: c => { const d = D.documentacao[c.dataset.label][String(c.dataIndex+1)]; return d ? `de ${d.propostas} propostas (${d.aceitas_pct}%)` : ''; }}}}}});
}
function rejeicoes(){
  const codigos = [...new Set(D.modelos.flatMap(m => Object.keys(D.rejeicoes[m]||{})))];
  const tot = Object.fromEntries(codigos.map(c => [c, D.modelos.reduce((s,m) => s + ((D.rejeicoes[m]||{})[c]||0), 0)]));
  codigos.sort((a,b) => tot[b]-tot[a]); const top = codigos.slice(0, 10);
  grafico('g-rej', {type:'bar', data:{labels: top, datasets: D.modelos.map(m => ({label:m, data: top.map(c => (D.rejeicoes[m]||{})[c]||0), backgroundColor:cor(m)}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, title:{display:true,text:'propostas rejeitadas (3 épocas)'}}, y:{stacked:true}}}});
}
function recuperacao(){
  grafico('g-rec', {type:'line', data:{labels: Ls.map(l => 'L'+l), datasets: D.modelos.map(m => ({label:m, data: Ls.map(l => (D.recuperacao[m][l]||{}).hit3_90), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'hit@3 nos 90 (%)'}, suggestedMin:70, suggestedMax:85}}, plugins:{tooltip:{callbacks:{afterLabel: c => { const r = D.recuperacao[c.dataset.label][String(c.dataIndex)]; return `${r.verbetes} verbetes (${r.novos} novos), ~${r.tokens} tokens`; }}}}}});
}
function custo(){
  grafico('g-custo', {type:'bar', data:{labels: Ls.map(l => 'diagnóstico com L'+l), datasets: D.modelos.map(m => ({label:m, data: Ls.map(l => (D.custo[m][l]||{}).segundos), backgroundColor:cor(m)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'segundos por diagnóstico (mediana, 90)'}, beginAtZero:true}}, plugins:{tooltip:{callbacks:{afterLabel: c => { const r = D.custo[c.dataset.label][String(c.dataIndex)]; return r ? `prefill ${r.prefill_s} s · geração ${r.geracao_s} s · p95 ${r.p95} s` : ''; }}}}}});
}
function revisao(){
  const mods = Object.keys(D.revisao); const cats = ['Correta','Parcial','Errada']; const cores = {Correta:'#2e7d4f',Parcial:'#b7791f',Errada:'#b3392b'};
  grafico('g-rev', {type:'bar', data:{labels: mods, datasets: cats.map(c => ({label:c, data: mods.map(m => D.revisao[m][c]), backgroundColor: cores[c]}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true}, y:{stacked:true, max:100, title:{display:true,text:'% das edições revisadas'}}}, plugins:{tooltip:{callbacks:{afterLabel: c => 'n = '+D.revisao[c.label].n}}}}});
}
function f2b(){
  const conds = ['A0','A1','A2','A3','A4','A5']; const mods = Object.keys(D.f2b);
  grafico('g-f2b', {type:'bar', data:{labels: conds, datasets: mods.map(m => ({label:m, data: conds.map(c => (D.f2b[m][c]||{}).acerto ?? null), backgroundColor:cor(m)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'acerto (%) nos 90'}, min:0, max:100}}, plugins:{tooltip:{callbacks:{afterLabel: c => { const r = D.f2b[c.dataset.label][c.label]; return r ? `n = ${r.n} · ${r.segundos} s/caso` : ''; }}}}}});
}
function f2a(){
  const mods = Object.keys(D.f2a); const est = [...new Set(mods.flatMap(m => Object.keys(D.f2a[m])))];
  grafico('g-f2a', {type:'bar', data:{labels: est, datasets: mods.map(m => ({label:m, data: est.map(e => (D.f2a[m][e]||{}).acerto ?? null), backgroundColor:cor(m)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'acerto (%) — Fase 2-A, Ryzen'}, min:0, max:100}}}});
}
function desenhar(id){
  if(feitos.has(id)) return; feitos.add(id);
  ({visao:[linhaCurvas, barrasFases], fase3:[documentacao, rejeicoes, recuperacao, custo, revisao], decisao:[pareto, bootstrap], fases2:[f2b, f2a]}[id]||[]).forEach(f => { try{ f(); }catch(e){ console.error(e); } });
}
['sel-conj','sel-met'].forEach(i => document.getElementById(i).addEventListener('change', linhaCurvas));
document.getElementById('sel-fases').addEventListener('change', barrasFases);
document.getElementById('sel-boot').addEventListener('change', bootstrap);
let fEstado = 'aberta', fEric = false;
function filtrar(){
  document.querySelectorAll('.ficha').forEach(f => { f.hidden = !((fEstado === 'todas' || f.dataset.estado === fEstado) && (!fEric || f.dataset.quem === 'eric')); });
  document.querySelectorAll('.bloco-pend').forEach(b => { const fs = [...b.querySelectorAll('.ficha')]; b.hidden = fs.length > 0 && fs.every(f => f.hidden); });
  document.querySelectorAll('.filtros button').forEach(b => b.setAttribute('aria-pressed', b.dataset.estado ? String(b.dataset.estado === fEstado) : String(fEric)));
}
document.querySelectorAll('.filtros button').forEach(b => b.addEventListener('click', () => { if(b.dataset.estado) fEstado = b.dataset.estado; else fEric = !fEric; filtrar(); }));
function irPara(secao, id){
  mostrar(secao); const el = document.getElementById(id); if(!el) return;
  if(el.hidden){ fEstado = 'todas'; fEric = false; filtrar(); }
  el.scrollIntoView({behavior:'smooth', block:'start'}); el.classList.add('realce'); setTimeout(() => el.classList.remove('realce'), 2500);
}
document.querySelectorAll('[data-ir]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); const [s, id] = a.dataset.ir.split('|'); irPara(s, id); }));
document.querySelectorAll('button.copiar').forEach(b => b.addEventListener('click', async () => {
  try{ await navigator.clipboard.writeText(b.dataset.cmd); b.textContent = 'copiado'; }catch(e){ b.textContent = 'selecione e copie'; }
  setTimeout(() => b.textContent = 'copiar', 1800);
}));
filtrar();
const inicial = (location.hash||'#inicio').slice(1);
mostrar(document.getElementById(inicial) ? inicial : 'inicio');
"""


def kpis(dados: dict, vered: dict) -> str:
    v = dados["vencedor"]
    p36 = dados["bootstrap"]["nos_36"][f'{v["modelo"]}/L{v["biblioteca_epoca"]}']["p"]
    meta = dados["meta"]
    mde36 = next(x["delta_pp"] for x in dados["mde"] if x["n"] == 36)
    itens = [
        ("Modelo escolhido", f'{v["modelo"]}', f'biblioteca L{v["biblioteca_epoca"]} · {vered[v["modelo"]]["licenca"]}'),
        ("Acurácia balanceada (36)", f'{fmt(v["acuracia_balanceada_36"])}%', f'acerto simples {fmt(v["acerto_36"])}%'),
        ("P(top-1) no bootstrap", f'{fmt(p36 * 100)}%', f'{dados["bootstrap_meta"]["n"]} réplicas, nos 36'),
        ("Custo por diagnóstico", f'{fmt(v["segundos_mediana_36"])} s', "mediana nos 36, máquina-alvo i5"),
        ("Inferências da bateria", f'{meta["n_diagnosticos"] + meta["n_propostas"]:,}'.replace(",", "."), f'{meta["n_diagnosticos"]:,} diagnósticos + {meta["n_propostas"]} propostas'.replace(",", ".")),
        ("Erros de infraestrutura", f'{meta["erros_infra"]}', "em 4 modelos × 4 versões × 90 casos"),
        ("Efeito mínimo detectável", f'{fmt(mde36)} pp', "nos 36; nenhum p < 0,05"),
    ]
    return '<div class="kpis">' + "".join(f"<div class='kpi'><span>{html.escape(t)}</span><b>{html.escape(b)}</b><small>{html.escape(s)}</small></div>" for t, b, s in itens) + "</div>"


def cards_modelos(dados: dict, vered: dict) -> str:
    out = []
    for m in MODELOS_F3:
        v = vered[m]; titulo, leitura = LEITURA[m]
        rev = v["revisao"]
        rev_txt = f'{fmt(rev["Correta"])}% / {fmt(rev["Parcial"])}% / {fmt(rev["Errada"])}% (n = {rev["n"]})' if rev else "sem edições aceitas"
        fatos = [("Melhor versão", f'L{v["melhor_L"]}'), ("Acurácia balanceada (36)", f'{fmt(v["balanceada"])}%'),
                 ("Acerto (36)", f'{fmt(v["acerto"])}%'), ("P(top-1) nos 36", f'{fmt((v["p_top1"] or 0) * 100)}%'),
                 ("Segundos / diagnóstico", f'{fmt(v["segundos"])} s'), ("Autoenvenenamento máx.", f'{fmt(v["autoenv"])}%'),
                 ("Edições aceitas / propostas", f'{v["aceitas"]} / {v["propostas"]}'), ("Revisão correta / parcial / errada", rev_txt),
                 ("Licença", v["licenca"]), ("Risco (Pareto)", fmt(v["risco"]))]
        out.append(f"""<article class="card{' venc' if v['vencedor'] else ''}">
<h3><span class="dot" style="background:{CORES[m]}"></span>{html.escape(m)} {'<span class="tag">escolhido</span>' if v['vencedor'] else ''}</h3>
<p class="nota"><strong>{html.escape(titulo)}</strong></p>
<div class="fatos">{''.join(f'<div><span>{html.escape(a)}</span><b>{html.escape(b)}</b></div>' for a, b in fatos)}</div>
<p>{html.escape(leitura)}</p></article>""")
    return '<div class="grade">' + "".join(out) + "</div>"


def heatmap(dados: dict, chave: str, nomes: dict, titulo: str) -> str:
    linhas = []
    for m in MODELOS_F3:
        for k in sorted(dados[chave][m], key=int):
            vals = dados[chave][m][k]
            tds = "".join(f'<td class="num" style="background:{_cor_heat(vals.get(L))}">{fmt(vals.get(L))}%</td>' for L in "0123")
            linhas.append(f"<tr><td>{html.escape(m)}</td><td>{k} {nomes[int(k)]}</td>{tds}</tr>")
    return f'<div class="tabela heat"><table><thead><tr><th>Modelo</th><th>{titulo}</th><th>L0</th><th>L1</th><th>L2</th><th>L3</th></tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'


def _cor_heat(v) -> str:
    if v is None:
        return "transparent"
    a = max(0.0, min(1.0, (v - 20) / 80))
    return f"color-mix(in srgb, var(--acento) {int(a * 55)}%, transparent)"


def tabela_hipoteses(hips: list[dict]) -> str:
    linhas = []
    for h, enunciado in HIPOTESES:
        v = next(x for x in hips if x["h"] == h)
        linhas.append(f'<tr><td class="h">{h}</td><td>{html.escape(enunciado)}<br><span class="tag {v["cor"]}">{html.escape(v["veredito"])}</span><br><span class="nota">{html.escape(v["ev"])}</span></td></tr>')
    return f'<div class="tabela"><table><thead><tr><th>Hipótese</th><th>Enunciado pré-registrado, veredito e evidência</th></tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'


def figura(figs: dict, num: str) -> str:
    if num not in figs:
        return ""
    return f'<figure><img src="{figs[num]}" alt="{html.escape(FIGURAS[num])}"><figcaption>Figura {num} — {html.escape(FIGURAS[num])} (gerada por script a partir dos registros oficiais).</figcaption></figure>'


# ------------------------------------------------------------------ projeto: início, pendências, roadmap

ESTADO_FASE = {"concluida": "Concluída", "andamento": "Em andamento", "nao_iniciada": "Não iniciada", "outro": "—"}
ESTADO_CORRIDA = {"feita": "Feita", "rodando": "Rodando", "pendente": "Pendente", "opcional": "Opcional",
                  "aguarda": "Aguarda decisão", "outro": "—"}


def _chip(classe: str, texto: str) -> str:
    return f'<span class="chip {classe}">{html.escape(texto)}</span>'


def faixa_fases(road: dict, compacta: bool = False) -> str:
    itens = []
    for f in road["fases"]:
        corpo = "" if compacta else f"<small>{pt.inline(f.o_que_e)}</small><p>{pt.inline(f.estado)}</p>"
        itens.append(f'<div class="fase {f.classe}"><b>{pt.inline(f.nome)}</b>{_chip(f.classe, ESTADO_FASE.get(f.classe, "—"))}{corpo}</div>')
    return '<div class="fases">' + "".join(itens) + "</div>"


def cartoes_corridas(road: dict) -> str:
    out = []
    for c in road["corridas"]:
        cmd = ""
        if c.comando:
            cmd = (f'<div class="cmd"><pre><code>{html.escape(c.comando)}</code></pre>'
                   f'<button class="copiar" type="button" data-cmd="{html.escape(c.comando, quote=True)}">copiar</button></div>')
        fatos = [("Estado", c.estado), ("Inferências / tempo", c.tempo), ("Pré-requisito", c.prerequisito), ("O que fecha", c.fecha)]
        fatos_html = "".join(f"<div><span>{html.escape(a)}</span><b>{pt.inline(b)}</b></div>" for a, b in fatos if b)
        out.append(f'<article class="corrida {c.classe}"><header><span class="numero">{html.escape(c.numero)}</span><h3>{pt.inline(c.nome)}</h3>'
                   f'{_chip(c.classe, ESTADO_CORRIDA.get(c.classe, "—"))}</header><div class="fatos2">{fatos_html}</div>{cmd}</article>')
    return '<div class="corridas">' + "".join(out) + "</div>"


def avisos_corridas(road: dict) -> list[str]:
    """Confere a coluna Estado do roadmap contra a pasta de saída de cada corrida (resumo_fase3.json
    gravado = corrida avaliada); só avisa, não muda nada."""
    avisos = []
    for c in road["corridas"]:
        if not c.saida or "-Modo" not in c.comando:
            continue  # só as corridas do rodar_fase3b.ps1 gravam resumo_fase3.json na própria pasta de saída
        pasta = EXP / "resultados_alvo" / c.saida
        avaliada = (pasta / "resumo_fase3.json").exists()
        if c.classe in ("pendente", "aguarda", "opcional") and avaliada:
            avisos.append(f"corrida {c.numero} ({c.saida}) está avaliada em disco, mas o roadmap diz {c.estado[:30]!r}")
        if c.classe == "feita" and not pasta.exists():
            avisos.append(f"corrida {c.numero} ({c.saida}) marcada como feita, mas a pasta não existe")
    return avisos


def secao_inicio(dados: dict, pend: list, road: dict) -> str:
    fichas = [f for b in pend for f in b.fichas]
    abertas = [f for f in fichas if f.aberta]
    do_eric = [f for f in abertas if f.depende_do_eric]
    corr = road["corridas"]
    n_rod = sum(c.classe == "rodando" for c in corr)
    n_pend = sum(c.classe in ("pendente", "aguarda") for c in corr)
    n_feitas = sum(c.classe == "feita" for c in corr)
    fase = next((f for f in road["fases"] if f.classe == "andamento"), None)
    v = dados["vencedor"]
    m = re.search(r"fim do \*\*(Mês \d+)\*\*", road["posicao"])
    itens = [("Fase atual", fase.nome if fase else "—", f"cronograma do projeto: fim do {m.group(1)}" if m else ""),
             ("Modelo escolhido", v["modelo"], f'biblioteca L{v["biblioteca_epoca"]} (decisão 52)'),
             ("Pendências abertas", str(len(abertas)), f"{len(do_eric)} dependem de decisão do Eric"),
             ("Corridas da 3-B", f"{n_rod} rodando · {n_pend} pendentes", f"{n_feitas} feitas"),
             ("Estado registrado em", road["data"] or "—", "roadmap.md e pendencias.md")]
    kp = '<div class="kpis">' + "".join(f"<div class='kpi'><span>{html.escape(t)}</span><b>{html.escape(b)}</b><small>{html.escape(s)}</small></div>" for t, b, s in itens) + "</div>"
    lista = "".join(f'<li><a href="#{f.id_html}" data-ir="pendencias|{f.id_html}"><span class="numero">{f.numero}</span> {pt.inline(f.titulo)}</a>'
                    f'<br><span class="nota">Recomendação: {pt.inline(f.campos.get("Recomendação", "—"))}</span></li>' for f in do_eric)
    corridas = "".join(f'<li>{_chip(c.classe, ESTADO_CORRIDA.get(c.classe, "—"))} <strong>{pt.inline(c.nome.split(" — ")[0])}</strong> — {pt.inline(c.estado)}</li>' for c in corr)
    return f'''<section id="inicio">
<h1>Onde o projeto está</h1>
<p class="lead">Painel único do TCC: o estado de cada fase, as decisões que esperam resposta, as corridas que faltam e todos os números dos testes — tudo lido dos arquivos do repositório por script, nada digitado à mão.</p>
{kp}
<h2>Fases</h2>
{faixa_fases(road, compacta=True)}
{pt.md_doc_para_html(road["posicao"])}
<h2>O que precisa de você</h2>
<p>Cada item abre a ficha completa na aba Pendências: o que é, por que importa, opções e recomendação.</p>
<ol class="lista-eric">{lista}</ol>
<h2>Corridas da Fase 3-B</h2>
<ul class="lista-corridas">{corridas}</ul>
<p class="nota">Comandos, pré-requisitos e o que cada corrida fecha: aba Roadmap.</p>
</section>'''


def secao_pendencias(pend: list) -> str:
    fichas = [f for b in pend for f in b.fichas]
    n_ab = sum(f.aberta for f in fichas)
    n_fe = len(fichas) - n_ab
    blocos_html = []
    for b in pend:
        cards = "".join(pt.html_ficha(f) for f in b.fichas)
        if b.fichas:
            intro = f"<details><summary>Contexto do bloco</summary>{pt.md_doc_para_html(b.intro)}</details>" if b.intro.strip() else ""
            resto = f"<details><summary>Texto original das pendências antigas deste bloco</summary>{pt.md_doc_para_html(b.resto)}</details>" if b.resto.strip() else ""
        else:
            intro = f"<details><summary>Ver o texto original (bloco só de registro)</summary>{pt.md_doc_para_html(b.intro)}{pt.md_doc_para_html(b.resto)}</details>"
            resto = ""
        blocos_html.append(f'<div class="bloco-pend"><h2>{pt.inline(b.titulo)}</h2>{intro}{cards}{resto}</div>')
    return f'''<section id="pendencias" hidden>
<h1>Pendências e decisões</h1>
<p class="lead">Uma ficha por pergunta, em linguagem direta: o que é, por que importa, as opções, a recomendação e a decisão (quando sai). {n_ab} abertas e {n_fe} fechadas; o filtro começa nas abertas. Para responder, basta citar o número da ficha no chat.</p>
<div class="filtros" role="group" aria-label="Filtro das fichas"><button type="button" data-estado="aberta" aria-pressed="true">Abertas ({n_ab})</button><button type="button" data-estado="fechada" aria-pressed="false">Fechadas ({n_fe})</button><button type="button" data-estado="todas" aria-pressed="false">Todas</button><button type="button" data-quem="eric" aria-pressed="false">Só o que depende do Eric</button></div>
{"".join(blocos_html)}
</section>'''


def secao_roadmap(road: dict) -> str:
    resto = "".join(f"<h2>{pt.inline(t)}</h2>{pt.md_doc_para_html(c)}" for t, c in road["secoes"])
    return f'''<section id="roadmap" hidden>
<h1>Roadmap — onde estamos e o que falta rodar</h1>
<p class="lead">Estado por fase, corridas pendentes com o comando pronto, a sonda de correção, o esqueleto das Fases 4 e 5 e a tabela para encaixar pontos novos. Fonte: <code>roadmap.md</code> de {html.escape(road["data"])}.</p>
<h2>1. Onde estamos, por fase</h2>
{faixa_fases(road)}
{pt.md_doc_para_html(road["posicao"])}
<h2>2. O que precisamos rodar (máquina), em ordem</h2>
{cartoes_corridas(road)}
{pt.md_doc_para_html(road["fora_da_maquina"])}
{resto}
</section>'''


def pagina(dados: dict, blocos: dict, figs: dict, pend: list, road: dict) -> str:
    vered = texto_vereditos(dados)
    hips = vereditos_hipoteses(dados)
    v = dados["vencedor"]
    B = lambda nome: md_para_html(blocos[nome])  # noqa: E731
    ponte = dados["tres_b"].get("fase3b_ponte", {}).get("linhas", [])
    ponte_txt = "; ".join(f'{x["modelo"]} b/c {x["pareado_vs_f3"]["b"]}/{x["pareado_vs_f3"]["c"]}' for x in ponte)
    dados_json = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    return f"""<!-- ! Alteração de IA - Revisar: painel do projeto, GERADO por ferramentas/gerar_dashboard.py a partir de pendencias.md, roadmap.md e dos registros oficiais dos testes (não editar à mão; --check acusa diferença).
     ! Motivo: o Eric pediu as pendências e o roadmap em forma visual e um único painel do projeto, acessível de qualquer lugar; todo valor sai dos mesmos arquivos do Memorial. -->
<title>Painel do Agente de QA</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<header class="topo"><div class="in">
<div class="marca">Painel do Agente de QA<small>TCC · agente de QA E2E autônomo com self-healing · estado em {html.escape(road["data"])} · registros dos testes de {html.escape(dados["meta"]["resumo_gerado_em"][:10])}</small></div>
<nav aria-label="Seções">
<span class="grupo">Projeto</span><button data-alvo="inicio">Início</button><button data-alvo="pendencias">Pendências</button><button data-alvo="roadmap">Roadmap</button>
<span class="grupo">Testes</span><button data-alvo="visao">Resultados</button><button data-alvo="modelos">Modelos</button><button data-alvo="fase3">Fase 3</button>
<button data-alvo="decisao">Decisão</button><button data-alvo="hipoteses">Hipóteses</button><button data-alvo="fases2">Fases 2-A e 2-B</button>
<button data-alvo="comparacao">Entre fases</button><button data-alvo="metodo">Método e limites</button>
</nav></div></header>
<main>
{secao_inicio(dados, pend, road)}
{secao_pendencias(pend)}
{secao_roadmap(road)}
<section id="visao" hidden>
<h1>O que os testes decidiram</h1>
<p class="lead">Quatro modelos locais diagnosticaram 90 falhas de integração do sistema-cobaia em quatro versões da biblioteca de conhecimento (a original L0 e as três que cada modelo escreveu, L1–L3). Pela regra fixada antes da bateria, o padrão do agente passa a ser <strong>{html.escape(v["modelo"])}</strong> com a biblioteca no estado <strong>L{v["biblioteca_epoca"]}</strong>.</p>
{kpis(dados, vered)}
<h2>Acurácia balanceada por versão da biblioteca</h2>
<p>Acurácia balanceada = média do acerto por causa raiz (penaliza um modelo que colapsa num rótulo). Os 36 casos de avaliação nunca receberam a causa correta; os 54 de aprendizado, sim — é onde o modelo propôs edições.</p>
<div class="controles"><label>Conjunto <select id="sel-conj"><option value="36">36 de avaliação</option><option value="54">54 de aprendizado</option><option value="90">90 (todos)</option></select></label>
<label>Métrica <select id="sel-met"><option value="balanceada">acurácia balanceada</option><option value="acerto">acerto simples</option></select></label></div>
<div class="chart"><canvas id="g-curvas"></canvas></div>
<h2>As três fases, lado a lado</h2>
<p>2-A: prompts sem documentação, numa máquina de desenvolvimento (Ryzen). 2-B: biblioteca escrita à mão, recuperada por busca (A2), na máquina-alvo (i5). Fase 3: a biblioteca editada pelo próprio modelo, época a época. Os 36 casos são os mesmos nas três fases; os quatro casos corrigidos antes da Fase 3 ({", ".join(dados["casos_alterados"])}) caem no conjunto de aprendizado.</p>
<div class="controles"><label>Conjunto <select id="sel-fases"><option value="36">36 de avaliação</option><option value="90">90 (todos)</option></select></label></div>
<div class="chart"><canvas id="g-fases"></canvas></div>
{figura(figs, "16")}
</section>

<section id="modelos" hidden>
<h1>Avaliação de cada modelo</h1>
<p class="lead">Números da regra de decisão (36 casos de avaliação), da bateria e da revisão humana das edições; a leitura de cada veredito é a da análise decisória do Memorial (§8.1).</p>
{cards_modelos(dados, vered)}
<h2>Modelos eliminados antes da Fase 3</h2>
<p>Na Fase 2-B, o <code>phi4-mini:3.8b</code> não aproveitou documentação nenhuma e o <code>qwen2.5-coder:1.5b</code> (e suas variantes de quantização) não fez a tarefa. Os números estão na seção "Fases 2-A e 2-B" e nas tabelas entre fases.</p>
<h2>Acerto por classe de defeito (90 casos)</h2>
<p>As seis classes seguem as fases de um compilador: léxica (o corpo é legível?), sintática (a forma bate?), semântica (tipos e domínios), tradução (mapeamento entre camadas), runtime (tempo e estado) e efeito (o que o usuário vê). A classe tradução é a mais difícil para todos.</p>
{heatmap(dados, "classes", CLASSES, "Classe")}
<h2>Acerto por nível de dificuldade (90 casos)</h2>
{heatmap(dados, "niveis", NIVEIS, "Nível")}
</section>

<section id="fase3" hidden>
<h1>Fase 3 — a biblioteca gerida pelo modelo</h1>
<p class="lead">Cada modelo recebeu uma cópia da biblioteca original e, em três épocas, diagnosticou os 90 casos e propôs edições nos 54 de aprendizado (nota, retificação ou verbete novo, só por acréscimo). Um validador em código, com 30 motivos de rejeição, decidiu o que entrou. Bateria de 13 a 15/09/2026 na máquina-alvo, {dados["meta"]["n_diagnosticos"]:,} diagnósticos e {dados["meta"]["n_propostas"]} rodadas de proposta, {dados["meta"]["erros_infra"]} erros de infraestrutura.</p>
<h2>Edições aceitas por época</h2>
<p>A biblioteca satura: as aceitações caem de uma época para a outra porque as rejeições passam a ser por duplicidade e por teto de notas por verbete. O Granite não teve nenhuma edição aceita: suas propostas ultrapassavam o teto de texto do validador.</p>
<div class="chart"><canvas id="g-doc"></canvas></div>
<details><summary>Tabela: documentação por época (propostas, aceitas, operações, tokens)</summary>{B("documentacao")}</details>
<h2>Por que as propostas foram rejeitadas</h2>
<div class="chart alto"><canvas id="g-rej"></canvas></div>
<details><summary>Tabela: códigos de rejeição por modelo</summary>{B("rejeicoes")}</details>
{figura(figs, "14")}
<h2>Recuperação: a biblioteca maior não ajuda o recuperador</h2>
<p>hit@3 = proporção de casos em que o verbete de ouro está entre os três recuperados (BM25). Com mais verbetes e notas, o hit@3 cai levemente; nenhum verbete novo escrito pelo modelo chegou ao contexto dos 36 casos de avaliação.</p>
<div class="chart"><canvas id="g-rec"></canvas></div>
<details><summary>Tabela: recuperação por versão da biblioteca</summary>{B("recuperacao")}</details>
{figura(figs, "13")}{figura(figs, "15")}
<h2>Custo por diagnóstico</h2>
<p>Medianas nos 90 casos por versão da biblioteca. A biblioteca anotada encarece o prefill (a parte do tempo gasta lendo o prompt); o custo da passada final com L3 foi medido num momento diferente da corrida e não prova que L3 seja mais barata.</p>
<div class="chart"><canvas id="g-custo"></canvas></div>
<details><summary>Tabela: custo por inferência (diagnóstico e proposta, prefill e geração, horas por modelo)</summary>{B("custo")}</details>
<h2>Revisão humana das edições aceitas</h2>
<p>Amostra determinística de até 30 edições por modelo, avaliada contra o código do cobaia com a rubrica correta / parcial / errada (primeira passada por IA, aceita pelo Eric). No vencedor, a maioria das edições corretas repete o que o verbete já dizia.</p>
<div class="chart baixo"><canvas id="g-rev"></canvas></div>
{B("revisao")}
<h2>Curvas, pareamentos e trocas de rótulo</h2>
<details><summary>Acerto por versão (36 e 54)</summary>{B("curva_acerto")}</details>
<details><summary>Acurácia balanceada por versão (36, 54 e 90)</summary>{B("curva_balanceada")}</details>
<details><summary>Pareado L1/L2/L3 contra L0 (McNemar exato, Holm, g de Cohen, Q de Cochran)</summary>{B("pareado")}</details>
<details><summary>Trocas de rótulo entre épocas (✓→✗ = autoenvenenamento)</summary>{B("flips")}</details>
<details><summary>Efeito mínimo detectável por tamanho de amostra</summary>{B("mde")}<p class="nota">Com 36 casos só uma diferença de cerca de 19 pontos percentuais sairia significativa; o maior ganho medido foi de 11,1 pp. A ausência de p < 0,05 é um limite da amostra, não a prova de que não há efeito — por isso a decisão combina critérios em vez de depender de um teste.</p></details>
<details><summary>Qualidade das respostas (rótulo mais frequente, fora do conjunto, contexto com nota)</summary>{B("qualidade")}</details>
{figura(figs, "12")}
</section>

<section id="decisao" hidden>
<h1>A decisão, na ordem em que foi tomada</h1>
<p class="lead">1) Regra pré-registrada: ranking por acurácia balanceada nos 36, veto por autoenvenenamento acima de {fmt(dados["meta"]["limiar_veto"])}%, desempate por licença e depois pela época mais baixa. 2) Robustez: bootstrap por caso, estabilidade do ranking, fronteira de Pareto e escore ponderado com pesos declarados antes de olhar o resultado. 3) Ponte de versão do Ollama antes de misturar corridas.</p>
<h2>Passo 1 — a regra</h2>
{B("dm_regra_36")}
<h2>Passo 2 — quão frágil é a escolha</h2>
<p>Bootstrap: {dados["bootstrap_meta"]["n"]} reamostragens dos casos (semente {dados["bootstrap_meta"]["semente"]}); P(top-1) é a fração das réplicas em que a combinação (modelo, versão) tem a maior acurácia balanceada.</p>
<div class="controles"><label>Conjunto <select id="sel-boot"><option value="nos_36">36 de avaliação</option><option value="nos_90">90 (todos)</option></select></label></div>
<div class="chart alto"><canvas id="g-boot"></canvas></div>
<details><summary>Tabela: intervalos bootstrap e P(top-1)</summary>{B("dm_bootstrap")}</details>
<p>Estabilidade: em {dados["estabilidade"]["total"]} cortes (colunas das três fases nos 36 e nos 90, e classes de defeito), cada modelo ficou em primeiro este número de vezes — {"; ".join(f"{m}: {n}" for m, n in dados["estabilidade"]["top1"].items())}. Sem edição, o Granite é o mais estável; com a biblioteca editada, o qwen2.5:7b passa à frente.</p>
<h2>Fronteira de Pareto: acerto × custo × risco</h2>
<p>Losangos maiores = combinações não dominadas (nenhuma outra é ao mesmo tempo mais certeira, mais barata e menos arriscada): {", ".join(dados["pareto"]["nao_dominados"])}.</p>
<div class="chart alto"><canvas id="g-pareto"></canvas></div>
<details><summary>Tabela: Pareto</summary>{B("dm_pareto")}</details>
{figura(figs, "18")}
<h2>Escore ponderado e sensibilidade</h2>
{B("dm_escore")}
<h2>Ponte de versão (Fase 3-B)</h2>
<p>O Ollama passou de 0.34.0 (bateria) para 0.34.1 depois dela. A ponte repete L0 nos 36 no runtime novo e compara caso a caso com a Fase 3: {html.escape(ponte_txt)} — pareáveis (b + c ≤ 2). O Granite não rodou por falta de RAM e ficou fora da 3-B.</p>
{B("dm_3b")}
<h2>Frase da decisão</h2>
{B("dm_frase")}
<p><strong>O que a decisão não diz.</strong> Não diz que a biblioteca escrita pelo modelo é melhor por conter conhecimento verdadeiro: diz que, medida nos 36 casos nunca vistos, a versão L1 produziu mais acertos e nenhum a menos, com custo de prefill maior e notas de qualidade duvidosa. E não diz que o qwen2.5:7b é melhor que o Granite em geral: sem edição, o Granite acerta mais; com edição, só o qwen2.5:7b conseguiu escrever no formato exigido.</p>
</section>

<section id="hipoteses" hidden>
<h1>Hipóteses pré-registradas e vereditos</h1>
<p class="lead">As seis hipóteses foram escritas antes da bateria (achado 4.29 do Memorial). Cada veredito abaixo cita o número que o sustenta, lido dos registros oficiais.</p>
{tabela_hipoteses(hips)}
<h2>Achados que a bateria acrescentou</h2>
<ul>
<li><strong>4.30</strong> O Granite não documentou porque o formato não coube no teto de texto, não porque não soube.</li>
<li><strong>4.31</strong> O resultado reproduz entre execuções e entre versões do runtime (b = c = 0 na maioria dos pareamentos).</li>
<li><strong>4.32</strong> A biblioteca satura em três épocas sob a regra de só acréscimo (rejeições por duplicidade e teto de notas).</li>
<li><strong>4.33</strong> Nenhum ganho alcança o efeito mínimo detectável — e isso é um resultado, não uma falha.</li>
<li><strong>4.34</strong> O pico é L1, não L3.</li>
<li><strong>4.35</strong> As edições aceitas são, na maioria, redundantes ou erradas — e o ganho veio mesmo assim.</li>
</ul>
</section>

<section id="fases2" hidden>
<h1>Fases 2-A e 2-B</h1>
<p class="lead">A Fase 2-A mediu os modelos sem documentação, com estratégias de prompt diferentes, numa máquina de desenvolvimento. A Fase 2-B, na máquina-alvo, mediu o efeito da biblioteca escrita à mão em seis condições: sem documentação (A0), biblioteca inteira no prompt (A1), recuperação por busca com três verbetes (A2), verbete de ouro forçado (A3, o teto), verbete distrator (A4) e verbete errado (A5, adversarial).</p>
<h2>Fase 2-B — acerto por condição</h2>
<div class="chart alto"><canvas id="g-f2b"></canvas></div>
<p>A recuperação (A2) foi o modo adotado: a biblioteca inteira no prompt (A1) custa mais e não rende mais. A condição A5 mede a adesão cega a documentação errada — o risco que a validação em código da Fase 3 existe para conter.</p>
{figura(figs, "07")}{figura(figs, "08")}{figura(figs, "11")}
<details><summary>Mais figuras da Fase 2-B (prefill × acerto; quantização e trocas de rótulo)</summary>{figura(figs, "09")}{figura(figs, "10")}</details>
<h2>Fase 2-A — acerto por estratégia de prompt</h2>
<div class="chart"><canvas id="g-f2a"></canvas></div>
<details><summary>Figuras da Fase 2-A</summary>{figura(figs, "01")}{figura(figs, "02")}{figura(figs, "03")}{figura(figs, "04")}{figura(figs, "05")}{figura(figs, "06")}</details>
</section>

<section id="comparacao" hidden>
<h1>Entre fases: o que cada etapa acrescentou</h1>
{B("cf_leitura")}
<h2>Acerto (90 casos)</h2>{B("cf_acerto_90")}
<h2>Acurácia balanceada (90 casos)</h2>{B("cf_balanceada_90")}
<h2>Acerto (36 de avaliação)</h2>{B("cf_acerto_36")}
<h2>Acurácia balanceada (36 de avaliação)</h2>{B("cf_balanceada_36")}
<h2>Custo por caso</h2>{B("cf_custo")}
<h2>Riscos</h2>{B("cf_riscos")}
<details><summary>Pareamentos entre fases (McNemar)</summary>{B("cf_pareamentos")}</details>
{figura(figs, "17")}
</section>

<section id="metodo" hidden>
<h1>Método, limitações e o que vem a seguir</h1>
<h2>Como a Fase 3 foi medida</h2>
<ul>
<li><strong>Partição</strong>: 54 casos de aprendizado (3 por célula classe × nível) e 36 de avaliação (2 por célula), sorteados por hash; só nos 54 o modelo vê a causa correta.</li>
<li><strong>Biblioteca</strong>: cópia por modelo; edição só por acréscimo (nota, retificação apontando o trecho, verbete novo); validação em código antes de entrar; snapshot fechado com hash a cada época.</li>
<li><strong>Métricas</strong>: acurácia balanceada (primária), acerto com IC de Wilson, McNemar exato pareado contra L0, Q de Cochran (L0..L3) com Holm, g de Cohen, trocas de rótulo (autoenvenenamento), hit@k e MRR do recuperador, efeito mínimo detectável.</li>
<li><strong>Decisão</strong>: regra pré-registrada, depois bootstrap (2.000 réplicas), estabilidade, Pareto e escore ponderado como robustez; ponte de versão antes de misturar corridas.</li>
<li><strong>Condições fixas</strong>: um modelo residente por vez, só CPU, contexto de 8.192 tokens, temperatura 0,1, prompts idênticos aos da 2-B.</li>
</ul>
<h2>Limitações declaradas</h2>
<ol>
<li>Amostra de 36 casos: efeito mínimo detectável alto; a decisão é por convergência de critérios, sob incerteza declarada.</li>
<li>Teste reutilizado: os 36 foram vistos em quatro passadas por modelo; só casos inéditos fecham a questão (teste (a) da 3-B).</li>
<li>Revisão das edições por IA, um único revisor.</li>
<li>Custo por versão medido em momentos diferentes da mesma corrida.</li>
<li>Granite sem ponte de versão e sem reteste com teto de texto maior.</li>
<li>Uma execução por condição, sem semente fixa; ruído medido de 0 a 2 casos em 36.</li>
<li>Escritor e leitor confundidos: a biblioteca L1 só foi lida pelo próprio qwen2.5:7b (teste (b) da 3-B).</li>
</ol>
<h2>Fase 3-B — os testes complementares</h2>
<ul>
<li><strong>(b) Troca cruzada</strong>: L1 e L3 do qwen2.5:7b lidas pelos dois Coder nos 36 — o ganho é da biblioteca ou de quem a lê?</li>
<li><strong>(a) Casos inéditos</strong>: 36 casos novos, escritos só a partir do código do cobaia, com o qwen2.5:7b e o 3B em L0, L1 e L3 — o ganho generaliza?</li>
<li><strong>Sonda de detecção de correção</strong>: o modelo percebe, ao rever um caso corrigido, que a própria nota ficou desatualizada?</li>
</ul>
<p class="nota">O estado de cada corrida (feita, rodando, pendente) e o comando pronto estão na aba Roadmap; as decisões que esperam resposta, na aba Pendências.</p>
<div class="rodape">Fontes: <code>resumo_fase3.json</code> ({html.escape(dados["meta"]["resumo_gerado_em"])}), <code>comparacao_fases.json</code> ({html.escape(dados["meta"]["comparacao_gerado_em"])}), <code>decisao_modelo.json</code> ({html.escape(dados["meta"]["decisao_gerado_em"])}), resumos das Fases 2-A/2-B, <code>tabelas_relatorio.md</code> e as figuras 01–18 de <code>resultados_alvo/graficos/</code>; <code>pendencias.md</code> e <code>roadmap.md</code> do Memorial (fichas e tabelas lidas por <code>ferramentas/painel_textos.py</code>). Gerado por <code>ferramentas/gerar_dashboard.py</code>; nenhum número foi digitado à mão.</div>
</section>
</main>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js"></script>
<script>window.DADOS = {dados_json};</script>
<script>{JS}</script>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--saida", default=str(SAIDA_PADRAO))
    ap.add_argument("--check", action="store_true", help="regera e compara com o arquivo gravado")
    args = ap.parse_args()
    r = ler_json(F3 / "resumo_fase3.json")
    c = ler_json(F3 / "comparacao_fases.json")
    d = ler_json(F3 / "decisao_modelo.json")
    m2b = ler_json(EXP / "resultados_alvo" / "resumo_metricas.json")
    m2a = ler_json(EXP / "resumo_metricas.json")
    blocos = blocos_tabelas(F3 / "tabelas_relatorio.md")
    dados = montar_dados(r, c, d, m2b, m2a)
    figs = figuras_b64()
    pend = pt.ler_pendencias(MEMORIAL / "pendencias.md")
    road = pt.ler_roadmap(MEMORIAL / "roadmap.md")
    for aviso in avisos_corridas(road):
        print("aviso:", aviso, file=sys.stderr)
    html_final = pagina(dados, blocos, figs, pend, road)
    saida = Path(args.saida)
    if args.check:
        atual = saida.read_text(encoding="utf-8") if saida.exists() else ""
        if atual == html_final:
            print(f"--check: {saida.name} idêntico ao regerado ({len(html_final):,} caracteres)")
            return
        print(f"--check: {saida.name} DIFERE do regerado — rode sem --check para regravar")
        sys.exit(1)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(html_final, encoding="utf-8", newline="\n")
    print(f"gravado: {saida} ({len(html_final):,} caracteres; {len(figs)} figuras; {len(blocos)} blocos de tabela; "
          f"{sum(len(b.fichas) for b in pend)} fichas de pendência; {len(road['fases'])} fases; {len(road['corridas'])} corridas)")


if __name__ == "__main__":
    main()
