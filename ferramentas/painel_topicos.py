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
import unicodedata
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import painel_atlas as pa
import painel_explorador as pe
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

# Mapa do painel: grupo → (id da seção, nome na aba, o que a aba responde). É a fonte da barra lateral de navegação e
# da lista "Mapa do painel" da aba Início. A ordem é a de importância para quem decide: primeiro o projeto e o que
# depende do Eric, depois a decisão e os resultados que a sustentam, a biblioteca gerida pelo modelo (o experimento
# central), a Pré-Fase 4 (a fase em andamento), a pesquisa e o método e, por último, as fases anteriores.
# ! Alteração de IA - Revisar: (06/10/2026) grupos renomeados e reordenados por importância, com a aba mais importante
# de cada grupo em primeiro (Decisão antes de Resultados; Pesquisa antes de Ferramental).
# ! Motivo: pedido do Eric em 06/10: com 23 abas a faixa horizontal ficou ilegível, e a ordem antiga era a de
# construção (Resultados antes da Decisão, Fases anteriores antes da Pesquisa), não a de leitura.
NAV = [
    ("Projeto", [
        ("inicio", "Início", "Onde o projeto está, o que depende do Eric e o mapa deste painel."),
        ("pendencias", "Pendências", "Uma ficha por decisão: o que é, por que importa, opções, recomendação e decisão."),
        ("roadmap", "Roadmap", "Estado por fase, corridas com o comando pronto e o esqueleto das Fases 4 e 5."),
        ("fechamento", "Fechamento", "As Fases 3 e 3-B podem ser dadas por concluídas? O estado de cada tópico e o que depende do Eric."),
    ]),
    ("Decisão e resultados", [
        ("decisao", "Decisão", "A regra pré-registrada, o bootstrap, a fronteira de Pareto e a frase da decisão."),
        ("visao", "Resultados", "O que os testes decidiram: acurácia por versão da biblioteca e as três fases lado a lado."),
        ("hipoteses", "Hipóteses", "As seis hipóteses pré-registradas, o veredito de cada uma e os achados novos."),
        ("modelos", "Modelos", "Veredito e números de cada modelo, acerto por classe de defeito e por nível."),
        ("comparativo", "qwen × Coder", "Em que cenários o qwen2.5-coder:7b seria melhor que o qwen2.5:7b, e por que a decisão ficou."),
    ]),
    ("Biblioteca gerida pelo modelo", [
        ("fase3", "Fase 3", "A biblioteca gerida pelo modelo: edições, rejeições, recuperação, custo e revisão humana."),
        ("tresb", "Fase 3-B", "Casos inéditos, ponte de versão, sonda de correção e as corridas complementares."),
        ("cruzada", "Troca cruzada", "A biblioteca escrita por um modelo, lida por outros dois: o ganho é dela ou de quem a lê?"),
        ("curadoria", "Curadoria da L1", "O que a cópia de produção herdou da biblioteca escrita pelo modelo."),
        ("recuperador", "Recuperador", "BM25 com sinais contra embeddings e híbrido: vale trocar?"),
        ("ablacao", "Ablação", "Sem ajuste por instrução, o modelo faz a tarefa? O piso da família."),
    ]),
    # grupo da Pré-Fase 4 (01/10/2026): um id só entra neste mapa junto com a seção dele, porque
    # teste_toda_aba_do_mapa_existe_na_pagina exige que todo botão da navegação tenha a sua seção
    ("Pré-Fase 4", [
        ("colibri", "Modelos grandes pelo disco", "Dá para rodar nesta máquina um modelo gigante lendo os pesos do SSD? O que o colibri pede, o que foi medido aqui e o que se aproveita."),
        ("atlas", "Atlas", "Que verbetes a busca entrega para cada tipo de defeito e o que o modelo faz com eles: o mapa, a rota de cada caso e as trocas entre causas."),
        ("raciocinio", "Raciocínio aberto", "Dá para ver por que o modelo respondeu o que respondeu? A trilha bruta, o relatório por caso e o que o código consegue conferir."),
    ]),
    ("Pesquisa e método", [
        ("pesquisa", "Pesquisa", "As rodadas de literatura, as afirmações verificadas e os filtros adotados."),
        ("metodo", "Método e limites", "Como a Fase 3 foi medida, as limitações declaradas e a Fase 3-B."),
        ("ferramental", "Ferramental", "As ferramentas locais, a economia de tokens e a medição do servidor de memória do código."),
    ]),
    ("Fases anteriores", [
        ("fases2", "Fases 2-A e 2-B", "Prompts sem documentação e a biblioteca escrita à mão em seis condições."),
        ("comparacao", "Entre fases", "O que cada etapa acrescentou, nos 90 e nos 36, com custo e riscos."),
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
    # ! Alteração de IA - Revisar: (06/10/2026) o confronto nos 36 inéditos (corrida 7) entra no cartão, na frase de abertura e numa seção própria.
    # ! Motivo: a aba dizia que a corrida 7 só rodaria "se o Eric quiser"; ele rodou em 06/10, e o resultado toca a decisão 52 (ficha 21).
    ined_cq = {x["L"]: x for x in cq.get("confronto_ineditos", [])}
    i1 = ined_cq.get(1)
    frase_ineditos = (f'Nos <strong>36 inéditos</strong> (corrida 7, 06/10) o Coder fica à frente com L0 e L1 (com a L1 de cada um, {i1["so_coder"]} casos só dele contra '
                      f'{i1["so_qwen"]} só do qwen, p = {fmt(i1["p_mcnemar"], 3)}) e atrás com L3; nos 72 casos com L1 o placar empata. É a condição 1 do que mudaria a decisão 52, '
                      'parcialmente cumprida e dentro do ruído: o que fazer com ela é a ficha 21.' if i1 else "")
    itens_kpi = [
        ("Células em que o Coder lidera", str(n_vence), f"maior vantagem {pp(max_delta)}; {n_vence_36} delas nos 36 nunca vistos"),
        ("Nos 36 inéditos com L1 (06/10)", f'{i1["so_qwen"]} × {i1["so_coder"]}' if i1 else "não rodou", f'casos que só um acertou; {fmt(i1["acerto_A"])}% × {fmt(i1["acerto_B"])}%, p = {fmt(i1["p_mcnemar"], 3)}' if i1 else "corrida 7"),
        ("Nos 36 nunca vistos, melhor versão", f"{fmt(melhor_A)}% × {fmt(melhor_B)}%", f"qwen L{LA} × Coder L{LB}, acerto simples"),
        ("Confronto em L1 nos 36", f'{c1["so_qwen"]} × {c1["so_coder"]}', f'casos que só um acertou; ambos {c1["ambos"]}, p = {fmt(c1["p_mcnemar"], 3)}'),
        ("Edições aceitas na época 1", f'{doc1["aceitas_A"]} × {doc1["aceitas_B"]}', f'de {doc1["propostas_A"]} × {doc1["propostas_B"]} propostas; corretas na revisão {fmt(corr["A"])}% × {fmt(corr["B"])}%'),
        ("hit@3 com a biblioteca L1 (90)", f'{fmt(rec1["hit3_90_A"])}% × {fmt(rec1["hit3_90_B"])}%', f'{rec1["verbetes_A"]} × {rec1["verbetes_B"]} verbetes'),
        ("P(top-1) do Coder nos 36", f"≤ {fmt(100 * p_max_B)}%", f'primeiro em {est.get(B, 0)} × {est.get(A, 0)} de {cq["decisao"]["total_rankings"]} ordenações; {fmt(l1["s_A"])} × {fmt(l1["s_B"])} s por diagnóstico em L1'),
    ]
    corridas = cartoes_corridas(road, numeros=["1", "7"], sufixo="-cq")
    html_ = f'''<section id="comparativo" hidden>
<h1>qwen2.5:7b × qwen2.5-coder:7b: em que cenários o Coder seria melhor?</h1>
<p class="lead">Pergunta do Eric em 29/09: "pode ser que em alguns cenários o coder seja mais interessante". Resposta: o Coder fica à frente em <strong>{n_vence} células</strong>, todas pequenas (a maior por {pp(max_delta)}) e quase todas nos 54 casos de aprendizado e nas classes léxica, runtime e efeito. Nos <strong>36 casos nunca vistos</strong> o qwen2.5:7b vence em todas as versões da biblioteca ({fmt(melhor_A)}% × {fmt(melhor_B)}% na melhor versão de cada um), e em nenhuma ordenação o Coder tem chance real de ser o primeiro (P(top-1) ≤ {fmt(100 * p_max_B)}%). Como escritor, o Coder é mais contido e mais certo ({fmt(corr["B"])}% de edições corretas contra {fmt(corr["A"])}%). A decisão 52 fica. {frase_ineditos}</p>
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
<h2>Nos 36 casos inéditos (corrida 7, 06/10/2026)</h2>
<p>O Coder 7B diagnosticou os mesmos 36 inéditos que o qwen rodou em 28/09, com a biblioteca original e com as versões que ele mesmo escreveu. Caso a caso, por versão e por classe (6 casos por classe: um caso vale 16,7 pontos).</p>
{B_("cq_ineditos")}
{detalhes("Por classe, com a L1 de cada um", B_("cq_ineditos_classe"))}
<h2>As duas corridas que fechariam a pergunta</h2>
{corridas}
{fontes(["<code>comparativo-qwen25-7b-vs-coder-7b.md</code> (Memorial, 3-resultados-e-analises)", "<code>comparativo_qwen_coder.json</code> e <code>.md</code> gerados por <code>comparar_qwen_coder.py</code> (--check)", "achado 4.38; decisão 52 mantida"])}
</section>'''
    return dados, html_


# ------------------------------------------------------------------ 2. Fase 3-B

def secao_tres_b(ined: dict, dados: dict, road: dict, cartoes_corridas, md_doc_para_html, an: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: em 01/10/2026 a aba ganhou a soma dos 36 oficiais com os 36 inéditos e a tabela dos
    # casos que mudam entre corridas iguais (lidas de `analise_fase3b.json`, parâmetro `an`), e três textos mudaram: o
    # rótulo do cartão do 3B, a frase de abertura e a remissão à troca cruzada.
    # ! Motivo: o cartão dizia "a biblioteca do qwen não muda o 3B", mas nos inéditos cada modelo leu a biblioteca que
    # ele mesmo escreveu (hash 53ccf19abeac e d9a86e383103 no 3B); a abertura dizia que faltava a troca cruzada, que
    # rodou em 01/10 e ganhou aba própria.
    cur: dict = defaultdict(dict)
    for x in ined["por_modelo_biblioteca_particao"]:
        cur[x["modelo"]][str(x["biblioteca_epoca"])] = {"acerto": x["causa_correta_pct"], "bal": x["acuracia_balanceada_pct"], "s": x["segundos_mediana"]}
    modelos = [m for m in (A, B, COD3B) if m in cur]
    Ls = sorted({L for m in modelos for L in cur[m]}, key=int)
    oficial = {m: {L: {"acerto": dados["curvas"]["36"][m][L]["acerto"], "bal": dados["curvas"]["36"][m][L]["balanceada"]} for L in Ls} for m in modelos}
    rec: dict = defaultdict(dict)
    for x in ined["recuperacao"]:
        rec[x["modelo"]][str(x["biblioteca_epoca"])] = x["hit@3"]
    rec_of = {m: {L: dados["recuperacao"][m][L]["hit3_36"] for L in Ls} for m in modelos}
    par = [x for x in ined["pareado_vs_L0"] if x.get("particao", "avaliacao") == "avaliacao"]
    # ! Alteração de IA - Revisar: a aba passa a ler todas as pontes de versão (`dados["pontes"]`, montado em
    # gerar_dashboard.pontes_de_versao) e a resumir a mais recente (30/09/2026, noite).
    # ! Motivo: só a ponte de 21/09 (Ollama 0.34.1) era lida, pelo nome fixo `fase3b_ponte`; a de 30/09 (0.34.4)
    # deu o Coder 7B com b + c = 4, acima do limite da decisão 47, e o texto fixo "a ponte é pareável" ficaria errado.
    pontes = dados.get("pontes", [])
    ult = pontes[-1] if pontes else {"versao": "?", "linhas": []}
    q = cur[A]
    L_ult = Ls[-1]
    p_ult = next((x for x in par if x["modelo"] == A and str(x["biblioteca_epoca"]) == L_ult), {})
    corr3b = [c for c in road["corridas"] if c.comando and "-Modo" in c.comando]
    n_feitas = sum(c.classe == "feita" for c in corr3b)
    n_pend = sum(c.classe in ("pendente", "aguarda") for c in corr3b)
    n_opc = sum(c.classe == "opcional" for c in corr3b)
    ponte_txt = "; ".join(f'{x["modelo"]} b/c {x["b"]}/{x["c"]}' for x in ult["linhas"])
    n_par = sum(x["pareavel"] for x in ult["linhas"])
    acima = [x["modelo"] for x in ult["linhas"] if not x["pareavel"]]
    if not ult["linhas"]:
        ponte_frase = "A ponte de versão do Ollama ainda não foi registrada na decisão."
    elif acima:
        ponte_frase = (f'Na ponte de versão mais recente (Ollama {ult["versao"]}), {n_par} de {len(ult["linhas"])} modelos continuam pareáveis com a Fase 3; '
                       f'{", ".join(acima)} passou do limite e é lido contra a própria ponte.')
    else:
        ponte_frase = f'A ponte de versão mais recente (Ollama {ult["versao"]}) é pareável nos {len(ult["linhas"])} modelos.'
    dados_js = {"modelos": modelos, "Ls": Ls, "ineditos": {m: cur[m] for m in modelos}, "oficiais": oficial,
                "rec_ineditos": {m: rec[m] for m in modelos}, "rec_oficiais": rec_of}
    tab_par = tabela(["Modelo", "Versão", "Diferença contra L0", "b / c (✗→✓ / ✓→✗)", "p (McNemar exato)"],
                     [[x["modelo"], f'L{x["biblioteca_epoca"]}', pp(x.get("delta_pp")), f'{x.get("b", "—")} / {x.get("c", "—")}', fmt(x.get("p_mcnemar"), 3)] for x in par])
    tab_ponte = tabela(["Ponte", "Modelo", "Acerto em L0 (36)", "Acurácia balanceada", "b / c contra a Fase 3", "p (McNemar exato)", "Leitura"],
                       [[f'Ollama {p["versao"]}', x["modelo"], f'{fmt(x["acerto"])}%', f'{fmt(x["bal"])}%', f'{x["b"]} / {x["c"]}', fmt(x["p"], 3),
                         "pareável" if x["pareavel"] else "divergente"] for p in pontes for x in p["linhas"]])
    sec = {t[:3]: c for t, c in road["secoes"]}
    leitura_ined = next((c for t, c in road["secoes"] if t.startswith("2.1")), "")
    leitura_ponte = next(((t, c) for t, c in road["secoes"] if t.startswith("2.3")), None)
    sonda = next((c for t, c in road["secoes"] if t.startswith("3. ")), "")
    itens_kpi = [
        (f"{A} nos 36 inéditos", " → ".join(f'{fmt(q[L]["acerto"])}%' for L in Ls), f'acerto com {" → ".join("L" + L for L in Ls)}; balanceada ' + " / ".join(fmt(q[L]["bal"]) for L in Ls)),
        (f"{COD3B} nos 36 inéditos", " → ".join(f'{fmt(cur[COD3B][L]["acerto"])}%' for L in Ls) if COD3B in cur else "—", "a biblioteca que ele mesmo escreveu não muda nenhum acerto"),
        (f"L{L_ult} contra L0 no qwen", pp(p_ult.get("delta_pp")), f'b/c {p_ult.get("b", "—")}/{p_ult.get("c", "—")}, p = {fmt(p_ult.get("p_mcnemar"), 3)}'),
        ("hit@3 nos inéditos (qwen)", " → ".join(f'{fmt(rec[A][L])}%' for L in Ls), f'nos 36 oficiais: ' + " → ".join(f'{fmt(rec_of[A][L])}%' for L in Ls)),
        ("Ponte de versão", f"{n_par} de {len(ult['linhas'])} pareáveis", f"Ollama {ult['versao']}: {ponte_txt}; pareável quando b + c ≤ 2"),
        ("Corridas da 3-B", f"{n_feitas} feitas · {n_pend} pendentes", f"{n_opc} opcionais"),
    ]
    # ! Alteração de IA - Revisar: (06/10/2026) as duas corridas opcionais, rodadas pelo Eric em 06/10, entram na aba lidas de
    # analise_fase3b.json: o Coder 7B contra o qwen nos mesmos inéditos (corrida 7) e a adesão cega com a L3 própria (corrida 5).
    # ! Motivo: sem isto a aba diria que as corridas eram opcionais e não rodadas, e os números ficariam só no relatório.
    entre = (an or {}).get("ineditos", {}).get("entre_modelos", [])
    a5 = (an or {}).get("a5", {}).get("linhas", [])
    c7 = {x["biblioteca_epoca"]: x for x in entre if x["modelo"] == B}
    if B in cur:
        itens_kpi.insert(2, (f"Coder 7B nos 36 inéditos (06/10)", " → ".join(f'{fmt(cur[B][L]["acerto"])}%' for L in Ls),
                             f'contra o qwen com a L1 de cada um: b/c {c7[1]["b"]}/{c7[1]["c"]}, p = {fmt(c7[1]["p_mcnemar"], 3)}; nos 72, {c7[1]["somados"]["b"]}/{c7[1]["somados"]["c"]}' if 1 in c7 else "sem confronto"))
    if a5:
        itens_kpi.insert(3, ("Adesão cega com a L3 própria (06/10)", " · ".join(f'{fmt(l["seguiu_pct"])}%' for l in a5),
                             "; ".join(f'{NOME_CURTO.get(l["modelo"], l["modelo"])}: seguiu a causa plantada em {l["seguiu"]} de {l["n"]}' for l in a5)))
    # a análise identifica a classe pelo id sem acento (lexica, traducao); o painel mostra o nome com acento
    classes_entre = [("".join(ch for ch in unicodedata.normalize("NFKD", nome) if not unicodedata.combining(ch)), nome) for _, nome in sorted(CLASSES.items(), key=lambda kv: int(kv[0]))]
    tab_entre = ('<div class="tabela"><table><thead><tr><th>Modelo</th><th>Biblioteca de cada um</th><th>Acerto nos 36 inéditos</th><th>Acerto do qwen2.5:7b</th>'
                 '<th>b / c (só o modelo / só o qwen)</th><th>Diferença</th><th>p (McNemar exato)</th><th>Nos 72 (oficiais + inéditos): b / c</th>'
                 + "".join(f"<th>{esc(n)}</th>" for _, n in classes_entre) + "</tr></thead><tbody>"
                 + "".join(f'<tr data-entre-modelos="{html.escape(x["modelo"] + "/L" + str(x["biblioteca_epoca"]), quote=True)}"><td>{esc(x["modelo"])}</td><td>L{x["biblioteca_epoca"]}</td>'
                           f'<td class=num>{fmt(x["acerto_pct"])}%</td><td class=num>{fmt(x["acerto_doador_pct"])}%</td><td class=num>{x["b"]} / {x["c"]}</td><td class=num>{pp(x["delta_pp"])}</td>'
                           f'<td class=num>{fmt(x["p_mcnemar"], 3)}</td><td class=num>{x["somados"]["b"]} / {x["somados"]["c"]}</td>'
                           + "".join(f'<td class=num>{x["por_classe"][i]["acertos"]} / {x["por_classe"][i]["acertos_doador"]} de {x["por_classe"][i]["n"]}</td>' if i in x["por_classe"] else "<td>n/d</td>" for i, _ in classes_entre)
                           + "</tr>" for x in entre) + "</tbody></table></div>")
    tab_a5 = ('<div class="tabela"><table><thead><tr><th>Modelo</th><th>Biblioteca</th><th>Casos</th><th>Seguiu a causa plantada</th><th>Acertou mesmo assim</th>'
              '<th>O mesmo modelo, a mesma biblioteca, na condição normal (A2, Fase 3)</th><th>Adesão cega na Fase 2-B (biblioteca original)</th></tr></thead><tbody>'
              + "".join(f'<tr data-a5="{html.escape(l["modelo"], quote=True)}"><td>{esc(l["modelo"])}</td><td>L{l["biblioteca_epoca"]} própria</td><td class=num>{l["n"]}</td>'
                        f'<td class=num>{l["seguiu"]} ({fmt(l["seguiu_pct"])}%)</td><td class=num>{l["acertos"]} ({fmt(l["acerto_pct"])}%)</td><td class=num>{fmt(l["acerto_a2_pct"])}%</td>'
                        f'<td class=num>{"não medida" if l["adesao_2b_pct"] is None else fmt(l["adesao_2b_pct"]) + "%"}</td></tr>' for l in a5) + "</tbody></table></div>")
    bloco_opcionais = ""
    if entre or a5:
        bloco_opcionais = ('<h2>As duas corridas que eram opcionais (06/10/2026)</h2>'
                           + ('<h3>Modelo contra modelo nos mesmos 36 inéditos (corrida 7)</h3><p>O Coder 7B rodou os 36 inéditos em 06/10 com a biblioteca original e com as versões que '
                              'ele mesmo escreveu; o qwen e o Coder 3B tinham rodado em 28/09. b conta os casos que só o modelo da linha acertou e c os que só o qwen acertou; as colunas '
                              'por classe trazem os acertos do modelo e do qwen nos 6 casos da classe.</p>' + tab_entre if entre else "")
                           + ('<h3>Adesão cega à documentação errada, com a biblioteca própria (corrida 5)</h3><p>Na condição A5 o contexto afirma uma causa errada para o sintoma e '
                              'nunca traz o verbete de ouro. Na Fase 2-B isso foi medido com a biblioteca original; aqui cada modelo leu a própria L3 nos 36 oficiais.</p>' + tab_a5 if a5 else ""))
    agrupado = (an or {}).get("ineditos", {}).get("agrupado", [])
    tab_agrupado = tabela(["Modelo", "Biblioteca", "Casos", "Acerto com L0", "Acerto com a biblioteca", "Oficiais: b / c", "Inéditos: b / c", "Somados: b / c", "Diferença", "p (McNemar exato)"],
                          [[x["modelo"], f'L{x["biblioteca_epoca"]}', x["n_comuns"], f'{fmt(x["acerto_l0_pct"])}%', f'{fmt(x["acerto_pct"])}%', f'{x["oficiais"]["b"]} / {x["oficiais"]["c"]}',
                            f'{x["ineditos"]["b"]} / {x["ineditos"]["c"]}', f'{x["b"]} / {x["c"]}', pp(x["delta_pp"]), fmt(x["p_mcnemar"], 3)] for x in agrupado])
    mde = {x["n"]: x["delta_pp"] for x in (an or {}).get("ineditos", {}).get("efeito_minimo_detectavel", [])}
    maior = max((x["delta_pp"] for x in agrupado), default=None)
    frase_72 = (f'Somando os 36 oficiais e os 36 inéditos, o maior ganho é de {pp(maior)}, abaixo do efeito mínimo detectável com 72 casos ({fmt(mde.get(72))} pontos): '
                "a biblioteca fica acima de L0 nas duas versões, sem resolução estatística." if agrupado and mde.get(72) else "")
    ruido = (an or {}).get("ruido_l0", [])
    # ! Alteração de IA - Revisar: a variação entre corridas passa a ser contada com a mesma entrada (01/10/2026, depois da
    # revisão independente do relatório da 3-B): sai da conta o caso cujo texto foi corrigido entre as duas corridas.
    # ! Motivo: o `efe-3` teve o sintoma corrigido em 28/09; contá-lo como "caso que mudou entre corridas iguais" dava 4
    # casos no Coder 7B, e com a mesma entrada são 3.
    tab_ruido = tabela(["Modelo (L0, 36 casos)", "Corrida A", "Corrida B", "Casos que mudaram de acerto", "Com a mesma entrada", "Só B acertou", "Só A acertou", "Rótulos que mudaram", "Quais"],
                       [[x["modelo"], x["corrida_a"], x["corrida_b"], x["discordantes"], x.get("discordantes_mesma_entrada", x["discordantes"]), x["b"], x["c"], x.get("rotulos_diferentes", "—"),
                         ", ".join(x["casos"]) or "nenhum"] for x in ruido])
    mesma = [x.get("discordantes_mesma_entrada", x["discordantes"]) for x in ruido]
    saldo_mesma = max((abs(x.get("b_mesma_entrada", x["b"]) - x.get("c_mesma_entrada", x["c"])) for x in ruido), default=0)
    frase_ruido = (f'Com a mesma entrada, entre duas corridas iguais do mesmo modelo mudam de acerto de {min(mesma)} a {max(mesma)} casos em 36, com saldo de até {saldo_mesma}: é a régua para ler '
                   f'qualquer diferença pequena deste painel. A coluna "Casos que mudaram de acerto" conta também o efe-3, cujo texto foi corrigido em 28/09 e que não é a mesma entrada.' if ruido else "")
    html_ = f'''<section id="tresb" hidden>
<h1>Fase 3-B: o ganho da biblioteca generaliza para casos nunca vistos?</h1>
<p class="lead">Trinta e seis casos inéditos, escritos só a partir do código do sistema-cobaia e nunca vistos por nenhum modelo, foram diagnosticados com a biblioteca original (L0) e com as versões que cada modelo escreveu (L1 e L3). O qwen acerta {" → ".join(f'{fmt(q[L]["acerto"])}%' for L in Ls)}: o ganho de L1 medido nos 36 oficiais <strong>não reaparece</strong>, e L{L_ult} rende {pp(p_ult.get("delta_pp"))} (b/c {p_ult.get("b", "—")}/{p_ult.get("c", "—")}, p = {fmt(p_ult.get("p_mcnemar"), 3)}). O 3B acerta o mesmo nas três versões. {esc(frase_72)} {esc(ponte_frase)} A troca cruzada, que separa quem escreveu a biblioteca de quem a lê, tem <a href="#cruzada" data-ir="cruzada|">aba própria</a>.</p>
{kpis(itens_kpi)}
<h2>Oficiais × inéditos</h2>
<p>Linha cheia: os 36 casos oficiais de avaliação (vistos em quatro passadas por modelo). Linha tracejada: os 36 inéditos. Se o ganho fosse da biblioteca, as duas linhas subiriam juntas.</p>
<div class="controles"><label>Métrica <select id="sel-tb-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-tb-gen"></canvas></div>
<h2>O recuperador nos inéditos</h2>
<p>hit@3 = o verbete de ouro está entre os três recuperados. Nos inéditos o recuperador acerta menos e cai com as notas acrescentadas; nos oficiais, fica estável.</p>
<div class="chart baixo"><canvas id="g-tb-rec"></canvas></div>
{tab_par}
{"<h2>Oficiais e inéditos somados (72 casos)</h2><p>Cada versão da biblioteca contra a original, nos dois conjuntos e na soma. b conta os casos que só a versão nova acertou; c, os que só a original acertou.</p>" + tab_agrupado if agrupado else ""}
{bloco_opcionais}
<h2>Ponte de versão do Ollama</h2>
<p>A bateria oficial rodou no Ollama 0.34.0, e o Ollama se atualiza sozinho. A cada versão nova, a ponte repete L0 nos 36 e compara caso a caso com a Fase 3: b conta os casos que só a ponte acertou, c os que só a Fase 3 acertou. Com b + c até 2 as corridas dessa versão são pareáveis com a Fase 3; acima disso, o modelo é lido contra a própria ponte e a ressalva vai para o relatório (decisão 47).</p>
{tab_ponte}
{"<h3>Quanto o resultado varia sozinho</h3><p>" + esc(frase_ruido) + "</p>" + tab_ruido if ruido else ""}
{detalhes(f"Leitura da ponte mais recente (roadmap §{leitura_ponte[0][:3]})", md_doc_para_html(leitura_ponte[1])) if leitura_ponte else ""}
<h2>Corridas da Fase 3-B</h2>
{cartoes_corridas(road, numeros=[c.numero for c in corr3b], sufixo="-3b")}
{detalhes("Primeira leitura dos inéditos (roadmap §2.1)", md_doc_para_html(leitura_ined))}
{detalhes("Sonda de detecção de correção (roadmap §3)", md_doc_para_html(sonda))}
{fontes(["<code>resultados_alvo/fase3b_ineditos/resumo_fase3.json</code> (corrida 2, 28/09) e <code>fase3b_ineditos_coder7b/</code> (corrida 7, 06/10)", "<code>resultados_alvo/fase3b_a5/</code> (corrida 5, 06/10)", "<code>decisao_modelo.json</code> (pontes de versão: " + ", ".join(p["saida"] for p in pontes) + ")", "<code>resultados_alvo/fase3/analise_fase3b.json</code> (72 casos somados, variação entre corridas, modelo contra modelo e adesão cega)", "<code>roadmap.md</code> §2, §2.1, §2.3 e §3", "achados 4.37, 4.43 e 4.44; relatório <code>fase-3b-relatorio.md</code>"])}
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
# ! Alteração de IA - Revisar: (01/10/2026) a lista ganhou a rodada 5 (Pré-Fase 4), os rótulos deixaram de usar
# travessão e o arquivo do mapa de filtros passou a ter nome próprio; a leitura de um mapa adotado, adiado,
# descartado saiu de dentro de secao_pesquisa para _mapa_de_vereditos, que as abas Pesquisa e "Modelos grandes pelo
# disco" usam; _secoes_do_levantamento e _pre_fase4_no_levantamento leem as sínteses e os mapas do §6.14.
# ! Motivo: secao_pesquisa lia o mapa de filtros de RODADAS[-1], "o último levantamento da lista"; com a rodada 5 no
# fim da lista ela procuraria o §6.13.10 no arquivo errado e a geração do painel pararia com ValueError. O mapa de
# filtros é o da rodada 4; o da rodada 5 (viabilidade) e as sínteses dela vão para a aba do colibri, porque é por
# ela que o Eric lê a análise que pediu em 01/10.
LEVANTAMENTO_FILTROS = "levantamento-2026-09-29-documentacao-autogerida.md"
LEVANTAMENTO_PRE_FASE4 = "levantamento-2026-10-01-pre-fase-4.md"
RODADAS = [
    ("levantamento-2026-09-11-fase-3.md", "Rodadas 1 e 2 (11 e 23/09): Fase 3", "Fase 3"),
    ("levantamento-2026-09-22-llms-locais.md", "Rodada 3 (22/09): LLMs locais", "LLMs locais"),
    (LEVANTAMENTO_FILTROS, "Rodada 4 (29/09): documentação autogerida", "documentação autogerida"),
    (LEVANTAMENTO_PRE_FASE4, "Rodada 5 (01/10): Pré-Fase 4", "Pré-Fase 4"),
]
_POR_EXTENSO = {4: "Quatro", 5: "Cinco", 6: "Seis", 7: "Sete"}


def _veredito(celula: str) -> str:
    v = re.sub(r"[*`_]", "", celula).strip().lower()  # a coluna vem em negrito no Markdown (**adotado**)
    return "adotado" if v.startswith("adot") else "adiado" if v.startswith("adia") else "descartado" if v.startswith("desc") else "outro"


def _mapa_de_vereditos(trecho: str, id_tabela: str, rotulo: str) -> tuple[str, Counter, int]:
    """A primeira tabela Tema, Opção, Veredito, Motivo, Fonte do trecho, com os botões de filtro por veredito.
    Devolve o HTML, a contagem por veredito e o número de linhas."""
    cab, linhas, _ = pt.primeira_tabela(trecho)
    col = {c: i for i, c in enumerate(cab)}
    cont = Counter(_veredito(r[col["Veredito"]]) for r in linhas)
    trs = []
    for r in linhas:
        v = _veredito(r[col["Veredito"]])
        trs.append(f'<tr data-valor="{v}"><td>{pt.inline(r[col["Tema"]])}</td><td>{pt.inline(r[col["Opção"]])}</td>'
                   f'<td>{chip(v, v)}</td><td>{pt.inline(r[col["Motivo"]])}</td><td class="nota">{pt.inline(r[col.get("Fonte", len(cab) - 1)])}</td></tr>')
    mapa = (f'<div class="filtros filtro-tabela" data-alvo="{id_tabela}" role="group" aria-label="{rotulo}">'
            f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(linhas)})</button>'
            + "".join(f'<button type="button" data-valor="{v}" aria-pressed="false">{v.capitalize()} ({cont[v]})</button>' for v in ("adotado", "adiado", "descartado") if cont[v])
            + f'</div><div class="tabela" id="{id_tabela}"><table><thead><tr><th>Tema</th><th>Opção</th><th>Veredito</th><th>Motivo</th><th>Fonte</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    return mapa, cont, len(linhas)


def _secoes_do_levantamento(lev: str) -> list[dict]:
    """As subseções de tópico de um levantamento: número, título, chave, contagens, texto da síntese, implicações
    e lacunas (o que vem sob cada título de nível 5)."""
    saida = []
    for parte in re.split(r"(?m)^(?=#### )", lev.replace("\r\n", "\n")):
        linhas = parte.split("\n")
        m = _TOPICO.match(linhas[0])
        if not m:
            continue
        blocos: dict[str, list[str]] = {}
        atual = None
        for l in linhas[1:]:
            mh = re.match(r"^##### (.+?)\s*$", l)
            if mh:
                atual = mh.group(1)
                blocos[atual] = []
            elif atual:
                blocos[atual].append(l)
        implicacoes = next((v for k, v in blocos.items() if k.startswith("Implicações")), [])
        saida.append({"secao": m.group(1), "titulo": m.group(2), "chave": m.group(3), "aprovadas": int(m.group(4)), "rejeitadas": int(m.group(5)),
                      "nao_verificadas": int(m.group(6) or 0), "texto": "\n".join(blocos.get("Texto", [])).strip(),
                      "implicacoes": [l[2:] for l in implicacoes if l.startswith("* ")],
                      "lacunas": [l[2:] for l in blocos.get("Lacunas", []) if l.startswith("* ")]})
    return saida


def _pre_fase4_no_levantamento(lev: str | None) -> dict | None:
    """Do levantamento da Pré-Fase 4 (§6.14): as subseções já integradas, as chaves dos tópicos da parte A, quantos
    tópicos ainda não rodaram e o trecho dos mapas (§6.14.13)."""
    if not lev or "#### 6.14.13" not in lev:
        return None
    lev = lev.replace("\r\n", "\n")
    cab, linhas, _ = pt.primeira_tabela(lev)  # a primeira tabela do arquivo é a das subseções, com a parte de cada tópico
    col = {c: i for i, c in enumerate(cab)}
    parte_a = {re.sub(r"[`*]", "", r[col["Tópico"]]).strip() for r in linhas if r[col["Parte"]].strip() == "A"}
    faltam = sum(1 for r in linhas if "ainda não rodou" in r[col["Aprovadas"]])
    # ! Alteração de IA - Revisar: (05/10/2026) além do aviso "O que mudou", a aba recebe os avisos do cabeçalho sobre a
    # memória da máquina e sobre as correções da revisão, quando existem no arquivo.
    # ! Motivo: as sínteses mostradas na aba passaram a ser as corrigidas depois da revisão de 01/10; sem os avisos o
    # leitor não saberia que o texto foi corrigido, nem que "15,69 GB" é a RAM que o Windows enxerga (a instalada é 16 GB).
    avisos = [m.group(1) for titulo in ("O que mudou depois de a parte A ser escrita", "Memória da máquina", "Correções da revisão")
              for m in [re.search(r"^\d+\. (\*\*" + re.escape(titulo) + r"\.\*\* .*)$", lev, re.M)] if m]
    return {"secoes": _secoes_do_levantamento(lev), "parte_a": parte_a, "faltam": faltam, "mapas": lev[lev.index("#### 6.14.13"):],
            "mudou": re.search(r"^\d+\. (\*\*O que mudou depois de a parte A ser escrita\.\*\* .*)$", lev, re.M), "avisos": avisos}


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
    r4 = (PESQUISA / LEVANTAMENTO_FILTROS).read_text(encoding="utf-8")
    mapa, cont, n_filtros = _mapa_de_vereditos(r4[r4.index("#### 6.13.10"):], "tab-mapa", "Filtro do mapa")
    # rodada 5 (Pré-Fase 4): o que já foi integrado e o que ainda não rodou
    r5 = _pre_fase4_no_levantamento((PESQUISA / LEVANTAMENTO_PRE_FASE4).read_text(encoding="utf-8"))
    do_r5 = [t for t in topicos if t["curto"] == "Pré-Fase 4"]
    falta_r5 = r5["faltam"] if r5 else 0
    frase_r5 = (f' A rodada 5 (01/10) é a da Pré-Fase 4: {len(do_r5)} tópicos integrados, com {sum(t["aprovadas"] for t in do_r5)} afirmações aprovadas'
                + (f', e {falta_r5} tópicos do raciocínio aberto ainda por rodar' if falta_r5 else '')
                + '; o mapa de viabilidade e as sínteses dela estão na aba <a href="#colibri" data-ir="colibri|">Modelos grandes pelo disco</a>.') if do_r5 else ""
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
        ("Filtros para a documentação autogerida", f'{cont["adotado"]} adotados', f'{cont["adiado"]} adiados · {cont["descartado"]} descartados (rodada 4, ficha 16)'),
    ]
    n_rodadas = len(RODADAS) + 1  # o primeiro arquivo guarda as rodadas 1 e 2
    html_ = f'''<section id="pesquisa" hidden>
<h1>Pesquisa bibliográfica: o que a literatura diz e o que entrou no projeto</h1>
<p class="lead">{_POR_EXTENSO.get(n_rodadas, str(n_rodadas))} rodadas de levantamento, cada tópico pesquisado por um agente, cada afirmação verificada por outro agente cético contra a fonte, e a síntese integrada ao Memorial (§6.9 a §6.14) com as referências no padrão ABNT. A rodada 4 (29/09) respondeu ao pedido do Eric sobre como melhorar a documentação autogerida e evitar alucinação: {len([t for t in topicos if t["rodada"].startswith("Rodada 4")])} tópicos, {sum(t["aprovadas"] for t in topicos if t["rodada"].startswith("Rodada 4"))} afirmações aprovadas e um mapa de {n_filtros} filtros, dos quais {cont["adotado"]} entram como candidatos ao plano da Fase 4 (ficha 16).{frase_r5}</p>
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
    "Rodada 5 abriu a Pré-Fase 4: rodar modelo grande lendo os pesos do disco, as pesquisas em que o colibri se apoia, modelos MoE pequenos em CPU e o atlas de especialistas."
    + (f" Os {falta_r5} tópicos sobre o raciocínio aberto ainda não rodaram." if falta_r5 else " Os tópicos sobre o raciocínio aberto também estão integrados."),
])}
{fontes(["<code>2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md</code>, <code>-22-llms-locais.md</code>, <code>-29-documentacao-autogerida.md</code>, <code>levantamento-2026-10-01-pre-fase-4.md</code>", "<code>mapa-de-decisoes-fase-3.md</code>, <code>fichamento-referencias-projeto.md</code>, <code>referencias.md</code>"])}
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


# ------------------------------------------------------------------ 8. troca cruzada

# ! Alteração de IA - Revisar: aba nova (01/10/2026) com a troca cruzada da Fase 3-B: a biblioteca escrita pelo
# qwen2.5:7b lida pelos dois Coder. Tudo vem de `resultados_alvo/fase3/analise_fase3b.json` (analisar_fase3b.py).
# ! Motivo: era a última corrida prevista da 3-B e a que responde se o ganho da Fase 3 é da biblioteca ou de quem a
# lê; pela regra do painel, toda análise nova ganha aba (pergunta, resposta, números-chave, gráficos, leitura, fontes).
NOME_CURTO = {"qwen2.5:7b": "qwen2.5:7b", "qwen2.5-coder:7b": "Coder 7B", "qwen2.5-coder:3b": "Coder 3B"}
NOME_CONTRA = {"l0_ponte": "o próprio L0 na ponte (mesma versão do Ollama)", "propria": "a própria biblioteca na Fase 3",
               "doador": "o doador lendo a mesma biblioteca (Fase 3)"}


def _saldo_txt(b: int, c: int) -> str:
    s = b - c
    if s == 0:
        return "saldo zero"
    return f'{abs(s)} caso{"s" if abs(s) != 1 else ""} {"a mais" if s > 0 else "a menos"}'


def secao_cruzada(an: dict, road: dict, cartoes_corridas) -> tuple[dict, str]:
    cz, meta = an["cruzada"], an["metadados"]
    doador, leitores = meta["doador"], meta["leitores"]
    nome = lambda m: NOME_CURTO.get(m, m)  # noqa: E731
    cel = {(c["leitor"], c["origem"], c["biblioteca_epoca"]): c for c in cz["celulas"]}
    par = {(p["leitor"], p["biblioteca_epoca"], p["contra"]): p for p in cz["pareados"]}
    rot = {(r["leitor"], r["biblioteca"]): r for r in cz["rotulos"]}
    agr = {(l["modelo"], l["biblioteca_epoca"]): l for l in an["ineditos"]["agrupado"]}
    ponto = lambda c: {"acerto": c["acerto_pct"], "bal": c["acuracia_balanceada_pct"]}  # noqa: E731
    versoes = ["0", "1", "3"]
    doador_lido = {m: {"0": ponto(cel[(m, "ponte", 0)]), "1": ponto(cel[(m, "cruzada", 1)]), "3": ponto(cel[(m, "cruzada", 3)])} for m in leitores}
    propria = {m: {v: ponto(cel[(m, "fase3", int(v))]) for v in versoes} for m in [doador] + leitores}
    # rótulos curtos: o eixo do gráfico corta o começo de um rótulo comprido
    trocas = [{"leitor": doador, "epoca": e, "rot": f"{nome(doador)} · própria L{e}", "b": agr[(doador, e)]["oficiais"]["b"], "c": agr[(doador, e)]["oficiais"]["c"]}
              for e in (1, 3) if (doador, e) in agr]
    trocas += [{"leitor": m, "epoca": e, "rot": f"{nome(m)} · L{e} do doador", "b": par[(m, e, "l0_ponte")]["b"], "c": par[(m, e, "l0_ponte")]["c"]} for m in leitores for e in (1, 3)]
    dados_js = {"doador": doador, "leitores": leitores, "versoes": versoes, "doador_lido": doador_lido, "propria": propria, "trocas": trocas}

    q1 = cel[(doador, "fase3", 1)]
    versao = meta["versao_da_ponte_de_base"]
    frases = [f'{nome(m)}: {fmt(cel[(m, "ponte", 0)]["acerto_pct"])}% com a biblioteca original e {fmt(cel[(m, "cruzada", 1)]["acerto_pct"])}% com a L1 do {nome(doador)} '
              f'({_saldo_txt(par[(m, 1, "l0_ponte")]["b"], par[(m, 1, "l0_ponte")]["c"])})' for m in leitores]
    pior = min(leitores, key=lambda m: par[(m, 1, "l0_ponte")]["b"] - par[(m, 1, "l0_ponte")]["c"])
    r_pior = rot[(pior, "L1 do doador")]
    ruido = an["ruido_l0"]
    itens_kpi = [(f"{nome(m)} com a L1 do {nome(doador)}", f'{fmt(cel[(m, "ponte", 0)]["acerto_pct"])}% → {fmt(cel[(m, "cruzada", 1)]["acerto_pct"])}%',
                  f'b/c {par[(m, 1, "l0_ponte")]["b"]}/{par[(m, 1, "l0_ponte")]["c"]} contra o próprio L0, p = {fmt(par[(m, 1, "l0_ponte")]["p_mcnemar"], 3)}') for m in leitores]
    itens_kpi += [
        ("A mesma L1 lida por quem a escreveu", f'{fmt(q1["acerto_pct"])}%', "; ".join(f'{nome(m)} b/c {par[(m, 1, "doador")]["b"]}/{par[(m, 1, "doador")]["c"]} contra ele' for m in leitores)),
        (f"Rótulo que o {nome(pior)} passa a dar", f'{r_pior["respostas_no_rotulo_com_l0"]} → {r_pior["respostas_no_rotulo"]} respostas',
         f'{r_pior["rotulo_mais_frequente"]}; ' + ("nenhum dos 36 casos tem essa causa" if r_pior["casos_com_esse_gabarito"] == 0 else f'{r_pior["casos_com_esse_gabarito"]} dos 36 casos têm essa causa')),
        ("Contextos com nota do doador", f'{fmt(cel[(pior, "cruzada", 1)]["contexto_com_nota_pct"])}%',
         "com a própria L1: " + "; ".join(f'{nome(m)} {fmt(cel[(m, "fase3", 1)]["contexto_com_nota_pct"])}%' for m in leitores)),
        ("Variação entre corridas iguais", f'{min(x["discordantes_mesma_entrada"] for x in ruido)} a {max(x["discordantes_mesma_entrada"] for x in ruido)} casos',
         f'em 36, com a mesma entrada e saldo de até {max(abs(x["b_mesma_entrada"] - x["c_mesma_entrada"]) for x in ruido)}; régua para ler os saldos acima'),
    ]
    linhas_par = "".join(
        f'<tr data-valor="{p["contra"]}"><td>{esc(nome(p["leitor"]))} lendo L{p["biblioteca_epoca"]}</td><td>{esc(NOME_CONTRA[p["contra"]])}</td>'
        f'<td>{"sim" if p["pareavel_pela_ponte"] else "não"}</td><td class=num>{p["b"]} / {p["c"]}</td>'
        f'<td class=num>{pp(p["delta_pp"])}</td><td class=num>{fmt(p["p_mcnemar"], 3)}</td><td class=num>{p["b_mesma_entrada"]} / {p["c_mesma_entrada"]}</td><td class=num>{p["rotulos_diferentes"]}</td></tr>'
        for p in cz["pareados"])
    cont = Counter(p["contra"] for p in cz["pareados"])
    tab_par = ('<div class="filtros filtro-tabela" data-alvo="tab-cz-par" role="group" aria-label="Filtro dos pareamentos">'
               f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(cz["pareados"])})</button>'
               + "".join(f'<button type="button" data-valor="{k}" aria-pressed="false">Contra {esc(NOME_CONTRA[k])} ({cont[k]})</button>' for k in NOME_CONTRA if cont[k])
               + '</div><div class="tabela" id="tab-cz-par"><table><thead><tr><th>Leitor e biblioteca do doador</th><th>Comparado com</th><th>Pareável pela ponte</th>'
               f'<th>b / c</th><th>Diferença</th><th>p (McNemar exato)</th><th>b / c sem o caso de texto corrigido</th><th>Rótulos que mudaram</th></tr></thead><tbody>{linhas_par}</tbody></table></div>')
    # as listas de casos de cada pareamento ficam num bloco recolhido: na tabela principal elas a deixavam larga demais
    tab_par_casos = tabela(["Leitor e biblioteca do doador", "Comparado com", "Ganhou", "Perdeu", "Trocas em casos que já oscilam entre corridas de L0"],
                           [[f'{nome(p["leitor"])} lendo L{p["biblioteca_epoca"]}', NOME_CONTRA[p["contra"]], ", ".join(p["ganhos"]) or "nenhum", ", ".join(p["perdas"]) or "nenhum",
                             (", ".join(p["em_casos_que_oscilam"]) or "nenhuma") if p["contra"] == "l0_ponte" else "—"] for p in cz["pareados"]])
    classes = list(dict.fromkeys(l["classe"] for l in cz["por_classe"]))
    por_classe = {(l["leitor"], l["biblioteca"], l["classe"]): l for l in cz["por_classe"]}
    tab_classe = tabela(["Quem lê", "Biblioteca lida"] + classes,
                        [[nome(m), b] + [f'{por_classe[(m, b, c)]["acertos"]} / {por_classe[(m, b, c)]["n"]}' if (m, b, c) in por_classe else "—" for c in classes]
                         for m, b in dict.fromkeys((l["leitor"], l["biblioteca"]) for l in cz["por_classe"])])
    tab_celulas = tabela(["Quem lê", "Biblioteca lida", "Acerto nos 36", "IC 95%", "Acurácia balanceada", "Contexto com nota", "Citou verbete anotado", "Tokens de entrada", "s por diagnóstico"],
                         [[nome(c["leitor"]), c["biblioteca"], f'{fmt(c["acerto_pct"])}%', f'{fmt(c["ic95"][0])} a {fmt(c["ic95"][1])}', f'{fmt(c["acuracia_balanceada_pct"])}%',
                           f'{fmt(c["contexto_com_nota_pct"])}%', f'{fmt(c["citou_verbete_anotado_pct"])}%', fmt(c["tokens_entrada_mediana"], 0), fmt(c["segundos_mediana"])] for c in cz["celulas"]])
    tab_rot = tabela(["Quem lê", "Biblioteca lida", "Rótulo mais respondido", "Respostas com ele", "Com L0", "Casos com essa causa", "Verbetes mais citados como fonte", "Verbetes mais presentes no contexto"],
                     [[nome(r["leitor"]), r["biblioteca"], r["rotulo_mais_frequente"], f'{r["respostas_no_rotulo"]} ({fmt(r["parcela_rotulo_pct"])}%)', r["respostas_no_rotulo_com_l0"], r["casos_com_esse_gabarito"],
                       "; ".join(f'{x["verbete"]} ({x["respostas"]})' for x in r["fontes_mais_citadas"]), "; ".join(f'{x["verbete"]} ({x["casos"]})' for x in r["verbetes_mais_presentes"])] for r in cz["rotulos"]])
    tab_casos = tabela(["Quem lê", "Biblioteca", "Caso", "Passou a", "Causa do gabarito", "Resposta com L0", "Resposta com a biblioteca do doador", "Fonte citada", "Verbete de ouro no contexto", "O doador acerta"],
                       [[nome(c["leitor"]), f'L{c["biblioteca_epoca"]}', c["caso"], c["mudou_para"], c["esperado"], c["resposta_l0"], c["resposta"], ", ".join(c["fontes_citadas"]) or "—",
                         "sim" if c["ouro_no_contexto"] else "não", "sim" if c["doador_acertou"] else "não"] for c in cz["casos"]])
    perdas_pior = [c for c in cz["casos"] if c["leitor"] == pior and c["biblioteca_epoca"] == 1 and c["mudou_para"] == "errado"]
    no_rotulo = sum(1 for c in perdas_pior if c["resposta"] == r_pior["rotulo_mais_frequente"])
    com_ouro = sum(1 for c in perdas_pior if c["ouro_no_contexto"])
    fonte_top = r_pior["fontes_mais_citadas"][0] if r_pior["fontes_mais_citadas"] else None
    melhor = max(leitores, key=lambda m: par[(m, 1, "l0_ponte")]["b"] - par[(m, 1, "l0_ponte")]["c"])
    itens_leitura = [
        f'<strong>O ganho não é da biblioteca sozinha.</strong> Lida por quem a escreveu, a L1 rende {fmt(q1["acerto_pct"])}%; lida pelo {esc(nome(melhor))}, fica com {_saldo_txt(par[(melhor, 1, "l0_ponte")]["b"], par[(melhor, 1, "l0_ponte")]["c"])} '
        f'sobre o próprio L0, dentro da variação entre corridas ({len(par[(melhor, 1, "l0_ponte")]["em_casos_que_oscilam"])} das {par[(melhor, 1, "l0_ponte")]["b"] + par[(melhor, 1, "l0_ponte")]["c"]} trocas caem em casos que já '
        f'oscilam sozinhos); lida pelo {esc(nome(pior))}, fica com {_saldo_txt(par[(pior, 1, "l0_ponte")]["b"], par[(pior, 1, "l0_ponte")]["c"])}, o único saldo fora dessa variação, ainda sem significância.',
        f'<strong>No {esc(nome(pior))} as notas do doador são lidas e seguidas, para pior.</strong> Ele passa a responder <code>{esc(r_pior["rotulo_mais_frequente"])}</code> ({r_pior["respostas_no_rotulo_com_l0"]} respostas com L0, {r_pior["respostas_no_rotulo"]} com a biblioteca do doador), '
        + ("causa que nenhum dos 36 casos tem" if r_pior["casos_com_esse_gabarito"] == 0 else f'causa de {r_pior["casos_com_esse_gabarito"]} dos 36 casos') + (f', citando <code>{esc(fonte_top["verbete"])}</code> como fonte em {fonte_top["respostas"]} respostas' if fonte_top else "") +
        f'. Em {no_rotulo} das {len(perdas_pior)} perdas a resposta nova é esse rótulo, e em {com_ouro} das {len(perdas_pior)} o verbete de ouro estava no contexto: nessas, a falha é de uso, não de busca. '
        f'Em rótulos, {par[(pior, 1, "l0_ponte")]["rotulos_diferentes"]} das 36 respostas mudam; entre corridas iguais dele mudam de {min(x["rotulos_diferentes"] for x in ruido if x["modelo"] == pior)} a '
        f'{max(x["rotulos_diferentes"] for x in ruido if x["modelo"] == pior)}.',
        f'<strong>O que a cruzada não separa.</strong> O ganho medido na Fase 3 não acompanha a biblioteca quando muda quem a lê, mas o {esc(nome(doador))} não leu a biblioteca de outro modelo: não dá para dizer se o ganho é '
        "do par (o modelo com a biblioteca que ele mesmo escreveu) ou do leitor. E o ganho dele com a própria L1 (4 casos) também não alcança significância.",
        f'<strong>O que fica para a Fase 4.</strong> O padrão do agente é o {esc(nome(doador))} com a biblioteca que ele mesmo escreveu (decisão 69): trocar o modelo que lê exige medir de novo, e a ideia de escrever com o melhor '
        "modelo e ler com o mais barato sai. Uma nota em verbete que aparece em quase metade dos contextos alcança quase metade dos diagnósticos.",
    ]
    numeros = [c.numero for c in road["corridas"] if c.saida in (meta["fontes"]["cruzada"], meta["ponte_de_base"])]
    html_ = f'''<section id="cruzada" hidden>
<h1>Troca cruzada: o ganho é da biblioteca ou de quem a lê?</h1>
<p class="lead">Não é da biblioteca sozinha. Os dois Coder diagnosticaram os mesmos 36 casos, com o mesmo prompt e a mesma busca, lendo a biblioteca escrita pelo {esc(nome(doador))}. {esc("; ".join(frases))}. Lida por quem a escreveu, a mesma L1 rende {fmt(q1["acerto_pct"])}%. O ganho medido na Fase 3 não acompanha a biblioteca quando muda quem a lê.</p>
{kpis(itens_kpi)}
<h2>Acerto por versão da biblioteca, por quem lê</h2>
<p>Linha cheia: a biblioteca escrita pelo {esc(nome(doador))} (no ponto L0, a biblioteca original; para os dois Coder, medida na ponte em Ollama {esc(versao)}). Linha tracejada: cada Coder lendo a biblioteca que ele mesmo escreveu, na Fase 3. Se o ganho fosse da biblioteca, as linhas cheias subiriam juntas.</p>
<div class="controles"><label>Métrica <select id="sel-cz-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-cz-leit"></canvas></div>
<h2>Casos ganhos e perdidos contra o próprio L0</h2>
<p>Cada barra compara um modelo com uma versão da biblioteca contra ele mesmo com a biblioteca original: à direita os casos que passou a acertar, à esquerda os que deixou de acertar. Os dois Coder são comparados na mesma versão do Ollama (ponte de 30/09); o {esc(nome(doador))}, dentro da Fase 3.</p>
<div class="chart"><canvas id="g-cz-trocas"></canvas></div>
<h2>Os pareamentos, um a um</h2>
<p>b conta os casos que só o leitor com a biblioteca do doador acertou; c, os que só o outro lado acertou. Só a comparação contra a ponte é feita na mesma versão do Ollama e com o mesmo texto dos casos; as outras duas cruzam versões e, para o Coder 7B, não são pareáveis (decisão 47). Nelas, a coluna "sem o caso de texto corrigido" tira o efe-3, corrigido em 28/09.</p>
{tab_par}
{detalhes("Casos ganhos e perdidos em cada pareamento", tab_par_casos)}
<h2>Leitura</h2>
{leitura(itens_leitura)}
{detalhes("Todas as células: quem lê, o que lê e quanto acerta", tab_celulas)}
{detalhes("Acertos por classe de defeito (6 casos por classe)", tab_classe)}
{detalhes("Rótulo mais respondido e verbetes citados", tab_rot)}
{detalhes("Casos que mudaram contra o próprio L0, um a um", tab_casos)}
<h2>As corridas</h2>
{cartoes_corridas(road, numeros=numeros, sufixo="-cz")}
{fontes(["<code>resultados_alvo/fase3/analise_fase3b.json</code> e <code>.md</code>, gerados por <code>analisar_fase3b.py</code> (--check)", "<code>resultados_alvo/fase3b_cruzada_qwen/</code> e <code>fase3b_ponte_0344/</code>", "relatório <code>fase-3b-relatorio.md</code> §5 e §6", "achados 4.42 e 4.43; decisão 69"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 9. fechamento das Fases 3 e 3-B

# ! Alteração de IA - Revisar: aba nova (01/10/2026) com a lista de fechamento das Fases 3 e 3-B, lida da tabela do
# §9 de `3-resultados-e-analises/fase-3b-relatorio.md`, e com as fichas de pendência que continuam abertas.
# ! Motivo: o Eric pediu a verificação de que todos os tópicos das duas fases podem ser dados por concluídos antes de
# passar o planejamento da Fase 4; ele decide pelo painel, e a resposta precisa estar numa tela só, tópico por tópico.
ESTADOS_FECHAMENTO = {"concluido": ("Concluído", "concluida"), "ressalva": ("Concluído com ressalva", "andamento"),
                      "nao_rodado": ("Não rodado", "opcional"), "descartado": ("Descartado", "descartado"), "outro": ("Em aberto", "outro")}


def _classe_fechamento(estado: str) -> str:
    e = estado.strip().lower()
    if "ressalva" in e:
        return "ressalva"
    if e.startswith("conclu"):
        return "concluido"
    if e.startswith("não rodado") or e.startswith("nao rodado"):
        return "nao_rodado"
    if e.startswith("descartado"):
        return "descartado"
    return "outro"


def secao_fechamento(relatorio_md: str, pend: list, md_doc_para_html) -> tuple[dict, str]:
    md = pt.sem_comentarios(relatorio_md)
    secs = {t.split(".")[0]: c for t, c in pt.secoes(md) if t and t[0].isdigit()}
    cab, linhas, _ = pt.primeira_tabela(secs["9"])
    col = {c: i for i, c in enumerate(cab)}
    cont = Counter(_classe_fechamento(r[col["Estado"]]) for r in linhas)
    abertas = [f for b in pend for f in b.fichas if f.aberta]
    trs = "".join(
        f'<tr data-valor="{_classe_fechamento(r[col["Estado"]])}"><td class=num>{esc(r[col["#"]])}</td><td>{pt.inline(r[col["Tópico"]])}</td><td>{esc(r[col["Fase"]])}</td>'
        f'<td>{chip(ESTADOS_FECHAMENTO[_classe_fechamento(r[col["Estado"]])][1], r[col["Estado"]])}</td><td>{pt.inline(r[col["Evidência"]])}</td><td>{pt.inline(r[col["O que fica"]])}</td></tr>'
        for r in linhas)
    tab = ('<div class="filtros filtro-tabela" data-alvo="tab-fechamento" role="group" aria-label="Filtro do fechamento">'
           f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(linhas)})</button>'
           + "".join(f'<button type="button" data-valor="{k}" aria-pressed="false">{esc(ESTADOS_FECHAMENTO[k][0])} ({cont[k]})</button>' for k in ESTADOS_FECHAMENTO if cont[k])
           + '</div><div class="tabela" id="tab-fechamento"><table><thead><tr><th>#</th><th>Tópico</th><th>Fase</th><th>Estado</th><th>Evidência</th><th>O que fica</th></tr></thead>'
           f'<tbody>{trs}</tbody></table></div>')
    fechado = cont["outro"] == 0
    resposta = ("Sim. Nenhum tópico obrigatório está aberto." if fechado else f'Ainda não: {cont["outro"]} tópico(s) em aberto.')
    lista = "".join(f'<li><a href="#{f.id_html}" data-ir="pendencias|{f.id_html}"><span class="numero">{f.numero}</span> {pt.inline(f.titulo)}</a>'
                    f'<br><span class="nota">Recomendação: {pt.inline(f.campos.get("Recomendação", "—"))}</span></li>' for f in abertas)
    itens_kpi = [
        ("Concluídos", str(cont["concluido"]), f"de {len(linhas)} tópicos"),
        ("Concluídos com ressalva", str(cont["ressalva"]), "a ressalva está na coluna O que fica"),
        ("Não rodados", str(cont["nao_rodado"]), "corridas opcionais ou inviáveis; o motivo está na tabela"),
        ("Descartados com motivo", str(cont["descartado"]), "registrados para o texto final"),
        ("Decisões do Eric em aberto", str(len(abertas)), "fichas na aba Pendências; não impedem o planejamento da Fase 4" if abertas else "nenhuma ficha aberta"),
    ]
    html_ = f'''<section id="fechamento" hidden>
