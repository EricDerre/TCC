#!/usr/bin/env python3
# ! Alteração de IA - Revisar: abas por tópico do painel do projeto (30/09/2026, pedido do Eric): comparativo
# qwen2.5:7b × qwen2.5-coder:7b, Fase 3-B (inéditos, ponte, sonda e corridas), curadoria da L1, recuperador,
# ablação base × instruct, pesquisa bibliográfica e ferramental. Cada função secao_* lê os JSON/MD versionados
# e devolve os dados dos gráficos (Chart.js, desenhados pelo JS de gerar_dashboard.py) e o HTML da seção.
# ! Motivo: o Eric pediu "a aba do comparativo do qwen 2.5 7b e o coder" e que o painel seja "o grande
# compilador / centralizador das análises e dados, com cada aba específica falando sobre os tópicos ...
# sumarizado e focando no visual e facilidade de entendimento"; gerar_dashboard.py já passava de 900 linhas,
# então as abas novas vivem aqui, no mesmo padrão: pergunta, resposta em uma frase, números-chave, um ou
# dois gráficos, leitura curta e as tabelas completas recolhidas. Nenhum número é digitado à mão.
"""Abas por tópico do painel do projeto. Uso: importado por gerar_dashboard.py (montar(ctx))."""
from __future__ import annotations

import html
import re
from collections import Counter, defaultdict
from pathlib import Path

import painel_textos as pt

RAIZ = Path(__file__).resolve().parent.parent
EXP = RAIZ / "Programacao" / "AgenteCore" / "experimentos"
RES = EXP / "resultados_alvo"
MEMORIAL = RAIZ / "Documentacao" / "memorial"
PESQUISA = MEMORIAL / "2-pesquisa-e-literatura"
FERRAMENTAL = MEMORIAL / "5-metodo-e-ferramental"

A, B = "qwen2.5:7b", "qwen2.5-coder:7b"
COD3B = "qwen2.5-coder:3b"
CLASSES = {1: "léxica", 2: "sintática", 3: "semântica", 4: "tradução", 5: "runtime", 6: "efeito"}
# Cor de cada série: posição fixa na paleta validada (tokens --s1..--s8 no CSS de gerar_dashboard.py). A ordem
# das posições é o que garante que séries vizinhas se distinguem, inclusive para quem não vê cores.
SLOTS = {"qwen2.5:7b": 1, "granite4.2:8b": 2, "qwen2.5-coder:7b": 3, "qwen2.5-coder:3b": 4, "phi4-mini:3.8b": 5,
         "qwen2.5-coder:1.5b": 6, "qwen2.5-coder:1.5b-instruct-fp16": 7, "qwen2.5-coder:1.5b-instruct-q8_0": 8,
         "qwen2.5:0.5b-instruct": 1, "qwen2.5:0.5b-base": 2}

# Mapa do painel: grupo → (id da seção, nome na aba, o que a aba responde). É a fonte da barra de navegação e
# da lista "Mapa do painel" da aba Início.
NAV = [
    ("Projeto", [
        ("inicio", "Início", "Onde o projeto está, o que depende do Eric e o mapa deste painel."),
        ("pendencias", "Pendências", "Uma ficha por decisão: o que é, por que importa, opções, recomendação e decisão."),
        ("roadmap", "Roadmap", "Estado por fase, corridas com o comando pronto e o esqueleto das Fases 4 e 5."),
    ]),
    ("Modelos", [
        ("visao", "Resultados", "O que os testes decidiram: acurácia por versão da biblioteca e as três fases lado a lado."),
        ("modelos", "Modelos", "Veredito e números de cada modelo, acerto por classe de defeito e por nível."),
        ("decisao", "Decisão", "A regra pré-registrada, o bootstrap, a fronteira de Pareto e a frase da decisão."),
        ("comparativo", "qwen × Coder", "Em que cenários o qwen2.5-coder:7b seria melhor que o qwen2.5:7b, e por que a decisão ficou."),
        ("hipoteses", "Hipóteses", "As seis hipóteses pré-registradas, o veredito de cada uma e os achados novos."),
    ]),
    ("Biblioteca", [
        ("fase3", "Fase 3", "A biblioteca gerida pelo modelo: edições, rejeições, recuperação, custo e revisão humana."),
        ("tresb", "Fase 3-B", "Casos inéditos, ponte de versão, sonda de correção e as corridas complementares."),
        ("curadoria", "Curadoria da L1", "O que a cópia de produção herdou da biblioteca escrita pelo modelo."),
        ("recuperador", "Recuperador", "BM25 com sinais contra embeddings e híbrido: vale trocar?"),
        ("ablacao", "Ablação", "Sem ajuste por instrução, o modelo faz a tarefa? O piso da família."),
    ]),
    ("Fases anteriores", [
        ("fases2", "Fases 2-A e 2-B", "Prompts sem documentação e a biblioteca escrita à mão em seis condições."),
        ("comparacao", "Entre fases", "O que cada etapa acrescentou, nos 90 e nos 36, com custo e riscos."),
    ]),
    ("Pesquisa e método", [
        ("pesquisa", "Pesquisa", "As quatro rodadas de literatura, as afirmações verificadas e os filtros adotados."),
        ("ferramental", "Ferramental", "As ferramentas locais, a economia de tokens e a medição do servidor de memória do código."),
        ("metodo", "Método e limites", "Como a Fase 3 foi medida, as limitações declaradas e a Fase 3-B."),
    ]),
]


# ------------------------------------------------------------------ utilidades

def esc(s) -> str:
    return html.escape(str(s), quote=False)


def fmt(v, casas: int = 1) -> str:
    if v is None:
        return "—"
    return f"{v:.{casas}f}".replace(".", ",")


def pp(v) -> str:
    """Diferença em pontos percentuais, com sinal tipográfico."""
    if v is None:
        return "—"
    return f"{v:+.1f}".replace(".", ",").replace("-", "−") + " pp"


def kpis(itens: list[tuple[str, str, str]]) -> str:
    """Cartões de número-chave; valores compridos (três números com setas) descem um degrau de tamanho."""
    return '<div class="kpis">' + "".join(
        f"<div class='kpi'><span>{esc(t)}</span><b{' class=longo' if len(b) > 14 else ''}>{esc(b)}</b><small>{esc(s)}</small></div>" for t, b, s in itens) + "</div>"


_NUM = re.compile(r"^[+−\-]?[\d.,]+( pp|%| s)?$")


def tabela(cab: list[str], linhas: list[list], raw: bool = False, classe: str = "") -> str:
    """Tabela HTML. Com raw=True as células já vêm em HTML (não são escapadas)."""
    def td(c) -> str:
        s = str(c)
        num = bool(_NUM.match(re.sub(r"<[^>]+>", "", s).strip())) or s.strip() in {"—", "-"}
        return f'<td{" class=num" if num else ""}>{s if raw else esc(s)}</td>'
    th = "".join(f"<th>{esc(c)}</th>" for c in cab)
    trs = "".join("<tr>" + "".join(td(c) for c in r) + "</tr>" for r in linhas)
    return f'<div class="tabela {classe}"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def detalhes(titulo: str, corpo: str) -> str:
    return f"<details><summary>{esc(titulo)}</summary>{corpo}</details>"


def leitura(itens: list[str]) -> str:
    """Lista de leitura curta; os itens já vêm em HTML (podem levar <strong> e <code>)."""
    return '<ul class="leitura">' + "".join(f"<li>{i}</li>" for i in itens) + "</ul>"


def fontes(itens: list[str]) -> str:
    return '<p class="nota fontes"><strong>Fontes:</strong> ' + "; ".join(itens) + ".</p>"


def chip(classe: str, texto: str) -> str:
    return f'<span class="chip {classe}">{esc(texto)}</span>'


def celula_duelo(a, b, modelo_a: str = A, modelo_b: str = B) -> str:
    """Célula 'a / b' tingida com a cor de quem está à frente; a intensidade acompanha a diferença."""
    if a is None or b is None:
        return "<td class=num>—</td>"
    d = round(b - a, 1)
    if abs(d) < 0.05:
        return f"<td class='num dc'>{fmt(a)} / {fmt(b)} <span class='delta zero'>=</span></td>"
    venc = modelo_b if d > 0 else modelo_a
    forca = min(60, int(abs(d) * 3) + 8)
    return (f"<td class='num dc' style='background:color-mix(in srgb, var(--s{SLOTS[venc]}) {forca}%, transparent)'>"
            f"{fmt(a)} / {fmt(b)} <span class='delta {'pos' if d > 0 else 'neg'}'>{pp(d)}</span></td>")


def heat(v, piso: float = 0.0, teto: float = 100.0) -> str:
    if v is None:
        return "transparent"
    a = max(0.0, min(1.0, (v - piso) / (teto - piso)))
    return f"color-mix(in srgb, var(--acento) {int(a * 55)}%, transparent)"


# ------------------------------------------------------------------ 1. comparativo qwen × Coder

ROTULO_FASE = {"2A_linear_ryzen": "2-A (Ryzen)", "2B_A0": "2-B A0", "2B_A2": "2-B A2", "F3_L0": "F3 L0",
               "F3_L1": "F3 L1", "F3_L2": "F3 L2", "F3_L3": "F3 L3"}


def secao_comparativo(cq: dict, blocos_cq: dict, md_para_html, road: dict, cartoes_corridas) -> tuple[dict, str]:
    meta = cq["metadados"]
    LA, LB = meta["melhor_L_nos_36"][A], meta["melhor_L_nos_36"][B]
    v36 = {x["contexto"]: x for x in cq["fase3_versoes"]}
    melhor_A = v36[f"F3 · L{LA} · 36 de avaliação"]["acerto_A"]
    melhor_B = v36[f"F3 · L{LB} · 36 de avaliação"]["acerto_B"]
    l1 = v36["F3 · L1 · 36 de avaliação"]
    conf = {x["contexto"]: x for x in cq["confronto_f3"]}
    c1 = conf["F3 · L1 · 36 de avaliação"]
    doc1 = next(x for x in cq["fase3_documentacao"] if x["epoca"] == 1)
    tot = {s: {k: sum((x.get(f"{k}_{s}") or 0) for x in cq["fase3_revisao"]) for k in ("Correta", "Parcial", "Errada")} for s in "AB"}
    corr = {s: 100 * tot[s]["Correta"] / max(1, sum(tot[s].values())) for s in "AB"}
    rec1 = next(x for x in cq["fase3_recuperacao"] if x["L"] == 1)
    boot36 = cq["decisao"]["bootstrap"]["nos_36"]
    p_max_B = max(v["p_top1"] for k, v in boot36.items() if k.startswith(B + "/"))
    est = cq["decisao"]["estabilidade_top1"]
    vence = sorted(cq["onde_o_coder_vence"], key=lambda x: -x["delta"])
    n_vence, max_delta = len(vence), max(x["delta"] for x in vence)
    n_vence_36 = sum(1 for x in vence if "36" in x["onde"])
    # dados dos gráficos
    traj = {"36": [], "90": []}
    for x in cq["entre_fases"]:
        chave, conj = x["contexto"].split(" · nos ")
        if chave in ROTULO_FASE:
            traj[conj].append({"rot": ROTULO_FASE[chave], "acerto_A": x["acerto_A"], "acerto_B": x["acerto_B"],
                               "bal_A": x["bal_A"], "bal_B": x["bal_B"]})
    confronto = {"36": [], "90": []}
    for x in cq["confronto_2b"]:
        confronto["90"].append({"rot": x["contexto"].replace(" · ", " "), "so_A": x["so_qwen"], "so_B": x["so_coder"],
                                "ambos": x["ambos"], "nenhum": x["nenhum"], "p": x["p_mcnemar"]})
    for x in cq["confronto_f3"]:
        conj = "36" if "36" in x["contexto"] else "90"
        confronto[conj].append({"rot": x["contexto"].split(" · ")[1], "so_A": x["so_qwen"], "so_B": x["so_coder"],
                                "ambos": x["ambos"], "nenhum": x["nenhum"], "p": x["p_mcnemar"]})
    revisao = {s: {k: round(100 * tot[s][k] / max(1, sum(tot[s].values())), 1) for k in tot[s]} | {"n": sum(tot[s].values())} for s in "AB"}
    dados = {"A": A, "B": B, "trajetoria": traj, "confronto": confronto, "revisao": revisao}
    # tabelas por classe e por nível (duelo)
    contextos_classe = [("2-A (linear)", cq["fase2a_classe"]), ("2-B A2", cq["fase2b_classe_A2"]), ("F3 L0 (90)", cq["fase3_classe_L0"]),
                        ("F3 L1 (90)", cq["fase3_classe_L1"]), (f"F3 melhor L (qwen L{LA} × Coder L{LB})", cq["fase3_classe_melhor"])]
    linhas = []
    for i, nome in CLASSES.items():
        cels = []
        for _, lista in contextos_classe:
            x = next((r for r in lista if r["classe"].startswith(f"{i} ")), None)
            cels.append(celula_duelo(x["acerto_A"], x["acerto_B"]) if x else "<td>—</td>")
        linhas.append(f"<tr><td>{i} {nome}</td>{''.join(cels)}</tr>")
    th = "".join(f"<th>{esc(n)}</th>" for n, _ in contextos_classe)
    tab_classes = f'<div class="tabela duelo"><table><thead><tr><th>Classe</th>{th}</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'
    contextos_nivel = [("2-B A2", cq["fase2b_nivel_A2"]), ("F3 L0 (90)", cq["fase3_nivel_L0"]), ("F3 L1 (90)", cq["fase3_nivel_L1"])]
    linhas = []
    for x0 in cq["fase2b_nivel_A2"]:
        nivel = x0["nivel"]
        cels = [celula_duelo(x["acerto_A"], x["acerto_B"]) if (x := next((r for r in lista if r["nivel"] == nivel), None)) else "<td>—</td>"
                for _, lista in contextos_nivel]
        linhas.append(f"<tr><td>{esc(nivel)}</td>{''.join(cels)}</tr>")
    th = "".join(f"<th>{esc(n)}</th>" for n, _ in contextos_nivel)
    tab_niveis = f'<div class="tabela duelo"><table><thead><tr><th>Nível</th>{th}</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'
    tab_vence = tabela(["Onde", "Métrica", A, B, "Diferença", "n"],
                       [[x["onde"], x["metrica"], fmt(x["A"]), fmt(x["B"]), pp(x["delta"]), x["n"]] for x in vence])
    tab_doc = tabela(["Época", "Propostas (qwen / Coder)", "Aceitas", "Aceitação", "Tokens acrescentados", "Verbetes"],
                     [[x["epoca"], f'{x["propostas_A"]} / {x["propostas_B"]}', f'{x["aceitas_A"]} / {x["aceitas_B"]}',
                       f'{fmt(x["aceitas_pct_A"])}% / {fmt(x["aceitas_pct_B"])}%', f'{x["tokens_A"]:,} / {x["tokens_B"]:,}'.replace(",", "."),
                       f'{x["verbetes_A"]} / {x["verbetes_B"]}'] for x in cq["fase3_documentacao"]])
    tab_rec = tabela(["Versão", "hit@3 nos 90 (qwen / Coder)", "hit@3 nos 36", "Verbetes"],
                     [[f'L{x["L"]}', f'{fmt(x["hit3_90_A"])}% / {fmt(x["hit3_90_B"])}%', f'{fmt(x["hit3_36_A"])}% / {fmt(x["hit3_36_B"])}%',
                       f'{x["verbetes_A"]} / {x["verbetes_B"]}'] for x in cq["fase3_recuperacao"]])
    B_ = lambda nome: md_para_html(blocos_cq[nome]) if nome in blocos_cq else ""  # noqa: E731
    itens_kpi = [
        ("Células em que o Coder lidera", str(n_vence), f"maior vantagem {pp(max_delta)}; {n_vence_36} delas nos 36 nunca vistos"),
        ("Nos 36 nunca vistos, melhor versão", f"{fmt(melhor_A)}% × {fmt(melhor_B)}%", f"qwen L{LA} × Coder L{LB}, acerto simples"),
        ("Confronto em L1 nos 36", f'{c1["so_qwen"]} × {c1["so_coder"]}', f'casos que só um acertou; ambos {c1["ambos"]}, p = {fmt(c1["p_mcnemar"], 3)}'),
        ("Edições aceitas na época 1", f'{doc1["aceitas_A"]} × {doc1["aceitas_B"]}', f'de {doc1["propostas_A"]} × {doc1["propostas_B"]} propostas; corretas na revisão {fmt(corr["A"])}% × {fmt(corr["B"])}%'),
        ("hit@3 com a biblioteca L1 (90)", f'{fmt(rec1["hit3_90_A"])}% × {fmt(rec1["hit3_90_B"])}%', f'{rec1["verbetes_A"]} × {rec1["verbetes_B"]} verbetes'),
        ("P(top-1) do Coder nos 36", f"≤ {fmt(100 * p_max_B)}%", f'primeiro em {est.get(B, 0)} × {est.get(A, 0)} de {cq["decisao"]["total_rankings"]} ordenações; {fmt(l1["s_A"])} × {fmt(l1["s_B"])} s por diagnóstico em L1'),
    ]
    corridas = cartoes_corridas(road, numeros=["1", "7"], sufixo="-cq")
    html_ = f'''<section id="comparativo" hidden>
<h1>qwen2.5:7b × qwen2.5-coder:7b: em que cenários o Coder seria melhor?</h1>
<p class="lead">Pergunta do Eric em 29/09: "pode ser que em alguns cenários o coder seja mais interessante". Resposta: o Coder fica à frente em <strong>{n_vence} células</strong>, todas pequenas (a maior por {pp(max_delta)}) e quase todas nos 54 casos de aprendizado e nas classes léxica, runtime e efeito. Nos <strong>36 casos nunca vistos</strong> o qwen2.5:7b vence em todas as versões da biblioteca ({fmt(melhor_A)}% × {fmt(melhor_B)}% na melhor versão de cada um), e em nenhuma ordenação o Coder tem chance real de ser o primeiro (P(top-1) ≤ {fmt(100 * p_max_B)}%). Como escritor, o Coder é mais contido e mais certo ({fmt(corr["B"])}% de edições corretas contra {fmt(corr["A"])}%). A decisão 52 fica; o que fecharia a pergunta é a troca cruzada (corrida 1) e, se o Eric quiser, o Coder 7B nos 36 inéditos (corrida 7).</p>
{kpis(itens_kpi)}
<h2>A trajetória dos dois pelas três fases</h2>
<p>Os mesmos casos, da Fase 2-A (sem documentação, máquina de desenvolvimento) à Fase 3 (biblioteca editada pelo próprio modelo). Nos 36 de avaliação, o qwen abre vantagem a partir da biblioteca L1; nos 90 as curvas se cruzam.</p>
<div class="controles"><label>Conjunto <select id="sel-cq-conj"><option value="36">36 de avaliação</option><option value="90">90 (todos)</option></select></label>
<label>Métrica <select id="sel-cq-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-cq-traj"></canvas></div>
<h2>Quem acerta o que o outro erra</h2>
<p>Em cada condição, os casos que só um dos dois acertou (os discordantes do teste de McNemar). Nos 36 nunca vistos com L1, são {c1["so_qwen"]} casos só do qwen contra {c1["so_coder"]} só do Coder; com {c1["ambos"]} acertados por ambos, o teste não separa os dois (p = {fmt(c1["p_mcnemar"], 3)}).</p>
<div class="controles"><label>Conjunto <select id="sel-cq-conf"><option value="36">36 de avaliação (Fase 3)</option><option value="90">90 (2-B e Fase 3)</option></select></label></div>
<div class="chart"><canvas id="g-cq-conf"></canvas></div>
<h2>Por classe de defeito e por nível</h2>
<p>Cada célula mostra <em>qwen / Coder</em> e a diferença; a cor é a de quem está à frente (azul = qwen, verde-água = Coder) e fica mais forte quanto maior a diferença. O Coder leva vantagem em léxica, runtime e efeito; o qwen em sintática, semântica e tradução.</p>
{tab_classes}
{tab_niveis}
<h2>Como escritor da biblioteca</h2>
<p>Na época 1, o Coder propôs menos e teve aceitação igual ({fmt(doc1["aceitas_pct_A"])}% × {fmt(doc1["aceitas_pct_B"])}%), escreveu menos da metade dos tokens e não criou verbetes novos. Na revisão humana das edições aceitas, a fração correta é maior no Coder.</p>
<div class="chart baixo"><canvas id="g-cq-rev"></canvas></div>
{tab_doc}
<h2>Recuperação e trocas de rótulo</h2>
<p>Com a biblioteca L1 do Coder, o recuperador acha o verbete de ouro um pouco mais vezes nos 90 ({fmt(rec1["hit3_90_B"])}% contra {fmt(rec1["hit3_90_A"])}%): a biblioteca menor e sem verbetes novos não atrapalha o BM25.</p>
{tab_rec}
{detalhes("Trocas de rótulo entre versões (autoenvenenamento, ✓→✗ e ✗→✓)", B_("cq_flips"))}
{detalhes("Rejeições do validador por modelo", B_("cq_rejeicoes"))}
<h2>Onde o Coder vence, célula a célula</h2>
{detalhes(f"As {n_vence} células em que o Coder fica à frente", tab_vence)}
<h2>A decisão, revista com os dois lado a lado</h2>
{detalhes("Regra 36 (ranking por acurácia balanceada nos 36)", B_("cq_regra36"))}
{detalhes("Bootstrap: P(top-1) e intervalos", B_("cq_bootstrap"))}
{detalhes("Escore ponderado e fronteira de Pareto", B_("cq_escore_pareto"))}
{detalhes("Ponte de versão do Ollama (0.34.0 → 0.34.1)", B_("cq_ponte"))}
{detalhes("Riscos entre fases", B_("cq_riscos"))}
<h2>O que fecharia a pergunta</h2>
{corridas}
{fontes(["<code>comparativo-qwen25-7b-vs-coder-7b.md</code> (Memorial, 3-resultados-e-analises)", "<code>comparativo_qwen_coder.json</code> e <code>.md</code> gerados por <code>comparar_qwen_coder.py</code> (--check)", "achado 4.38; decisão 52 mantida"])}
</section>'''
    return dados, html_