<h1>Fechamento: as Fases 3 e 3-B podem ser dadas por concluídas?</h1>
<p class="lead">{esc(resposta)} Dos {len(linhas)} tópicos, {cont["concluido"]} estão concluídos, {cont["ressalva"]} concluídos com ressalva declarada, {cont["nao_rodado"]} não rodaram (corridas opcionais ou inviáveis) e {cont["descartado"]} {"foi descartado" if cont["descartado"] == 1 else "foram descartados"} com motivo. {"Faltam " + str(len(abertas)) + " decisões do Eric, que não impedem o planejamento da Fase 4." if abertas else "Não há decisão pendente."}</p>
{kpis(itens_kpi)}
<h2>O que depende do Eric</h2>
{"<ol class='lista-eric'>" + lista + "</ol>" if abertas else "<p>Nenhuma ficha aberta.</p>"}
<h2>Tópico por tópico</h2>
{tab}
{detalhes("O que muda e o que não muda com a Fase 3-B (relatório §7)", md_doc_para_html(secs.get("7", "")))}
{detalhes("O que a literatura previa e o que saiu (relatório §6)", md_doc_para_html(secs.get("6", "")))}
{detalhes("Limitações que ficam (relatório §8)", md_doc_para_html(secs.get("8", "")))}
{fontes(["<code>3-resultados-e-analises/fase-3b-relatorio.md</code> §6 a §9", "<code>pendencias.md</code> (fichas abertas)", "<code>roadmap.md</code>"])}
</section>'''
    return {"contagem": dict(cont), "fichas_abertas": len(abertas), "fechado": fechado}, html_


# ------------------------------------------------------------------ 10. Pré-Fase 4: modelos grandes pelo disco

# ! Alteração de IA - Revisar: aba nova (01/10/2026) da Pré-Fase 4: a conta de viabilidade do repositório colibri nesta
# máquina, a leitura medida do NVMe e a amostra de probabilidades por token do Ollama.
# ! Motivo: o Eric pediu a viabilidade de rodar modelo grande lendo os pesos do disco, só com CPU, com ganhos e custos, e
# a regra do painel é uma aba por análise. Todo número vem de resultados_alvo/pre_fase4/viabilidade_modelos_grandes.json
# (gerado por viabilidade_modelos_grandes.py, com --check) e da amostra gravada por sondar_logprobs.py; a comparação de
# tempos mistura duas grandezas de propósito e diz isso no gráfico: o tempo de hoje é o do diagnóstico inteiro, e o do
# colibri é só o da geração da resposta, porque o repositório não mede a leitura do prompt em máquina pequena.

def _milhar(v) -> str:
    return f"{float(v):,.0f}".replace(",", ".")


def _amostra_de_tokens(amostra: dict | None) -> dict | None:
    """Da amostra de sondar_logprobs.py: os tokens da primeira linha da resposta, com a probabilidade de cada um, e as
    alternativas no ponto em que o modelo escolhe a causa (o primeiro token depois de 'CAUSA_RAIZ:')."""
    lp = ((((amostra or {}).get("chamadas") or {}).get("a") or {}).get("resposta") or {}).get("logprobs") or []
    if not lp:
        return None
    linha, acumulado, i_rotulo = [], "", None
    for i, t in enumerate(lp):
        if i_rotulo is None and re.search(r"CAUSA_RAIZ\s*:\s*$", acumulado) and t["token"].strip():
            i_rotulo = i
        linha.append({"token": t["token"], "p": math.exp(t["logprob"])})
        acumulado += t["token"]
        if "\n" in t["token"]:
            break
    alternativas = ([{"token": a["token"], "p": math.exp(a["logprob"])} for a in (lp[i_rotulo].get("top_logprobs") or [])[:5]]
                    if i_rotulo is not None else [])
    return {"linha": linha, "alternativas": alternativas, "rotulo": acumulado.split(":", 1)[1].strip() if ":" in acumulado else ""}


# ! Alteração de IA - Revisar: (01/10/2026) bloco "O que a literatura sustenta" da aba do colibri, lido do levantamento
# §6.14: o mapa adotado, adiado, descartado da parte A com filtro por veredito, os riscos, a leitura do mapa e as
# sínteses verificadas por extenso, recolhidas.
# ! Motivo: o Eric pediu "uma análise densa do conteúdo e das pesquisas que ele se baseia" com ganhos e custos, e
# decide pelo painel, não pelo arquivo .md; sem este bloco a análise ficaria só no levantamento. Nada é digitado aqui:
# o texto vem do arquivo gerado por integrar_pesquisa_pre_fase4.py, inclusive o aviso do que mudou depois de a parte A
# ser escrita (a sonda de probabilidades e a decisão do Eric sobre a telemetria).
def _literatura_do_colibri(lev: str | None) -> tuple[str, list[tuple[str, str, str]], str | None]:
    """Devolve o HTML do bloco, os cartões de número-chave que ele acrescenta e a linha de fonte."""
    lit = _pre_fase4_no_levantamento(lev)
    if not lit:
        return ('<p class="nota">A rodada 5 da pesquisa (o repositório por inteiro, as pesquisas que ele cita, inferência com os pesos fora da RAM, modelos MoE '
                'pequenos e atlas de especialistas) ainda não foi integrada ao levantamento, como §6.14.</p>'), [], None
    mapa, cont, n = _mapa_de_vereditos(lit["mapas"], "tab-mapa-co", "Filtro do mapa de viabilidade")
    _, riscos, _ = pt.primeira_tabela(lit["mapas"][lit["mapas"].index("**Riscos**"):])
    tab_riscos = ('<div class="tabela"><table><thead><tr><th>Risco</th><th>Mitigação</th><th>Fonte</th></tr></thead><tbody>'
                  + "".join(f'<tr data-risco="{i}"><td>{pt.inline(r[0])}</td><td>{pt.inline(r[1])}</td><td class="nota">{pt.inline(r[2])}</td></tr>' for i, r in enumerate(riscos, 1))
                  + "</tbody></table></div>")
    resto = lit["mapas"][lit["mapas"].index("**Leitura**") + len("**Leitura**"):]
    fim = resto.find("\n**Parte ")
    leitura_do_mapa = pt.md_doc_para_html((resto if fim < 0 else resto[:fim]).strip())
    secoes = [s for s in lit["secoes"] if s["chave"] in lit["parte_a"]]
    aprovadas, rejeitadas = sum(s["aprovadas"] for s in secoes), sum(s["rejeitadas"] for s in secoes)
    sinteses = "".join(
        f'<details data-sintese="{html.escape(s["chave"], quote=True)}"><summary>§{s["secao"]} {esc(s["titulo"])} ({s["aprovadas"]} afirmações aprovadas)</summary>'
        f'<div class="relatorio">{pt.md_doc_para_html(s["texto"])}<h4>O que isso implica para o agente e para a Fase 4</h4>{leitura([pt.inline(x) for x in s["implicacoes"]])}'
        f'<h4>O que a literatura não responde</h4>{leitura([pt.inline(x) for x in s["lacunas"]])}</div></details>' for s in secoes)
    mudou = "".join(f'<p class="nota">{pt.inline(a)}</p>' for a in lit["avisos"])  # o que mudou, a memória da máquina e as correções da revisão
    bloco = f'''<h2>O que a literatura sustenta</h2>