# ------------------------------------------------------------------ 2. Fase 3-B

def secao_tres_b(ined: dict, dados: dict, road: dict, cartoes_corridas, md_doc_para_html) -> tuple[dict, str]:
    cur: dict = defaultdict(dict)
    for x in ined["por_modelo_biblioteca_particao"]:
        cur[x["modelo"]][str(x["biblioteca_epoca"])] = {"acerto": x["causa_correta_pct"], "bal": x["acuracia_balanceada_pct"], "s": x["segundos_mediana"]}
    modelos = [m for m in (A, COD3B) if m in cur]
    Ls = sorted({L for m in modelos for L in cur[m]}, key=int)
    oficial = {m: {L: {"acerto": dados["curvas"]["36"][m][L]["acerto"], "bal": dados["curvas"]["36"][m][L]["balanceada"]} for L in Ls} for m in modelos}
    rec: dict = defaultdict(dict)
    for x in ined["recuperacao"]:
        rec[x["modelo"]][str(x["biblioteca_epoca"])] = x["hit@3"]
    rec_of = {m: {L: dados["recuperacao"][m][L]["hit3_36"] for L in Ls} for m in modelos}
    par = [x for x in ined["pareado_vs_L0"] if x.get("particao", "avaliacao") == "avaliacao"]
    ponte = dados["tres_b"].get("fase3b_ponte", {}).get("linhas", [])
    q = cur[A]
    L_ult = Ls[-1]
    p_ult = next((x for x in par if x["modelo"] == A and str(x["biblioteca_epoca"]) == L_ult), {})
    corr3b = [c for c in road["corridas"] if c.comando and "-Modo" in c.comando]
    n_feitas = sum(c.classe == "feita" for c in corr3b)
    n_pend = sum(c.classe in ("pendente", "aguarda") for c in corr3b)
    n_opc = sum(c.classe == "opcional" for c in corr3b)
    ponte_txt = "; ".join(f'{x["modelo"]} b/c {x["pareado_vs_f3"]["b"]}/{x["pareado_vs_f3"]["c"]}' for x in ponte)
    dados_js = {"modelos": modelos, "Ls": Ls, "ineditos": {m: cur[m] for m in modelos}, "oficiais": oficial,
                "rec_ineditos": {m: rec[m] for m in modelos}, "rec_oficiais": rec_of}
    tab_par = tabela(["Modelo", "Versão", "Diferença contra L0", "b / c (✗→✓ / ✓→✗)", "p (McNemar exato)"],
                     [[x["modelo"], f'L{x["biblioteca_epoca"]}', pp(x.get("delta_pp")), f'{x.get("b", "—")} / {x.get("c", "—")}', fmt(x.get("p_mcnemar"), 3)] for x in par])
    tab_ponte = tabela(["Modelo", "b / c contra a Fase 3 (L0, 36)", "Leitura"],
                       [[x["modelo"], f'{x["pareado_vs_f3"]["b"]} / {x["pareado_vs_f3"]["c"]}', "pareável" if x["pareado_vs_f3"]["b"] + x["pareado_vs_f3"]["c"] <= 2 else "divergente"] for x in ponte])
    sec = {t[:3]: c for t, c in road["secoes"]}
    leitura_ined = next((c for t, c in road["secoes"] if t.startswith("2.1")), "")
    sonda = next((c for t, c in road["secoes"] if t.startswith("3. ")), "")
    itens_kpi = [
        (f"{A} nos 36 inéditos", " → ".join(f'{fmt(q[L]["acerto"])}%' for L in Ls), f'acerto com {" → ".join("L" + L for L in Ls)}; balanceada ' + " / ".join(fmt(q[L]["bal"]) for L in Ls)),
        (f"{COD3B} nos 36 inéditos", " → ".join(f'{fmt(cur[COD3B][L]["acerto"])}%' for L in Ls) if COD3B in cur else "—", "a biblioteca do qwen não muda o 3B"),
        (f"L{L_ult} contra L0 no qwen", pp(p_ult.get("delta_pp")), f'b/c {p_ult.get("b", "—")}/{p_ult.get("c", "—")}, p = {fmt(p_ult.get("p_mcnemar"), 3)}'),
        ("hit@3 nos inéditos (qwen)", " → ".join(f'{fmt(rec[A][L])}%' for L in Ls), f'nos 36 oficiais: ' + " → ".join(f'{fmt(rec_of[A][L])}%' for L in Ls)),
        ("Ponte de versão", f"{sum(x['pareado_vs_f3']['b'] + x['pareado_vs_f3']['c'] <= 2 for x in ponte)} de {len(ponte)} pareáveis", f"{ponte_txt}; pareável quando b + c ≤ 2"),
        ("Corridas da 3-B", f"{n_feitas} feitas · {n_pend} pendentes", f"{n_opc} opcionais"),
    ]
    html_ = f'''<section id="tresb" hidden>
<h1>Fase 3-B: o ganho da biblioteca generaliza para casos nunca vistos?</h1>
<p class="lead">Trinta e seis casos inéditos, escritos só a partir do código do sistema-cobaia e nunca vistos por nenhum modelo, foram diagnosticados com a biblioteca original (L0) e com as versões escritas pelo qwen2.5:7b (L1 e L3). O qwen acerta {" → ".join(f'{fmt(q[L]["acerto"])}%' for L in Ls)}: o ganho de L1 medido nos 36 oficiais <strong>não reaparece</strong>, e L{L_ult} rende {pp(p_ult.get("delta_pp"))} (b/c {p_ult.get("b", "—")}/{p_ult.get("c", "—")}, p = {fmt(p_ult.get("p_mcnemar"), 3)}). O 3B fica igual nas três versões. A ponte de versão do Ollama é pareável. Falta a troca cruzada (corrida 1), que separa quem escreveu a biblioteca de quem a lê.</p>
{kpis(itens_kpi)}
<h2>Oficiais × inéditos</h2>
<p>Linha cheia: os 36 casos oficiais de avaliação (vistos em quatro passadas por modelo). Linha tracejada: os 36 inéditos. Se o ganho fosse da biblioteca, as duas linhas subiriam juntas.</p>
<div class="controles"><label>Métrica <select id="sel-tb-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-tb-gen"></canvas></div>
<h2>O recuperador nos inéditos</h2>
<p>hit@3 = o verbete de ouro está entre os três recuperados. Nos inéditos o recuperador acerta menos e cai com as notas acrescentadas; nos oficiais, fica estável.</p>
<div class="chart baixo"><canvas id="g-tb-rec"></canvas></div>
{tab_par}
<h2>Ponte de versão do Ollama</h2>
<p>A bateria oficial rodou no Ollama 0.34.0; a 3-B roda no 0.34.1. A ponte repete L0 nos 36 no runtime novo e compara caso a caso.</p>
{tab_ponte}
<h2>Corridas da Fase 3-B</h2>
{cartoes_corridas(road, numeros=[c.numero for c in corr3b], sufixo="-3b")}
{detalhes("Primeira leitura dos inéditos (roadmap §2.1)", md_doc_para_html(leitura_ined))}
{detalhes("Sonda de detecção de correção (roadmap §3)", md_doc_para_html(sonda))}
{fontes(["<code>resultados_alvo/fase3b_ineditos/resumo_fase3.json</code> (corrida 2, 28/09)", "<code>decisao_modelo.json</code> (ponte)", "<code>roadmap.md</code> §2, §2.1 e §3", "achado 4.37"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 3. curadoria da L1

def secao_curadoria(cur: dict, planilha_md: str) -> tuple[dict, str]:
    cab, linhas, _ = pt.primeira_tabela(pt.sem_comentarios(planilha_md))
    col = {c: i for i, c in enumerate(cab)}
    cont: dict = defaultdict(Counter)
    for r in linhas:
        cont[r[col["Operação"]]][r[col["Avaliação"]]] += 1
    operacoes = list(cont)
    aval = Counter(r[col["Avaliação"]] for r in linhas)
    ret = cont.get("retificacao", Counter())
    dados_js = {"operacoes": operacoes, "por": {o: dict(cont[o]) for o in operacoes}}
    removidas = tabela(["#", "Caso", "Verbete", "Operação", "Texto", "Por que saiu"],
                       [[x["numero"], x["caso"], x["verbete"], x["operacao"], x["texto"], x.get("comentario", "")] for x in cur["removidas"]])
    completa = tabela(cab, [[pt.inline(c) for c in r] for r in linhas], raw=True)
    itens_kpi = [
        ("Edições da época 1", str(cur["edicoes_na_epoca"]), f'{aval.get("Correta", 0)} corretas · {aval.get("Parcial", 0)} parciais · {aval.get("Errada", 0)} erradas'),
        ("Mantidas na produção", str(cur["mantidas"]), f'{len(cur["removidas"])} removidas (avaliação {", ".join(cur["politica"].get("remover", []))})'),
        ("Retificações", f'{ret.get("Errada", 0)} de {sum(ret.values())} erradas', "a operação que mais errou"),
        ("Verbetes na cópia curada", str(cur["n_verbetes"]), f'hash {cur["hash_curada"]}'),
        ("Reconstrução conferida", "hash igual", f'reaplicar as {cur["edicoes_na_epoca"]} edições reproduz {cur["hash_oficial"]}'),
    ]
    html_ = f'''<section id="curadoria" hidden>
<h1>Curadoria da L1: o que a produção herdou da biblioteca escrita pelo modelo?</h1>
<p class="lead">A versão L1 do qwen2.5:7b foi a que mais acertou nos 36 oficiais, mas suas {cur["edicoes_na_epoca"]} edições nunca tinham sido conferidas uma a uma. A revisão contra o código do sistema-cobaia deu {aval.get("Correta", 0)} corretas, {aval.get("Parcial", 0)} parciais e {aval.get("Errada", 0)} erradas; as erradas foram removidas e a cópia de produção (<code>biblioteca_producao/</code>) ficou com {cur["mantidas"]} edições em {cur["n_verbetes"]} verbetes. Um teste reaplica todas as edições e exige o hash oficial da época 1, para a cópia ter origem rastreável.</p>
{kpis(itens_kpi)}
<h2>Acerto das edições por tipo de operação</h2>
<p>As notas (acréscimo de contexto a um verbete) são em maioria corretas ou parciais; as retificações (correção de um trecho) erram na maior parte; os verbetes novos não acertaram nenhum.</p>
<div class="chart baixo"><canvas id="g-cur-op"></canvas></div>
<h2>O que saiu da cópia de produção</h2>
{removidas}
{detalhes(f"Planilha completa da curadoria ({len(linhas)} edições)", completa)}
{leitura([
    "O ganho de L1 nos 36 oficiais veio com edições em maioria erradas ou redundantes: a forma (notas e cabeçalhos no contexto) pesou mais que a verdade do conteúdo (achado 4.35).",
    "A cópia curada é o ponto de partida da Fase 4; a versão oficial em <code>resultados_alvo/fase3/</code> não muda.",
    "Se um veredito da planilha mudar, apagar <code>biblioteca_producao/</code> e rodar <code>curar_biblioteca.py --curar</code> de novo.",
])}
{fontes(["<code>resultados_alvo/fase3/curadoria_L1__qwen2.5_7b.md</code> (planilha)", "<code>Programacao/AgenteCore/biblioteca_producao/curadoria.json</code>", "<code>curar_biblioteca.py</code>; achado 4.40; ficha 2"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 4. recuperador

def secao_recuperador(rec: dict, ineditos_rec_txt: str = "") -> tuple[dict, str]:
    res = rec["resultados"]
    metodos = list(dict.fromkeys(x["metodo"] for x in res))
    bibs = list(dict.fromkeys(x["biblioteca"] for x in res))
    conjs = list(dict.fromkeys(x["conjunto"] for x in res))
    val: dict = defaultdict(lambda: defaultdict(dict))
    for x in res:
        val[x["biblioteca"]][x["conjunto"]][x["metodo"]] = {k: x[k] for k in ("hit@1", "hit@3", "hit@5", "mrr")}
    bib0, conj0 = bibs[0], conjs[0]
    bm25 = next(m for m in metodos if m.lower().startswith("bm25"))
    v0 = val[bib0][conj0]
    ordem = sorted(metodos, key=lambda m: -v0[m]["hit@3"])
    denso = [m for m in metodos if "denso" in m.lower()]
    hib = [m for m in metodos if "híbrido" in m.lower() or "hibrido" in m.lower()]
    dados_js = {"metodos": metodos, "bibliotecas": bibs, "conjuntos": conjs, "valores": {b: {c: dict(val[b][c]) for c in val[b]} for b in val}}

    def tab_classes(conj: str) -> str:
        linhas = []
        for i, nome in CLASSES.items():
            cels = []
            for m in metodos:
                x = next((r for r in res if r["biblioteca"] == bib0 and r["conjunto"] == conj and r["metodo"] == m), None)
                v = (x or {}).get("por_classe", {}).get(str(i), {}).get("hit@3")
                cels.append(f'<td class="num" style="background:{heat(v)}">{fmt(v)}%</td>' if v is not None else "<td>—</td>")
            linhas.append(f"<tr><td>{i} {nome}</td>{''.join(cels)}</tr>")
        th = "".join(f"<th>{esc(m)}</th>" for m in metodos)
        return f'<div class="tabela heat"><table><thead><tr><th>Classe ({esc(conj)}, {esc(bib0)})</th>{th}</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'

    completa = tabela(["Biblioteca", "Conjunto", "Método", "hit@1", "hit@3", "hit@5", "MRR", "n"],
                      [[x["biblioteca"], x["conjunto"], x["metodo"], f'{fmt(x["hit@1"])}%', f'{fmt(x["hit@3"])}%', f'{fmt(x["hit@5"])}%', fmt(x["mrr"], 3), x["n"]] for x in res])
    trad = next((r for r in res if r["biblioteca"] == bib0 and r["conjunto"] == conj0 and r["metodo"] == bm25), {}).get("por_classe", {}).get("4", {}).get("hit@3")
    conj_ined = next((c for c in conjs if "inédit" in c or "inedit" in c), conjs[-1])
    melhor_hib = max(hib, key=lambda m: v0[m]["hit@3"]) if hib else None
    itens_kpi = [
        (f"BM25 com sinais ({conj0})", f'{fmt(v0[bm25]["hit@3"])}%', f'hit@3; hit@5 {fmt(v0[bm25]["hit@5"])}%, {bib0}'),
        *([(f"{melhor_hib} ({conj0})", f'{fmt(v0[melhor_hib]["hit@3"])}%', "hit@3; o melhor híbrido")] if melhor_hib else []),
        *[(f"{m} ({conj0})", f'{fmt(v0[m]["hit@3"])}%', "hit@3") for m in sorted(denso, key=lambda m: -v0[m]["hit@3"])][:2],
        (f"BM25 nos {conj_ined}", f'{fmt(val[bib0][conj_ined][bm25]["hit@3"])}%', "hit@3; o corpus de teste que a Fase 3 nunca viu"),
        ("Classe tradução (BM25)", f"{fmt(trad)}%", f'hit@3; a classe mais fraca; {rec["metadados"]["chamadas_embed"]} chamadas de embedding na mesma CPU'),
    ]
    html_ = f'''<section id="recuperador" hidden>
<h1>Recuperador: vale trocar o BM25 com sinais por embeddings ou por um híbrido?</h1>
<p class="lead">Não, nesta medição. A decisão 55 tinha adotado a recuperação híbrida pela literatura, sem medida própria. Medido offline com o <code>{esc(rec["metadados"]["embedding"])}</code> nos 90 casos oficiais e nos 36 inéditos, o BM25 com sinais em código chega a {fmt(v0[bm25]["hit@3"])}% de hit@3 ({fmt(v0[bm25]["hit@5"])}% em hit@5), o embedding denso a {", ".join(fmt(v0[m]["hit@3"]) + "%" for m in denso)} e o híbrido a {", ".join(fmt(v0[m]["hit@3"]) + "%" for m in hib)}: o híbrido fica <strong>abaixo do BM25 sozinho</strong>. A recuperação híbrida saiu do desenho da Fase 4 (decisão 61); o ganho barato a medir é k = 5.</p>
{kpis(itens_kpi)}
<h2>Os métodos, lado a lado</h2>
<p>Consulta em termos = os sinais que o código extrai do caso (rota, campos, mensagens); consulta em texto = o caso escrito por extenso. O embedding só funciona razoavelmente com os termos, e mesmo assim fica longe do BM25.</p>
<div class="controles"><label>Biblioteca <select id="sel-rec-bib">{"".join(f'<option value="{esc(b)}">{esc(b)}</option>' for b in bibs)}</select></label>
<label>Métrica <select id="sel-rec-met"><option value="hit@3">hit@3</option><option value="hit@1">hit@1</option><option value="hit@5">hit@5</option><option value="mrr">MRR</option></select></label></div>
<div class="chart"><canvas id="g-rec-met"></canvas></div>
<h2>Por classe de defeito</h2>
<p>hit@3 por classe, na biblioteca original. A classe tradução (mapeamento entre camadas) é a mais fraca em todos os métodos; os sinais em código continuam sendo o caminho para ela.</p>
{tab_classes(conj0)}
{tab_classes(conj_ined)}
{detalhes(f"Tabela completa ({len(res)} combinações)", completa)}
{leitura([
    "O corpus é pequeno (dezenas de verbetes curtos) e a consulta é técnica e em português: a busca lexical com sinais extraídos por código vence a semântica.",
    "Trocar o modelo de embedding só faria sentido se a Fase 4 mostrasse necessidade; por ora, nada muda no harness.",
])}
{fontes(["<code>resultados_alvo/recuperador/experimento_recuperador.json</code> e <code>.md</code> (<code>experimento_recuperador.py</code>, --check)", "achado 4.39; decisão 61; ficha 11(f)"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 5. ablação base × instruct

def secao_ablacao(abl: dict, ref3b_90, ref3b_ined) -> tuple[dict, str]:
    linhas = abl["por_modelo_condicao"]
    dados_js = {"linhas": [{"modelo": x["modelo"], "cond": x["condicao"], "acerto": x["causa_correta_pct"], "formato": x["formato_valido_pct"],
                            "fora": x["fora_do_conjunto_pct"], "ic": x["causa_correta_ic95"]} for x in linhas]}
    tab = tabela(["Modelo", "Condição", "Acerto", "IC 95%", "Campo correto", "Formato válido", "Formato ok, conteúdo errado", "Rótulo fora do conjunto", "s / caso"],
                 [[x["modelo"], x["condicao"], f'{fmt(x["causa_correta_pct"])}%', f'{fmt(x["causa_correta_ic95"][0])}–{fmt(x["causa_correta_ic95"][1])}',
                   f'{fmt(x["campo_correto_pct"])}%', f'{fmt(x["formato_valido_pct"])}%', f'{fmt(x["formato_ok_conteudo_errado_pct"])}%',
                   f'{fmt(x["fora_do_conjunto_pct"])}%', fmt(x["segundos_medio"])] for x in linhas])
    g = {(x["modelo"], x["condicao"]): x for x in linhas}
    base, inst = "qwen2.5:0.5b-base", "qwen2.5:0.5b-instruct"
    itens_kpi = [
        ("Base, sem biblioteca (A0)", f'{fmt(g[(base, "A0")]["causa_correta_pct"])}%', f'formato válido {fmt(g[(base, "A0")]["formato_valido_pct"])}%'),
        ("Base, com biblioteca (A2)", f'{fmt(g[(base, "A2")]["causa_correta_pct"])}%', f'formato válido {fmt(g[(base, "A2")]["formato_valido_pct"])}%, rótulo inventado {fmt(g[(base, "A2")]["fora_do_conjunto_pct"])}%'),
        ("Instruct 0,5B, sem biblioteca", f'{fmt(g[(inst, "A0")]["causa_correta_pct"])}%', f'formato válido {fmt(g[(inst, "A0")]["formato_valido_pct"])}%'),
        ("Instruct 0,5B, com biblioteca", f'{fmt(g[(inst, "A2")]["causa_correta_pct"])}%', f'formato válido cai para {fmt(g[(inst, "A2")]["formato_valido_pct"])}%'),
        ("Referência: qwen2.5-coder:3b", f"{fmt(ref3b_90)}%", f"nos 90 com a biblioteca original; {fmt(ref3b_ined)}% nos inéditos"),
    ]
    html_ = f'''<section id="ablacao" hidden>
<h1>Sem ajuste por instrução, o modelo faz a tarefa?</h1>
<p class="lead">Não. O piso metodológico pedido na ficha 11(d): o <code>qwen2.5:0.5b-base</code> (só pré-treinado) e o <code>qwen2.5:0.5b-instruct</code> (mesmo porte, com ajuste por instrução) nos 90 casos, sem biblioteca (A0) e com a biblioteca recuperada (A2). O base acerta <strong>0 de 90</strong> nas duas condições: com a biblioteca ele copia a forma dos verbetes ({fmt(g[(base, "A2")]["formato_valido_pct"])}% no formato) mas inventa o rótulo em {fmt(g[(base, "A2")]["fora_do_conjunto_pct"])}% dos casos. O instruct de 0,5B chega a {fmt(g[(inst, "A0")]["causa_correta_pct"])}% e piora com a biblioteca. O ajuste por instrução é condição necessária, não suficiente: o piso da família está no porte.</p>
{kpis(itens_kpi)}
<h2>Acertar, responder no formato e inventar o rótulo</h2>
<p>A diferença entre "responder no formato" e "acertar" é o que a acurácia balanceada e a contagem de rótulos fora do conjunto medem. A biblioteca no prompt ensina a forma ao modelo base, não o conteúdo.</p>
<div class="chart"><canvas id="g-abl"></canvas></div>
{tab}
{fontes(["<code>resultados_alvo/ablacao_base_instruct/resumo_metricas.json</code> (<code>executar_bateria.py</code>, estratégia linear, 360 inferências, 29/09)", "achado 4.41; ficha 11(d)"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 6. pesquisa bibliográfica

_TOPICO = re.compile(r"^#### (\d+\.\d+\.\d+) (.+?) \(`([^`]+)` — (\d+) aprovadas?, (\d+) rejeitadas?(?:, (\d+) não verificadas?)?\)\s*$")
RODADAS = [
    ("levantamento-2026-09-11-fase-3.md", "Rodadas 1 e 2 (11 e 23/09) — Fase 3", "Fase 3"),
    ("levantamento-2026-09-22-llms-locais.md", "Rodada 3 (22/09) — LLMs locais", "LLMs locais"),
    ("levantamento-2026-09-29-documentacao-autogerida.md", "Rodada 4 (29/09) — documentação autogerida", "documentação autogerida"),
]


def secao_pesquisa() -> tuple[dict, str]:
    topicos = []
    for arquivo, rodada, curto in RODADAS:
        for l in (PESQUISA / arquivo).read_text(encoding="utf-8").splitlines():
            m = _TOPICO.match(l)
            if m:
                topicos.append({"rodada": rodada, "curto": curto, "secao": m.group(1), "titulo": m.group(2), "chave": m.group(3),
                                "aprovadas": int(m.group(4)), "rejeitadas": int(m.group(5)), "nao_verificadas": int(m.group(6) or 0)})
    n_ref = sum(1 for l in (PESQUISA / "referencias.md").read_text(encoding="utf-8").splitlines() if l.startswith("- "))
    tot_ap = sum(t["aprovadas"] for t in topicos)
    tot_rej = sum(t["rejeitadas"] for t in topicos)
    tot_nv = sum(t["nao_verificadas"] for t in topicos)
    # mapa dos filtros (rodada 4, §6.13.10)
    r4 = (PESQUISA / RODADAS[-1][0]).read_text(encoding="utf-8")
    ini = r4.index("#### 6.13.10")
    cab, linhas, _ = pt.primeira_tabela(r4[ini:])
    col = {c: i for i, c in enumerate(cab)}

    def veredito(r):
        v = re.sub(r"[*`_]", "", r[col["Veredito"]]).strip().lower()  # a coluna vem em negrito no Markdown (**adotado**)
        return "adotado" if v.startswith("adot") else "adiado" if v.startswith("adia") else "descartado" if v.startswith("desc") else "outro"
    cont = Counter(veredito(r) for r in linhas)
    trs = []
    for r in linhas:
        v = veredito(r)
        trs.append(f'<tr data-valor="{v}"><td>{pt.inline(r[col["Tema"]])}</td><td>{pt.inline(r[col["Opção"]])}</td>'
                   f'<td>{chip(v, v)}</td><td>{pt.inline(r[col["Motivo"]])}</td><td class="nota">{pt.inline(r[col.get("Fonte", len(cab) - 1)])}</td></tr>')
    mapa = (f'<div class="filtros filtro-tabela" data-alvo="tab-mapa" role="group" aria-label="Filtro do mapa">'
            f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(linhas)})</button>'
            + "".join(f'<button type="button" data-valor="{v}" aria-pressed="false">{v.capitalize()} ({cont[v]})</button>' for v in ("adotado", "adiado", "descartado") if cont[v])
            + f'</div><div class="tabela" id="tab-mapa"><table><thead><tr><th>Tema</th><th>Opção</th><th>Veredito</th><th>Motivo</th><th>Fonte</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    # tabela dos tópicos com barra
    trs = []
    for t in topicos:
        n = t["aprovadas"] + t["rejeitadas"] + t["nao_verificadas"]
        pa = 100 * t["aprovadas"] / n if n else 0
        pr = 100 * t["rejeitadas"] / n if n else 0
        barra = f'<div class="barra" title="{t["aprovadas"]} aprovadas, {t["rejeitadas"]} rejeitadas, {t["nao_verificadas"]} não verificadas"><span class="ap" style="width:{pa:.0f}%"></span><span class="rej" style="width:{pr:.0f}%"></span></div>'
        trs.append(f'<tr><td class="nota">{esc(t["rodada"])}</td><td>§{t["secao"]} {pt.inline(t["titulo"])}</td><td class="num">{t["aprovadas"]}</td><td class="num">{t["rejeitadas"]}</td><td class="num">{t["nao_verificadas"]}</td><td>{barra}</td></tr>')
    tab_topicos = f'<div class="tabela"><table><thead><tr><th>Rodada</th><th>Tópico</th><th>Aprovadas</th><th>Rejeitadas</th><th>Não verificadas</th><th>Proporção</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>'
    por_rodada = Counter(t["curto"] for t in topicos)
    itens_kpi = [
        ("Entradas em referencias.md", str(n_ref), "referências levantadas e deduplicadas por script"),
        ("Tópicos sintetizados", str(len(topicos)), " · ".join(f"{n} ({r})" for r, n in por_rodada.items())),
        ("Afirmações verificadas", f"{tot_ap} aprovadas", f"{tot_rej} rejeitadas · {tot_nv} não verificadas; cada uma checada por um agente cético"),
        ("Filtros para a documentação autogerida", f'{cont["adotado"]} adotados', f'{cont["adiado"]} adiados · {cont["descartado"]} descartados (rodada 4 → ficha 16)'),
    ]
    html_ = f'''<section id="pesquisa" hidden>
<h1>Pesquisa bibliográfica: o que a literatura diz e o que entrou no projeto</h1>
<p class="lead">Quatro rodadas de levantamento, cada tópico pesquisado por um agente, cada afirmação verificada por outro agente cético contra a fonte, e a síntese integrada ao Memorial (§6.9 a §6.13) com as referências no padrão ABNT. A rodada 4 (29/09) respondeu ao pedido do Eric sobre como melhorar a documentação autogerida e evitar alucinação: {len([t for t in topicos if t["rodada"].startswith("Rodada 4")])} tópicos, {sum(t["aprovadas"] for t in topicos if t["rodada"].startswith("Rodada 4"))} afirmações aprovadas e um mapa de {len(linhas)} filtros, dos quais {cont["adotado"]} entram como candidatos ao plano da Fase 4 (ficha 16).</p>
{kpis(itens_kpi)}
<h2>Filtros para a documentação autogerida (rodada 4)</h2>
<p>Cada linha é uma prática que a literatura sustenta, com o veredito para este projeto: <em>adotado</em> entra no plano da Fase 4, <em>adiado</em> espera medição de custo, <em>descartado</em> não cabe no desenho (prompt fixo, CPU, um modelo residente).</p>
{mapa}
<h2>Tópicos por rodada</h2>
<p>Barra verde = afirmações aprovadas; vermelha = rejeitadas; o restante, não verificadas. As rejeitadas ficam registradas com o motivo nos levantamentos.</p>
{tab_topicos}
{leitura([
    "Rodadas 1 e 2 fundamentaram a Fase 3 (tokenização, arquitetura em CPU, memória gerida pelo modelo, métricas); o mapa de decisões (§6.10) diz o que cada achado previa e o que a Fase 3 mediu.",
    "Rodada 3 avaliou o ferramental das LLMs locais: cache de respostas exato adotado, cache semântico descartado, MCP e skills descartados para o agente local.",
    "Rodada 4 é o insumo direto da ficha 16 (filtros na geração e na gestão da documentação).",
])}
{fontes(["<code>2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md</code>, <code>-22-llms-locais.md</code>, <code>-29-documentacao-autogerida.md</code>", "<code>mapa-de-decisoes-fase-3.md</code>, <code>fichamento-referencias-projeto.md</code>, <code>referencias.md</code>"])}
</section>'''
    return {}, html_


# ------------------------------------------------------------------ 7. ferramental

def secao_ferramental(med: dict | None, readme: str) -> tuple[dict, str]:
    # tabela de ferramentas do README (seção "Ferramentas de apoio")
    ini = readme.index("## Ferramentas de apoio")
    fim = readme.find("\n## ", ini + 5)
    cab, linhas, _ = pt.primeira_tabela(pt.sem_comentarios(readme[ini:fim if fim > 0 else None]))
    tab_ferr = tabela(cab, [[pt.inline(c) for c in r] for r in linhas], raw=True)
    dados_js: dict = {}
    bloco_mcp = ""
    if med:
        pa = med["por_agente"]
        tarefas = {"t1": "Onde a constante é usada", "t2": "Caminho entre duas funções", "t3": "Quem lê o fechamento.json"}

        def media(t, braco, campo):
            return sum(pa[f"{t}_{braco}_r{i}"][campo] for i in (1, 2)) / 2
        serie = [{"tarefa": nome, "grep_total": media(t, "grep", "total"), "mcp_total": media(t, "mcp", "total"),
                  "grep_novos": media(t, "grep", "novos"), "mcp_novos": media(t, "mcp", "novos")} for t, nome in tarefas.items()]
        sg, sm = sum(x["grep_total"] for x in serie), sum(x["mcp_total"] for x in serie)
        ng, nm = sum(x["grep_novos"] for x in serie), sum(x["mcp_novos"] for x in serie)
        var_t, var_n = 100 * (sm / sg - 1), 100 * (nm / ng - 1)
        dados_js = {"mcp": serie}
        itens_kpi = [
            ("Servidor × grep, tokens no total", pp(var_t).replace(" pp", "%"), "soma das três tarefas; a regra exigia −20%"),
            ("Servidor × grep, tokens novos", pp(var_n).replace(" pp", "%"), "sem contar a leitura de cache"),
            ("Acerto das respostas", "igual", "gabarito tirado do código por script; 12 subagentes Sonnet"),
            ("Incidentes", "0", "Defender sem detecção; nada gravado no repositório"),
            ("Veredito", "removido", "decisão 62 (regra de permanência da decisão 49)"),
        ]
        bloco_mcp = f'''<h2>O servidor de memória do código (codebase-memory-mcp)</h2>
<p>Instalado com salvaguardas em 22/09 sob uma regra fixada antes: fica só se cortar 20% ou mais dos tokens em três tarefas fixas, sem incidente. Em 29/09, com o servidor ativo, cada tarefa foi feita duas vezes só com busca de texto (grep) e duas só com o servidor, por subagentes iguais; o consumo foi somado dos transcritos com <code>medir_tokens.py --agentes</code>.</p>
{kpis(itens_kpi)}
<div class="controles"><label>Métrica <select id="sel-fer-met"><option value="total">tokens no total</option><option value="novos">tokens novos (sem leitura de cache)</option></select></label></div>
<div class="chart"><canvas id="g-fer-mcp"></canvas></div>
<p class="nota">Por que perdeu: cada chamada do subagente relê o contexto inteiro, e o braço do servidor gasta uma chamada só para carregar as ferramentas; num repositório de cerca de 80 arquivos Python, duas ou três buscas de texto já acham o que é preciso.</p>'''
    html_ = f'''<section id="ferramental" hidden>
<h1>Ferramental: o que a máquina faz antes do modelo</h1>
<p class="lead">Regra do projeto desde 21/09: <strong>primeiro a máquina, depois o modelo</strong>. Busca, contagem, render de tabela, conciliação, medição e verificação rodam em scripts locais (Python padrão, pasta <code>ferramentas/</code>); o modelo lê só o resumo. Este painel é um exemplo: todo número dele sai dos mesmos arquivos do Memorial, e o <code>--check</code> acusa qualquer edição manual.</p>
<h2>As ferramentas</h2>
{tab_ferr}
<h2>Economia de tokens</h2>
{leitura([
    "Saídas longas de testes e baterias passam pelo gancho <code>gancho_pre_bash.py</code> → <code>resumir_saida.py</code> antes de entrar no contexto.",
    "Subagentes só para trabalho mecânico e verificação de citações (modelos menores); um revisor por entregável; ondas de no máximo 30 agentes.",
    "Modelo, esforço e plugins fixados no início da sessão (cache de prefixo); regras por tipo de arquivo em <code>.claude/rules/</code>.",
    "Nenhum JSON de resultado colado em prompt: agentes leem arquivos; a medição de consumo é local (<code>medir_tokens.py</code>).",
])}
{bloco_mcp}
{fontes(["<code>README.md</code> (tabela das ferramentas)", "<code>5-metodo-e-ferramental/ferramental-do-claude-code.md</code> §7.2 e §7.9", "<code>5-metodo-e-ferramental/dados/medicao-permanencia-mcp.json</code>", "decisões 49 e 62"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ JS e CSS das abas novas

JS_TOPICOS = r"""
const T = D.topicos;
const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`; };
function cqTrajetoria(){
  const conj = document.getElementById('sel-cq-conj').value, met = document.getElementById('sel-cq-met').value; const pts = T.cq.trajetoria[conj];
  grafico('g-cq-traj', {type:'line', data:{labels: pts.map(p => p.rot), datasets:[T.cq.A, T.cq.B].map(m => ({label:m, data: pts.map(p => p[met+(m===T.cq.A?'_A':'_B')]), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='bal'?'acurácia balanceada (%)':'acerto (%)'}, suggestedMin:40, suggestedMax:95}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function cqConfronto(){
  const conj = document.getElementById('sel-cq-conf').value; const rows = T.cq.confronto[conj];
  grafico('g-cq-conf', {type:'bar', data:{labels: rows.map(r => r.rot), datasets:[{label:'só o '+T.cq.A+' acertou', data: rows.map(r => r.so_A), backgroundColor:cor(T.cq.A)}, {label:'só o '+T.cq.B+' acertou', data: rows.map(r => r.so_B), backgroundColor:cor(T.cq.B)}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true}}, plugins:{tooltip:{callbacks:{afterLabel: c => { const r = rows[c.dataIndex]; return `ambos ${r.ambos} · nenhum ${r.nenhum} · p (McNemar) ${r.p}`; }}}}}});
}
function cqRevisao(){
  const cats = ['Correta','Parcial','Errada'], cores = {Correta:css('--bom'),Parcial:css('--meio'),Errada:css('--ruim')}; const mods = [T.cq.A, T.cq.B];
  grafico('g-cq-rev', {type:'bar', data:{labels: mods, datasets: cats.map(k => ({label:k, data: mods.map(m => T.cq.revisao[m===T.cq.A?'A':'B'][k]), backgroundColor: cores[k]}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, max:100, title:{display:true,text:'% das edições revisadas'}}, y:{stacked:true}}, plugins:{tooltip:{callbacks:{afterLabel: c => 'n = '+T.cq.revisao[c.label===T.cq.A?'A':'B'].n}}}}});
}
function tbGeneraliza(){
  const met = document.getElementById('sel-tb-met').value; const ds = [];
  T.tresb.modelos.forEach(m => { ds.push({label:m+' · 36 oficiais', data: T.tresb.Ls.map(l => T.tresb.oficiais[m][l][met]), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4});
    ds.push({label:m+' · 36 inéditos', data: T.tresb.Ls.map(l => T.tresb.ineditos[m][l][met]), borderColor:cor(m), backgroundColor:cor(m), borderDash:[6,4], tension:.2, pointRadius:4, pointStyle:'rectRot'}); });
  grafico('g-tb-gen', {type:'line', data:{labels: T.tresb.Ls.map(l => 'L'+l), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='bal'?'acurácia balanceada (%)':'acerto (%)'}, suggestedMin:50, suggestedMax:95}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function tbRecuperacao(){
  const ds = [];
  T.tresb.modelos.forEach(m => { ds.push({label:m+' · inéditos', data: T.tresb.Ls.map(l => T.tresb.rec_ineditos[m][l]), backgroundColor:cor(m)}); ds.push({label:m+' · oficiais', data: T.tresb.Ls.map(l => T.tresb.rec_oficiais[m][l]), backgroundColor:rgba(cor(m), .4)}); });
  grafico('g-tb-rec', {type:'bar', data:{labels: T.tresb.Ls.map(l => 'L'+l), datasets: ds}, options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'hit@3 (%)'}, min:0, max:100}}}});
}
function curOperacoes(){
  const cats = ['Correta','Parcial','Errada'], cores = {Correta:css('--bom'),Parcial:css('--meio'),Errada:css('--ruim')};
  grafico('g-cur-op', {type:'bar', data:{labels: T.curadoria.operacoes, datasets: cats.map(k => ({label:k, data: T.curadoria.operacoes.map(o => T.curadoria.por[o][k]||0), backgroundColor: cores[k]}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, title:{display:true,text:'edições'}, beginAtZero:true}, y:{stacked:true}}}});
}
function recMetodos(){
  const bib = document.getElementById('sel-rec-bib').value, met = document.getElementById('sel-rec-met').value; const v = T.recuperador.valores[bib]||{};
  grafico('g-rec-met', {type:'bar', data:{labels: T.recuperador.metodos, datasets: T.recuperador.conjuntos.map((c, i) => ({label:c, data: T.recuperador.metodos.map(m => (v[c]||{})[m] ? v[c][m][met] : null), backgroundColor: css('--s'+(i+1))}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='mrr'?'MRR':met+' (%)'}, min:0, max: met==='mrr'?1:100}}}});
}
function ablBarras(){
  const L = T.ablacao.linhas; const series = [['acerto','acerto (%)'],['formato','formato válido (%)'],['fora','rótulo fora do conjunto (%)']];
  grafico('g-abl', {type:'bar', data:{labels: L.map(x => x.modelo.replace('qwen2.5:','')+' · '+x.cond), datasets: series.map(([k, nome], i) => ({label:nome, data: L.map(x => x[k]), backgroundColor: css('--s'+(i+1))}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true,text:'% dos 90 casos'}}}, plugins:{tooltip:{callbacks:{afterLabel: c => c.datasetIndex===0 ? 'IC 95% '+L[c.dataIndex].ic.join('–') : ''}}}}});
}
function ferMcp(){
  if(!T.ferramental.mcp) return; const met = document.getElementById('sel-fer-met').value; const S = T.ferramental.mcp;
  grafico('g-fer-mcp', {type:'bar', data:{labels: S.map(x => x.tarefa), datasets:[{label:'grep, Glob e Read', data: S.map(x => Math.round(x['grep_'+met])), backgroundColor: css('--s1')}, {label:'servidor codebase-memory', data: S.map(x => Math.round(x['mcp_'+met])), backgroundColor: css('--s2')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'tokens (média de 2 repetições)'}, beginAtZero:true}}}});
}
"""

DESENHAR_TOPICOS = {"comparativo": ["cqTrajetoria", "cqConfronto", "cqRevisao"], "tresb": ["tbGeneraliza", "tbRecuperacao"],
                    "curadoria": ["curOperacoes"], "recuperador": ["recMetodos"], "ablacao": ["ablBarras"], "ferramental": ["ferMcp"]}
SELETORES_TOPICOS = {"sel-cq-conj": "cqTrajetoria", "sel-cq-met": "cqTrajetoria", "sel-cq-conf": "cqConfronto", "sel-tb-met": "tbGeneraliza",
                     "sel-rec-bib": "recMetodos", "sel-rec-met": "recMetodos", "sel-fer-met": "ferMcp"}

CSS_TOPICOS = r"""
.leitura{padding-left:22px;max-width:90ch}.leitura li{margin:6px 0}.fontes{max-width:none}
main > section{scroll-margin-top:120px}.kpi b.longo{font-size:20px}
.dc{white-space:nowrap}.delta{display:inline-block;font:600 11px var(--fm);padding:0 5px;border-radius:4px;margin-left:4px;background:var(--bg2);color:var(--ink)}
.delta.zero{color:var(--ink2)}
.duelo td:first-child,.heat td:first-child{white-space:nowrap}
.barra{display:flex;height:10px;width:100%;min-width:120px;background:color-mix(in srgb,var(--ink2) 15%,transparent);border-radius:5px;overflow:hidden}
.barra .ap{background:var(--bom);height:100%}.barra .rej{background:var(--ruim);height:100%}
.mapa-painel{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:12px;margin:14px 0}
.mapa-painel div{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:12px 14px}
.mapa-painel h3{margin:0 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--ink2);font-family:var(--fb)}
.mapa-painel ul{list-style:none;padding:0;margin:0}.mapa-painel li{margin:6px 0;font-size:13px}.mapa-painel a{color:var(--acento);font-weight:600;text-decoration:none}.mapa-painel a:hover{text-decoration:underline}
.chip.adotado{background:color-mix(in srgb,var(--bom) 18%,transparent);color:var(--bom)}.chip.adiado{background:color-mix(in srgb,var(--meio) 18%,transparent);color:var(--meio)}.chip.descartado{background:color-mix(in srgb,var(--ruim) 16%,transparent);color:var(--ruim)}
"""


# ------------------------------------------------------------------ montagem

def montar(ctx: dict) -> tuple[dict, str]:
    """ctx: dados (montar_dados), road, cartoes_corridas, md_para_html, md_doc_para_html, cq, blocos_cq, ineditos,
    curadoria, planilha_curadoria, recuperador, ablacao, medicao_mcp, readme. Devolve (dados_topicos, html)."""
    dados, road = ctx["dados"], ctx["road"]
    partes: list[tuple[str, dict, str]] = []
    d, h = secao_comparativo(ctx["cq"], ctx["blocos_cq"], ctx["md_para_html"], road, ctx["cartoes_corridas"])
    partes.append(("cq", d, h))
    d, h = secao_tres_b(ctx["ineditos"], dados, road, ctx["cartoes_corridas"], ctx["md_doc_para_html"])
    partes.append(("tresb", d, h))
    d, h = secao_curadoria(ctx["curadoria"], ctx["planilha_curadoria"])
    partes.append(("curadoria", d, h))
    d, h = secao_recuperador(ctx["recuperador"])
    partes.append(("recuperador", d, h))
    ined = partes[1][1]["ineditos"]
    d, h = secao_ablacao(ctx["ablacao"], dados["curvas"]["90"][COD3B]["0"]["acerto"], ined.get(COD3B, {}).get("0", {}).get("acerto"))
    partes.append(("ablacao", d, h))
    d, h = secao_pesquisa()
    partes.append(("pesquisa", d, h))
    d, h = secao_ferramental(ctx.get("medicao_mcp"), ctx["readme"])
    partes.append(("ferramental", d, h))
    return {k: d for k, d, _ in partes}, "\n".join(h for _, _, h in partes)