<p>A rodada 5 da pesquisa leu o repositório por inteiro, as pesquisas que ele cita e a literatura independente sobre inferência com os pesos fora da RAM: {len(secoes)} tópicos, {aprovadas} afirmações aprovadas por verificadores céticos e {rejeitadas} {"rejeitada" if rejeitadas == 1 else "rejeitadas"}. O mapa dá o veredito de cada opção para esta máquina: <em>adotado</em> serve agora, sem trocar o modelo decidido; <em>adiado</em> só serviria com outra máquina, outro motor ou depois da Fase 4; <em>descartado</em> não serve, com o motivo.</p>
{mapa}
{mudou}
{detalhes("Riscos que a literatura aponta e a mitigação de cada um", tab_riscos)}
{detalhes("Leitura do mapa, por extenso", leitura_do_mapa)}
<h3>As sínteses, por extenso</h3>
<p>Cada síntese foi escrita só com as afirmações que sobreviveram à verificação. As referências completas e as afirmações rejeitadas, com o motivo, estão no levantamento (§6.14.12) e em <code>referencias.md</code>.</p>
{sinteses}'''
    cartoes = [("Opções avaliadas pela literatura", f'{cont["adotado"]} adotadas', f'{cont["adiado"]} adiadas · {cont["descartado"]} descartadas, de {n} no mapa da rodada 5')]
    fonte = f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code> (§{secoes[0]["secao"]} a §{secoes[-1]["secao"]} e mapa em §6.14.13)' if secoes else None
    return bloco, cartoes, fonte


def secao_colibri(v: dict | None, amostra: dict | None, road: dict, cartoes_corridas, levantamento: str | None = None) -> tuple[dict, str]:
    titulo = "Dá para rodar nesta máquina um modelo gigante lendo os pesos do disco?"
    if not v:
        return {"barras": []}, (f'<section id="colibri" hidden>\n<h1>{titulo}</h1>\n<p class="lead">As sondas da Pré-Fase 4 ainda não foram rodadas '
                                'nesta máquina: faltam <code>resultados_alvo/pre_fase4/disco.json</code> e <code>viabilidade_modelos_grandes.json</code> '
                                '(<code>python ferramentas/medir_disco.py</code> e <code>python viabilidade_modelos_grandes.py</code>).</p>\n</section>')
    maq, med, meta = v["maquina"], v["medianas_do_agente"], v["metadados"]
    fam = v["familias"]
    # ! Alteração de IA - Revisar: (01/10/2026, tarde) o veredito de cada modelo passou a ter três estados: roda com
    # folga, fica no limite (cabe no disco livre e pede exatamente a RAM instalada) ou não roda.
    # ! Motivo: a conta comparava o "16 GB min" do repositório com os 15,69 GB que o Windows enxerga e a aba dizia que a
    # RAM mínima "passa da instalada"; a máquina tem 16 GB instalados, o mínimo declarado. A resposta da aba fica mais
    # exata: um modelo roda com folga e dois grandes ficam no limite, sem medida publicada nessa classe de máquina.
    rodam = [f for f in fam if f["roda"] == "sim"]
    no_limite = [f for f in fam if f["roda"] == "no_limite"]
    instalada = maq["ram_instalada_gb"]
    glm = next(f for f in fam if f["nome"] == "GLM-5.2")
    nvme = v["cenarios_de_disco"][0]
    terceiros = v["medidas_de_terceiros"]
    do_glm = [x for x in terceiros if x["modelo"] == "GLM-5.2"]
    perto = next((x for x in do_glm if "12600K" in x["maquina"]), do_glm[0])
    perto_partes = [p.strip() for p in perto["maquina"].split(",")]
    seg_hoje = float(med["segundos"])
    tokens = float(med["tokens_saida"])

    # rótulo em três linhas curtas (lista de textos no Chart.js): numa linha só, e mesmo em duas, o começo do nome era
    # cortado à esquerda do eixo nas larguras menores
    barras = [{"rot": [meta["modelo_do_agente"], "neste notebook, hoje", "diagnóstico inteiro"], "minutos": round(seg_hoje / 60, 2), "hoje": True,
               "nota": f"diagnóstico inteiro: leitura do prompt e resposta ({fmt(seg_hoje)} s de mediana)"}]
    for x in terceiros:
        p = [s.strip() for s in x["maquina"].split(",")]
        rot = [x["modelo"], p[0].replace("Intel ", ""), p[1] + (" · opção com perda" if "perda" in x["nota"] else "")]
        barras.append({"rot": rot, "minutos": round(x["minutos_por_resposta"], 2), "hoje": False,
                       "nota": f'{fmt(x["tok_por_s"], 2)} token/s; {x["nota"]}'})
    dados_js = {"barras": barras, "tokens": tokens}

    def cabe(ok: bool, sim: str, nao: str) -> str:
        return chip("adotado" if ok else "descartado", sim if ok else nao)

    chip_da_ram = {"sim": chip("adotado", "cabe"), "no_minimo": chip("adiado", "no mínimo"), "nao": chip("descartado", "não cabe")}
    chip_do_veredito = {"sim": chip("adotado", "roda"), "no_limite": chip("adiado", "no limite"), "nao": chip("descartado", "não roda")}

    def linha_familia(x: dict) -> str:
        par = "não informado" if x["parametros_bi"] is None else _milhar(x["parametros_bi"])
        atv = "não informado" if x["ativos_bi"] is None else _milhar(x["ativos_bi"])
        return (f'<tr data-familia="{html.escape(x["nome"], quote=True)}" data-veredito="{x["roda"]}"><td><strong>{esc(x["nome"])}</strong></td><td class=num>{par}</td><td class=num>{atv}</td>'
                f'<td class=num>{fmt(float(x["disco_gb"]))} GB</td><td><code>{esc(x["ram_texto"])}</code></td>'
                f'<td>{cabe(x["disco_livre"], "cabe", "não cabe")}</td><td>{chip_da_ram[x["ram"]]}</td>'
                f'<td>{chip_do_veredito[x["roda"]]}</td></tr>')

    tab_fam = ('<div class="tabela"><table><thead><tr><th>Modelo</th><th>Parâmetros (bilhões)</th><th>Ativos por token (bilhões)</th><th>Disco pedido</th>'
               '<th>RAM pedida (texto do repositório)</th><th>Disco livre desta máquina</th><th>RAM pedida contra a instalada</th><th>Veredito</th></tr></thead><tbody>'
               + "".join(linha_familia(x) for x in fam) + "</tbody></table></div>")
    nem_vazio = [x["nome"] for x in fam if not x["disco_total"]]
    tab_disco = tabela(["Disco", "Leitura (GB/s)", "Medido ou premissa", "Segundos de disco por token frio", "Teto de tokens por segundo", "Minutos só de leitura para a resposta mediana"],
                       [[c["disco"], fmt(c["gb_por_s"], 2), "premissa" if c["premissa"] else "medido", fmt(c["segundos_por_token_frio"]), fmt(c["tokens_por_s_teto"], 3),
                         fmt(c["minutos_de_leitura_por_resposta"])] for c in v["cenarios_de_disco"]])
    tab_ter = tabela(["Máquina (medida publicada no repositório)", "Modelo", "Tokens por segundo", "Condição", "Minutos só de geração para a nossa resposta mediana",
                      "Vezes o tempo total de um diagnóstico de hoje", "Issue"],
                     [[x["maquina"], x["modelo"], fmt(x["tok_por_s"], 2), x["nota"], fmt(x["minutos_por_resposta"]), fmt(x["vezes_o_tempo_de_hoje"]), f'#{x["issue"]}']
                      for x in terceiros])
    min_glm = [x["minutos_por_resposta"] for x in do_glm]
    dm = v["disco_medido"]
    premissas = v["cenarios_de_disco"][1:]

    itens_kpi = [
        ("Famílias do colibri que rodam aqui", f"{len(rodam)} de {len(fam)}",
         ("com folga, só " + ", ".join(f["nome"] for f in rodam) if rodam else "nenhuma com folga")
         + (f'; no limite de RAM: {", ".join(f["nome"] for f in no_limite)}' if no_limite else "")),
        ("RAM instalada", f'{fmt(instalada)} GB', f'o sistema enxerga {fmt(maq["ram_gb"], 2)} GB, e cerca de {fmt(maq["ram_livre_no_inicio_de_corrida_gb"])} GB ficam livres no início de uma corrida; '
                                                    f'o GLM-5.2 pede {glm["ram_min_gb"]} GB no mínimo'),
        ("Disco livre", f'{fmt(maq["disco_livre_gb"])} GB', f'o GLM-5.2 pede {_milhar(glm["disco_gb"])} GB'),
        ("Leitura do NVMe", f'{fmt(nvme["gb_por_s"], 2)} GB/s', f'por fora do cache do sistema; {dm["blocos"]} leituras de {dm["bloco_bytes"] // 2**20} MB em {dm["threads"]} threads'),
        ("Uma resposta nossa em máquina parecida", f'{fmt(perto["minutos_por_resposta"])} min', f'só a geração, a {fmt(perto["tok_por_s"], 2)} token/s ({perto_partes[0]}, {perto_partes[1]}); hoje o diagnóstico inteiro leva {fmt(seg_hoje)} s'),
    ]

    bloco_sonda = ""
    am = _amostra_de_tokens(amostra)
    if am:
        ma, conf = amostra["metadados"], amostra["conferencias"]
        ch = amostra["chamadas"]
        itens_kpi.append(("Probabilidade por token no Ollama", "disponível", f'{conf["a"]["top_por_posicao_max"]} alternativas por posição; valor de {conf["temperatura"]["veredito"]} da temperatura'))

        def tok(t: dict) -> str:
            txt = t["token"].replace("\n", "\\n").replace(" ", "␣")
            return f'<span class="tok" style="--p:{round(t["p"] * 45)}%"><code>{esc(txt)}</code><small>{fmt(t["p"] * 100)}%</small></span>'

        linhas_alt = "".join(f'<tr data-alternativa="{i}"><td><code>{esc(a["token"].replace(" ", chr(0x2423)))}</code></td><td class=num>{fmt(a["p"] * 100, 2)}%</td></tr>'
                             for i, a in enumerate(am["alternativas"], 1))
        tab_conf = tabela(["O que foi conferido", "Resultado"], [
            ["Tokens da resposta com probabilidade", f'{conf["a"]["tokens_com_logprob"]} de {ch["a"]["resposta"].get("eval_count")} gerados'],
            ["Alternativas devolvidas por posição", str(conf["a"]["top_por_posicao_max"])],
            ["Vêm os bytes de cada token (acento partido entre dois tokens se remonta)", "sim" if conf["a"]["tem_bytes"] else "não"],
            ["Os tokens, juntos, são a resposta devolvida", "sim" if conf["a"]["texto_bate"] else "não"],
            ["A probabilidade é a de antes ou a de depois da temperatura", f'{conf["temperatura"]["veredito"]} (razão {fmt(conf["temperatura"]["razao"], 3)} entre a chamada a 0,1 e a chamada a 1,0; 1 seria igual)'],
            ["Tokens do prompt lidos do cache na segunda chamada", f'{ch["b"]["resposta"].get("prompt_eval_cached_count")} de {ch["b"]["resposta"].get("prompt_eval_count")} (campo prompt_eval_cached_count)'],
            ["A resposta sai igual com e sem o pedido de probabilidades", "sim" if conf["resposta_igual_sem_logprobs"] else "não: mesma causa e mesmos campos, frase de impacto com outras palavras (temperatura 0,1, sem semente)"],
        ])
        bloco_sonda = f'''<h2>O que a sonda do Ollama mostrou</h2>
<p>Amostra de ferramenta, com o <code>{esc(ma["modelo"])}</code> no caso <code>{esc(ma["caso"])}</code> e a biblioteca L{ma["biblioteca_epoca"]} dele, no Ollama {esc(ma["versao_ollama"])}; não é resultado de corrida. O Ollama devolve, para cada token que o modelo escreve, a probabilidade que ele deu a esse token e às alternativas. Abaixo, a primeira linha da resposta, token a token; o símbolo <code>␣</code> marca um espaço.</p>
<div class="toks">{"".join(tok(t) for t in am["linha"])}</div>
<p>O modelo decide a causa no primeiro token depois de <code>CAUSA_RAIZ:</code>; daí em diante o resto do rótulo sai quase certo. Nesse ponto, as opções que ele pesou foram estas:</p>
<div class="tabela estreita"><table><thead><tr><th>Token candidato</th><th>Probabilidade</th></tr></thead><tbody>{linhas_alt}</tbody></table></div>
<p>É esse número que a corrida 12 grava para os 72 casos: se a probabilidade do rótulo for baixa justamente onde o modelo erra, ela serve de aviso para chamar um humano.</p>
{detalhes("O que a sonda conferiu", tab_conf)}'''

    leitura_itens = [
        f'<strong>O que barra os modelos grandes aqui é o espaço em disco e a RAM, não a velocidade do disco.</strong> O NVMe entrega {fmt(nvme["gb_por_s"], 2)} GB/s, o que daria cerca de {fmt(nvme["segundos_por_token_frio"])} s de leitura por token do GLM-5.2. Mas o modelo pede {_milhar(glm["disco_gb"])} GB de disco e a máquina tem {fmt(maq["disco_livre_gb"])} GB livres. Na RAM, os {fmt(instalada)} GB instalados são exatamente o mínimo que o repositório declara para ele, e cerca de {fmt(maq["ram_livre_no_inicio_de_corrida_gb"])} GB ficam livres no início de uma corrida.',
        f'<strong>Mesmo onde ele roda, o tempo não serve ao agente.</strong> Nas máquinas parecidas com a nossa em que o repositório publica medida, uma resposta de {fmt(tokens, 0)} tokens levaria de {fmt(min(min_glm))} a {fmt(max(min_glm))} minutos só para ser gerada. Hoje o diagnóstico inteiro leva {fmt(seg_hoje)} s.',
        ("<strong>O único modelo que roda com folga não é candidato a motor do agente.</strong> " + ", ".join(f'{f["nome"]} ({_milhar(f["parametros_bi"])} bilhões de parâmetros no total, {_milhar(f["ativos_bi"])} em uso a cada token)' for f in rodam)
         + " cabe na máquina, mas trocar de modelo exige medir de novo (decisão 69). Ele entra na corrida 13 só como material do atlas."),
        "<strong>Disco comum e HD.</strong> O repositório não publica medida em HD. Pela leitura por token que ele declara, só o disco custaria "
        + " e ".join(f'{fmt(c["segundos_por_token_frio"])} s por token em {c["disco"].split(" (")[0]}' for c in premissas) + " (velocidades postas como premissa, não medidas).",
        "<strong>O que se aproveita sem trocar de motor</strong> é a ideia da escolha fechada por probabilidade: em vez de só ler o rótulo que o modelo escreveu, ler também a probabilidade que ele deu ao rótulo. O nosso diagnóstico é uma escolha entre 23 causas, e o Ollama instalado já devolve esse número."
    ]
    if no_limite:
        # a medida publicada com menos memória: a do GLM-5.2 na máquina de menor RAM, sem a opção com perda
        com_ram = [(int(re.search(r"(\d+) GB", x["maquina"]).group(1)), x) for x in do_glm if re.search(r"(\d+) GB", x["maquina"]) and "perda" not in x["nota"]]
        menor_ram, menor = min(com_ram, key=lambda par: par[0]) if com_ram else (None, None)
        leitura_itens.insert(1, f'<strong>{"Dois modelos grandes ficam" if len(no_limite) == 2 else "Há modelo grande que fica"} no limite.</strong> '
                                + " e ".join(f'{f["nome"]} ({_milhar(f["parametros_bi"])} bilhões de parâmetros, {_milhar(f["disco_gb"])} GB em disco)' for f in no_limite)
                                + f' cabem no disco livre e pedem exatamente a RAM instalada. O repositório não publica medida de nenhum deles numa máquina de {fmt(instalada, 0)} GB'
                                + (f'; a medida com menos memória que ele publica é a do GLM-5.2 numa máquina de {menor_ram} GB, a {fmt(menor["tok_por_s"], 2)} token/s.' if menor else '.')
                                + ' Rodar um deles seria uma medição nova, fora do que a corrida 13 prevê.')
    if nem_vazio:
        leitura_itens.insert(1, f'<strong>Nem com o disco vazio</strong> caberia {", ".join(nem_vazio)}: o disco tem {fmt(maq["disco_total_gb"])} GB no total.')
    conferido = (f'conferidas pela rodada 5 da pesquisa (ressalva: {esc(meta["ressalva_da_conferencia"])})' if meta["conferido_pela_rodada_5"]
                 else "ainda não conferidas pela rodada 5 da pesquisa")
    bloco_literatura, cartoes_literatura, fonte_literatura = _literatura_do_colibri(levantamento)
    itens_kpi += cartoes_literatura
    html_ = f'''<section id="colibri" hidden>
<h1>{titulo}</h1>
<p class="lead">Só no limite, e não para o agente. O colibri roda modelos de centenas de bilhões de parâmetros deixando na RAM a parte que todo token usa e lendo do NVMe, a cada token, só os especialistas que o modelo aciona. Das {len(fam)} famílias que ele suporta, {len(rodam)} roda com folga nesta máquina ({", ".join(f["nome"] for f in rodam) or "nenhuma"}){f" e {len(no_limite)} cabem no disco livre e ficam exatamente no mínimo de RAM que o repositório declara ({', '.join(f['nome'] for f in no_limite)}), sem nenhuma medida publicada numa máquina dessa classe" if no_limite else ""}; as outras esbarram no espaço em disco ou na RAM. Nas máquinas maiores em que ele foi medido, uma resposta do tamanho das nossas levaria de {fmt(min(min_glm))} a {fmt(max(min_glm))} minutos só para ser gerada.</p>
{kpis(itens_kpi)}
<h2>O que cada modelo pede e o que esta máquina tem</h2>
<p>Requisitos da tabela do README do repositório (acesso em {esc(meta["acesso"])}), comparados com a máquina medida por <code>ferramentas/medir_disco.py</code>. Roda com folga o modelo que cabe no disco livre e pede menos RAM do que a instalada; fica no limite o que cabe no disco livre e pede exatamente a RAM instalada, que é o mínimo declarado pelo repositório.</p>
{tab_fam}
<h2>Quanto tempo levaria um diagnóstico</h2>
<p>A primeira barra é o tempo de hoje, do diagnóstico inteiro. As outras são as velocidades que o repositório publica para cada máquina, aplicadas à nossa resposta mediana de {fmt(tokens, 0)} tokens: contam só a geração, porque a leitura do prompt em máquina pequena não é medida lá. O tempo real seria maior.</p>
<div class="chart alto"><canvas id="g-co-min"></canvas></div>
{detalhes("Medidas publicadas no repositório, aplicadas à nossa resposta", tab_ter)}
{detalhes("Quanto o disco sozinho custaria por token, por tipo de disco", tab_disco)}
{bloco_sonda}
<h2>Leitura</h2>
{leitura(leitura_itens)}
{bloco_literatura}
<h2>As medições desta frente</h2>
{cartoes_corridas(road, numeros=["11", "12", "13"], sufixo="-co")}
{fontes(["<code>resultados_alvo/pre_fase4/viabilidade_modelos_grandes.json</code> (<code>viabilidade_modelos_grandes.py</code>, com <code>--check</code>)", "<code>resultados_alvo/pre_fase4/disco.json</code> (<code>ferramentas/medir_disco.py</code>)", "amostra de <code>sondar_logprobs.py</code> em <code>resultados_alvo/pre_fase4/</code>", f'constantes do repositório <a href="{esc(meta["repositorio"])}">JustVugg/colibri</a>, {conferido}'] + ([fonte_literatura] if fonte_literatura else []) + ["decisão 70; roadmap §3.1"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 11. Pré-Fase 4: raciocínio aberto

# ! Alteração de IA - Revisar: aba nova (01/10/2026) da Pré-Fase 4 com o que a trilha bruta e o relatório de raciocínio
# mostram das corridas já gravadas: quantos diagnósticos foram remontados, em quantos o modelo não escreveu raciocínio,
# o que o código consegue conferir sem o gabarito e um relatório de caso inteiro, como exemplo.
# ! Motivo: o Eric pediu (01/10/2026) o "pensamento" da IA aberto, com arquivo bruto e relatório para humanos; a regra
# do painel é uma aba por análise. Os números vêm de resultados_alvo/pre_fase4/indicadores_raciocinio.json (gerado por
# gerar_relatorio_raciocinio.py --vitrine, com --check) e o exemplo é um dos relatórios versionados. O conversor de
# Markdown do painel não trata cerca de código nem <details>, que o relatório usa; por isso a seção tem o próprio
# conversor, que rebaixa os títulos para caberem dentro da aba e mantém os blocos como texto literal.

def _relatorio_para_html(md: str) -> str:
    linhas = pt.sem_comentarios(md).split("\n")
    out: list[str] = []
    par: list[str] = []
    i = 0

    def fecha() -> None:
        if par:
            out.append(f"<p>{pt.inline(' '.join(par))}</p>")
            par.clear()

    while i < len(linhas):
        l = linhas[i]
        if l.startswith("```"):
            fecha()
            cerca = l[:len(l) - len(l.lstrip("`"))]
            i += 1
            bloco = []
            while i < len(linhas) and not linhas[i].startswith(cerca):
                bloco.append(linhas[i])
                i += 1
            i += 1
            out.append('<pre class="bruto"><code>' + html.escape("\n".join(bloco), quote=False) + "</code></pre>")
            continue
        m = re.match(r"^<details><summary>(.*?)</summary>\s*$", l)
        if m:
            fecha()
            out.append(f"<details><summary>{esc(m.group(1))}</summary>")
            i += 1
            continue
        if l.strip() == "</details>":
            fecha()
            out.append("</details>")
            i += 1
            continue
        if not l.strip():
            fecha()
            i += 1
            continue
        if l.startswith("|"):
            fecha()
            tab = []
            while i < len(linhas) and linhas[i].startswith("|"):
                tab.append(linhas[i])
                i += 1
            out.append(pt.tabela_html(tab))
            continue
        m = re.match(r"^(#{1,4}) (.+)$", l)
        if m:
            fecha()
            nivel = min(len(m.group(1)) + 2, 6)      # o título do relatório vira h3; as seções, h4; as subseções, h5
            out.append(f"<h{nivel}>{pt.inline(m.group(2))}</h{nivel}>")
            i += 1
            continue
        par.append(l.strip())
        i += 1
    fecha()
    return "\n".join(out)


# Nome das três conferências que usam o gabarito, para o bloco de avaliação do explorador de casos.
ROTULO_AVALIACAO = {"causa_correta": "A causa respondida é a do caso", "campo_correto": "O campo apontado é o do caso",
                    "verbete_de_ouro_no_contexto": "O verbete que trata da causa certa estava no contexto"}
# O caso que o explorador abre escolhido: o mesmo do relatório de exemplo (a conferência em código acusa a resposta errada).
CASO_PADRAO_DO_EXPLORADOR = ("fase3b_cruzada_qwen__qwen2.5-coder_3b__L1", "sin-4")


def secao_raciocinio(ind: dict | None, exemplo: str | None, trilhas: dict | None = None, confianca: dict | None = None) -> tuple[dict, str]:
    titulo = "Dá para ver por que o modelo respondeu o que respondeu?"
    if not ind:
        return {"trilhas": [], "explorador": {"trilhas": []}}, (f'<section id="raciocinio" hidden>\n<h1>{titulo}</h1>\n<p class="lead">As trilhas ainda não foram geradas nesta máquina: falta '
                                 '<code>resultados_alvo/pre_fase4/indicadores_raciocinio.json</code> (<code>python gerar_relatorio_raciocinio.py --vitrine</code>).</p>\n</section>')
    cs = ind["corridas"]

    corrida_curta = {"fase3": "Fase 3, 90 casos", "fase3b_ineditos": "36 casos inéditos", "fase3b_cruzada_qwen": "troca cruzada, 36 casos"}

    def nome(c: dict) -> str:
        dono = c.get("dono_da_biblioteca") or c["modelo"]
        de_quem = "" if dono == c["modelo"] else f' do {NOME_CURTO.get(dono, dono)}'
        return f'{NOME_CURTO.get(c["modelo"], c["modelo"])} · {corrida_curta.get(c["corrida"], c["corrida"])} · biblioteca L{c["biblioteca_epoca"]}{de_quem}'

    def soma(regra: str, chave: str) -> int:
        return sum(x.get(chave, 0) for c in cs for x in c["conferencias"] if x["regra"] == regra)

    total = sum(c["diagnosticos"] for c in cs)
    sem = sum(c["sem_raciocinio_antes_das_linhas"] for c in cs)
    inteiro = sum(c["prova_do_prompt"].get("prompt_inteiro", 0) for c in cs)
    so_doc = sum(c["prova_do_prompt"].get("contexto", 0) for c in cs)
    nao_comp = sum(c["prova_do_prompt"].get("nao_comprovado", 0) for c in cs)
    fora_ctx = soma("fonte_estava_no_contexto", "nao_confere")
    citadas = soma("fonte_estava_no_contexto", "confere") + fora_ctx
    fora_conj = soma("rotulo_no_conjunto", "nao_confere")
    inexistentes = soma("fonte_existe_na_biblioteca", "nao_confere")
    sem_apoio = sum(c["acerto_por_sustentacao"]["nao_sustentado"]["n"] for c in cs)
    com_grupo = [c for c in cs if c["acerto_por_sustentacao"]["nao_sustentado"]["n"] and c["acerto_por_sustentacao"]["sustentado"]["n"]]
    texto_sinal = ""
    if com_grupo:
        pior = min(com_grupo, key=lambda c: c["acerto_por_sustentacao"]["nao_sustentado"]["acerto_pct"])
        ps, pn = pior["acerto_por_sustentacao"]["sustentado"], pior["acerto_por_sustentacao"]["nao_sustentado"]
        texto_sinal = (f' Na trilha em que a documentação mais atrapalhou ({esc(nome(pior))}), o acerto foi de {fmt(ps["acerto_pct"])}% quando sim ({ps["acertos"]} de {ps["n"]}) '
                       f'e de {fmt(pn["acerto_pct"])}% quando não ({pn["acertos"]} de {pn["n"]}).')
    if fora_ctx == 0 and inexistentes == 0:
        leitura_fontes = (f"<strong>Nestas trilhas o modelo não inventou fonte:</strong> os {citadas} verbetes citados existiam e estavam no contexto entregue. "
                          f"Respostas com causa fora das 23 permitidas: {fora_conj} em {total}.")
    else:
        leitura_fontes = (f"<strong>Fontes citadas:</strong> {fora_ctx} de {citadas} estavam fora do contexto entregue e {inexistentes} não existiam na biblioteca. "
                          f"Respostas com causa fora das 23 permitidas: {fora_conj} em {total}.")
    # o arquivo de cada trilha é <corrida>__<modelo com _ no lugar de :>__L<versão>; o nome legível é o da tabela
    nomes_das_trilhas = {f'{c["corrida"]}__{c["modelo"].replace(":", "_").replace("/", "_")}__L{c["biblioteca_epoca"]}': nome(c) for c in cs}
    explorador = pe.dados_do_explorador(trilhas, nomes_das_trilhas, {**ROTULO_CONFERENCIA, **ROTULO_AVALIACAO}, CLASSES, CASO_PADRAO_DO_EXPLORADOR)
    # ! Alteração de IA - Revisar: (06/10/2026) a sonda de confiança (corrida 12) entra na aba: AUROC de cada sinal por
    # biblioteca, o que a revisão dos 10%, 20% e 30% de menor probabilidade pega, e o acerto da cópia curada contra a L1 e a L0.
    # ! Motivo: a aba prometia a análise "quando a corrida 12 terminar"; ela rodou em 06/10 (fichas 18 e 19). Tudo vem de
    # resultados_alvo/pre_fase4/confianca.json.
    conf = confianca or {}
    resumos = conf.get("resumos") or []
    tot = resumos[0] if resumos else None
    por_bib = [r for r in resumos[1:]] if resumos else []
    SINAIS = [("p_conjunta", "probabilidade conjunta do rótulo"), ("p_primeiro", "primeiro token"), ("um_menos_massa", "1 menos a massa de outra causa"),
              ("sustentado", "causa tratada por verbete do contexto"), ("coerente", "causa na classe que a rota aponta")]
    dados_conf = {"sinais": [n for _, n in SINAIS],
                  "bibliotecas": [{"rot": r["nome"].split(", ")[-1], "auroc": [(r["sinais"].get(s) or {}).get("auroc") for s, _ in SINAIS]} for r in por_bib]}
    bloco_conf, itens_conf = "", []
    if tot:
        ac = conf.get("acerto", [])
        pares = {(x["comparacao"], x["conjunto"]): x for x in conf.get("pares", [])}
        rev = {x["fracao"]: x for x in tot["revisao"]}
        a72 = {x["rotulo"]: x for x in ac if x["conjunto"] == "todos"}
        cur = a72.get("L1 curada")
        l1 = a72.get("L1")
        p_cur = pares.get(("L1 curada contra L1", "todos"))
        confiantes = sum(1 for l in conf.get("casos", []) if not l["acerto"] and (l["p_conjunta"] or 0) > 0.85)
        itens_conf = [
            ("AUROC da probabilidade do rótulo", fmt(tot["sinais"]["p_conjunta"]["auroc"], 3),
             f'[{fmt(tot["sinais"]["p_conjunta"]["ic95"][0], 3)} a {fmt(tot["sinais"]["p_conjunta"]["ic95"][1], 3)}] em {tot["casos"]} diagnósticos, {tot["erros"]} erros; verbete do contexto {fmt(tot["sinais"]["sustentado"]["auroc"], 3)}, classe da rota {fmt((tot["sinais"].get("coerente") or {}).get("auroc"), 3)}'),
            ("Revisar os 10% menos prováveis", f'{rev[0.1]["erros_pegos"]} de {tot["erros"]} erros', f'{rev[0.1]["revisados"]} casos revisados, {rev[0.1]["acertos_revisados"]} à toa; com 30%: {rev[0.3]["erros_pegos"]} de {tot["erros"]}'),
            ("Erros confiantes", f"{confiantes} de {tot['erros']}", f'probabilidade acima de 0,85; mediana {fmt(tot["p_conjunta_mediana"]["certos"], 3)} nos certos e {fmt(tot["p_conjunta_mediana"]["errados"], 3)} nos errados'),
        ]
        if cur and l1 and p_cur:
            itens_conf.append(("Cópia curada da L1 nos 72 casos", f'{fmt(cur["acerto_pct"])}% × {fmt(l1["acerto_pct"])}%',
                               f'contra a L1 inteira na mesma corrida: b/c {p_cur["b"]}/{p_cur["c"]}, p = {fmt(p_cur["p_mcnemar"], 2)}; {fmt(cur["segundos_mediana"])} × {fmt(l1["segundos_mediana"])} s por diagnóstico'))
        tab_res = tabela(["Recorte", "Casos", "Erros"] + [n for _, n in SINAIS] + ["Mediana nos certos", "Mediana nos errados", "Erros com a causa certa em 2º"],
                         [[r["nome"], r["casos"], r["erros"]] + [("n/d" if not r["sinais"].get(s) or r["sinais"][s].get("auroc") is None else f'{fmt(r["sinais"][s]["auroc"], 3)} [{fmt(r["sinais"][s]["ic95"][0], 2)} a {fmt(r["sinais"][s]["ic95"][1], 2)}]') for s, _ in SINAIS]
                          + [fmt(r["p_conjunta_mediana"]["certos"], 3), fmt(r["p_conjunta_mediana"]["errados"], 3), f'{r["erros_com_o_gabarito_na_segunda"]} de {r["erros"]}'] for r in resumos])
        tab_rev = tabela(["Recorte", "Parcela revisada", "Casos revisados", "Erros pegos", "Acertos revisados à toa", "Risco no que sobra"],
                         [[r["nome"], f'{fmt(100 * x["fracao"], 0)}%', x["revisados"], f'{x["erros_pegos"]} de {x["erros"]}', x["acertos_revisados"], "n/d" if x["risco_no_que_sobra"] is None else f'{fmt(100 * x["risco_no_que_sobra"])}%']
                          for r in resumos for x in r["revisao"]])
        tab_ac = ('<div class="tabela"><table><thead><tr><th>Biblioteca</th><th>Conjunto</th><th>Casos</th><th>Acertos</th><th>Acerto</th><th>s por diagnóstico (mediana)</th><th>Tokens do prompt (mediana)</th></tr></thead><tbody>'
                  + "".join(f'<tr data-conf-acerto="{html.escape(x["rotulo"] + "/" + x["conjunto"], quote=True)}"><td>{esc(x["rotulo"])}</td><td>{esc(x["conjunto"])}</td><td class=num>{x["n"]}</td><td class=num>{x["acertos"]}</td>'
                            f'<td class=num>{fmt(x["acerto_pct"])}%</td><td class=num>{fmt(x["segundos_mediana"])}</td><td class=num>{fmt(x["tokens_entrada_mediana"], 0)}</td></tr>' for x in ac) + "</tbody></table></div>")
        tab_par = tabela(["Comparação", "Conjunto", "Casos", "Acerto da primeira", "Acerto da segunda", "b", "c", "Diferença", "p (McNemar exato)", "Casos que mudaram"],
                         [[x["comparacao"], x["conjunto"], x["n"], f'{fmt(x["acerto_pct"])}%', f'{fmt(x["acerto_base_pct"])}%', x["b"], x["c"], pp(x["delta_pp"]), fmt(x["p_mcnemar"], 4), ", ".join(x["ganhos"] + x["perdas"]) or "nenhum"]
                          for x in conf.get("pares", []) + conf.get("contra_corridas_anteriores", [])])
        bloco_conf = f"""<h2>A probabilidade do rótulo separa acerto de erro? (corrida 12, 06/10/2026)</h2>
<p>O Ollama devolve a probabilidade de cada token que o modelo escreve. A corrida 12 gravou essa probabilidade para o rótulo da causa nos 72 casos que nenhuma biblioteca viu, com o qwen2.5:7b lendo a biblioteca original (L0), a L1 inteira e a cópia curada da L1 que a Fase 4 vai usar: {tot["casos"]} diagnósticos, {tot["erros"]} erros. A medida principal, fixada antes da corrida, é a probabilidade conjunta dos tokens do rótulo; a AUROC diz quanto cada sinal separa acerto de erro (0,5 é sortear, 1,0 separa tudo).</p>
{kpis(itens_conf)}
<div class="chart"><canvas id="g-ra-conf"></canvas></div>
{tab_res}
{leitura([f"<strong>Separa, e melhor que os dois sinais grátis, mas metade dos erros sai confiante.</strong> AUROC {fmt(tot['sinais']['p_conjunta']['auroc'], 3)} contra {fmt(tot['sinais']['sustentado']['auroc'], 3)} e {fmt((tot['sinais'].get('coerente') or {}).get('auroc'), 3)}; {confiantes} dos {tot['erros']} erros têm probabilidade acima de 0,85, e em {tot['erros_com_o_gabarito_na_segunda']} deles a causa certa era a segunda opção.",
          f"<strong>Serve de triagem, não de barreira.</strong> Mandar para revisão os 10% de menor probabilidade ({rev[0.1]['revisados']} casos) pega {rev[0.1]['erros_pegos']} dos {tot['erros']} erros; 30% ({rev[0.3]['revisados']} casos) pega {rev[0.3]['erros_pegos']}, revisando {rev[0.3]['acertos_revisados']} acertos à toa. Para a Fase 4, vale como ordem de prioridade de revisão e como aviso na trilha."]
         + ([f"<strong>A cópia curada rende como a L1 inteira e custa menos.</strong> {fmt(cur['acerto_pct'])}% contra {fmt(l1['acerto_pct'])}% nos 72 casos na mesma corrida (b/c {p_cur['b']}/{p_cur['c']}), dentro da variação entre corridas iguais; {fmt(cur['segundos_mediana'])} s contra {fmt(l1['segundos_mediana'])} s por diagnóstico, com menos texto no contexto. Segue como ponto de partida da Fase 4 (decisão 71)."] if cur and l1 and p_cur else []))}
{detalhes("Revisão humana por parcela de menor probabilidade", tab_rev)}
{detalhes("Acerto de cada biblioteca na corrida 12 (36 oficiais, 36 inéditos, 72)", tab_ac)}
{detalhes("Pares caso a caso: entre as bibliotecas da corrida e contra as corridas anteriores", tab_par)}
"""
    dados_js = {"explorador": explorador, "confianca": dados_conf,
                "trilhas": [{"rot": nome(c).split(" · "), "sustentado": c["acerto_por_sustentacao"]["sustentado"]["acerto_pct"],
                             "nao": c["acerto_por_sustentacao"]["nao_sustentado"]["acerto_pct"],
                             "n_sus": c["acerto_por_sustentacao"]["sustentado"]["n"], "n_nao": c["acerto_por_sustentacao"]["nao_sustentado"]["n"]} for c in cs]}
    itens_kpi = [
        ("Diagnósticos remontados", str(total), f"{len(cs)} corridas gravadas, sem rodar modelo"),
        ("Sem raciocínio escrito", f"{sem} de {total}", "o modelo vai direto às quatro linhas pedidas"),
        ("Prompt provado por inteiro", f"{inteiro} de {total}", f"nos outros {so_doc} só a documentação entregue tem prova gravada" + (f"; {nao_comp} não comprovados" if nao_comp else "")),
        ("Verbetes citados fora do contexto", f"{fora_ctx} de {citadas}", "o modelo só citou o que recebeu" if fora_ctx == 0 else "citações a verbete que não foi entregue"),
        ("Causa fora das 23 permitidas", str(fora_conj), "respostas com rótulo inventado"),
        ("Causa sem apoio no contexto", str(sem_apoio), "respostas cuja causa nenhum verbete entregue trata"),
    ]
    linhas_conf = "".join(
        f'<tr data-conferencia="{html.escape(x["regra"], quote=True)}"><td>{esc(nome(c))}</td><td>{esc(ROTULO_CONFERENCIA.get(x["regra"], x["regra"]))}</td>'
        f'<td class=num>{x.get("confere", 0)}</td><td class=num>{x.get("nao_confere", 0)}</td><td class=num>{x.get("nao_se_aplica", 0)}</td>'
        f'<td class=num>{x.get("nao_verificavel", 0) + x.get("informativo", 0)}</td></tr>' for c in cs for x in c["conferencias"])
    tab_conf = ('<div class="tabela"><table><thead><tr><th>Trilha</th><th>Conferência (sem usar o gabarito)</th><th>Confere</th><th>Não confere</th>'
                f'<th>Não se aplica</th><th>Não verificável ou informativo</th></tr></thead><tbody>{linhas_conf}</tbody></table></div>')
    tab_sus = tabela(["Trilha", "Diagnósticos", "Acerto quando algum verbete do contexto trata da causa respondida", "Acerto quando nenhum trata"],
                     [[nome(c), c["diagnosticos"],
                       f'{fmt(c["acerto_por_sustentacao"]["sustentado"]["acerto_pct"])}% ({c["acerto_por_sustentacao"]["sustentado"]["acertos"]} de {c["acerto_por_sustentacao"]["sustentado"]["n"]})',
                       f'{fmt(c["acerto_por_sustentacao"]["nao_sustentado"]["acerto_pct"])}% ({c["acerto_por_sustentacao"]["nao_sustentado"]["acertos"]} de {c["acerto_por_sustentacao"]["nao_sustentado"]["n"]})']
                      for c in cs])
    bloco_exemplo = ""
    if exemplo:
        bloco_exemplo = ('<h2>Como é o relatório de um caso</h2>\n<p>Um dos relatórios da vitrine, inteiro: um caso da troca cruzada em que o Coder 3B, lendo a biblioteca do '
                         '<code>qwen2.5:7b</code>, respondeu uma causa que nenhum verbete entregue tratava. O relatório é gerado por script, só do arquivo bruto; as três '
                         'camadas vêm separadas, e a resposta certa aparece numa seção só.</p>\n'
                         + detalhes("Abrir o relatório do caso", '<div class="relatorio">' + _relatorio_para_html(exemplo) + "</div>"))
    html_ = f'''<section id="raciocinio" hidden>
<h1>{titulo}</h1>
<p class="lead">Em parte. Dá para ver tudo o que o programa fez (o que a busca pontuou e entregou, o prompt, a resposta, os tempos) e conferir por código o que o modelo declarou. O raciocínio em si não está lá: em {sem} dos {total} diagnósticos remontados o modelo não escreveu nenhum, foi direto às quatro linhas. Por isso o relatório separa três camadas e nunca trata a alegação do modelo como fato.</p>
{kpis(itens_kpi)}
<h2>As três camadas</h2>
{leitura(["<strong>O que o programa fez</strong> é fato: o caso que entrou, os verbetes que a busca pontuou e os que entregou, o prompt montado, a resposta crua, os tempos. Nas corridas gravadas o prompt não foi guardado; ele é remontado pelas mesmas funções do executor, e cada trilha diz até onde essa remontagem está provada.",
          "<strong>O que o modelo declarou</strong> é alegação: a causa, o campo, a frase de impacto e os verbetes citados, sempre como trecho literal da resposta, com a posição.",
          "<strong>O que o código conferiu</strong> é o que se pôde checar da alegação sem saber a resposta certa. O que não dá para conferir por código (a frase de impacto, e qual nota de um verbete o modelo usou) é dito, não omitido."])}
<h2>Um sinal que o agente pode calcular sozinho</h2>
<p>Em cada resposta o código pergunta: algum verbete entregue ao modelo trata da causa que ele respondeu? Não precisa de gabarito.{texto_sinal} Os grupos "quando não" são pequenos; a sonda de confiança (corrida 12) mede o mesmo sinal junto com a probabilidade do rótulo.</p>
<div class="chart"><canvas id="g-ra-sus"></canvas></div>
{tab_sus}
<h2>O que o código conferiu, por trilha</h2>
<p>Oito conferências por resposta, todas sem usar o gabarito. As duas últimas não dão veredito: a lista das notas do modelo nos verbetes citados é informativa, e a frase de impacto não tem como ser conferida por código.</p>
{detalhes("Todas as conferências, trilha por trilha", tab_conf)}
{bloco_conf}
{pe.bloco_html(explorador)}
{bloco_exemplo}
<h2>Leitura</h2>
{leitura([
    f"<strong>O modelo decidido não mostra o caminho.</strong> Em {sem} de {total} respostas não há texto antes das quatro linhas, embora o prompt peça uma explicação curta. O que se abre é o caminho do programa e a conferência das alegações, não um raciocínio escrito.",
    leitura_fontes,
    "<strong>O erro mais comum não é inventar, é responder uma causa que a documentação entregue não trata.</strong> Esse caso é detectável em código, na hora, e vira candidato a aviso para quem desenvolve.",
    "<strong>O relatório mostra de quem é cada nota.</strong> Quando o verbete citado tem notas escritas pelo modelo, o relatório lista quantas são e o veredito da revisão humana de cada uma; não dá para saber qual delas pesou na resposta, e isso fica escrito.",
    ("<strong>A probabilidade do rótulo é o melhor dos três sinais, e nenhum deles é barreira.</strong> A seção da corrida 12, acima, traz os números; a especificação da trilha para a Fase 4 entra nesta aba quando a rodada B da pesquisa terminar." if tot
     else "A especificação da trilha para a Fase 4 e a análise da probabilidade do rótulo entram nesta aba quando a rodada B da pesquisa e a corrida 12 terminarem.")])}
{fontes(["<code>resultados_alvo/pre_fase4/confianca.json</code> e <code>.md</code> (<code>analisar_confianca.py</code>, corrida 12 em <code>resultados_alvo/pre_fase4_confianca/</code>)", "<code>resultados_alvo/pre_fase4/indicadores_raciocinio.json</code> (<code>gerar_relatorio_raciocinio.py --vitrine</code>, com <code>--check</code>)", "trilhas em <code>resultados_alvo/pre_fase4/trilhas/</code> (<code>trilha.py</code>) e relatórios em <code>resultados_alvo/pre_fase4/relatorios/</code>", "decisão 70; roadmap §3.1"])}
</section>'''
    return dados_js, html_


ROTULO_CONFERENCIA = {
    "quatro_linhas_presentes": "A resposta tem as quatro linhas pedidas",
    "rotulo_no_conjunto": "A causa está entre as permitidas",
    "fonte_existe_na_biblioteca": "O verbete citado existe na biblioteca",
    "fonte_estava_no_contexto": "O verbete citado estava no contexto entregue ao modelo",
    "campo_existe_no_caso": "O campo apontado aparece no caso",
    "rotulo_sustentado_por_verbete_do_contexto": "Algum verbete do contexto trata da causa respondida",
    "notas_nos_verbetes_citados": "Notas escritas pelo modelo nos verbetes citados",
    "impacto": "Frase de impacto",
}


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
function czLeitores(){
  const met = document.getElementById('sel-cz-met').value; const C = T.cruzada; const ds = [];
  ds.push({label: C.doador+' · a biblioteca que ele escreveu (Fase 3)', data: C.versoes.map(v => C.propria[C.doador][v][met]), borderColor:cor(C.doador), backgroundColor:cor(C.doador), tension:.2, pointRadius:4});
  C.leitores.forEach(m => { ds.push({label: m+' · a biblioteca do '+C.doador, data: C.versoes.map(v => C.doador_lido[m][v][met]), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4});
    ds.push({label: m+' · a própria biblioteca (Fase 3)', data: C.versoes.map(v => C.propria[m][v][met]), borderColor:cor(m), backgroundColor:cor(m), borderDash:[6,4], tension:.2, pointRadius:4, pointStyle:'rectRot'}); });
  grafico('g-cz-leit', {type:'line', data:{labels: C.versoes.map(v => 'L'+v), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='bal'?'acurácia balanceada nos 36 (%)':'acerto nos 36 (%)'}, suggestedMin:50, suggestedMax:95}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function czTrocas(){
  const R = T.cruzada.trocas;
  grafico('g-cz-trocas', {type:'bar', data:{labels: R.map(r => r.rot), datasets:[{label:'passou a acertar', data: R.map(r => r.b), backgroundColor: css('--bom')}, {label:'deixou de acertar', data: R.map(r => -r.c), backgroundColor: css('--ruim')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, title:{display:true,text:'casos em 36 (perdas à esquerda, ganhos à direita)'}, ticks:{stepSize:1, callback: v => Math.abs(v)}}, y:{stacked:true, ticks:{autoSkip:false}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+Math.abs(c.raw)+' caso(s)', afterBody: it => { const r = R[it[0].dataIndex]; return 'saldo: '+(r.b - r.c > 0 ? '+' : '')+(r.b - r.c); }}}}}});
}
function coMinutos(){
  const B = (T.colibri||{}).barras||[]; if(!B.length) return;
  grafico('g-co-min', {type:'bar', data:{labels: B.map(b => b.rot), datasets:[
      {label:'este projeto hoje: diagnóstico inteiro', data: B.map(b => b.hoje ? b.minutos : null), backgroundColor: css('--s1')},
      {label:'colibri em máquinas de terceiros: só a geração da resposta', data: B.map(b => b.hoje ? null : b.minutos), backgroundColor: css('--s2')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
      scales:{x:{stacked:true, beginAtZero:true, title:{display:true, text:'minutos para uma resposta de '+T.colibri.tokens+' tokens'}}, y:{stacked:true, ticks:{autoSkip:false}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+' min', afterLabel: c => B[c.dataIndex].nota}}}}});
}
function raSustentacao(){
  const L = (T.raciocinio||{}).trilhas||[]; if(!L.length) return;
  grafico('g-ra-sus', {type:'bar', data:{labels: L.map(x => x.rot), datasets:[
      {label:'algum verbete do contexto trata da causa respondida', data: L.map(x => x.sustentado), backgroundColor: css('--s1')},
      {label:'nenhum verbete do contexto trata', data: L.map(x => x.nao), backgroundColor: css('--s2')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true, text:'acerto (%)'}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%', afterLabel: c => 'n = '+(c.datasetIndex===0 ? L[c.dataIndex].n_sus : L[c.dataIndex].n_nao)}}}}});
}
function raConfianca(){
  const C = (T.raciocinio||{}).confianca; if(!C || !C.bibliotecas.length) return;
  grafico('g-ra-conf', {type:'bar', data:{labels: C.sinais, datasets: C.bibliotecas.map((b, i) => ({label: b.rot, data: b.auroc, backgroundColor: css('--s' + (i + 1))}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0.4, max:1, title:{display:true, text:'AUROC (0,5 = sortear)'}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label + ': ' + (c.raw === null ? 'n/d' : c.formattedValue)}}}}});
}
function ferMcp(){
  if(!T.ferramental.mcp) return; const met = document.getElementById('sel-fer-met').value; const S = T.ferramental.mcp;
  grafico('g-fer-mcp', {type:'bar', data:{labels: S.map(x => x.tarefa), datasets:[{label:'grep, Glob e Read', data: S.map(x => Math.round(x['grep_'+met])), backgroundColor: css('--s1')}, {label:'servidor codebase-memory', data: S.map(x => Math.round(x['mcp_'+met])), backgroundColor: css('--s2')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'tokens (média de 2 repetições)'}, beginAtZero:true}}}});
}
""" + pa.JS_ATLAS + pe.JS_EXPLORADOR

DESENHAR_TOPICOS = {"comparativo": ["cqTrajetoria", "cqConfronto", "cqRevisao"], "tresb": ["tbGeneraliza", "tbRecuperacao"],
                    "cruzada": ["czLeitores", "czTrocas"], "colibri": ["coMinutos"], "raciocinio": ["raSustentacao", "raConfianca", "raExplorar"], "atlas": ["atlasIniciar"],
                    "curadoria": ["curOperacoes"], "recuperador": ["recMetodos"], "ablacao": ["ablBarras"], "ferramental": ["ferMcp"]}
SELETORES_TOPICOS = {"sel-cq-conj": "cqTrajetoria", "sel-cq-met": "cqTrajetoria", "sel-cq-conf": "cqConfronto", "sel-tb-met": "tbGeneraliza", "sel-cz-met": "czLeitores",
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
.toks{display:flex;flex-wrap:wrap;gap:4px;margin:12px 0}
.tok{display:inline-flex;flex-direction:column;align-items:center;gap:2px;padding:4px 7px;border-radius:6px;border:1px solid var(--linha);background:color-mix(in srgb,var(--s1) var(--p,0%),transparent)}
.tok code{background:none;padding:0;font:500 13px var(--fm);color:var(--ink)}.tok small{font:400 10px var(--fb);color:var(--ink2)}
.tabela.estreita{max-width:420px}
pre.bruto{margin:8px 0;background:var(--acento2);border-radius:6px;padding:10px 12px;font:12px/1.5 var(--fm);white-space:pre-wrap;overflow-wrap:anywhere;max-width:100%}
pre.bruto code{background:none;padding:0;font:inherit}
.relatorio{border-left:3px solid var(--linha);padding:2px 0 8px 16px;margin:8px 0}.relatorio h3{margin-top:10px}.relatorio h5{font:600 13px var(--fb);margin:14px 0 6px}
.chip.adotado{background:color-mix(in srgb,var(--bom) 18%,transparent);color:var(--bom)}.chip.adiado{background:color-mix(in srgb,var(--meio) 18%,transparent);color:var(--meio)}.chip.descartado{background:color-mix(in srgb,var(--ruim) 16%,transparent);color:var(--ruim)}
""" + pa.CSS_ATLAS + pe.CSS_EXPLORADOR


# ! Alteração de IA - Revisar: (01/10/2026) bloco da aba Atlas com a validação do texto do Gemini, lido da subseção
# "3.1" do relatório da Pré-Fase 4: uma linha por afirmação, com o veredito em destaque (certo, com ressalva, errado).
# ! Motivo: o Eric pediu que a descrição que o Gemini deu das imagens fosse validada; a resposta, com a fonte de cada
# veredito, está no relatório, e é pelo painel que ele lê. O texto não é copiado para o código: vem do arquivo.
RELATORIO_PRE_FASE4 = MEMORIAL / "3-resultados-e-analises" / "pre-fase-4-relatorio.md"


def validacao_do_gemini() -> str:
    if not RELATORIO_PRE_FASE4.exists():
        return ""
    md = pt.sem_comentarios(RELATORIO_PRE_FASE4.read_text(encoding="utf-8").replace("\r\n", "\n"))
    ini = md.find("### 3.1 ")
    if ini < 0:
        return ""
    fim = md.find("\n### ", ini + 4)
    trecho = md[ini:fim if fim > 0 else len(md)]
    cab, linhas, resto = pt.primeira_tabela(trecho.split("\n", 1)[1])
    if not linhas:
        return ""

    def classe(veredito: str) -> tuple[str, str]:
        v = veredito.strip().lower()
        if v.startswith("errado"):
            return "errado", "descartado"
        return ("certo", "adotado") if v == "correto" else ("ressalva", "adiado")

    trs = []
    for k, r in enumerate(linhas, 1):
        nome, cor = classe(r[1])
        trs.append(f'<tr data-afirmacao="{k}" data-veredito="{nome}"><td>{pt.inline(r[0])}</td><td>{chip(cor, r[1])}</td><td>{pt.inline(r[2])}</td>'
                   f'<td class="nota">{pt.inline(r[3])}</td></tr>')
    paragrafos = [p.strip() for p in resto.split("\n\n") if p.strip()]
    antes = pt.inline(paragrafos[0]) if paragrafos else ""
    depois = "".join(f"<p>{pt.inline(p)}</p>" for p in paragrafos[1:])
    cont = Counter(classe(r[1])[0] for r in linhas)
    resumo = (f"A descrição do Gemini estava certa? Das {len(linhas)} afirmações conferidas, {cont['certo']} estão certas, "
              f"{cont['ressalva']} valem em parte ou com ressalva e {cont['errado']} estão erradas")
    return (f'<details class="at-gemini"><summary>{esc(resumo)}</summary>\n<p>{antes}</p>\n'
            f'<div class="tabela"><table><thead><tr>{"".join(f"<th>{esc(c)}</th>" for c in cab)}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>\n{depois}</details>')


# ------------------------------------------------------------------ montagem

def montar(ctx: dict) -> tuple[dict, str]:
    """ctx: dados (montar_dados), road, cartoes_corridas, md_para_html, md_doc_para_html, cq, blocos_cq, ineditos,
    curadoria, planilha_curadoria, recuperador, ablacao, medicao_mcp, readme. Devolve (dados_topicos, html)."""
    dados, road = ctx["dados"], ctx["road"]
    partes: list[tuple[str, dict, str]] = []
    d, h = secao_comparativo(ctx["cq"], ctx["blocos_cq"], ctx["md_para_html"], road, ctx["cartoes_corridas"])
    partes.append(("cq", d, h))
    d, h = secao_tres_b(ctx["ineditos"], dados, road, ctx["cartoes_corridas"], ctx["md_doc_para_html"], ctx.get("analise3b"))
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
    if ctx.get("analise3b"):
        d, h = secao_cruzada(ctx["analise3b"], road, ctx["cartoes_corridas"])
        partes.append(("cruzada", d, h))
    if ctx.get("relatorio3b"):
        d, h = secao_fechamento(ctx["relatorio3b"], ctx.get("pend", []), ctx["md_doc_para_html"])
        partes.append(("fechamento", d, h))
    # a aba da Pré-Fase 4 existe sempre (o mapa de navegação a lista); sem os arquivos das sondas ela mostra o estado vazio
    lev = PESQUISA / LEVANTAMENTO_PRE_FASE4
    d, h = secao_colibri(ctx.get("viabilidade"), ctx.get("logprobs_amostra"), road, ctx["cartoes_corridas"], lev.read_text(encoding="utf-8") if lev.exists() else None)
    partes.append(("colibri", d, h))
    d, h = pa.secao_atlas(ctx.get("atlas"), kpis, leitura, fontes, detalhes, validacao_do_gemini())
    partes.append(("atlas", d, h))
    d, h = secao_raciocinio(ctx.get("indicadores_raciocinio"), ctx.get("relatorio_exemplo"), ctx.get("trilhas"), ctx.get("confianca"))
    partes.append(("raciocinio", d, h))
    return {k: d for k, d, _ in partes}, "\n".join(h for _, _, h in partes)
