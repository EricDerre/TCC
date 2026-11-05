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

# ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) o endereço da página da sessão, gerada por ferramentas/sessao_revisao.py.
# ! Motivo: o Eric decide pelo painel, e a aba da trilha aponta para onde a sessão acontece.
URL_SESSAO_REVISAO = "https://claude.ai/artifact/7UrQ4gaqHj9qnvo22tfDgS"

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
        ("recuperador", "Recuperador", "A busca por palavras contra a busca por significado e a mistura das duas: vale trocar?"),
        ("ablacao", "Ablação", "Sem ajuste por instrução, o modelo faz a tarefa? O piso da família."),
    ]),
    # grupo da Pré-Fase 4 (01/10/2026): um id só entra neste mapa junto com a seção dele, porque
    # teste_toda_aba_do_mapa_existe_na_pagina exige que todo botão da navegação tenha a sua seção
    ("Pré-Fase 4", [
        ("colibri", "Modelos grandes pelo disco", "Dá para rodar nesta máquina um modelo gigante lendo os pesos do SSD? O que o colibri pede, o que foi medido aqui e o que se aproveita."),
        ("atlas", "Atlas", "Que verbetes a busca entrega para cada tipo de defeito e o que o modelo faz com eles: o mapa, a rota de cada caso e as trocas entre causas."),
        ("raciocinio", "Raciocínio aberto", "Dá para ver por que o modelo respondeu o que respondeu? A trilha bruta, o relatório por caso, o que o código consegue conferir e o que a literatura sustenta para a arquitetura da trilha."),
        ("cerebro", "Cérebro e memória", "Dá para mostrar a rede neural como o cérebro do agente, ao vivo? O Brainiac e os grafos do código e do conhecimento servem? O que a literatura sustenta nesta máquina e neste painel."),
    ]),
    # grupo da Fase 4 (27/10/2026): a corrida 17 é a primeira análise da fase; o id entra junto com a seção (secao_reproducao)
    ("Fase 4", [
        # ! Alteração de IA - Revisar: (05/11/2026, P8) a aba do fechamento abre o grupo; o id entra junto com a seção (secao_fechamento_f4).
        # ! Motivo: é a aba da fase que o plano previa (seção 3.8): quem abre o grupo vê primeiro o que fechou e o que ficou como limitação.
        ("fechamentof4", "Fechamento da fase", "A Fase 4 fez o que o plano pediu? As regras uma a uma, o que fica como limitação declarada, o que depende do Eric e o que o documento do TCC precisa carregar, lidos do relatório da fase."),
        ("reproducao", "Reprodução na tela", "Quantos casos de avaliação a tela consegue reproduzir, com que custo por cenário e o que fica fora: a corrida 17 nos 72 casos e a mesma corrida nos 36 inéditos da ficha 27."),
        # aba da corrida 16 (27/10/2026, P3): o id entra junto com a seção (secao_calibracao)
        ("calibracao", "Calibração", "Quantos verbetes entregar ao modelo, onde ficam os cortes do selo de confiança e quanto a probabilidade da resposta separa acerto de erro: a corrida 16 nos 90 casos."),
        ("tela", "Tela e caso escrito", "O agente dá o mesmo diagnóstico ao caso lido da tela e ao mesmo caso escrito? As corridas 18 e 18b nos casos que reproduzem, com a regra que compara os dois lados, os selos, as causas respondidas e o tamanho do prompt."),
        # aba da corrida 19 (01/11/2026, P4): o id entra junto com a seção (secao_cura)
        ("cura", "Cura de seletor", "Quando o localizador de um passo quebra, o agente acha outro em código e o roteiro passa na reexecução? A corrida 19 nos quatro roteiros do front legado, com quatro modos de quebra nas duas formas, a taxa de cura e o tempo até o resultado."),
        # aba da corrida 20 (03/11/2026, P5): o id entra junto com a seção (secao_biblioteca)
        ("biblioteca", "Biblioteca em produção", "O que o agente propõe para a biblioteca passa pelos filtros em código, melhora os casos inéditos, e a marca de corrigido acerta? A corrida 20: o lote, os filtros, a reavaliação, a correção e a sonda."),
        # ! Alteração de IA - Revisar: (04/11/2026, P6) aba da corrida 21; o id entra junto com a seção (secao_cenarios).
        # ! Motivo: o ensaio dos cenários da Fase 5 é a sexta análise da Fase 4 e, pela regra do painel, vira uma aba.
        ("cenarios", "Cenários da Fase 5", "Quanto tempo o agente leva da detecção ao resultado nos dez cenários da ficha 36 e em quantos acerta? As corridas 21 e 21b, o ensaio de uma repetição: tempo até o resultado, quantos chegaram a ele, a ficha da falha de cada cenário e o protocolo da medida com pessoas."),
        # ! Alteração de IA - Revisar: (04/11/2026, P7) aba da corrida 22; o id entra junto com a seção (secao_trilha).
        # ! Motivo: a avaliação da própria trilha é a sétima análise da Fase 4 e, pela regra do painel, vira uma aba.
        ("trilha", "Avaliação da trilha", "A trilha do agente aponta os erros reais e o passo certo quando a falha é injetada de propósito? A corrida 22 nos 36 casos de avaliação: os sinais de alerta, as mudanças de propósito na entrada e a amostra de relatórios da sessão de revisão."),
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


def secao_comparativo(cq: dict, blocos_cq: dict, md_para_html, road: dict, cartoes_corridas, analise3b: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e parágrafos à vista da aba reescritos em frases curtas, sem p, b/c, hit@3, L1 nem "casos discordantes".
    # ! Motivo: o texto à vista trazia siglas e números soltos (p de McNemar, b/c, hit@3, L1, P(top-1)) que o Eric pediu para tirar; os números continuam nas tabelas recolhidas.
    meta = cq["metadados"]
    LA, LB =meta["melhor_L_nos_36"][A], meta["melhor_L_nos_36"][B]
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
    # ! Alteração de IA - Revisar: (23/10/2026) a repetição dos inéditos (corrida 15) entra no cartão, na frase de abertura e numa seção
    # própria; o veredito da ficha 21 (saldo do Coder dentro ou fora da variação entre corridas iguais) é lido de analise_fase3b.json.
    # ! Motivo: o Eric escolheu repetir a corrida antes de decidir (ficha 21, opção b); a aba precisa mostrar a repetição ao lado da corrida 7
    # e dizer o que ela decidiu, sem número digitado.
    r1 = {x["L"]: x for x in cq.get("confronto_ineditos_repeticao", [])}.get(1)
    rep_an = next((x for x in (analise3b or {}).get("repeticao", {}).get("entre_modelos", []) if x["modelo"] == B and x["biblioteca_epoca"] == 1), None)
    if rep_an:
        veredito = (f'a diferença cabe na variação normal entre corridas iguais (até {rep_an["limiar_ruido"]} casos) e a decisão 52 fica (decisão 73)' if rep_an["dentro_da_variacao"]
                    else f'a diferença passa em um caso a variação normal entre corridas iguais (até {rep_an["limiar_ruido"]} casos), mas não separa os dois; '
                         f'nos 72 casos nunca vistos o Coder acerta sozinho {rep_an["somados"]["b"]} e o qwen {rep_an["somados"]["c"]}. A decisão 52 fica, '
                         'com o saldo registrado como limitação declarada (decisão 73)')
        frase_rep = (f' Na <strong>repetição de 23/10</strong> (corrida 15, Ollama 0.40.2, a biblioteca que cada um escreveu), {r1["so_coder"]} casos só o Coder acertou contra {r1["so_qwen"]} só o qwen: '
                     f'saldo {rep_an["saldo"]:+d}, contra {rep_an["saldo_original"]:+d} na corrida 7. {veredito[0].upper() + veredito[1:]}.') if r1 else ""
    else:
        frase_rep = ""
    frase_ineditos = (f'Nos <strong>36 inéditos</strong> (corrida 7, 06/10) o Coder fica à frente com L0 e L1 (com a L1 de cada um, {i1["so_coder"]} casos só dele contra '
                      f'{i1["so_qwen"]} só do qwen, p = {fmt(i1["p_mcnemar"], 3)}) e atrás com L3; nos 72 casos com L1 o placar empata. É a condição 1 do que mudaria a decisão 52, '
                      'parcialmente cumprida e dentro do ruído: o que fazer com ela era a ficha 21.' + frase_rep if i1 else "")
    itens_kpi = [
        ("Onde o Coder fica à frente", str(n_vence), f"cenários, todos por pouco (até {pp(max_delta)}); {n_vence_36} nos 36 nunca vistos"),
        ("36 nunca vistos, 1ª corrida (06/10)", f'{i1["so_qwen"]} × {i1["so_coder"]}' if i1 else "não rodou", f'só o qwen × só o Coder; acerto {fmt(i1["acerto_A"])}% × {fmt(i1["acerto_B"])}%' if i1 else "corrida 7"),
        ("36 nunca vistos, repetição (23/10)", f'{r1["so_qwen"]} × {r1["so_coder"]}' if r1 else "não rodou",
         ('só o qwen × só o Coder' + (f'; saldo {rep_an["saldo"]:+d}' if rep_an else "")) if r1 else "corrida 15"),
        ("Melhor versão nos 36 nunca vistos", f"{fmt(melhor_A)}% × {fmt(melhor_B)}%", "acerto de cada um com a sua melhor versão"),
        ("Disputa nos 36 de avaliação", f'{c1["so_qwen"]} × {c1["so_coder"]}', f'só o qwen × só o Coder; {c1["ambos"]} acertados pelos dois'),
        ("Edições aceitas na 1ª época", f'{doc1["aceitas_A"]} × {doc1["aceitas_B"]}', f'de {doc1["propostas_A"]} × {doc1["propostas_B"]} propostas; corretas na revisão {fmt(corr["A"])}% × {fmt(corr["B"])}%'),
        ("Verbete certo entre os três (90)", f'{fmt(rec1["hit3_90_A"])}% × {fmt(rec1["hit3_90_B"])}%', f'com a 1ª versão de cada um ({rec1["verbetes_A"]} × {rec1["verbetes_B"]} verbetes)'),
        ("Chance de o Coder ser o 1º", f"≤ {fmt(100 * p_max_B)}%", f'1º em {est.get(B, 0)} × {est.get(A, 0)} de {cq["decisao"]["total_rankings"]} ordenações; {fmt(l1["s_A"])} × {fmt(l1["s_B"])} s por diagnóstico'),
    ]
    corridas = cartoes_corridas(road, numeros=["1", "7", "14", "15"], sufixo="-cq")
    html_ = f'''<section id="comparativo" hidden>
<h1>qwen2.5:7b × qwen2.5-coder:7b: em que cenários o Coder seria melhor?</h1>
<p class="lead">Pergunta do Eric em 29/09: "pode ser que em alguns cenários o coder seja mais interessante". Resposta: o Coder fica à frente em <strong>{n_vence} células</strong>, todas pequenas (a maior por {pp(max_delta)}) e quase todas nos 54 casos de aprendizado e nas classes léxica, runtime e efeito. Nos <strong>36 casos nunca vistos</strong> o qwen2.5:7b vence em todas as versões da biblioteca ({fmt(melhor_A)}% × {fmt(melhor_B)}% na melhor versão de cada um), e em nenhuma ordenação o Coder tem chance real de ser o primeiro (P(top-1) ≤ {fmt(100 * p_max_B)}%). Como escritor, o Coder é mais contido e mais certo ({fmt(corr["B"])}% de edições corretas contra {fmt(corr["A"])}%). A decisão 52 fica. {frase_ineditos}</p>
{kpis(itens_kpi)}
<h2>A trajetória dos dois pelas três fases</h2>
<p>Os mesmos casos, da Fase 2-A (sem documentação, máquina de desenvolvimento) à Fase 3 (biblioteca editada pelo próprio modelo). Nos 36 de avaliação, o qwen abre vantagem a partir da primeira versão da biblioteca escrita pelo modelo (L1); nos 90 as curvas se cruzam.</p>
<div class="controles"><label>Conjunto <select id="sel-cq-conj"><option value="36">36 de avaliação</option><option value="90">90 (todos)</option></select></label>
<label>Métrica <select id="sel-cq-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-cq-traj"></canvas></div>
<h2>Quem acerta o que o outro erra</h2>
<p>Em cada condição, as barras mostram os casos em que só um dos dois acertou. Nos 36 de avaliação com a primeira versão (L1), {c1["so_qwen"]} casos são só do qwen e {c1["so_coder"]} só do Coder; {c1["ambos"]} foram acertados pelos dois. A diferença cabe na variação normal: não separa os dois.</p>
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
<h2>Se o verbete certo chega entre os três entregues, e as trocas de causa respondida</h2>
<p>Com a primeira versão escrita pelo Coder (L1), o verbete certo chega entre os três entregues em {fmt(rec1["hit3_90_B"])}% dos 90 casos, contra {fmt(rec1["hit3_90_A"])}% com a do qwen. A biblioteca menor e sem verbetes novos não atrapalha a busca (BM25).</p>
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
<p>O Coder 7B diagnosticou os mesmos 36 casos nunca vistos que o qwen rodou em 28/09, com a biblioteca original e com as versões que ele mesmo escreveu. A tabela mostra caso a caso, por versão e por classe.</p>
{B_("cq_ineditos")}
{detalhes("Por classe, com a L1 de cada um", B_("cq_ineditos_classe"))}
<h2>Repetição nos 36 inéditos (corrida 15, 23/10/2026)</h2>
<p>Os dois modelos repetiram os mesmos 36 casos nunca vistos, cada um com a primeira versão da biblioteca que ele mesmo escreveu, numa corrida só e no Ollama 0.40.2, depois da ponte de versão (corrida 14). A primeira tabela compara os dois; a segunda mostra quanto cada modelo mudou sozinho contra a própria corrida original (corrida 2 para o qwen, 7 para o Coder).{(" " + frase_rep.strip()) if frase_rep else ""}</p>
{B_("cq_ineditos_repeticao")}
{detalhes("Cada modelo contra a própria corrida original", B_("cq_repeticao_vs_original"))}
{detalhes("Por classe, na repetição", B_("cq_ineditos_repeticao_classe"))}
<h2>As corridas desta pergunta</h2>
{corridas}
{fontes(["<code>comparativo-qwen25-7b-vs-coder-7b.md</code> (Memorial, 3-resultados-e-analises)", "<code>comparativo_qwen_coder.json</code> e <code>.md</code> gerados por <code>comparar_qwen_coder.py</code> (--check)", "<code>analise_fase3b.json</code>, bloco <code>repeticao</code> (saldo contra a variação entre corridas iguais)", "achados 4.38, 4.52 e 4.53; decisões 52 e 73"])}
</section>'''
    return dados, html_


# ------------------------------------------------------------------ 2. Fase 3-B

def secao_tres_b(ined: dict, dados: dict, road: dict, cartoes_corridas, md_doc_para_html, an: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e parágrafos à vista reescritos sem b/c, p, hit@3, L0/L1/L3 soltos nem setas.
    # ! Motivo: o texto à vista trazia siglas e números soltos (b + c, p de McNemar, hit@3) que o Eric pediu para tirar; os números continuam nas tabelas recolhidas.
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
        (f"{A} nos 36 nunca vistos", " / ".join(f'{fmt(q[L]["acerto"])}%' for L in Ls), "com a biblioteca original, a 1ª e a 3ª versão"),
        (f"{COD3B} nos 36 nunca vistos", " / ".join(f'{fmt(cur[COD3B][L]["acerto"])}%' for L in Ls) if COD3B in cur else "—", "a biblioteca que ele escreveu não muda o acerto"),
        (f"Versão {L_ult} contra a original, no qwen", pp(p_ult.get("delta_pp")), f'só a versão {L_ult} acertou {p_ult.get("b", "—")} casos; só a original, {p_ult.get("c", "—")}'),
        ("Verbete certo entre os três (qwen)", " / ".join(f'{fmt(rec[A][L])}%' for L in Ls), f'nos 36 nunca vistos; nos 36 oficiais: ' + " / ".join(f'{fmt(rec_of[A][L])}%' for L in Ls)),
        ("Ponte de versão", f"{n_par} de {len(ult['linhas'])} pareáveis", f"no Ollama {ult['versao']}; pareável = até 2 casos em que só um lado acertou"),
        ("Corridas da 3-B", f"{n_feitas} feitas · {n_pend} pendentes", f"{n_opc} opcionais"),
    ]
    # ! Alteração de IA - Revisar: (06/10/2026) as duas corridas opcionais, rodadas pelo Eric em 06/10, entram na aba lidas de
    # analise_fase3b.json: o Coder 7B contra o qwen nos mesmos inéditos (corrida 7) e a adesão cega com a L3 própria (corrida 5).
    # ! Motivo: sem isto a aba diria que as corridas eram opcionais e não rodadas, e os números ficariam só no relatório.
    entre = (an or {}).get("ineditos", {}).get("entre_modelos", [])
    a5 = (an or {}).get("a5", {}).get("linhas", [])
    c7 = {x["biblioteca_epoca"]: x for x in entre if x["modelo"] == B}
    if B in cur:
        itens_kpi.insert(2, (f"Coder 7B nos 36 nunca vistos (06/10)", " / ".join(f'{fmt(cur[B][L]["acerto"])}%' for L in Ls),
                             f'só o Coder acertou {c7[1]["b"]}, só o qwen {c7[1]["c"]}; nos 72, {c7[1]["somados"]["b"]} e {c7[1]["somados"]["c"]}' if 1 in c7 else "sem confronto"))
    if a5:
        itens_kpi.insert(3, ("Seguiu a causa errada plantada (06/10)", " · ".join(f'{fmt(l["seguiu_pct"])}%' for l in a5),
                             "; ".join(f'{NOME_CURTO.get(l["modelo"], l["modelo"])}: {l["seguiu"]} de {l["n"]}' for l in a5)))
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
                              'ele mesmo escreveu; o qwen e o Coder 3B tinham rodado em 28/09. A tabela conta os casos que só o modelo da linha acertou e os que só o qwen acertou; as colunas '
                              'por classe trazem os acertos do modelo e do qwen nos 6 casos da classe.</p>' + tab_entre if entre else "")
                           + ('<h3>Se o modelo segue a documentação errada, com a biblioteca que ele escreveu (corrida 5)</h3><p>Neste teste o contexto afirma uma causa errada para o sintoma e '
                              'nunca traz o verbete certo. Na Fase 2-B isso foi medido com a biblioteca original; aqui cada modelo leu a 3ª versão que ele mesmo escreveu (L3), nos 36 oficiais.</p>' + tab_a5 if a5 else ""))
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
<h2>O verbete certo chega entre os três entregues? Nos casos nunca vistos</h2>
<p>O gráfico mostra com que frequência o verbete certo está entre os três entregues ao modelo. Nos casos nunca vistos o recuperador acerta menos e piora com as notas acrescentadas; nos oficiais fica estável.</p>
<div class="chart baixo"><canvas id="g-tb-rec"></canvas></div>
{tab_par}
{"<h2>Oficiais e inéditos somados (72 casos)</h2><p>Cada versão da biblioteca contra a original, nos dois conjuntos e na soma. A tabela conta os casos em que só a versão nova acertou e os em que só a original acertou.</p>" + tab_agrupado if agrupado else ""}
{bloco_opcionais}
<h2>Ponte de versão do Ollama</h2>
<p>A bateria oficial rodou no Ollama 0.34.0, e o Ollama se atualiza sozinho. A cada versão nova, a ponte repete a biblioteca original nos 36 casos e compara caso a caso com a Fase 3. Se até 2 casos mudam de lado (só a ponte ou só a Fase 3 acertou), as corridas dessa versão são pareáveis com a Fase 3. Acima disso, o modelo é lido contra a própria ponte e a ressalva vai para o relatório (decisão 47).</p>
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
    # ! Alteração de IA - Revisar: (05/11/2026) cartões e parágrafos à vista reescritos sem hit@3, hit@5, embedding solto nem "harness".
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; os números continuam nas tabelas e nos gráficos.
    res =rec["resultados"]
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
        (f"Busca por palavras com sinais, BM25 ({conj0})", f'{fmt(v0[bm25]["hit@3"])}%', f'verbete certo entre os três; entre os cinco, {fmt(v0[bm25]["hit@5"])}%'),
        *([(f"{melhor_hib} ({conj0})", f'{fmt(v0[melhor_hib]["hit@3"])}%', "o melhor híbrido, entre os três")] if melhor_hib else []),
        *[(f"{m} ({conj0})", f'{fmt(v0[m]["hit@3"])}%', "verbete certo entre os três") for m in sorted(denso, key=lambda m: -v0[m]["hit@3"])][:2],
        (f"Busca por palavras (BM25) nos {conj_ined}", f'{fmt(val[bib0][conj_ined][bm25]["hit@3"])}%', "entre os três, em casos que a Fase 3 nunca viu"),
        ("Classe tradução (BM25)", f"{fmt(trad)}%", "a classe mais fraca, entre os três"),
    ]
    html_ = f'''<section id="recuperador" hidden>
<h1>Recuperador: vale trocar a busca por palavras por uma busca por significado?</h1>
<p class="lead">Não, nesta medição. A decisão 55 tinha adotado a recuperação híbrida pela literatura, sem medida própria. Medido offline com o <code>{esc(rec["metadados"]["embedding"])}</code> nos 90 casos oficiais e nos 36 inéditos, o BM25 com sinais em código chega a {fmt(v0[bm25]["hit@3"])}% de hit@3 ({fmt(v0[bm25]["hit@5"])}% em hit@5), o embedding denso a {", ".join(fmt(v0[m]["hit@3"]) + "%" for m in denso)} e o híbrido a {", ".join(fmt(v0[m]["hit@3"]) + "%" for m in hib)}: o híbrido fica <strong>abaixo do BM25 sozinho</strong>. A recuperação híbrida saiu do desenho da Fase 4 (decisão 61); o ganho barato a medir é k = 5.</p>
{kpis(itens_kpi)}
<h2>Os métodos, lado a lado</h2>
<p>Consulta em termos usa os sinais que o código extrai do caso (rota, campos, mensagens); consulta em texto usa o caso escrito por extenso. A busca por significado (embedding) só funciona razoavelmente com os termos, e mesmo assim fica longe do BM25.</p>
<div class="controles"><label>Biblioteca <select id="sel-rec-bib">{"".join(f'<option value="{esc(b)}">{esc(b)}</option>' for b in bibs)}</select></label>
<label>Métrica <select id="sel-rec-met"><option value="hit@3">hit@3</option><option value="hit@1">hit@1</option><option value="hit@5">hit@5</option><option value="mrr">MRR</option></select></label></div>
<div class="chart"><canvas id="g-rec-met"></canvas></div>
<h2>Por classe de defeito</h2>
<p>Quantas vezes o verbete certo vem entre os três entregues, por classe, na biblioteca original. A classe tradução (mapeamento entre camadas) é a mais fraca em todos os métodos; os sinais em código continuam sendo o caminho para ela.</p>
{tab_classes(conj0)}
{tab_classes(conj_ined)}
{detalhes(f"Tabela completa ({len(res)} combinações)", completa)}
{leitura([
    "O corpus é pequeno (dezenas de verbetes curtos) e a consulta é técnica e em português: a busca lexical com sinais extraídos por código vence a semântica.",
    "Trocar o modelo de busca por significado (embedding) só faria sentido se a Fase 4 mostrasse necessidade; por ora, nada muda no próprio teste.",
])}
{fontes(["<code>resultados_alvo/recuperador/experimento_recuperador.json</code> e <code>.md</code> (<code>experimento_recuperador.py</code>, --check)", "achado 4.39; decisão 61; ficha 11(f)"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 5. ablação base × instruct

def secao_ablacao(abl: dict, ref3b_90, ref3b_ined) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões e parágrafo à vista reescritos sem "(A0)/(A2)", "rótulo" nem "acurácia balanceada".
    # ! Motivo: o texto à vista trazia siglas e termos de método que o Eric pediu para tirar; os números seguem na tabela recolhida.
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
        ("Base, sem biblioteca", f'{fmt(g[(base, "A0")]["causa_correta_pct"])}%', f'formato certo em {fmt(g[(base, "A0")]["formato_valido_pct"])}%'),
        ("Base, com biblioteca", f'{fmt(g[(base, "A2")]["causa_correta_pct"])}%', f'formato certo em {fmt(g[(base, "A2")]["formato_valido_pct"])}%; causa inventada em {fmt(g[(base, "A2")]["fora_do_conjunto_pct"])}%'),
        ("Instruct 0,5B, sem biblioteca", f'{fmt(g[(inst, "A0")]["causa_correta_pct"])}%', f'formato certo em {fmt(g[(inst, "A0")]["formato_valido_pct"])}%'),
        ("Instruct 0,5B, com biblioteca", f'{fmt(g[(inst, "A2")]["causa_correta_pct"])}%', f'o formato certo cai para {fmt(g[(inst, "A2")]["formato_valido_pct"])}%'),
        ("Referência: qwen2.5-coder:3b", f"{fmt(ref3b_90)}%", f"nos 90 casos; {fmt(ref3b_ined)}% nos nunca vistos"),
    ]
    html_ = f'''<section id="ablacao" hidden>
<h1>Sem ajuste por instrução, o modelo faz a tarefa?</h1>
<p class="lead">Não. O piso metodológico pedido na ficha 11(d): o <code>qwen2.5:0.5b-base</code> (só pré-treinado) e o <code>qwen2.5:0.5b-instruct</code> (mesmo porte, com ajuste por instrução) nos 90 casos, sem biblioteca (A0) e com a biblioteca recuperada (A2). O base acerta <strong>0 de 90</strong> nas duas condições: com a biblioteca ele copia a forma dos verbetes ({fmt(g[(base, "A2")]["formato_valido_pct"])}% no formato) mas inventa o rótulo em {fmt(g[(base, "A2")]["fora_do_conjunto_pct"])}% dos casos. O instruct de 0,5B chega a {fmt(g[(inst, "A0")]["causa_correta_pct"])}% e piora com a biblioteca. O ajuste por instrução é condição necessária, não suficiente: o piso da família está no porte.</p>
{kpis(itens_kpi)}
<h2>Acertar, responder no formato e inventar o rótulo</h2>
<p>Responder no formato e acertar são coisas diferentes, e o gráfico separa as duas. Ele também conta as causas inventadas, fora da lista permitida. A biblioteca no prompt ensina a forma ao modelo base, não o conteúdo.</p>
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
    tópicos ainda não rodaram, o trecho dos mapas e os números das subseções de rejeitadas e de mapas, lidos do
    próprio arquivo (§6.14.15 e §6.14.16 desde 23/10/2026; eram §6.14.12 e §6.14.13)."""
    # ! Alteração de IA - Revisar: (23/10/2026) o número da subseção dos mapas (e o das rejeitadas) passou a ser lido do
    # arquivo por expressão regular, em vez do literal "#### 6.14.13".
    # ! Motivo: com os três tópicos acrescentados à parte B em 23/10/2026, as duas subseções finais do levantamento
    # mudaram de número (§6.14.15 e §6.14.16); com o literal antigo a aba do colibri deixaria de achar o mapa.
    lev = (lev or "").replace("\r\n", "\n")
    m_mapas = re.search(r"^#### (6\.14\.\d+) Mapas adotado", lev, re.M)
    if not m_mapas:
        return None
    m_rej = re.search(r"^#### (6\.14\.\d+) Afirmações rejeitadas", lev, re.M)
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
    return {"secoes": _secoes_do_levantamento(lev), "parte_a": parte_a, "faltam": faltam, "mapas": lev[m_mapas.start():],
            "secao_mapas": m_mapas.group(1), "secao_rejeitadas": m_rej.group(1) if m_rej else "",
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
                + (f', e {falta_r5} tópicos da parte B (raciocínio aberto, memória e visualização) ainda por rodar' if falta_r5 else '')
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
<h2>As afirmações, rodada a rodada</h2>
<div class="chart baixo"><canvas id="g-pe-rodadas"></canvas></div>
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
    por_afirmacoes: dict[str, dict] = {}
    for t_ in topicos:
        r_ = por_afirmacoes.setdefault(t_["curto"], {"rodada": t_["curto"], "aprovadas": 0, "rejeitadas": 0, "nao_verificadas": 0})
        for chave_ in ("aprovadas", "rejeitadas", "nao_verificadas"):
            r_[chave_] += t_[chave_]
    return {"rodadas": list(por_afirmacoes.values())}, html_


# ------------------------------------------------------------------ 7. ferramental

def secao_ferramental(med: dict | None, readme: str) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) a tabela de ferramentas vem de DETALHES-TECNICOS.md (o parâmetro continua `readme`, o texto que traz a seção "Ferramentas de apoio").
    # ! Motivo: a seção saiu do README para o documento técnico, a pedido do Eric.
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
{fontes(["<code>DETALHES-TECNICOS.md</code> (tabela das ferramentas)", "<code>5-metodo-e-ferramental/ferramental-do-claude-code.md</code> §7.2 e §7.9", "<code>5-metodo-e-ferramental/dados/medicao-permanencia-mcp.json</code>", "decisões 49 e 62"])}
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
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos sem b/c, p, L0/L1 soltos, "rótulo", setas nem o "(4 casos)" digitado à mão.
    # ! Motivo: o texto à vista trazia siglas e números soltos que o Eric pediu para tirar; o "4 casos" estava escrito no texto em vez de vir dos dados, e os números seguem nas tabelas recolhidas.
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
    itens_kpi = [(f"{nome(m)} lendo a biblioteca do {nome(doador)}", f'de {fmt(cel[(m, "ponte", 0)]["acerto_pct"])}% para {fmt(cel[(m, "cruzada", 1)]["acerto_pct"])}%',
                  f'contra a biblioteca original: {_saldo_txt(par[(m, 1, "l0_ponte")]["b"], par[(m, 1, "l0_ponte")]["c"])}') for m in leitores]
    itens_kpi += [
        ("A mesma biblioteca, lida por quem a escreveu", f'{fmt(q1["acerto_pct"])}%', "contra ele: " + "; ".join(f'{nome(m)} {_saldo_txt(par[(m, 1, "doador")]["b"], par[(m, 1, "doador")]["c"])}' for m in leitores)),
        (f"Causa que o {nome(pior)} passa a responder", f'de {r_pior["respostas_no_rotulo_com_l0"]} para {r_pior["respostas_no_rotulo"]} respostas',
         f'{r_pior["rotulo_mais_frequente"]}; ' + ("nenhum dos 36 casos tem essa causa" if r_pior["casos_com_esse_gabarito"] == 0 else f'{r_pior["casos_com_esse_gabarito"]} dos 36 casos têm essa causa')),
        ("Contextos com nota do doador", f'{fmt(cel[(pior, "cruzada", 1)]["contexto_com_nota_pct"])}%',
         "na própria: " + "; ".join(f'{nome(m)} {fmt(cel[(m, "fase3", 1)]["contexto_com_nota_pct"])}%' for m in leitores)),
        ("Variação entre corridas iguais", f'{min(x["discordantes_mesma_entrada"] for x in ruido)} a {max(x["discordantes_mesma_entrada"] for x in ruido)} casos',
         f'em 36, saldo de até {max(abs(x["b_mesma_entrada"] - x["c_mesma_entrada"]) for x in ruido)}; régua para os saldos acima'),
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
        f'<strong>O ganho não é da biblioteca sozinha.</strong> Lida por quem a escreveu, a primeira versão (L1) rende {fmt(q1["acerto_pct"])}%. Lida pelo {esc(nome(melhor))}, fica com {_saldo_txt(par[(melhor, 1, "l0_ponte")]["b"], par[(melhor, 1, "l0_ponte")]["c"])} '
        f'sobre a biblioteca original, dentro da variação entre corridas ({len(par[(melhor, 1, "l0_ponte")]["em_casos_que_oscilam"])} das {par[(melhor, 1, "l0_ponte")]["b"] + par[(melhor, 1, "l0_ponte")]["c"]} trocas caem em casos que já '
        f'oscilam sozinhos). Lida pelo {esc(nome(pior))}, fica com {_saldo_txt(par[(pior, 1, "l0_ponte")]["b"], par[(pior, 1, "l0_ponte")]["c"])}: é o único saldo fora dessa variação, e ainda assim pequeno demais para valer como prova.',
        f'<strong>No {esc(nome(pior))} as notas do doador são lidas e seguidas, para pior.</strong> Ele passa a responder <code>{esc(r_pior["rotulo_mais_frequente"])}</code> ({r_pior["respostas_no_rotulo_com_l0"]} respostas com a biblioteca original, {r_pior["respostas_no_rotulo"]} com a do doador), '
        + ("causa que nenhum dos 36 casos tem" if r_pior["casos_com_esse_gabarito"] == 0 else f'causa de {r_pior["casos_com_esse_gabarito"]} dos 36 casos') + (f', e cita <code>{esc(fonte_top["verbete"])}</code> como fonte em {fonte_top["respostas"]} respostas' if fonte_top else "") +
        f'. Em {no_rotulo} das {len(perdas_pior)} perdas a resposta nova é essa causa, e em {com_ouro} das {len(perdas_pior)} o verbete certo estava no contexto: nessas, a falha é de uso, não de busca. '
        f'A causa respondida muda em {par[(pior, 1, "l0_ponte")]["rotulos_diferentes"]} das 36 respostas; entre corridas iguais dele muda de {min(x["rotulos_diferentes"] for x in ruido if x["modelo"] == pior)} a '
        f'{max(x["rotulos_diferentes"] for x in ruido if x["modelo"] == pior)}.',
        f'<strong>O que a cruzada não separa.</strong> O ganho medido na Fase 3 não acompanha a biblioteca quando muda quem a lê, mas o {esc(nome(doador))} não leu a biblioteca de outro modelo: não dá para dizer se o ganho é '
        "do par (o modelo com a biblioteca que ele mesmo escreveu) ou do leitor. E o ganho dele com a biblioteca que ele mesmo escreveu também cabe na variação normal.",
        f'<strong>O que fica para a Fase 4.</strong> O padrão do agente é o {esc(nome(doador))} com a biblioteca que ele mesmo escreveu (decisão 69): trocar o modelo que lê exige medir de novo, e a ideia de escrever com o melhor '
        "modelo e ler com o mais barato sai. Uma nota em verbete que aparece em quase metade dos contextos alcança quase metade dos diagnósticos.",
    ]
    numeros = [c.numero for c in road["corridas"] if c.saida in (meta["fontes"]["cruzada"], meta["ponte_de_base"])]
    html_ = f'''<section id="cruzada" hidden>
<h1>Troca cruzada: o ganho é da biblioteca ou de quem a lê?</h1>
<p class="lead">Não é da biblioteca sozinha. Os dois Coder diagnosticaram os mesmos 36 casos, com o mesmo prompt e a mesma busca, lendo a biblioteca escrita pelo {esc(nome(doador))}. {esc("; ".join(frases))}. Lida por quem a escreveu, a mesma L1 rende {fmt(q1["acerto_pct"])}%. O ganho medido na Fase 3 não acompanha a biblioteca quando muda quem a lê.</p>
{kpis(itens_kpi)}
<h2>Acerto por versão da biblioteca, por quem lê</h2>
<p>Linha cheia: a biblioteca escrita pelo {esc(nome(doador))} (no primeiro ponto, a biblioteca original; para os dois Coder, medida na ponte em Ollama {esc(versao)}). Linha tracejada: cada Coder lendo a biblioteca que ele mesmo escreveu, na Fase 3. Se o ganho fosse da biblioteca, as linhas cheias subiriam juntas.</p>
<div class="controles"><label>Métrica <select id="sel-cz-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-cz-leit"></canvas></div>
<h2>Casos ganhos e perdidos contra a biblioteca original, no mesmo modelo</h2>
<p>Cada barra compara um modelo com uma versão da biblioteca contra ele mesmo com a biblioteca original: à direita os casos que passou a acertar, à esquerda os que deixou de acertar. Os dois Coder são comparados na mesma versão do Ollama (ponte de 30/09); o {esc(nome(doador))}, dentro da Fase 3.</p>
<div class="chart"><canvas id="g-cz-trocas"></canvas></div>
<h2>Cada comparação, uma a uma</h2>
<p>A tabela conta os casos que só o leitor com a biblioteca do doador acertou e os que só o outro lado acertou. Só a comparação contra a ponte é feita na mesma versão do Ollama e com o mesmo texto dos casos; as outras duas cruzam versões e, para o Coder 7B, não são pareáveis (decisão 47). Nelas, a coluna "sem o caso de texto corrigido" tira o efe-3, corrigido em 28/09.</p>
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
<p>Cada síntese foi escrita só com as afirmações que sobreviveram à verificação. As referências completas e as afirmações rejeitadas, com o motivo, estão no levantamento (§{lit["secao_rejeitadas"]}) e em <code>referencias.md</code>.</p>
{sinteses}'''
    cartoes = [("Opções avaliadas pela literatura", f'{cont["adotado"]} adotadas', f'{cont["adiado"]} adiadas · {cont["descartado"]} descartadas, de {n} no mapa da rodada 5')]
    fonte = f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code> (§{secoes[0]["secao"]} a §{secoes[-1]["secao"]} e mapa em §{lit["secao_mapas"]})' if secoes else None
    return bloco, cartoes, fonte


def secao_colibri(v: dict | None, amostra: dict | None, road: dict, cartoes_corridas, levantamento: str | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões de RAM, leitura do disco e resposta em máquina parecida encurtados, e "rótulo" trocado por "causa respondida" no texto à vista.
    # ! Motivo: os cartões passavam de 90 caracteres com detalhes que já estão nas tabelas recolhidas (leituras, blocos, threads); o texto usava "rótulo", termo que o Eric pediu para tirar.
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
        ("RAM instalada", f'{fmt(instalada)} GB', f'o sistema enxerga {fmt(maq["ram_gb"], 2)} GB; o GLM-5.2 pede {glm["ram_min_gb"]} GB no mínimo'),
        ("Disco livre", f'{fmt(maq["disco_livre_gb"])} GB', f'o GLM-5.2 pede {_milhar(glm["disco_gb"])} GB'),
        ("Velocidade de leitura do disco (NVMe)", f'{fmt(nvme["gb_por_s"], 2)} GB/s', f'medida sem usar o cache do sistema ({dm["blocos"]} leituras de {dm["bloco_bytes"] // 2**20} MB)'),
        ("Uma resposta nossa em máquina parecida", f'{fmt(perto["minutos_por_resposta"])} min', f'só gerar, a {fmt(perto["tok_por_s"], 2)} token/s ({perto_partes[0]}); hoje o diagnóstico inteiro leva {fmt(seg_hoje)} s'),
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
<p>Amostra de ferramenta, com o <code>{esc(ma["modelo"])}</code> no caso <code>{esc(ma["caso"])}</code> e a versão {ma["biblioteca_epoca"]} da biblioteca que ele escreveu, no Ollama {esc(ma["versao_ollama"])}; não é resultado de corrida. O Ollama devolve, para cada token que o modelo escreve, a probabilidade que ele deu a esse token e às alternativas. Abaixo, a primeira linha da resposta, token a token; o símbolo <code>␣</code> marca um espaço.</p>
<div class="toks">{"".join(tok(t) for t in am["linha"])}</div>
<p>O modelo decide a causa no primeiro token depois de <code>CAUSA_RAIZ:</code>; daí em diante o resto da causa respondida sai quase certo. Nesse ponto, as opções que ele pesou foram estas:</p>
<div class="tabela estreita"><table><thead><tr><th>Token candidato</th><th>Probabilidade</th></tr></thead><tbody>{linhas_alt}</tbody></table></div>
<p>É esse número que a corrida 12 grava para os 72 casos: se a probabilidade da causa respondida for baixa justamente onde o modelo erra, ela serve de aviso para chamar um humano.</p>
{detalhes("O que a sonda conferiu", tab_conf)}'''

    leitura_itens = [
        f'<strong>O que barra os modelos grandes aqui é o espaço em disco e a RAM, não a velocidade do disco.</strong> O NVMe entrega {fmt(nvme["gb_por_s"], 2)} GB/s, o que daria cerca de {fmt(nvme["segundos_por_token_frio"])} s de leitura por token do GLM-5.2. Mas o modelo pede {_milhar(glm["disco_gb"])} GB de disco e a máquina tem {fmt(maq["disco_livre_gb"])} GB livres. Na RAM, os {fmt(instalada)} GB instalados são exatamente o mínimo que o repositório declara para ele, e cerca de {fmt(maq["ram_livre_no_inicio_de_corrida_gb"])} GB ficam livres no início de uma corrida.',
        f'<strong>Mesmo onde ele roda, o tempo não serve ao agente.</strong> Nas máquinas parecidas com a nossa em que o repositório publica medida, uma resposta de {fmt(tokens, 0)} tokens levaria de {fmt(min(min_glm))} a {fmt(max(min_glm))} minutos só para ser gerada. Hoje o diagnóstico inteiro leva {fmt(seg_hoje)} s.',
        ("<strong>O único modelo que roda com folga não é candidato a motor do agente.</strong> " + ", ".join(f'{f["nome"]} ({_milhar(f["parametros_bi"])} bilhões de parâmetros no total, {_milhar(f["ativos_bi"])} em uso a cada token)' for f in rodam)
         + " cabe na máquina, mas trocar de modelo exige medir de novo (decisão 69). Ele entra na corrida 13 só como material do atlas."),
        "<strong>Disco comum e HD.</strong> O repositório não publica medida em HD. Pela leitura por token que ele declara, só o disco custaria "
        + " e ".join(f'{fmt(c["segundos_por_token_frio"])} s por token em {c["disco"].split(" (")[0]}' for c in premissas) + " (velocidades postas como premissa, não medidas).",
        "<strong>O que se aproveita sem trocar de motor</strong> é a ideia da escolha fechada por probabilidade: em vez de só ler a causa que o modelo escreveu, ler também a probabilidade que ele deu a ela. O nosso diagnóstico é uma escolha entre 23 causas, e o Ollama instalado já devolve esse número."
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
        # ! Alteração de IA - Revisar: (05/11/2026) linha começada por "- " vira item de lista, com o mesmo montador dos documentos do painel.
        # ! Motivo: as linhas da lista do Rastro no relatório v2 caíam no parágrafo e saíam coladas umas nas outras na página da sessão de revisão.
        if re.match(r"^\s*- ", l):
            fecha()
            bloco, i = pt._lista(linhas, i)
            out.append(bloco)
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


# ! Alteração de IA - Revisar: (23/10/2026) bloco "O que a literatura sustenta para a arquitetura da trilha" da aba "Raciocínio
# aberto", lido do levantamento §6.14 (parte B, onda 1): o mapa de decisões de arquitetura com filtro por veredito, os
# riscos, a leitura e as cinco sínteses por extenso (fidelidade do raciocínio, trilha e observabilidade, relatório para
# humanos, atribuição ao contexto, uso das trilhas). Os mapas do §6.14 vêm um por Workflow, separados pelo nome em
# negrito ("Parte A: ...", "Parte B, onda 1: ...", "Parte B, onda 2: ..."); _blocos_dos_mapas os separa.
# ! Motivo: o Eric decide pelo painel, e a especificação da linha de raciocínio aberta (próximo passo) sai deste mapa;
# sem o bloco a análise ficaria só no levantamento. Nada é digitado aqui: tudo vem do arquivo gerado por
# integrar_pesquisa_pre_fase4.py, e a onda 2 (confiança, Brainiac, grafos, visualização) terá a sua própria aba.
TOPICOS_RACIOCINIO = ("r5-fidelidade-do-raciocinio", "r5-trilha-e-observabilidade", "r5-relatorio-para-humanos", "r5-atribuicao-ao-contexto", "r5-uso-das-trilhas")
TOPICOS_VISUALIZACAO = ("r5-confianca-por-probabilidade", "r5-brainiac-segundo-cerebro", "r5-codebase-memory-visual", "r5-visualizacao-da-rede-neural")


def _blocos_dos_mapas(trecho: str) -> dict[str, str]:
    """Os mapas do §6.14, um por Workflow, pelo nome em negrito que abre cada um; o valor é o texto até o mapa seguinte."""
    blocos = {}
    for m in re.finditer(r"^\*\*(Parte [^*\n]+)\*\*\n", trecho, re.M):
        inicio = m.end()
        prox = re.search(r"^\*\*Parte ", trecho[inicio:], re.M)
        blocos[m.group(1)] = trecho[inicio:inicio + prox.start()] if prox else trecho[inicio:]
    return blocos


def _mapa_de_um_bloco(bloco: str, id_tabela: str, rotulo: str) -> tuple[str, Counter, int, str, str]:
    """De um bloco de mapa (tabela, riscos, leitura): a tabela com filtro, a contagem por veredito, o número de linhas,
    a tabela de riscos e a leitura em HTML."""
    mapa, cont, n = _mapa_de_vereditos(bloco, id_tabela, rotulo)
    _, riscos, _ = pt.primeira_tabela(bloco[bloco.index("**Riscos**"):])
    tab_riscos = ('<div class="tabela"><table><thead><tr><th>Risco</th><th>Mitigação</th><th>Fonte</th></tr></thead><tbody>'
                  + "".join(f'<tr data-risco="{i}"><td>{pt.inline(r[0])}</td><td>{pt.inline(r[1])}</td><td class="nota">{pt.inline(r[2])}</td></tr>' for i, r in enumerate(riscos, 1))
                  + "</tbody></table></div>")
    leitura_md = bloco[bloco.index("**Leitura**") + len("**Leitura**"):].strip()
    return mapa, cont, n, tab_riscos, pt.md_doc_para_html(leitura_md)


def _sinteses_por_extenso(secoes: list[dict]) -> str:
    return "".join(
        f'<details data-sintese="{esc(s["chave"])}"><summary>§{s["secao"]} {esc(s["titulo"])} ({s["aprovadas"]} afirmações aprovadas)</summary>'
        f'<div class="relatorio">{pt.md_doc_para_html(s["texto"])}<h4>O que isso implica para o agente e para a Fase 4</h4>{leitura([pt.inline(x) for x in s["implicacoes"]])}'
        f'<h4>O que a literatura não responde</h4>{leitura([pt.inline(x) for x in s["lacunas"]])}</div></details>' for s in secoes)


def _literatura_do_raciocinio(lev: str | None) -> tuple[str, list[tuple[str, str, str]], str | None]:
    """Devolve o HTML do bloco, os cartões de número-chave que ele acrescenta e a linha de fonte."""
    lit = _pre_fase4_no_levantamento(lev)
    blocos = _blocos_dos_mapas(lit["mapas"]) if lit else {}
    nome = next((k for k in blocos if k.startswith("Parte B, onda 1")), None)
    if not lit or not nome or "ainda não rodou" in blocos[nome]:
        return ('<h2>O que a literatura sustenta para a arquitetura da trilha</h2>\n<p class="nota">A parte B da rodada 5 da pesquisa (raciocínio aberto) ainda não foi '
                'integrada ao levantamento, como §6.14.</p>'), [], None
    mapa, cont, n, tab_riscos, leitura_do_mapa = _mapa_de_um_bloco(blocos[nome], "tab-mapa-ra", "Filtro do mapa de arquitetura")
    secoes = [s for s in lit["secoes"] if s["chave"] in TOPICOS_RACIOCINIO]
    aprovadas, rejeitadas = sum(s["aprovadas"] for s in secoes), sum(s["rejeitadas"] for s in secoes)
    bloco_html = f'''<h2>O que a literatura sustenta para a arquitetura da trilha</h2>
<p>A parte B da rodada 5 da pesquisa (onda 1, 23/10/2026) leu a literatura sobre fidelidade do raciocínio escrito, formatos de trilha e exigências de registro, relatório para quem desenvolve, atribuição ao contexto e uso das trilhas para melhorar o sistema: {len(secoes)} tópicos, {aprovadas} afirmações aprovadas por verificadores céticos e {rejeitadas} {"rejeitada" if rejeitadas == 1 else "rejeitadas"}. O mapa dá o veredito de cada opção de arquitetura para esta máquina: <em>adotado</em> entra na arquitetura da linha de raciocínio aberta da Fase 4; <em>adiado</em> só com outra máquina, outro motor ou depois da Fase 4; <em>descartado</em> não serve, com o motivo.</p>
{mapa}
{detalhes("Riscos que a literatura aponta e a mitigação de cada um", tab_riscos)}
{detalhes("Leitura do mapa, por extenso", leitura_do_mapa)}
<h3>As sínteses, por extenso</h3>
<p>Cada síntese foi escrita só com as afirmações que sobreviveram à verificação. As referências completas e as afirmações rejeitadas, com o motivo, estão no levantamento (§{lit["secao_rejeitadas"]}) e em <code>referencias.md</code>.</p>
{_sinteses_por_extenso(secoes)}'''
    cartoes = [("Opções de arquitetura da trilha avaliadas pela literatura", f'{cont["adotado"]} adotadas', f'{cont["adiado"]} adiadas · {cont["descartado"]} descartadas, de {n} no mapa da onda 1 da parte B')]
    fonte = (f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code> (§{secoes[0]["secao"]} a §{secoes[-1]["secao"]} e o mapa "Parte B, onda 1" em §{lit["secao_mapas"]})'
             if secoes else None)
    return bloco_html, cartoes, fonte


# ! Alteração de IA - Revisar: (23/10/2026) aba nova "Cérebro e memória" (id cerebro), lida só do levantamento §6.14 (parte B,
# onda 2): o mapa de viabilidade com filtro por veredito, um gráfico de vereditos por tema, os riscos, a leitura, as
# quatro sínteses por extenso (confiança por probabilidade, Brainiac, grafos do código e do conhecimento, visualização
# da rede neural) e uma leitura curta montada das linhas do próprio mapa.
# ! Motivo: o Eric perguntou em 23/10/2026 se dá para mostrar a rede neural como o "cérebro" do agente no painel, ao
# vivo, se o Brainiac serve e se o grafo do código seria um toque a mais; ele decide pelo painel, e a regra do projeto
# é uma aba por análise. Nada é digitado aqui: tudo vem do arquivo gerado por integrar_pesquisa_pre_fase4.py.
TEMAS_DA_LEITURA_CE = ("Cérebro ao vivo", "Rede neural como figura estática", "Atenção e ativações ao vivo", "Brainiac", "Grafo do conhecimento no painel",
                       "Grafo do código no painel", "Confiança pela probabilidade do rótulo", "Decodificação restrita")


def secao_cerebro(levantamento: str | None) -> tuple[dict, str]:
    titulo = "Dá para mostrar o cérebro do agente no painel, e o Brainiac ou um grafo do código servem?"
    lit = _pre_fase4_no_levantamento(levantamento)
    blocos = _blocos_dos_mapas(lit["mapas"]) if lit else {}
    nome = next((k for k in blocos if k.startswith("Parte B, onda 2")), None)
    if not lit or not nome or "ainda não rodou" in blocos[nome]:
        return {"temas": []}, (f'<section id="cerebro" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A onda 2 da parte B da rodada 5 da pesquisa (confiança por '
                               'probabilidade, Brainiac, grafos, visualização da rede neural) ainda não foi integrada ao levantamento, como §6.14.</p>\n</section>')
    bloco = blocos[nome]
    mapa, cont, n, tab_riscos, leitura_do_mapa = _mapa_de_um_bloco(bloco, "tab-mapa-ce", "Filtro do mapa de viabilidade do painel")
    cab, linhas, _ = pt.primeira_tabela(bloco)
    col = {c: i for i, c in enumerate(cab)}
    temas: list[dict] = []
    por_tema: dict[str, list] = {}
    for r in linhas:
        tema = re.sub(r"[*`_]", "", r[col["Tema"]]).strip()
        v = _veredito(r[col["Veredito"]])
        t = next((x for x in temas if x["tema"] == tema), None)
        if not t:
            t = {"tema": tema, "adotado": 0, "adiado": 0, "descartado": 0, "outro": 0}
            temas.append(t)
        t[v] += 1
        por_tema.setdefault(tema, []).append((v, r[col["Opção"]], r[col["Motivo"]]))
    secoes = [s for s in lit["secoes"] if s["chave"] in TOPICOS_VISUALIZACAO]
    aprovadas, rejeitadas = sum(s["aprovadas"] for s in secoes), sum(s["rejeitadas"] for s in secoes)
    com_adotado = sum(1 for t in temas if t["adotado"])
    itens_kpi = [("Opções avaliadas pela literatura", f'{cont["adotado"]} servem agora', f'{cont["adiado"]} só com outra máquina ou depois · {cont["descartado"]} não servem, de {n} no mapa da onda 2'),
                 ("Tópicos da onda 2", f"{len(secoes)}", f'{aprovadas} afirmações aprovadas por verificadores céticos · {rejeitadas} {"rejeitada" if rejeitadas == 1 else "rejeitadas"}'),
                 ("Temas do mapa", f"{len(temas)}", f"{com_adotado} com ao menos uma opção que serve agora")]
    lead = (f'Em parte. Dos {n} caminhos avaliados pela onda 2 da parte B da rodada 5 da pesquisa (23/10/2026), {cont["adotado"]} servem agora nesta máquina, sem trocar o '
            f'modelo nem o motor decididos; {cont["adiado"]} só serviriam com outra máquina, outro motor ou depois da Fase 4; {cont["descartado"]} não servem. O veredito de cada '
            'um, com o motivo e a fonte, está no mapa abaixo; o que vale para a trilha de raciocínio entrou na especificação da trilha (Memorial, seção 5).')
    pontos = []
    for tema in TEMAS_DA_LEITURA_CE:
        for v, opcao, motivo in por_tema.get(tema, []):
            pontos.append(f"<strong>{pt.inline(opcao)}:</strong> {chip(v, v)} {pt.inline(motivo)}")
            break
    html_ = f'''<section id="cerebro" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Vereditos por tema</h2>
<p>Cada barra é um tema do mapa de viabilidade; as cores dizem quantas opções daquele tema servem agora nesta máquina, quantas só serviriam com outra máquina, outro motor ou depois da Fase 4, e quantas não servem.</p>
<div class="chart" style="height:{max(260, 28 * len(temas) + 80)}px"><canvas id="g-ce-temas"></canvas></div>
<h2>O mapa de viabilidade, opção por opção</h2>
<p><em>Adotado</em> serve agora, nesta máquina, sem trocar o modelo nem o motor decididos; <em>adiado</em> só serviria com outra máquina (o mapa diz quanta RAM, GPU ou disco), outro motor, ou depois da Fase 4; <em>descartado</em> não serve, com o motivo.</p>
{mapa}
{detalhes("Riscos que a literatura aponta e a mitigação de cada um", tab_riscos)}
{detalhes("Leitura do mapa, por extenso", leitura_do_mapa)}
<h2>As sínteses, por extenso</h2>
<p>Cada síntese foi escrita só com as afirmações que sobreviveram à verificação. As referências completas e as afirmações rejeitadas, com o motivo, estão no levantamento (§{lit["secao_rejeitadas"]}) e em <code>referencias.md</code>.</p>
{_sinteses_por_extenso(secoes)}
<h2>Leitura</h2>
{leitura(pontos)}
{fontes([f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code> (§{secoes[0]["secao"]} a §{secoes[-1]["secao"]} e o mapa "Parte B, onda 2" em §{lit["secao_mapas"]})' if secoes else f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code>', "<code>5-metodo-e-ferramental/especificacao-trilha-e-relatorio.md</code> (seção 14)", "decisões 61, 70 e 75; roadmap §3.1"])}
</section>'''
    return {"temas": temas}, html_


def secao_raciocinio(ind: dict | None, exemplo: str | None, trilhas: dict | None = None, confianca: dict | None = None, levantamento: str | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, título e parágrafos à vista reescritos sem AUROC solto, b/c, p, "rótulo" nem "L1" sem explicação.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; a probabilidade do "rótulo" passa a ser a da causa respondida, e os números seguem nas tabelas recolhidas.
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
            ("O quanto a probabilidade da causa separa erros de acertos (AUROC)", fmt(tot["sinais"]["p_conjunta"]["auroc"], 3),
             f'em {tot["casos"]} diagnósticos; verbete do contexto {fmt(tot["sinais"]["sustentado"]["auroc"], 3)}, classe da rota {fmt((tot["sinais"].get("coerente") or {}).get("auroc"), 3)}'),
            ("Revisar os 10% menos prováveis", f'{rev[0.1]["erros_pegos"]} de {tot["erros"]} erros', f'{rev[0.1]["revisados"]} casos revisados, {rev[0.1]["acertos_revisados"]} deles acertos; com 30%: {rev[0.3]["erros_pegos"]} de {tot["erros"]}'),
            ("Erros confiantes", f"{confiantes} de {tot['erros']}", f'probabilidade acima de 0,85; mediana {fmt(tot["p_conjunta_mediana"]["certos"], 3)} nos certos e {fmt(tot["p_conjunta_mediana"]["errados"], 3)} nos errados'),
        ]
        if cur and l1 and p_cur:
            itens_conf.append(("Cópia curada contra a 1ª versão inteira (72 casos)", f'{fmt(cur["acerto_pct"])}% × {fmt(l1["acerto_pct"])}%',
                               f'só a cópia acertou {p_cur["b"]}, só a inteira {p_cur["c"]}; {fmt(cur["segundos_mediana"])} × {fmt(l1["segundos_mediana"])} s por diagnóstico'))
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
        bloco_conf = f"""<h2>A probabilidade da causa respondida separa acerto de erro? (corrida 12, 06/10/2026)</h2>
<p>O Ollama devolve a probabilidade de cada token que o modelo escreve. A corrida 12 gravou essa probabilidade para a causa respondida nos 72 casos que nenhuma biblioteca viu, com o qwen2.5:7b lendo a biblioteca original (L0), a primeira versão escrita pelo modelo inteira (L1) e a cópia curada dela que a Fase 4 vai usar: {tot["casos"]} diagnósticos, {tot["erros"]} erros. A medida principal, fixada antes da corrida, é a probabilidade conjunta dos tokens da causa. O quanto cada sinal separa erros de acertos (AUROC) vai de 0,5, que é sortear, a 1,0, que separa tudo.</p>
{kpis(itens_conf)}
<div class="chart"><canvas id="g-ra-conf"></canvas></div>
{tab_res}
{leitura([f"<strong>Separa, e melhor que os dois sinais grátis, mas metade dos erros sai confiante.</strong> O sinal separa erros de acertos em {fmt(tot['sinais']['p_conjunta']['auroc'], 3)}, contra {fmt(tot['sinais']['sustentado']['auroc'], 3)} e {fmt((tot['sinais'].get('coerente') or {}).get('auroc'), 3)} dos outros dois. Além disso, {confiantes} dos {tot['erros']} erros têm probabilidade acima de 0,85, e em {tot['erros_com_o_gabarito_na_segunda']} deles a causa certa era a segunda opção.",
          f"<strong>Serve de triagem, não de barreira.</strong> Mandar para revisão os 10% de menor probabilidade ({rev[0.1]['revisados']} casos) pega {rev[0.1]['erros_pegos']} dos {tot['erros']} erros; 30% ({rev[0.3]['revisados']} casos) pega {rev[0.3]['erros_pegos']}, revisando {rev[0.3]['acertos_revisados']} acertos à toa. Para a Fase 4, vale como ordem de prioridade de revisão e como aviso na trilha."]
         + ([f"<strong>A cópia curada rende como a primeira versão inteira e custa menos.</strong> {fmt(cur['acerto_pct'])}% contra {fmt(l1['acerto_pct'])}% nos 72 casos na mesma corrida ({p_cur['b']} casos só da cópia, {p_cur['c']} só da inteira), dentro da variação entre corridas iguais; {fmt(cur['segundos_mediana'])} s contra {fmt(l1['segundos_mediana'])} s por diagnóstico, com menos texto no contexto. Segue como ponto de partida da Fase 4 (decisão 71)."] if cur and l1 and p_cur else []))}
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
        ("Causa fora das 23 permitidas", str(fora_conj), "respostas com causa inventada"),
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
    # (23/10/2026) o bloco da literatura da parte B (onda 1): mapa de arquitetura, riscos, leitura e sínteses
    bloco_literatura, cartoes_literatura, fonte_literatura = _literatura_do_raciocinio(levantamento)
    itens_kpi += cartoes_literatura
    html_ = f'''<section id="raciocinio" hidden>
<h1>{titulo}</h1>
<p class="lead">Em parte. Dá para ver tudo o que o programa fez (o que a busca pontuou e entregou, o prompt, a resposta, os tempos) e conferir por código o que o modelo declarou. O raciocínio em si não está lá: em {sem} dos {total} diagnósticos remontados o modelo não escreveu nenhum, foi direto às quatro linhas. Por isso o relatório separa três camadas e nunca trata a alegação do modelo como fato.</p>
{kpis(itens_kpi)}
<h2>As três camadas</h2>
{leitura(["<strong>O que o programa fez</strong> é fato: o caso que entrou, os verbetes que a busca pontuou e os que entregou, o prompt montado, a resposta crua, os tempos. Nas corridas gravadas o prompt não foi guardado; ele é remontado pelas mesmas funções do executor, e cada trilha diz até onde essa remontagem está provada.",
          "<strong>O que o modelo declarou</strong> é alegação: a causa, o campo, a frase de impacto e os verbetes citados, sempre como trecho literal da resposta, com a posição.",
          "<strong>O que o código conferiu</strong> é o que se pôde checar da alegação sem saber a resposta certa. O que não dá para conferir por código (a frase de impacto, e qual nota de um verbete o modelo usou) é dito, não omitido."])}
<h2>Um sinal que o agente pode calcular sozinho</h2>
<p>Em cada resposta o código pergunta: algum verbete entregue ao modelo trata da causa que ele respondeu? Não precisa de gabarito.{texto_sinal} Os grupos "quando não" são pequenos; a sonda de confiança (corrida 12) mede o mesmo sinal junto com a probabilidade da causa respondida.</p>
<div class="chart"><canvas id="g-ra-sus"></canvas></div>
{tab_sus}
<h2>O que o código conferiu, por trilha</h2>
<p>Oito conferências por resposta, todas sem usar o gabarito. As duas últimas não dão veredito: a lista das notas do modelo nos verbetes citados é informativa, e a frase de impacto não tem como ser conferida por código.</p>
{detalhes("Todas as conferências, trilha por trilha", tab_conf)}
{bloco_conf}
{pe.bloco_html(explorador)}
{bloco_exemplo}
{bloco_literatura}
<h2>Leitura</h2>
{leitura([
    f"<strong>O modelo decidido não mostra o caminho.</strong> Em {sem} de {total} respostas não há texto antes das quatro linhas, embora o prompt peça uma explicação curta. O que se abre é o caminho do programa e a conferência das alegações, não um raciocínio escrito.",
    leitura_fontes,
    "<strong>O erro mais comum não é inventar, é responder uma causa que a documentação entregue não trata.</strong> Esse caso é detectável em código, na hora, e vira candidato a aviso para quem desenvolve.",
    "<strong>O relatório mostra de quem é cada nota.</strong> Quando o verbete citado tem notas escritas pelo modelo, o relatório lista quantas são e o veredito da revisão humana de cada uma; não dá para saber qual delas pesou na resposta, e isso fica escrito.",
    ("<strong>A probabilidade da causa respondida é o melhor dos três sinais, e nenhum deles é barreira.</strong> A seção da corrida 12, acima, traz os números; o que a literatura da parte B sustenta para a arquitetura da trilha está na seção acima, e a especificação da trilha para a Fase 4 sai dela." if tot
     else "A análise da probabilidade da causa respondida entra nesta aba quando a corrida 12 terminar; o que a literatura da parte B sustenta para a arquitetura da trilha está na seção acima, e a especificação da trilha para a Fase 4 sai dela.")])}
{fontes(["<code>resultados_alvo/pre_fase4/confianca.json</code> e <code>.md</code> (<code>analisar_confianca.py</code>, corrida 12 em <code>resultados_alvo/pre_fase4_confianca/</code>)", "<code>resultados_alvo/pre_fase4/indicadores_raciocinio.json</code> (<code>gerar_relatorio_raciocinio.py --vitrine</code>, com <code>--check</code>)", "trilhas em <code>resultados_alvo/pre_fase4/trilhas/</code> (<code>trilha.py</code>) e relatórios em <code>resultados_alvo/pre_fase4/relatorios/</code>"] + ([fonte_literatura] if fonte_literatura else []) + ["decisão 70; roadmap §3.1"])}
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
// ! Alteração de IA - Revisar: (05/11/2026) nomes legíveis nos eixos e nas legendas dos gráficos das abas da Fase 4; os identificadores seguem nas tabelas recolhidas.
// ! Motivo: os eixos mostravam nomes de código, como regra_b_por_gatilho e contrato-malformed_json, que só quem leu o script entende; o Eric pediu a leitura sem jargão.
const NOMES = {divergencia:'divergência, como a corrida rodou', por_gatilho:'divergência, só por gatilho', regra_b:'regra alternativa, em todos os casos', regra_b_por_gatilho:'regra alternativa, só por gatilho',
  remocao_ou_troca:'tirar ou trocar o verbete muda a resposta', sem_documentacao:'sem documentação, a resposta muda', repeticao_mudou:'repetir a pergunta muda a resposta', selo_baixo:'selo de confiança baixo', falha:'conferência em código não passa', qualquer:'qualquer um dos sinais',
  verbete_trocado:'verbete trocado', contrato_alterado:'contrato alterado', seletor_quebrado:'seletor quebrado',
  'front-busca':'busca', 'front-admin-login':'login do administrador', 'front-admin-produtos':'lista de produtos do administrador', 'front-cliente-reserva':'reserva do cliente',
  'contrato-malformed_json':'resposta cortada no meio', 'contrato-field_missing':'campo sumiu da resposta', 'contrato-field_renamed':'campo mudou de nome', 'contrato-type_drift':'campo mudou de tipo', 'contrato-escala_ou_unidade_errada':'preço na escala errada', 'contrato-error_500':'API devolve erro 500',
  'localizador-front-busca':'localizador: busca', 'localizador-front-admin-login':'localizador: login do administrador', 'localizador-front-admin-produtos':'localizador: lista de produtos', 'localizador-front-cliente-reserva':'localizador: reserva do cliente'};
const nome = s => NOMES[s] || String(s).replace(/_/g, ' ');
const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`; };
// ! Alteração de IA - Revisar: (05/11/2026) gráficos das abas Modelos, Entre fases e Pesquisa, que só tinham tabela.
// ! Motivo: o Eric pediu o gráfico à vista e os dados em "mais informações"; essas abas ficariam sem nada para ver com as tabelas recolhidas.
function modGraficos(){
  const L = document.getElementById('sel-mod-l').value;
  const barras = (id, fonte, nomes) => { const chaves = Object.keys(nomes);
    grafico(id, {type:'bar', data:{labels: chaves.map(k => nomes[k]), datasets: D.modelos.map(m => ({label:m, data: chaves.map(k => ((fonte[m]||{})[k]||{})[L] ?? null), backgroundColor:cor(m)}))},
      options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true, text:'acerto nos 90 casos (%)'}}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}}); };
  barras('g-mod-classe', D.classes, {1:'léxica', 2:'sintática', 3:'semântica', 4:'tradução', 5:'runtime', 6:'efeito'});
  barras('g-mod-nivel', D.niveis, {1:'fácil', 2:'médio', 3:'difícil'});
}
function cmpEtapas(){
  const conj = document.getElementById('sel-cmp-conj').value, met = document.getElementById('sel-cmp-met').value;
  const cols = ['2A_linear_ryzen','2B_A0','2B_A2','F3_L0','F3_L1','F3_L2','F3_L3'];
  const rot = ['Sem documentação (2-A)','Sem documentação (2-B)','Biblioteca à mão (2-B)','Original (Fase 3)','1ª versão do modelo','2ª versão','3ª versão'];
  grafico('g-cmp-etapas', {type:'line', data:{labels: rot, datasets: D.modelos.map(m => ({label:m, data: cols.map(c => (((D.fases[m]||{})[conj]||{})[c]||{})[met] ?? null), borderColor:cor(m), backgroundColor:cor(m), tension:.15, pointRadius:4, spanGaps:true}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true, text: met==='balanceada'?'acurácia balanceada (%)':'acerto (%)'}}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function peRodadas(){
  const R = (T.pesquisa||{}).rodadas||[]; if(!R.length) return;
  grafico('g-pe-rodadas', {type:'bar', data:{labels: R.map(x => x.rodada), datasets:[
      {label:'aprovadas', data: R.map(x => x.aprovadas), backgroundColor: css('--bom')},
      {label:'rejeitadas', data: R.map(x => x.rejeitadas), backgroundColor: css('--ruim')},
      {label:'não verificadas', data: R.map(x => x.nao_verificadas), backgroundColor: css('--s4')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, beginAtZero:true, title:{display:true, text:'afirmações'}}, y:{stacked:true}}}});
}
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
  grafico('g-tb-rec', {type:'bar', data:{labels: T.tresb.Ls.map(l => 'L'+l), datasets: ds}, options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'verbete certo entre os três entregues (%)'}, min:0, max:100}}}});
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
function ceTemas(){
  const Tm = (T.cerebro||{}).temas||[]; if(!Tm.length) return;
  grafico('g-ce-temas', {type:'bar', data:{labels: Tm.map(t => t.tema), datasets:[
      {label:'serve agora', data: Tm.map(t => t.adotado), backgroundColor: css('--bom')},
      {label:'só com outra máquina, outro motor ou depois da Fase 4', data: Tm.map(t => t.adiado), backgroundColor: css('--s3')},
      {label:'não serve', data: Tm.map(t => t.descartado), backgroundColor: css('--ruim')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
      scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'opções avaliadas no mapa da onda 2'}}, y:{stacked:true, ticks:{autoSkip:false}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue}}}}});
}
function ferMcp(){
  if(!T.ferramental.mcp) return; const met = document.getElementById('sel-fer-met').value; const S = T.ferramental.mcp;
  grafico('g-fer-mcp', {type:'bar', data:{labels: S.map(x => x.tarefa), datasets:[{label:'grep, Glob e Read', data: S.map(x => Math.round(x['grep_'+met])), backgroundColor: css('--s1')}, {label:'servidor codebase-memory', data: S.map(x => Math.round(x['mcp_'+met])), backgroundColor: css('--s2')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'tokens (média de 2 repetições)'}, beginAtZero:true}}}});
}
function repClasses(){
  const R = T.reproducao||{}; const C = R.classes||[]; if(!C.length || !C.some(c => c.avaliacao)) return;
  const rot = R.rotulos||{};
  const ds = [{label:(rot.avaliacao||'avaliação')+': com tela e modo', data: C.map(c => c.avaliacao ? c.avaliacao.na_tela : null), backgroundColor: css('--s1')},
              {label:(rot.avaliacao||'avaliação')+': reproduzem', data: C.map(c => c.avaliacao ? c.avaliacao.reproduzem : null), backgroundColor: css('--s2')}];
  if(C.some(c => c.ineditos)) ds.push({label:(rot.ineditos||'inéditos')+': com tela e modo', data: C.map(c => c.ineditos ? c.ineditos.na_tela : null), backgroundColor: css('--s3')},
                                      {label:(rot.ineditos||'inéditos')+': reproduzem', data: C.map(c => c.ineditos ? c.ineditos.reproduzem : null), backgroundColor: css('--s4')});
  grafico('g-rep-classe', {type:'bar', data:{labels: C.map(c => c.classe+' '+c.nome), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:2}}}}});
}
// aba Calibração (27/10/2026, P3): acerto, acurácia balanceada e AUROC por k; curva risco-cobertura do k escolhido
function calK(){
  const C = T.calibracao||{}; const K = C.por_k||[]; if(!K.length) return;
  grafico('g-cal-k', {type:'bar', data:{labels: K.map(x => x.k+' verbetes (k = '+x.k+')'), datasets:[
    {label:'acerto (%)', data: K.map(x => x.acerto_pct), backgroundColor: css('--s1')},
    {label:'acurácia balanceada (%)', data: K.map(x => x.acuracia_balanceada_pct), backgroundColor: css('--s2')},
    {label:'quanto a probabilidade separa erros de acertos (AUROC x 100)', data: K.map(x => x.auroc_p == null ? null : Math.round(x.auroc_p * 1000) / 10), backgroundColor: css('--s3')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, max:100, title:{display:true,text:'%'}}}}});
}
function calCurva(){
  const C = T.calibracao||{}; const P = C.curva||[]; if(!P.length) return;
  grafico('g-cal-curva', {type:'line', data:{labels: P.map(p => Math.round(p.cobertura * 100) + '%'),
    datasets:[{label:'risco (erros entre os casos respondidos, %)', data: P.map(p => Math.round(p.risco * 1000) / 10), borderColor: css('--s2'), backgroundColor: css('--s2'), fill:false, pointRadius:2, tension:0}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{title:{display:true,text:'cobertura (da maior probabilidade para a menor)'}}, y:{beginAtZero:true, title:{display:true,text:'risco (%)'}}}}});
}
// aba Tela e fixture (01/11/2026, corrida 18): acerto na tela e no fixture por classe; rótulos dados em cada lado
function telaClasses(){
  const D = T.tela||{}; const C = D.por_classe||[]; if(!C.length) return;
  const ds = [
    {label:'casos', data: C.map(c => c.casos), backgroundColor: css('--s4')},
    {label:'acerto na tela (18)', data: C.map(c => c.acerto_tela), backgroundColor: css('--s1')},
    {label:'acerto no caso escrito', data: C.map(c => c.acerto_fixture), backgroundColor: css('--s2')},
    ];
  // ! Alteração de IA - Revisar: (05/11/2026) o gráfico deixa de trazer as séries "mesmo rótulo", que seguem na tabela recolhida.
  // ! Motivo: seis séries por grupo não se liam; nos casos desta corrida, "mesmo rótulo" fica perto do acerto na tela.
  if(C.some(c => c.acerto_tela_v2 != null)) ds.push({label:'acerto na tela (18b, caso revisado)', data: C.map(c => c.acerto_tela_v2), backgroundColor: css('--s3')});
  grafico('g-tela-classe', {type:'bar', data:{labels: C.map(c => c.classe+' '+c.nome), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:1}}}}});
}
function telaRotulos(){
  const D = T.tela||{}; const R = D.rotulos||[]; if(!R.length) return;
  const ds = [
    {label:'é o gabarito de', data: R.map(x => x.gabarito), backgroundColor: css('--s4')},
    {label:'respondida na tela (18)', data: R.map(x => x.tela), backgroundColor: css('--s1')},
    {label:'respondida no caso escrito', data: R.map(x => x.fixture), backgroundColor: css('--s2')}];
  if(R.some(x => x.tela_v2 != null)) ds.push({label:'respondida na tela (18b, caso revisado)', data: R.map(x => x.tela_v2), backgroundColor: css('--s5')});
  grafico('g-tela-rotulos', {type:'bar', data:{labels: R.map(x => nome(x.rotulo)), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:2}}}}});
}
// aba Cura de seletor (01/11/2026, corrida 19): execuções por modo e por roteiro, empilhadas pela regra R3; MTTR por roteiro
function curaEmpilhado(id, L, chave){
  if(!L.length) return;
  grafico(id, {type:'bar', data:{labels: L.map(x => nome(x[chave])), datasets:[
      {label:'curadas, mesmo elemento', data: L.map(x => x.mesmo_elemento), backgroundColor: css('--bom')},
      {label:'curadas, outro elemento', data: L.map(x => x.outro_elemento), backgroundColor: css('--meio')},
      {label:'não curadas', data: L.map(x => x.nao_curadas), backgroundColor: css('--ruim')},
      {label:'não quebrou', data: L.map(x => x.nao_quebrou), backgroundColor: css('--s4')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{stepSize:2}, title:{display:true, text:'execuções'}}},
      plugins:{tooltip:{callbacks:{afterBody: it => { const x = L[it[0].dataIndex]; return 'taxa de cura ' + (x.taxa == null ? 'n/d' : x.taxa + '%') + ' · MTTR mediana ' + (x.mttr == null ? 'n/d' : x.mttr + ' s'); }}}}}});
}
function curaModos(){ const C = T.cura||{}; curaEmpilhado('g-cura-modo', C.por_modo||[], 'modo'); }
function curaRoteiros(){ const C = T.cura||{}; curaEmpilhado('g-cura-roteiro', C.por_roteiro||[], 'roteiro'); }
// aba Biblioteca em produção (03/11/2026, corrida 20): o que cada filtro barrou e a regra R5 nos inéditos
function bibFiltros(){
  const B = T.biblioteca||{}; const F = B.filtros||[];
  if(!F.length) return;
  grafico('g-bib-filtros', {type:'bar', data:{labels: F.map(x => nome(x.filtro)), datasets:[{label:'propostas barradas ou seguradas', data: F.map(x => x.recusas), backgroundColor: css('--s3')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'propostas'}}}}});
}
function bibReavaliacao(){
  const B = T.biblioteca||{}; const R = B.reavaliacao;
  if(!R) return;
  // ! Alteração de IA - Revisar: (05/11/2026) o gráfico fica só com os dois acertos; b e c seguem no texto da aba e nos cartões.
  // ! Motivo: porcentagem e contagem de casos dividiam o mesmo eixo, e as barras de b e c, com valor zero, não apareciam.
  grafico('g-bib-reavaliacao', {type:'bar', data:{labels:['com a cópia curada', 'com o lote'],
      datasets:[{label:'acerto nos 36 inéditos (%)', data:[R.acerto_base_pct, R.acerto_novo_pct], backgroundColor:[css('--s2'), css('--s1')]}]},
    options:{responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{y:{min:0, max:100, title:{display:true, text:'acerto nos 36 inéditos (%)'}}}}});
}
// aba Cenários da Fase 5 (04/11/2026, corrida 21): MTTR médio e Task Success por cenário, contrato e localizador em cores diferentes
function cenMttr(){
  const C = T.cenarios||{}; const L = C.por_cenario||[];
  if(!L.length) return;
  const ds = C.duas_corridas
    ? [{label:'corrida 21', data: L.map(x => x.mttr_anterior), backgroundColor: css('--s4')}, {label:'corrida 21b, com a correção da cura', data: L.map(x => x.mttr_media_s), backgroundColor: css('--s1')}]
    : [{label:'MTTR médio (s)', data: L.map(x => x.mttr_media_s), backgroundColor: L.map(x => x.tipo === 'contrato' ? css('--s1') : css('--s2'))}];
  grafico('g-cen-mttr', {type:'bar', data:{labels: L.map(x => nome(x.cenario)), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', plugins:{legend:{display: !!C.duas_corridas}},
      scales:{x:{beginAtZero:true, title:{display:true, text:'segundos, da detecção até o resultado'}}, y:{afterFit: s => { s.width = Math.max(s.width, 240); }}}}});
}
function cenSucesso(){
  const C = T.cenarios||{}; const L = C.por_cenario||[];
  if(!L.length) return;
  grafico('g-cen-ts', {type:'bar', data:{labels: L.map(x => nome(x.cenario)), datasets:[
      {label:'chegou ao resultado (Task Success)', data: L.map(x => x.sucessos), backgroundColor: css('--bom')},
      {label:'não chegou', data: L.map(x => x.n - x.sucessos), backgroundColor: css('--ruim')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'execuções'}},
      y:{stacked:true, afterFit: s => { s.width = Math.max(s.width, 240); }}}}});
}
// aba Avaliação da trilha (04/11/2026, corrida 22): TPR, TNR e o produto por sinal (o acaso dá 0,25) e as mutações pelo nó apontado
function triSinais(){
  const A = T.trilha||{}; const S = A.sinais||[];
  if(!S.length) return;
  grafico('g-tri-sinais', {type:'bar', data:{labels: S.map(x => nome(x.sinal)), datasets:[
      {label:'erros que pegou (TPR)', data: S.map(x => x.tpr), backgroundColor: css('--s1')},
      {label:'acertos que deixou em paz (TNR)', data: S.map(x => x.tnr), backgroundColor: css('--s2')},
      {label:'nota (TPR x TNR)', data: S.map(x => x.produto), backgroundColor: css('--s3')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{beginAtZero:true, max:1, title:{display:true, text:'de 0 a 1; na nota, o acaso dá 0,25'}}, y:{ticks:{autoSkip:false}, afterFit: s => { s.width = Math.max(s.width, 250); }}}}});
}
function triMutacoes(){
  const A = T.trilha||{}; const M = A.mutacoes||[];
  if(!M.length) return;
  grafico('g-tri-mutacoes', {type:'bar', data:{labels: M.map(x => nome(x.tipo)), datasets:[
      {label:'apontou o nó previsto', data: M.map(x => x.previsto), backgroundColor: css('--bom')},
      {label:'apontou outro nó', data: M.map(x => x.outro_no), backgroundColor: css('--ruim')},
      {label:'sem divergência', data: M.map(x => x.sem_divergencia), backgroundColor: css('--meio')},
      {label:'sem alvo', data: M.map(x => x.sem_alvo), backgroundColor: css('--s4')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:4}, title:{display:true, text:'casos (roteiros, no seletor)'}},
      y:{stacked:true, afterFit: s => { s.width = Math.max(s.width, 200); }}}}});
}
""" + pa.JS_ATLAS + pe.JS_EXPLORADOR

DESENHAR_TOPICOS = {"modelos": ["modGraficos"], "comparacao": ["cmpEtapas"], "pesquisa": ["peRodadas"], "comparativo": ["cqTrajetoria", "cqConfronto", "cqRevisao"], "tresb": ["tbGeneraliza", "tbRecuperacao"],
                    "cruzada": ["czLeitores", "czTrocas"], "colibri": ["coMinutos"], "raciocinio": ["raSustentacao", "raConfianca", "raExplorar"], "atlas": ["atlasIniciar"], "cerebro": ["ceTemas"],
                    "curadoria": ["curOperacoes"], "recuperador": ["recMetodos"], "ablacao": ["ablBarras"], "ferramental": ["ferMcp"],
                    "reproducao": ["repClasses"], "calibracao": ["calK", "calCurva"], "tela": ["telaClasses", "telaRotulos"], "cura": ["curaModos", "curaRoteiros"],
                    "biblioteca": ["bibFiltros", "bibReavaliacao"], "cenarios": ["cenMttr", "cenSucesso"], "trilha": ["triSinais", "triMutacoes"]}
SELETORES_TOPICOS = {"sel-cq-conj": "cqTrajetoria", "sel-cq-met": "cqTrajetoria", "sel-cq-conf": "cqConfronto", "sel-tb-met": "tbGeneraliza", "sel-cz-met": "czLeitores",
                     "sel-rec-bib": "recMetodos", "sel-rec-met": "recMetodos", "sel-fer-met": "ferMcp"}

CSS_TOPICOS = r"""
.chip.nao_cumprida{background:color-mix(in srgb,var(--ruim) 18%,transparent);color:var(--ruim)}
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

# ! Alteração de IA - Revisar: aba nova (27/10/2026) "Reprodução na tela", a primeira da Fase 4: a corrida 17 sobre os
# 72 casos de avaliação e a mesma corrida sobre os 36 inéditos da ficha 27, lidas de
# resultados_alvo/fase4/reproducibilidade.json e reproducibilidade_ineditos.json (avaliar_fase4.py, com --check).
# ! Motivo: a regra do painel é uma aba por análise e a corrida 17 (pacote P2) tinha ficado só no roadmap; o Eric
# decide pelo painel quais casos a tela reproduz antes de gastar modelo (corridas 16 e 18) e de conferir os inéditos.
# Sem os arquivos a aba mostra o estado vazio, como as da Pré-Fase 4.
def secao_reproducao(rep: dict | None, ined: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões de tempo e de corte da árvore encurtados, e "harness" e "poda" soltos trocados por "o próprio teste" e "o corte em código do que o modelo lê (poda)".
    # ! Motivo: os cartões traziam milissegundos da API e tamanhos do corpo que já estão nas tabelas recolhidas, e o texto usava termos de método que o Eric pediu para tirar.
    def por(d: dict | None, chave: str, campo: str) -> dict:
        return {x[campo]: x for x in d[chave]} if d else {}

    pc, pi = por(rep, "por_classe", "classe"), por(ined, "por_classe", "classe")
    campos = ("casos", "na_tela", "reproduzem", "fora")
    classes = [{"classe": i, "nome": nome,
                "avaliacao": {k: pc[i][k] for k in campos} if i in pc else None,
                "ineditos": {k: pi[i][k] for k in campos} if i in pi else None} for i, nome in CLASSES.items()]
    rotulos = {"avaliacao": f'{rep["resumo"]["casos"]} de avaliação' if rep else "casos de avaliação",
               "ineditos": f'{ined["resumo"]["casos"]} inéditos' if ined else "inéditos"}
    dados_js = {"classes": classes, "rotulos": rotulos}
    fontes_ = fontes(["<code>resultados_alvo/fase4/reproducibilidade.json</code> e <code>.md</code> (<code>avaliar_fase4.py --reproducao</code>, com <code>--check</code>; blocos <code>tb_f4_reproducao_*</code>)",
                      "<code>resultados_alvo/fase4/reproducibilidade_ineditos.json</code> e <code>.md</code> (a mesma avaliação com <code>--nome reproducibilidade_ineditos</code>)",
                      "<code>executar_fase4.py --modo reproducao</code> (regra R1; <code>--banco</code> escolhe os casos); roadmap §2.8; plano aprovado da Fase 4, seções 5 e 6; fichas 27, 28 e 29"])
    if not rep:
        html_ = f'''<section id="reproducao" hidden>
<h1>Reprodução na tela: quantos casos de avaliação a tela consegue reproduzir?</h1>
<p class="lead">A corrida 17 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/reproducibilidade.json</code>, gerado por <code>avaliar_fase4.py --reproducao</code> depois de <code>executar_fase4.py --modo reproducao --saida fase4_reproducao</code>.</p>
{cartoes_corridas(road, numeros=["17"], sufixo="-rep")}
{fontes_}
</section>'''
        return dados_js, html_
    r = rep["resumo"]
    ri = ined["resumo"] if ined else None
    t, tam = rep["tempo"], rep["tamanhos"]
    fora_motivos = "; ".join(f'{x["casos"]} {x["motivo"]}' for x in rep["fora_por_motivo"]).replace("pelo harness", "pelo próprio teste")
    itens_kpi = [
        ("Reproduzem na tela (corrida 17)", f'{r["reproduzem"]} de {r["casos"]}',
         f'{fmt(r["reproduzem_pct"])}% do conjunto; {fmt(r["reproduzem_dos_na_tela_pct"])}% dos {r["na_tela"]} com tela e modo'),
        ("Ficam fora", str(r["fora"]), fora_motivos),
        ("Tempo por cenário", f'{fmt(t["mediana_s"], 3)} s', f'mediana; o maior, {fmt(t["max_s"])} s, vem de casos de latência'),
        ("Corte da árvore da tela (poda)", f'{tam["arvore_antes_mediana"]} para {tam["arvore_depois_mediana"]}',
         f'nós antes e linhas depois, em medianas; o caso ao vivo fica com {tam["caso_chars_mediana"]} caracteres'),
        (("Inéditos da ficha 27", f'{ri["reproduzem"]} de {ri["casos"]}', f'{fmt(ri["reproduzem_pct"])}% dos {ri["casos"]}; {ri["fora"]} fora; corrida de {"/".join(reversed(ined["metadados"]["gerado_em"][:10].split("-")))}')
         if ri else ("Inéditos da ficha 27", "ainda não rodada", "a mesma corrida sobre os 36 inéditos")),
    ]

    def linha(rotulo: str, a: dict | None, i: dict | None) -> list:
        vazio = ("—", "—", "—", "—")
        return [rotulo, *((a["casos"], a["na_tela"], a["reproduzem"], a["fora"]) if a else vazio),
                *((i["casos"], i["na_tela"], i["reproduzem"], i["fora"]) if i else vazio)]

    cab_duplo = ["Classe", "Casos", "Com tela e modo", "Reproduzem", "Fora", "Inéditos: casos", "Com tela e modo", "Reproduzem", "Fora"]
    por_classe = tabela(cab_duplo, [linha(f'{c["classe"]} {c["nome"]}', c["avaliacao"], c["ineditos"]) for c in classes])
    pn, pni = por(rep, "por_nivel", "nivel"), por(ined, "por_nivel", "nivel")
    por_nivel = tabela([h.replace("Classe", "Nível") for h in cab_duplo], [linha(str(n), pn[n], pni.get(n)) for n in sorted(pn)])
    pm, pmi = por(rep, "por_modo", "modo"), por(ined, "por_modo", "modo")
    modos = sorted(set(pm) | set(pmi))
    por_modo = tabela(["Modo de injeção", "Casos", "Reproduzem", "Inéditos: casos", "Reproduzem", "Motivos registrados"],
                      [[f"<code>{esc(m)}</code>", pm.get(m, {}).get("casos", "—"), pm.get(m, {}).get("reproduzem", "—"),
                        pmi.get(m, {}).get("casos", "—"), pmi.get(m, {}).get("reproduzem", "—"),
                        esc("; ".join(dict.fromkeys(list(pm.get(m, {}).get("motivos", [])) + list(pmi.get(m, {}).get("motivos", [])))))] for m in modos], raw=True)

    def linhas_casos(d: dict | None, rotulo: str) -> list[list]:
        return [[esc(rotulo), f"<code>{esc(c['id'])}</code>", c["classe"], c["nivel"], f"<code>{esc(c['causa'])}</code>", f"<code>{esc(c['modo'])}</code>",
                 esc(c["cenario"]), "sim" if c["reproduz"] else "não", esc(c["motivo"]), fmt(c.get("segundos"), 3)] for c in (d["casos"] if d else [])]

    casos = tabela(["Corrida", "Caso", "Classe", "Nível", "Causa", "Modo", "Cenário", "Reproduz", "Motivo", "Segundos"],
                   linhas_casos(rep, rotulos["avaliacao"]) + linhas_casos(ined, rotulos["ineditos"]), raw=True)
    fora = tabela(["Corrida", "Caso", "Classe", "Nível", "Causa", "Por que ficou fora"],
                  [[esc(rot), f"<code>{esc(x['id'])}</code>", x["classe"], x["nivel"], f"<code>{esc(x['causa'])}</code>", esc(x["motivo"])]
                   for d, rot in ((rep, rotulos["avaliacao"]), (ined, rotulos["ineditos"])) if d for x in d["fora"]], raw=True)
    n_casos = len(rep["casos"]) + (len(ined["casos"]) if ined else 0)
    n_fora = r["fora"] + (ri["fora"] if ri else 0)
    lead = (f'Todos os que têm um modo de injeção e uma rota com página: {r["reproduzem"]} dos {r["casos"]} casos de avaliação na corrida 17 '
            f'({fmt(r["reproduzem_pct"])}% do conjunto, {fmt(r["reproduzem_dos_na_tela_pct"])}% dos {r["na_tela"]} com tela e modo) e, na mesma corrida sobre os inéditos da ficha 27, '
            + (f'{ri["reproduzem"]} dos {ri["casos"]} ({fmt(ri["reproduzem_pct"])}%). ' if ri else 'os 36 inéditos ainda não foram medidos. ')
            + f'Ficam fora {r["fora"]} dos {r["casos"]}: {fora_motivos}. Sem modelo: a regra R1 compara a chamada à API, o corpo e a árvore de acessibilidade '
              'com a corrida de referência em modo normal e confere o roteiro.')
    leitura_ = leitura([
        f"<strong>Quem tem tela e modo reproduz.</strong> Na corrida 17, {r['na_tela']} casos tinham os dois e {r['reproduzem']} reproduziram (bloco <code>tb_f4_reproducao_resumo</code>); "
        f"{r['roteiro_falhou']} deles também derrubaram uma conferência do roteiro.",
        f"<strong>O que fica fora não é falha da tela.</strong> {esc(fora_motivos)}: as rotas de pedido não têm página, <code>dado_desatualizado</code> não tem modo de injeção "
        "e as causas de efeito (localizador quebrado e estado da tela) são armadas pelo próprio teste no navegador, pela ficha 29.",
        (f"<strong>Os inéditos nasceram com os modos novos da ficha 28.</strong> {ri['na_tela']} dos {ri['casos']} têm tela e modo e "
         + ("todos reproduzem" if ri["reproduzem"] == ri["na_tela"] else f"{ri['reproduzem']} reproduzem")
         + f"; os {ri['fora']} fora são da mesma natureza. Eles esperam a conferência do Eric antes da corrida 16.") if ri
        else "<strong>Os 36 inéditos da ficha 27 ainda não passaram por esta corrida.</strong>",
        f"<strong>Custo.</strong> Mediana de {fmt(t['mediana_s'], 3)} s por cenário; os de latência chegam a {fmt(t['max_s'])} s porque o modo dorme por item da lista. "
        f"O corte em código do que o modelo lê (poda) leva a árvore de {tam['arvore_antes_mediana']} nós a {tam['arvore_depois_mediana']} linhas.",
    ])
    html_ = f'''<section id="reproducao" hidden>
<h1>Reprodução na tela: quantos casos de avaliação a tela consegue reproduzir?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Por classe de defeito</h2>
<p>Quantos casos de cada classe têm tela e modo e quantos reproduzem, nos {esc(rotulos["avaliacao"])} e nos {esc(rotulos["ineditos"])}. A classe de efeito fica fora por desenho: a quebra de localizador é armada pelo próprio teste, não pela API.</p>
<div class="chart"><canvas id="g-rep-classe"></canvas></div>
{por_classe}
<h2>Por nível e por modo de injeção</h2>
{por_nivel}
{detalhes(f"Por modo de injeção ({len(modos)} modos)", por_modo)}
{detalhes(f"Todos os casos com tela e modo ({n_casos})", casos)}
{detalhes(f"Casos fora ({n_fora})", fora)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["17"], sufixo="-rep")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 19. Fase 4: calibração e ponte (corrida 16)

# ! Alteração de IA - Revisar: aba nova (27/10/2026, Fase 4, pacote P3) com a leitura da corrida 16 (calibração e ponte),
# lida de resultados_alvo/fase4/calibracao.json e limiares.json (avaliar_fase4.py --calibracao): o k que a regra R8
# escolheu, os limiares do selo (regra R7, ficha 31), a AUROC da probabilidade do rótulo nos 90 casos com intervalo, a
# revisão humana por parcela, a curva risco-cobertura, a ponte de versão (regra R6) e a sondagem dos logprobs; sem o
# arquivo, o estado vazio com o cartão da corrida, como as outras abas.
# ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; a corrida 16 fixa o k e os limiares que a corrida 18
# usa, e o Eric decide pelo painel.
def secao_calibracao(cal: dict | None, lim: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos sem AUROC, IC, b/c, "acurácia balanceada", "gatilho" nem "rótulo" soltos.
    # ! Motivo: o texto à vista trazia siglas e números soltos que o Eric pediu para tirar; "k" passa a vir com o nome (número de verbetes entregues) e os valores seguem nas tabelas recolhidas.
    fontes_ = fontes(["<code>resultados_alvo/fase4/calibracao.json</code> e <code>.md</code> (<code>avaliar_fase4.py --calibracao</code>, com <code>--check</code>; blocos <code>tb_f4_calibracao_*</code>)",
                      "<code>resultados_alvo/fase4/limiares.json</code> (regra R7, ficha 31) e <code>pontes.json</code> (regra R6, decisão 47)",
                      "<code>executar_fase4.py --modo calibracao</code> (sondagem, ponte, L1 curada nos 90 com cada k, pelo executor congelado da Fase 3); roadmap §2.9; plano aprovado da Fase 4, seções 5, 6 e 8; fichas 30 e 31"])
    vazio = {"por_k": [], "curva": [], "k_escolhido": None, "limiares": None, "por_selo": []}
    if not cal:
        html_ = f'''<section id="calibracao" hidden>
<h1>Calibração: quantos verbetes entregar ao modelo e onde ficam os cortes do selo?</h1>
<p class="lead">A corrida 16 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/calibracao.json</code>, gerado por <code>avaliar_fase4.py --calibracao</code> depois de <code>executar_fase4.py --modo calibracao --saida fase4_calibracao --k 3,5</code> (noite A do plano aprovado).</p>
{cartoes_corridas(road, numeros=["16"], sufixo="-cal")}
{fontes_}
</section>'''
        return vazio, html_
    por_k = cal["por_k"]
    r8 = cal["r8"]
    limi = cal.get("limiares") or {}
    ponte = cal.get("ponte") or {}
    son = cal.get("sondagem") or {}
    escolhido = next((x for x in por_k if x["k"] == cal["k_escolhido"]), por_k[0])

    def auroc(x: dict, sinal: str) -> dict:
        return (x.get("sinais") or {}).get(sinal) or {}

    def auroc_txt(s: dict) -> str:
        if s.get("auroc") is None:
            return "n/d"
        ic = s.get("ic95")
        return fmt(s["auroc"], 3) + (f" [{fmt(ic[0], 3)}; {fmt(ic[1], 3)}]" if ic else "")

    dados_js = {"por_k": [{"k": x["k"], "n": x["n"], "acertos": x["acertos"], "acerto_pct": x["acerto_pct"], "acuracia_balanceada_pct": x["acuracia_balanceada_pct"],
                           "auroc_p": auroc(x, "p_rotulo").get("auroc"), "auroc_conjunta": auroc(x, "p_conjunta").get("auroc")} for x in por_k],
                "curva": [{"cobertura": p["cobertura"], "risco": p["risco"]} for p in escolhido.get("curva", [])],
                "k_escolhido": cal["k_escolhido"], "limiares": {"baixo_ate": limi.get("baixo_ate"), "alto_a_partir_de": limi.get("alto_a_partir_de")},
                "por_selo": cal.get("por_selo") or []}
    a_p = auroc(escolhido, "p_rotulo")
    # ! Alteração de IA - Revisar: (28/10/2026, leitura da corrida 16) a aba mostra os casos e os erros por selo (bloco
    # `tb_f4_calibracao_selos` de calibracao.json): cartão "Erros com selo alto", tabela e item da leitura.
    # ! Motivo: o selo alto é o que o agente mostra como confiável; quantos erros saem com ele é o número que a leitura
    # da corrida 16 precisa citar, e ele só existe no JSON desde a mesma data (antes só a parcela baixa era contada).
    por_selo = cal.get("por_selo") or []
    alto = next((x for x in por_selo if x["selo"] == "alto"), None)

    def erros_txt(x: dict) -> str:
        return f'{x["errados"]} {"erro" if x["errados"] == 1 else "erros"} em {x["casos"]} casos ({fmt(x["erro_pct"])}%)'
    parcela = limi.get("parcela_baixa")
    itens_kpi = [("Número de verbetes entregues (k) escolhido, regra R8", f'k = {cal["k_escolhido"]}', esc(r8["motivo"]))]
    for x in por_k:
        itens_kpi.append((f"Acerto com {x['k']} verbetes entregues", f'{x["acertos"]} de {x["n"]}',
                          f'{fmt(x["acerto_pct"])}%; {fmt(x["segundos_mediana"])} s por diagnóstico'
                          + ("" if x.get("completo", True) else "; corrida incompleta")))
    itens_kpi += [
        ("Selo baixo até", fmt(limi.get("baixo_ate"), 3),
         (f'os {fmt(100 * parcela, 0)}% menos prováveis: {limi.get("erros_pegos")} dos {limi.get("erros")} erros e {limi.get("acertos_revisados")} acertos revisados'
          if parcela is not None else "sem limiares")),
        ("Selo alto a partir de", fmt(limi.get("alto_a_partir_de"), 3), "mediana da probabilidade nos acertos (ficha 31, opção a); médio fica entre os dois"),
        ("O quanto a probabilidade separa erros de acertos", fmt(a_p.get("auroc"), 3) if a_p.get("auroc") is not None else "n/d",
         f'{a_p.get("n", escolhido["n"])} casos; pela probabilidade conjunta, {fmt(auroc(escolhido, "p_conjunta").get("auroc"), 3)}'),
        ("Ponte de versão (regra R6)", f'Ollama {ponte.get("versao", "n/d")}',
         (f'{"pareável" if ponte.get("pareavel") else "não pareável"} com a Fase 3: só a ponte acertou {ponte.get("b")}, só a Fase 3 {ponte.get("c")}, em {ponte.get("n")} casos; '
          + ("feita nesta corrida" if ponte.get("feita_nesta_corrida") else "já registrada")) if ponte else "sem ponte registrada"),
        ("Sondagem das probabilidades por token (logprobs)", ("ok" if son.get("ok") else "problema") if son else "não rodou",
         (f'até {son.get("top_por_posicao_max")} alternativas por posição; ' + ("com avisos (ver a tabela)" if son.get("mensagens") else "sem avisos")) if son else ""),
    ]
    if alto:
        itens_kpi.insert(4, ("Erros com selo alto", f'{alto["errados"]} de {alto["casos"]}',
                             f'{fmt(alto["erro_pct"])}% dos casos com selo alto saem errados (os nomes estão na tabela)'))
    tab_selos = tabela(["Selo", "Casos", "Certos", "Errados", "Erro (%)", "Casos errados"],
                       [[esc(x["selo"]), x["casos"], x["certos"], x["errados"], fmt(x["erro_pct"]), ", ".join(f"<code>{esc(c)}</code>" for c in x["casos_errados"]) or "nenhum"]
                        for x in por_selo], raw=True) if por_selo else ""
    bloco_selos = f"<p>Casos e erros por selo com os limiares desta corrida (regra R7; bloco <code>tb_f4_calibracao_selos</code>).</p>\n{tab_selos}" if por_selo else ""
    tab_k = tabela(["k", "Casos", "Completo", "Acertos", "Acerto (%)", "Acurácia balanceada (%)", "Nos 36 de avaliação (%)", "Nos 54 de aprendizado (%)",
                    "s por diagnóstico (mediana)", "Tokens de entrada (mediana)", "AUROC p do rótulo [IC 95%]", "AUROC p conjunta [IC 95%]", "Sem rótulo"],
                   [[f'k = {x["k"]}', x["n"], "sim" if x.get("completo", True) else "não", x["acertos"], fmt(x["acerto_pct"]), fmt(x["acuracia_balanceada_pct"]),
                     fmt(((x.get("por_particao") or {}).get("avaliacao") or {}).get("acerto_pct")), fmt(((x.get("por_particao") or {}).get("aprendizado") or {}).get("acerto_pct")),
                     fmt(x["segundos_mediana"]), fmt(x["tokens_entrada_mediana"], 0), auroc_txt(auroc(x, "p_rotulo")), auroc_txt(auroc(x, "p_conjunta")), x["sem_rotulo"]] for x in por_k])
    tab_rev = tabela(["k", "Parcela revisada", "Casos revisados", "Erros pegos", "Acertos revisados à toa", "Risco no que sobra"],
                     [[f'k = {x["k"]}', f'{fmt(100 * rv["fracao"], 0)}%', rv["revisados"], f'{rv["erros_pegos"]} de {rv["erros"]}', rv["acertos_revisados"],
                       "n/d" if rv["risco_no_que_sobra"] is None else f'{fmt(100 * rv["risco_no_que_sobra"])}%'] for x in por_k for rv in x.get("revisao", [])])
    par = r8.get("par") or {}
    tab_r8 = tabela(["Acurácia balanceada k = 3 (%)", "Acurácia balanceada k = 5 (%)", "b (só k = 5 acerta)", "c (só k = 3 acerta)", "p (McNemar exato)", "k escolhido", "Motivo"],
                    [[fmt(next((x["acuracia_balanceada_pct"] for x in por_k if x["k"] == 3), None)), fmt(next((x["acuracia_balanceada_pct"] for x in por_k if x["k"] == 5), None)),
                      par.get("b", "—"), par.get("c", "—"), fmt(par.get("p_mcnemar"), 3), f'k = {r8["k"]}', r8["motivo"]]])
    tab_ponte = tabela(["Ollama", "Corrida da ponte", "Feita nesta corrida", "Casos pareados", "b", "c", "Pareável (limite)", "Casos de texto corrigido fora"],
                       [[ponte.get("versao", "n/d"), ponte.get("corrida", "n/d"), "sim" if ponte.get("feita_nesta_corrida") else "não", ponte.get("n", "—"), ponte.get("b", "—"), ponte.get("c", "—"),
                         f'{"sim" if ponte.get("pareavel") else "não"} ({ponte.get("limite")})' if ponte else "n/d", ", ".join(ponte.get("casos_de_texto_alterado") or []) or "nenhum"]])
    tab_son = tabela(["Ollama", "Tokens com probabilidade", "Alternativas por posição (máx.)", "Bytes por token", "Texto remontado bate", "Probabilidade antes ou depois da temperatura",
                      "Resposta igual sem logprobs", "Rótulo lido", "p do rótulo", "Avisos"],
                     [[son.get("versao_ollama", "n/d"), son.get("tokens_com_logprob", "—"), son.get("top_por_posicao_max", "—"), "sim" if son.get("tem_bytes") else "não",
                       "sim" if son.get("texto_bate") else "não", son.get("temperatura", "n/d"), "sim" if son.get("resposta_igual_sem_logprobs") else "não",
                       son.get("rotulo_lido", "n/d"), fmt(son.get("p_rotulo"), 3), "; ".join(son.get("mensagens") or []) or "nenhum"]] if son else [["não rodou"] + ["—"] * 9])
    casos = tabela(["Caso", "Partição", "Gabarito", "Rótulo", "Resultado", "p do rótulo", "p conjunta", "Segunda causa", "Selo"],
                   [[f"<code>{esc(l['caso'])}</code>", esc(l.get("particao") or "—"), f"<code>{esc(l['gabarito'])}</code>", f"<code>{esc(l['rotulo'])}</code>",
                     "certo" if l["acerto"] else "errado", fmt(l["p"], 3), fmt(l["p_conjunta"], 3), esc(l.get("segunda") or "—"),
                     esc(("baixo" if l["p"] is not None and limi.get("baixo_ate") is not None and l["p"] <= limi["baixo_ate"]
                          else "alto" if l["p"] is not None and limi.get("alto_a_partir_de") is not None and l["p"] >= limi["alto_a_partir_de"]
                          else "médio" if l["p"] is not None else "—"))]
                    for l in sorted(escolhido.get("casos", []), key=lambda l: (l["p"] is None, l["p"] or 0, l["caso"]))], raw=True)
    lead = (f'A regra R8 escolheu k = {cal["k_escolhido"]}: {esc(r8["motivo"])}. Com esse k, o selo baixo vai até a probabilidade {fmt(limi.get("baixo_ate"), 3)} '
            f'(os {fmt(100 * parcela, 0) if parcela is not None else "—"}% de menor probabilidade, que pegam {limi.get("erros_pegos")} de {limi.get("erros")} erros) e o selo alto começa em '
            f'{fmt(limi.get("alto_a_partir_de"), 3)}; a probabilidade do rótulo separa acerto de erro com AUROC {fmt(a_p.get("auroc"), 3)} nos {escolhido["n"]} casos. '
            + (f'A ponte de versão (Ollama {ponte.get("versao")}) {"é pareável" if ponte.get("pareavel") else "não é pareável"} com a Fase 3 (b = {ponte.get("b")}, c = {ponte.get("c")}). ' if ponte else "")
            + (f'Sondagem dos logprobs: {"ok" if son.get("ok") else "com problema"}.' if son else ""))
    leitura_ = leitura([
        f"<strong>O número de verbetes entregues (k) da Fase 4.</strong> {esc(r8['motivo'])} (bloco <code>tb_f4_calibracao_r8</code>); a corrida 18 lê o k de <code>limiares.json</code>.",
        f"<strong>Os limiares do selo.</strong> Ficha 31 (a): baixo é a parcela de {fmt(100 * parcela, 0) if parcela is not None else '—'}% de menor probabilidade (o aviso que dispara a checagem extra e a revisão humana), "
        f"alto fica acima da mediana dos acertos. Revisar {limi.get('revisados')} casos pega {limi.get('erros_pegos')} de {limi.get('erros')} erros e deixa "
        f"{fmt(100 * limi['risco_no_que_sobra']) if limi.get('risco_no_que_sobra') is not None else '—'}% de erro no que sobra (<code>tb_f4_calibracao_revisao</code>).",
        f"<strong>A probabilidade é triagem, não barreira.</strong> O quanto o sinal separa erros de acertos é {fmt(a_p.get('auroc'), 3)} pelo primeiro token da causa e {fmt(auroc(escolhido, 'p_conjunta').get('auroc'), 3)} pela probabilidade conjunta, com k = {escolhido['k']} "
        "(blocos <code>tb_f4_calibracao_resumo</code> e <code>tb_f4_calibracao_por_k</code>): parte dos erros sai confiante, então o selo alto não dispensa a conferência (especificação da trilha, seção 6.3).",
        *([f"<strong>Erros por selo.</strong> " + "; ".join(f"selo {esc(x['selo'])}: {erros_txt(x)}" for x in por_selo) + " (<code>tb_f4_calibracao_selos</code>)."] if por_selo else []),
        (f"<strong>Ponte de versão.</strong> Ollama {ponte.get('versao')}: só a ponte acertou {ponte.get('b')} casos e só a Fase 3 {ponte.get('c')}, {'dentro' if ponte.get('pareavel') else 'fora'} do limite da decisão 47"
         + (" (feita nesta corrida)." if ponte.get("feita_nesta_corrida") else f" ({esc(str(ponte.get('corrida')))}).")) if ponte else "<strong>Ponte de versão.</strong> Não registrada.",
        f"<strong>Custo.</strong> " + "; ".join(f"k = {x['k']}: {fmt(x['segundos_mediana'])} s por diagnóstico, {fmt(x['tokens_entrada_mediana'], 0)} tokens de entrada na mediana" for x in por_k) + ".",
    ])
    html_ = f'''<section id="calibracao" hidden>
<h1>Calibração: quantos verbetes entregar ao modelo e onde ficam os cortes do selo?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Acerto e separação de erros e acertos, por número de verbetes entregues (k)</h2>
<p>A cópia curada da primeira versão escrita pelo modelo (L1 curada) nos 90 casos oficiais com cada k, pelo mesmo executor e o mesmo prompt da Fase 3. A probabilidade da causa respondida é lida no primeiro token depois de CAUSA_RAIZ.</p>
<div class="chart baixo"><canvas id="g-cal-k"></canvas></div>
{tab_k}
<h2>Quanto se erra ao responder só os mais prováveis, com {escolhido["k"]} verbetes entregues</h2>
<p>Respondendo só os casos de maior probabilidade: a cobertura (quantos são respondidos) e o risco (erros entre eles). É dela que saem os limiares.</p>
<div class="chart baixo"><canvas id="g-cal-curva"></canvas></div>
{tab_rev}
{bloco_selos}
<h2>Qual número de verbetes ficou, a ponte de versão e a sondagem das probabilidades</h2>
{tab_r8}
{detalhes("Ponte de versão (regra R6)", tab_ponte)}
{detalhes("Sondagem dos logprobs no Ollama instalado", tab_son)}
{detalhes(f"Caso a caso com k = {escolhido['k']} ({len(escolhido.get('casos', []))} casos, da menor probabilidade para a maior)", casos)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["16"], sufixo="-cal")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 20. Fase 4: tela e fixture (corrida 18)

# ! Alteração de IA - Revisar: aba nova (01/11/2026, Fase 4) com a leitura da corrida 18 (o mesmo caso lido da tela e do
# fixture, na mesma sessão do Ollama), lida de resultados_alvo/fase4/tela.json (avaliar_fase4.py --tela): a regra R2
# (mesmo rótulo nos dois lados, b e c, McNemar), o acerto de cada lado por classe, os selos e gatilhos na tela, os rótulos
# dados em cada lado contra o gabarito, o prompt da tela contra o maior da calibração e o caso a caso; sem o arquivo, o
# estado vazio com o cartão da corrida, como as outras abas.
# ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; a corrida 18 decide se o molde do sintoma e a poda
# voltam para revisão antes da noite C (regra R2), e o Eric decide pelo painel.
def secao_tela(tela: dict | None, tela_v2: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos sem b + c, p, "fixture", "rótulo", "gatilho", "poda" nem "harness" soltos.
    # ! Motivo: o texto à vista trazia siglas e números soltos que o Eric pediu para tirar; o cartão do corte sem diferença perdeu o trecho sobre o CORPO, que já está no item "Onde a tela perde" e nas tabelas.
    fontes_ = fontes(["<code>resultados_alvo/fase4/tela.json</code> e <code>.md</code> (<code>avaliar_fase4.py --tela</code>, com <code>--check</code>; blocos <code>tb_f4_tela_*</code>); a repetição com o caso ao vivo revisado em <code>tela_v2.json</code> (<code>--nome tela_v2</code>)",
                      "<code>executar_fase4.py --modo tela</code> (os casos que reproduzem em <code>reproducibilidade.json</code>, k e limiares de <code>limiares.json</code>, ponte de <code>pontes.json</code>; relatórios v2 por caso em <code>fase4_tela/relatorios/</code>)",
                      "roadmap §2.10; plano aprovado da Fase 4, seções 3.3, 5 e 6 (regra R2); ficha 37"])
    vazio = {"resumo": None, "por_classe": [], "rotulos": [], "v2": None}
    if not tela:
        html_ = f'''<section id="tela" hidden>
<h1>Tela e caso escrito: o agente dá o mesmo diagnóstico nos dois?</h1>
<p class="lead">A corrida 18 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/tela.json</code>, gerado por <code>avaliar_fase4.py --tela</code> depois de <code>executar_fase4.py --modo tela --saida fase4_tela</code> (noite B do plano aprovado).</p>
{cartoes_corridas(road, numeros=["18", "18b"], sufixo="-tela")}
{fontes_}
</section>'''
        return vazio, html_
    r = tela["resumo"]
    casos = tela["casos"]
    pcc = tela.get("prompt_contra_calibracao") or {}
    n = r["casos"] or 1
    # ! Alteração de IA - Revisar: (01/11/2026, ficha 37) a aba também lê a repetição da corrida 18 com o caso ao vivo
    # revisado (`tela_v2.json`, corrida 18b): cartão próprio, séries nos dois gráficos, colunas por classe e a comparação
    # caso a caso com a corrida original; sem o arquivo, mostra só a corrida 18.
    # ! Motivo: a regra R2 é relida na repetição, e o Eric decide pelo painel se a revisão do caso ao vivo resolveu.
    v2 = tela_v2 if tela_v2 and tela_v2.get("resumo") else None
    r2 = v2["resumo"] if v2 else None
    casos_v2 = {l["caso"]: l for l in (v2["casos"] if v2 else [])}
    classes_v2 = {x["classe"]: x for x in (v2["por_classe"] if v2 else [])}

    def contagem(campo: str, lista=None) -> dict:
        c: dict = {}
        for l in (casos if lista is None else lista):
            chave = l.get(campo) or "sem rótulo"
            c[chave] = c.get(chave, 0) + 1
        return c

    ct, cf, cg = contagem("rotulo_tela"), contagem("rotulo_fixture"), contagem("gabarito")
    ct2 = contagem("rotulo_tela", list(casos_v2.values())) if v2 else {}
    rotulos = [{"rotulo": x, "tela": ct.get(x, 0), "fixture": cf.get(x, 0), "gabarito": cg.get(x, 0), "tela_v2": ct2.get(x, 0) if v2 else None}
               for x in sorted(set(ct) | set(cf) | set(cg) | set(ct2), key=lambda x: (-(ct.get(x, 0) + cf.get(x, 0) + cg.get(x, 0) + ct2.get(x, 0)), x))]
    mais_tela = max(rotulos, key=lambda x: x["tela"]) if rotulos else None
    por_classe = [{"classe": x["classe"], "nome": CLASSES.get(x["classe"], ""), "casos": x["casos"], "acerto_tela": x["acerto_tela"],
                   "acerto_fixture": x["acerto_fixture"], "concordam": x["concordam"],
                   "acerto_tela_v2": classes_v2.get(x["classe"], {}).get("acerto_tela") if v2 else None,
                   "concordam_v2": classes_v2.get(x["classe"], {}).get("concordam") if v2 else None} for x in tela["por_classe"]]
    comparacao = []
    if v2:
        for l in casos:
            l2 = casos_v2.get(l["caso"])
            if l2:
                comparacao.append({"caso": l["caso"], "gabarito": l["gabarito"], "tela_18": l["rotulo_tela"], "tela_18b": l2["rotulo_tela"], "fixture_18b": l2["rotulo_fixture"],
                                   "acerto_18": l["acerto_tela"], "acerto_18b": l2["acerto_tela"], "concordam_18": l["concordam"], "concordam_18b": l2["concordam"],
                                   "mudou": l["rotulo_tela"] != l2["rotulo_tela"]})
    ganhos = sum(1 for c in comparacao if c["acerto_18b"] and not c["acerto_18"])
    perdas = sum(1 for c in comparacao if c["acerto_18"] and not c["acerto_18b"])
    pior = min(por_classe, key=lambda x: (x["acerto_tela"] / x["casos"] if x["casos"] else 1, -x["casos"])) if por_classe else None
    rotulos_diferentes = r["casos"] - r["concordam"]
    st, sf = r.get("selos_tela") or {}, r.get("selos_fixture") or {}
    acima = pcc.get("acima") or []
    dentro = bool(r.get("dentro_do_limite_r2"))
    cp = tela.get("corpo") or {}
    sem_dif = cp.get("sem_diferenca_contra_contrato")
    chaves_resumo = ("casos", "acerto_tela", "acerto_fixture", "concordam", "b", "c", "discordantes", "limite_r2", "dentro_do_limite_r2", "p_mcnemar",
                     "gatilhos_tela", "divergencias_tela", "segundos_tela_mediana", "segundos_fixture_mediana", "p_tela_mediana", "p_fixture_mediana", "trilha_bytes")
    dados_js = {"resumo": {k: r.get(k) for k in chaves_resumo}, "por_classe": por_classe, "rotulos": rotulos,
                "v2": {"resumo": {k: r2.get(k) for k in chaves_resumo}, "ganhos": ganhos, "perdas": perdas, "mudaram": sum(1 for c in comparacao if c["mudou"])} if v2 else None}
    itens_kpi = [
        ("Mesma causa na tela e no caso escrito (regra R2)", f'{r["concordam"]} de {r["casos"]}',
         f'{fmt(100 * r["concordam"] / n)}%; só um lado acerta em {r["discordantes"]}, limite {r["limite_r2"]}: {"dentro" if dentro else "fora"}'),
        ("Acerto na tela", f'{r["acerto_tela"]} de {r["casos"]}', f'{fmt(100 * r["acerto_tela"] / n)}%; no caso escrito {r["acerto_fixture"]} de {r["casos"]} ({fmt(100 * r["acerto_fixture"] / n)}%)'),
        ("Causa mais respondida na tela", f'{esc(mais_tela["rotulo"])} em {mais_tela["tela"]}' if mais_tela else "n/d",
         f'no caso escrito, em {mais_tela["fixture"]}; é o gabarito de {mais_tela["gabarito"]} dos {r["casos"]} casos' if mais_tela else ""),
        ("Selos na tela (alto / médio / baixo)", f'{st.get("alto", 0)} / {st.get("medio", 0)} / {st.get("baixo", 0)}',
         f'no caso escrito {sf.get("alto", 0)} / {sf.get("medio", 0)} / {sf.get("baixo", 0)}; probabilidade mediana {fmt(r["p_tela_mediana"], 2)} contra {fmt(r["p_fixture_mediana"], 2)}'),
        ("Avisos de checagem extra e divergências na tela", f'{r["gatilhos_tela"]} e {r["divergencias_tela"]}', f'intervenções desligadas nesta corrida ({r.get("intervencoes_tela", 0)} rodadas)'),
        ("Prompt da tela acima do limite da calibração", f'{len(acima)} de {r["casos"]}',
         f'limite de {pcc.get("limite_mais_10_pct")} tokens; o maior prompt da tela tem {pcc.get("maximo_da_tela")}'),
        ("Tempo por caso", f'{fmt(r["segundos_tela_mediana"])} s', f'mediana na tela; {fmt(r["segundos_fixture_mediana"])} s no caso escrito'),
    ]
    if sem_dif is not None:
        itens_kpi.insert(3, ("Casos em que o corte não achou diferença contra o contrato", f'{sem_dif} de {cp.get("casos_lidos")}',
                             f'mesma causa em {cp.get("sem_diferenca_concordam")}; com diferença de campo, em {cp.get("com_diferenca_concordam")} de {cp.get("com_diferenca_contra_contrato")}'))
    if v2:
        n2 = r2["casos"] or 1
        itens_kpi.insert(1, ("Repetição com o caso ao vivo revisado (corrida 18b)", f'{r2["concordam"]} de {r2["casos"]} com a mesma causa',
                             f'acerto na tela {r2["acerto_tela"]} ({fmt(100 * r2["acerto_tela"] / n2)}%) contra {r["acerto_tela"]} na 18; {ganhos} ganhos, {perdas} perdas'))
    tab_comparacao = tabela(["Caso", "Gabarito", "Rótulo na tela (18)", "Rótulo na tela (18b)", "Rótulo no fixture (18b)", "Tela 18", "Tela 18b", "Mesmo rótulo 18", "Mesmo rótulo 18b", "Rótulo da tela mudou"],
                            [[f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c['tela_18'] or 'sem rótulo')}</code>", f"<code>{esc(c['tela_18b'] or 'sem rótulo')}</code>",
                              f"<code>{esc(c['fixture_18b'] or 'sem rótulo')}</code>", "certo" if c["acerto_18"] else "errado", "certo" if c["acerto_18b"] else "errado",
                              "sim" if c["concordam_18"] else "não", "sim" if c["concordam_18b"] else "não", "sim" if c["mudou"] else "não"] for c in comparacao], raw=True) if v2 else ""
    tab_classe = tabela(["Classe", "Casos", "Acerto na tela", "Acerto no fixture", "Mesmo rótulo"] + (["Acerto na tela (18b)", "Mesmo rótulo (18b)"] if v2 else []),
                        [[f'{x["classe"]} {x["nome"]}', x["casos"], x["acerto_tela"], x["acerto_fixture"], x["concordam"]]
                         + ([x["acerto_tela_v2"] if x["acerto_tela_v2"] is not None else "—", x["concordam_v2"] if x["concordam_v2"] is not None else "—"] if v2 else []) for x in por_classe])
    tab_rotulos = tabela(["Rótulo", "Dado na tela", "Dado no fixture", "É o gabarito de"] + (["Dado na tela (18b)"] if v2 else []),
                         [[f"<code>{esc(x['rotulo'])}</code>", x["tela"], x["fixture"], x["gabarito"]] + ([x["tela_v2"]] if v2 else []) for x in rotulos], raw=True)
    tab_casos = tabela(["Caso", "Classe", "Gabarito", "Rótulo na tela", "Rótulo no fixture", "Tela", "Fixture", "Mesmo rótulo", "p tela", "Selo tela", "p fixture", "Selo fixture",
                        "Gatilho", "Divergência", "s tela", "s fixture"],
                       [[f"<code>{esc(l['caso'])}</code>", l["classe"], f"<code>{esc(l['gabarito'])}</code>", f"<code>{esc(l['rotulo_tela'] or 'sem rótulo')}</code>",
                         f"<code>{esc(l['rotulo_fixture'] or 'sem rótulo')}</code>", "certo" if l["acerto_tela"] else "errado", "certo" if l["acerto_fixture"] else "errado",
                         "sim" if l["concordam"] else "não", fmt(l["p_tela"], 2), esc(l.get("selo_tela") or "—"), fmt(l["p_fixture"], 2), esc(l.get("selo_fixture") or "—"),
                         "sim" if l["gatilho_tela"] else "não", "sim" if l["divergencia_tela"] else "não", fmt(l["segundos_tela"]), fmt(l["segundos_fixture"])] for l in casos], raw=True)
    lead = (f'{"Sim" if dentro else "Não"}. Nos {r["casos"]} casos que reproduzem, o agente dá o mesmo rótulo na tela e no fixture em {r["concordam"]} ({fmt(100 * r["concordam"] / n)}%): '
            f'acerta {r["acerto_tela"]} na tela e {r["acerto_fixture"]} no fixture; só a tela acerta em {r["b"]}, só o fixture em {r["c"]} (b + c = {r["discordantes"]}, '
            f'limite da regra R2 = {r["limite_r2"]}: {"dentro" if dentro else "fora"} do limite; p = {fmt(r["p_mcnemar"], 3)}). '
            + (f'Na tela o rótulo mais dado é <code>{esc(mais_tela["rotulo"])}</code>, em {mais_tela["tela"]} casos ({mais_tela["fixture"]} no fixture; gabarito de {mais_tela["gabarito"]}). ' if mais_tela else "")
            + f'{len(acima)} dos {r["casos"]} prompts da tela passam do limite de tokens da calibração.'
            + (f' Na repetição com o caso ao vivo revisado (corrida 18b), o mesmo rótulo sai em {r2["concordam"]} de {r2["casos"]} e a tela acerta {r2["acerto_tela"]} '
               f'(b + c = {r2["discordantes"]}, {"dentro" if r2.get("dentro_do_limite_r2") else "fora"} do limite da regra R2).' if v2 else ""))
    leitura_ = leitura([
        *([f"<strong>Repetição com o caso ao vivo revisado (corrida 18b).</strong> A mesma causa passou de {r['concordam']} para {r2['concordam']} dos {r2['casos']} casos e o acerto na tela de "
           f"{r['acerto_tela']} para {r2['acerto_tela']} (caso escrito: {r['acerto_fixture']} e {r2['acerto_fixture']}). Os casos em que só um lado acertou são {r2['discordantes']}, contra o limite {r2['limite_r2']}: a regra que compara tela e caso escrito (R2) "
           f"{'passa a valer' if r2.get('dentro_do_limite_r2') else 'continua fora do limite'}. Caso a caso, {ganhos} passaram a acertar na tela e {perdas} deixaram de acertar; "
           f"a causa respondida na tela mudou em {sum(1 for c in comparacao if c['mudou'])} casos (tabela de comparação; blocos <code>tb_f4_tela_resumo</code> e <code>tb_f4_tela_casos</code> de <code>tela_v2.json</code>)."] if v2 else []),
        (f"<strong>Regra que compara tela e caso escrito (R2) {'cumprida' if dentro else 'não cumprida'}.</strong> {rotulos_diferentes} casos recebem causas diferentes nos dois lados e em {r['discordantes']} só um lado acerta "
         f"(bloco <code>tb_f4_tela_resumo</code>); o limite é {r['limite_r2']}. "
         + ("" if dentro else "Pelo plano aprovado (regra R2), o molde do sintoma e o corte em código do que o modelo lê no caso ao vivo (poda) voltam para revisão antes da próxima noite com modelo.")),
        (f"<strong>A causa que a tela puxa.</strong> <code>{esc(mais_tela['rotulo'])}</code> sai {mais_tela['tela']} vezes na tela, {mais_tela['fixture']} no caso escrito, e é o gabarito de "
         f"{mais_tela['gabarito']} casos (tabela de causas): o caso ao vivo leva o modelo para uma causa que o caso escrito não sugere." if mais_tela else "<strong>Causas respondidas.</strong> Sem casos."),
        *([f"<strong>Onde a tela perde.</strong> Em {sem_dif} dos {cp.get('casos_lidos')} casos o corte não achou diferença de campo contra o contrato e o CORPO levou ao modelo o primeiro item "
           f"normal da lista (bloco <code>tb_f4_tela_corpo</code>): só {cp.get('sem_diferenca_concordam')} dão a mesma causa e {cp.get('sem_diferenca_colecao_na_tela')} viram "
           f"<code>colecao_no_lugar_de_objeto</code>; em {cp.get('sintoma_sem_medida')} o sintoma por molde diz \"Nenhuma diferença medida contra a referência\". "
           f"Nos {cp.get('com_diferenca_contra_contrato')} casos com diferença de campo, {cp.get('com_diferenca_concordam')} dão a mesma causa. As falhas de lista (contagem, duplicado, "
           "codificação, escala, latência) não são diferenças de campo: o caso ao vivo precisa dizer o que mudou contra a referência em modo normal, que o próprio teste já mede."] if sem_dif is not None else []),
        (f"<strong>A pior classe na tela.</strong> {pior['classe']} {esc(pior['nome'])}: {pior['acerto_tela']} de {pior['casos']} na tela contra {pior['acerto_fixture']} no caso escrito "
         f"(bloco <code>tb_f4_tela_por_classe</code>)." if pior else "<strong>Por classe.</strong> Sem dados."),
        f"<strong>Prompt maior que o da calibração.</strong> {len(acima)} dos {r['casos']} prompts da tela passam de {pcc.get('limite_mais_10_pct')} tokens (o maior da tela tem {pcc.get('maximo_da_tela')}; "
        f"o maior da calibração, {pcc.get('maximo_da_calibracao')}): o caso ao vivo é mais longo que o caso escrito, e os limiares do selo foram calibrados no escrito (plano, seção 3.3).",
        f"<strong>Selos e avisos de checagem extra.</strong> Na tela {st.get('baixo', 0)} casos ficam com selo baixo e {r['gatilhos_tela']} disparam o aviso que dispara a checagem extra; as intervenções ficaram desligadas nesta corrida, "
        f"então a FONTE fica declarada, não verificada. No caso escrito {sf.get('alto', 0)} casos têm selo alto, na tela {st.get('alto', 0)}.",
        f"<strong>Custo.</strong> {fmt(r['segundos_tela_mediana'])} s por caso na tela e {fmt(r['segundos_fixture_mediana'])} s no caso escrito (medianas); a trilha v2 da corrida tem {r['trilha_bytes']} bytes.",
    ])
    html_ = f'''<section id="tela" hidden>
<h1>Tela e caso escrito: o agente dá o mesmo diagnóstico nos dois?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Acerto e concordância por classe de defeito</h2>
<p>Cada caso que reproduz foi diagnosticado duas vezes na mesma sessão do Ollama: lido da tela (roteiro, interceptação, corte em código do que o modelo lê e sintoma por molde) e lido do caso escrito. O gabarito entra só nesta leitura.</p>
<div class="chart"><canvas id="g-tela-classe"></canvas></div>
{tab_classe}
<h2>Que causas cada lado responde</h2>
<p>Quantas vezes cada causa foi respondida na tela e no caso escrito, contra quantas vezes ela é o gabarito.</p>
<div class="chart"><canvas id="g-tela-rotulos"></canvas></div>
{tab_rotulos}
{detalhes(f"Caso a caso ({len(casos)} casos)", tab_casos)}
{detalhes(f"Corrida 18 contra a repetição 18b, caso a caso ({len(comparacao)} casos)", tab_comparacao) if v2 else ""}
{detalhes(f"Prompts da tela acima do limite da calibração ({len(acima)})", "<p>" + ", ".join(f"<code>{esc(c)}</code>" for c in acima) + "</p>" if acima else "<p>nenhum</p>")}
<h2>As corridas no roadmap</h2>
{cartoes_corridas(road, numeros=["18", "18b"], sufixo="-tela")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 21. Fase 4: cura de seletor (corrida 19)

# ! Alteração de IA - Revisar: aba nova (01/11/2026, Fase 4, pacote P4) com a leitura da corrida 19 (cura de seletor), lida
# de resultados_alvo/fase4/cura.json (avaliar_fase4.py --cura): a taxa de cura pela regra R3 (uma cura só conta quando o
# roteiro passa na reexecução; "mesmo elemento" separado de "outro elemento"), o MTTR da detecção à reexecução validada,
# por modo de quebra, por roteiro e pelas duas formas da quebra (harness e variante do PHP, decisão 80), o rendimento de
# cada estratégia de candidato e os casos "outro elemento"; sem o arquivo, o estado vazio com o cartão da corrida.
# ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; a corrida 19 é a primeira medida de MTTR só do agente
# e o Eric decide pelo painel se a cura em código basta para a Fase 5.
def secao_cura(cura: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos com "tempo até o resultado (MTTR)" e "o próprio teste" no lugar de MTTR e harness soltos.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; o cartão da quebra armada pelo teste contra a variante do PHP ficou com menos texto, e os valores seguem nas tabelas recolhidas.
    fontes_ = fontes(["<code>resultados_alvo/fase4/cura.json</code> e <code>.md</code> (<code>avaliar_fase4.py --cura</code>, com <code>--check</code>; blocos <code>tb_f4_cura_*</code>)",
                      "<code>executar_fase4.py --modo cura</code> (<code>cura_seletor.py</code>: candidatos em ordem fixa e verificação em código; <code>cenarios_fase4.QUEBRAS</code>: as 16 células; "
                      "<code>Programacao/CobaiaFront/quebra.php</code>: a variante do front ligada por <code>?quebra=</code> ou cookie; relatórios v2 por execução em <code>fase4_cura/relatorios/</code>)",
                      "roadmap §2.11; plano aprovado da Fase 4, seções 3.6, 5 (regra R3) e 6; fichas 29 (opção c, decisão 80), 35 e 36"])
    vazio = {"resumo": None, "por_modo": [], "por_roteiro": [], "por_forma": [], "estrategias": []}
    if not cura or not cura.get("resumo"):
        html_ = f'''<section id="cura" hidden>
<h1>Cura de seletor: quando o localizador quebra, o agente acha outro em código e o roteiro passa?</h1>
<p class="lead">A corrida 19 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/cura.json</code>, gerado por <code>avaliar_fase4.py --cura</code> depois de <code>executar_fase4.py --modo cura --saida fase4_cura</code> (pacote P4 do plano aprovado, sem modelo).</p>
{cartoes_corridas(road, numeros=["19"], sufixo="-cura")}
{fontes_}
</section>'''
        return vazio, html_
    r = cura["resumo"]
    f = cura.get("formas") or {}
    por_modo = [{"modo": x["modo"], "execucoes": x["execucoes"], "quebrou": x["quebrou"], "curadas": x["curadas"], "mesmo_elemento": x["mesmo_elemento"],
                 "outro_elemento": x["outro_elemento"], "nao_curadas": x["nao_curadas"], "nao_quebrou": x["nao_quebrou"], "taxa": x["taxa_de_cura_pct"],
                 "mttr": x["mttr_mediana_s"]} for x in cura["por_modo"]]
    por_roteiro = [{"roteiro": x["roteiro"], "execucoes": x["execucoes"], "quebrou": x["quebrou"], "curadas": x["curadas"], "mesmo_elemento": x["mesmo_elemento"],
                    "outro_elemento": x["outro_elemento"], "nao_curadas": x["nao_curadas"], "nao_quebrou": x["nao_quebrou"], "taxa": x["taxa_de_cura_pct"],
                    "mttr": x["mttr_mediana_s"]} for x in cura["por_roteiro"]]
    por_forma = [{"forma": x["forma"], "quebrou": x["quebrou"], "curadas": x["curadas"], "taxa": x["taxa_de_cura_pct"], "mttr": x["mttr_mediana_s"],
                  "mesmo_elemento": x["mesmo_elemento"], "outro_elemento": x["outro_elemento"]} for x in cura["por_forma"]]
    estrategias = [{"estrategia": x["estrategia"], "gerada": x["gerada"], "passou_estaticas": x["passou_estaticas"], "reexecutada": x["reexecutada"], "aplicada": x["aplicada"],
                    "recusada_em": x["recusada_em"]} for x in cura.get("por_estrategia") or []]
    mais_aplicada = max(estrategias, key=lambda x: x["aplicada"]) if estrategias else None
    pior_modo = min(por_modo, key=lambda x: (x["taxa"] if x["taxa"] is not None else 101, -x["quebrou"])) if por_modo else None
    melhor_modo = max(por_modo, key=lambda x: (x["taxa"] if x["taxa"] is not None else -1, x["quebrou"])) if por_modo else None
    dados_js = {"resumo": {k: r.get(k) for k in ("execucoes", "quebras_detectadas", "nao_quebrou", "curadas", "nao_curadas", "taxa_de_cura_pct", "mesmo_elemento",
                                                 "outro_elemento", "mttr_mediana_s", "mttr_min_s", "mttr_max_s", "repeticoes", "limiar_nome", "formas")},
                "por_modo": por_modo, "por_roteiro": por_roteiro, "por_forma": por_forma, "estrategias": estrategias}
    fh = next((x for x in por_forma if x["forma"] == "harness"), None)
    fp = next((x for x in por_forma if x["forma"] == "php"), None)
    itens_kpi = [
        ("Curadas, pela regra R3 (o roteiro precisa passar)", f'{r["curadas"]} de {r["quebras_detectadas"]}',
         f'{fmt(r["taxa_de_cura_pct"])}% das quebras detectadas; {r["nao_quebrou"]} execuções não quebraram'
         if r["taxa_de_cura_pct"] is not None else f'{r["execucoes"]} execuções; nenhuma quebra detectada'),
        ("Mesmo elemento da referência", f'{r["mesmo_elemento"]} de {r["curadas"]}',
         f'{r["outro_elemento"]} cura(s) com outro elemento que fez o roteiro passar (regra R3, tabela abaixo)'),
        ("Tempo até o resultado (MTTR), mediana", f'{fmt(r["mttr_mediana_s"])} s' if r["mttr_mediana_s"] is not None else "n/d",
         f'da detecção à reexecução validada; entre {fmt(r["mttr_min_s"])} e {fmt(r["mttr_max_s"])} s' if r["mttr_mediana_s"] is not None else "nenhuma cura validada"),
        ("Quebra armada pelo próprio teste contra a variante do PHP", f'{f.get("mesmo_resultado", 0)} de {f.get("celulas_comparadas", 0)} células com o mesmo resultado',
         f'árvore da página igual em {f.get("arvore_igual", 0)} células'
         + (f'; difere em {", ".join(f.get("arvore_diferente") or [])}' if f.get("arvore_diferente") else "")
         + (f'; cura {fmt(fh["taxa"])}% no próprio teste e {fmt(fp["taxa"])}% no PHP' if fh and fp and fh["taxa"] is not None and fp["taxa"] is not None else "")),
        ("Estratégia que mais curou", f'{esc(mais_aplicada["estrategia"])} em {mais_aplicada["aplicada"]}' if mais_aplicada else "n/d",
         "; ".join(f'{esc(x["estrategia"])} {x["aplicada"]}' for x in estrategias if x["aplicada"] and x is not mais_aplicada) or "nenhuma outra estratégia curou"),
        ("Limiar do nome parecido", fmt(r["limiar_nome"]), "o quanto o nome do candidato precisa se parecer; fixado no P4"),
    ]
    tab_modo = tabela(["Modo de quebra", "Execuções", "Quebraram", "Curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento", "Não curadas", "Não quebrou", "MTTR mediana (s)"],
                      [[f"<code>{esc(x['modo'])}</code>", x["execucoes"], x["quebrou"], x["curadas"], fmt(x["taxa"]) if x["taxa"] is not None else "n/d", x["mesmo_elemento"], x["outro_elemento"],
                        x["nao_curadas"], x["nao_quebrou"], fmt(x["mttr"]) if x["mttr"] is not None else "n/d"] for x in por_modo], raw=True)
    tab_roteiro = tabela(["Roteiro", "Execuções", "Quebraram", "Curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento", "Não curadas", "Não quebrou", "MTTR mediana (s)"],
                         [[f"<code>{esc(x['roteiro'])}</code>", x["execucoes"], x["quebrou"], x["curadas"], fmt(x["taxa"]) if x["taxa"] is not None else "n/d", x["mesmo_elemento"], x["outro_elemento"],
                           x["nao_curadas"], x["nao_quebrou"], fmt(x["mttr"]) if x["mttr"] is not None else "n/d"] for x in por_roteiro], raw=True)
    tab_forma = tabela(["Forma da quebra", "Quebraram", "Curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento", "MTTR mediana (s)"],
                       [[esc(x["forma"]), x["quebrou"], x["curadas"], fmt(x["taxa"]) if x["taxa"] is not None else "n/d", x["mesmo_elemento"], x["outro_elemento"],
                         fmt(x["mttr"]) if x["mttr"] is not None else "n/d"] for x in por_forma], raw=True)
    verifs = ["resolve_um_elemento", "visivel_e_habilitado", "mesmo_papel", "nome_parecido", "efeito_na_reexecucao"]
    tab_estr = tabela(["Estratégia", "Gerada", "Passou as estáticas", "Reexecutada", "Aplicada (curou)"] + [f"Recusada em {v}" for v in verifs],
                      [[f"<code>{esc(x['estrategia'])}</code>", x["gerada"], x["passou_estaticas"], x["reexecutada"], x["aplicada"]] + [x["recusada_em"].get(v, 0) for v in verifs]
                       for x in estrategias], raw=True)
    tab_outro = tabela(["Execução", "Roteiro", "Modo", "Forma", "Estratégia", "Seletor curado", "MTTR (s)"],
                       [[f"<code>{esc(x['id'])}</code>", esc(x["roteiro"]), f"<code>{esc(x['modo'])}</code>", esc(x["forma"]), f"<code>{esc(x['aplicado'])}</code>",
                         f"<code>{esc(x['seletor_curado'])}</code>", fmt(x["mttr_s"]) if x.get("mttr_s") is not None else "n/d"] for x in cura.get("outro_elemento") or []], raw=True)
    tab_nao = tabela(["Execução", "Roteiro", "Modo", "Forma", "Falha", "Reexecuções"],
                     [[f"<code>{esc(x['id'])}</code>", esc(x["roteiro"]), f"<code>{esc(x['modo'])}</code>", esc(x["forma"]), f"<code>{esc(x.get('falha') or '')}</code>", x["reexecucoes"]]
                      for x in cura.get("nao_curadas") or []], raw=True)
    tab_exec = tabela(["Execução", "Localizador", "Quebrou", "Curada", "Estratégia", "Seletor curado", "Mesmo elemento", "MTTR (s)", "Reexecuções"],
                      [[f"<code>{esc(x['id'])}</code>", f"<code>{esc(x['localizador'])}</code>", "sim" if x["quebrou"] else "não", "sim" if x["curado"] else "não",
                        f"<code>{esc(x['aplicado'])}</code>" if x.get("aplicado") else "", f"<code>{esc(x['seletor_curado'])}</code>" if x.get("seletor_curado") else "",
                        {True: "sim", False: "não"}.get(x["mesmo_elemento"], "n/d"), fmt(x["mttr_s"]) if x.get("mttr_s") is not None else "n/d", x["reexecucoes"]]
                       for x in cura.get("execucoes") or []], raw=True)
    lead = (f'{"Sim" if r["taxa_de_cura_pct"] is not None and r["taxa_de_cura_pct"] >= 50 else "Não"}, na medida da corrida 19: de {r["quebras_detectadas"]} quebras detectadas em '
            f'{r["execucoes"]} execuções (quatro roteiros do front legado, quatro modos de quebra, {len(r.get("formas") or [])} formas, {r["repeticoes"]} repetições), '
            f'{r["curadas"]} foram curadas pela regra R3 ({fmt(r["taxa_de_cura_pct"]) if r["taxa_de_cura_pct"] is not None else "n/d"}%), {r["mesmo_elemento"]} com o mesmo elemento da referência e '
            f'{r["outro_elemento"]} com outro elemento que fez o roteiro passar; o MTTR do agente, da detecção à reexecução validada, tem mediana de '
            f'{fmt(r["mttr_mediana_s"]) if r["mttr_mediana_s"] is not None else "n/d"} s. '
            + (f'O modo mais curado é <code>{esc(melhor_modo["modo"])}</code> ({fmt(melhor_modo["taxa"])}%) e o menos, <code>{esc(pior_modo["modo"])}</code> ({fmt(pior_modo["taxa"]) if pior_modo["taxa"] is not None else "n/d"}%). '
               if melhor_modo and pior_modo else "")
            + (f'As duas formas de quebra dão o mesmo resultado em {f.get("mesmo_resultado", 0)} das {f.get("celulas_comparadas", 0)} células comparadas.' if f.get("celulas_comparadas") else ""))
    leitura_ = leitura([
        f"<strong>Regra R3.</strong> Só conta como cura a reexecução em que o roteiro inteiro passa com o candidato no lugar do localizador: {r['curadas']} de {r['quebras_detectadas']} "
        f"(bloco <code>tb_f4_cura_resumo</code>); {r['outro_elemento']} dessas passaram com outro elemento, listado na tabela própria, e {r['nao_curadas']} não foram curadas.",
        (f"<strong>Por modo de quebra.</strong> <code>{esc(melhor_modo['modo'])}</code> cura {melhor_modo['curadas']} de {melhor_modo['quebrou']} e <code>{esc(pior_modo['modo'])}</code> "
         f"{pior_modo['curadas']} de {pior_modo['quebrou']} (bloco <code>tb_f4_cura_por_modo</code>): é onde a geração em código mais falha." if melhor_modo and pior_modo else "<strong>Por modo.</strong> Sem dados."),
        (f"<strong>Estratégias.</strong> <code>{esc(mais_aplicada['estrategia'])}</code> é a que mais levou o roteiro ao fim ({mais_aplicada['aplicada']} vezes); a tabela de estratégias diz em que "
         f"verificação cada uma foi recusada (bloco <code>tb_f4_cura_estrategias</code>)." if mais_aplicada else "<strong>Estratégias.</strong> Sem dados."),
        (f"<strong>Quebra armada pelo próprio teste contra a variante do PHP (decisão 80).</strong> A árvore da página quebrada é a mesma nas duas formas em {f.get('arvore_igual', 0)} das {f.get('celulas_comparadas', 0)} células e o "
         f"resultado é o mesmo em {f.get('mesmo_resultado', 0)}" + (f"; taxa de cura {fmt(fh['taxa'])}% no próprio teste e {fmt(fp['taxa'])}% no PHP" if fh and fp and fh["taxa"] is not None and fp["taxa"] is not None else "")
         + " (blocos <code>tb_f4_cura_formas</code> e <code>tb_f4_cura_por_forma</code>)."),
        f"<strong>Tempo até o resultado (MTTR).</strong> Mediana de {fmt(r['mttr_mediana_s']) if r['mttr_mediana_s'] is not None else 'n/d'} s, entre {fmt(r['mttr_min_s']) if r['mttr_min_s'] is not None else 'n/d'} e "
        f"{fmt(r['mttr_max_s']) if r['mttr_max_s'] is not None else 'n/d'} s: é a primeira medida de MTTR só do agente, sem linha de base manual (a linha de base é a Fase 5).",
        "<strong>Limitação declarada.</strong> A quebra é armada, não ocorrida; cada célula usa, no passo do alvo, o estilo de localizador que o modo quebra (por id, por classe, por texto ou "
        "por caminho na estrutura), e a mudança de texto acrescenta uma palavra; um sinônimo ficaria abaixo do limiar do nome.",
    ])
    html_ = f'''<section id="cura" hidden>
<h1>Cura de seletor: quando o localizador quebra, o agente acha outro em código e o roteiro passa?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Cura por modo de quebra</h2>
<p>Cada barra empilha as execuções do modo: curadas com o mesmo elemento da referência, curadas com outro elemento (regra R3), não curadas e as que não quebraram (o localizador sobreviveu à mutação).</p>
<div class="chart"><canvas id="g-cura-modo"></canvas></div>
{tab_modo}
<h2>Cura por roteiro e tempo até o resultado (MTTR)</h2>
<p>As mesmas contagens por roteiro do front legado; o tempo é a mediana, em segundos, da detecção à reexecução validada.</p>
<div class="chart"><canvas id="g-cura-roteiro"></canvas></div>
{tab_roteiro}
<h2>As duas formas da quebra</h2>
{tab_forma}
{detalhes("O que cada estratégia de candidato rendeu", tab_estr)}
{detalhes(f"Curas com outro elemento ({len(cura.get('outro_elemento') or [])})", tab_outro)}
{detalhes(f"Execuções não curadas ({len(cura.get('nao_curadas') or [])})", tab_nao)}
{detalhes(f"Execução a execução ({len(cura.get('execucoes') or [])})", tab_exec)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["19"], sufixo="-cura")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ Fase 4: biblioteca em produção e ciclo de correção (corrida 20)

# ! Alteração de IA - Revisar: (03/11/2026, Fase 4, pacote P5) a aba "Biblioteca em produção", lida de
# resultados_alvo/fase4/biblioteca.json (avaliar_fase4.py --biblioteca): o lote, o que cada filtro barrou, a regra R5 nos
# inéditos, a regra R4 no ciclo de correção, a sonda repetida com recuperação por id e a recuperação dos verbetes aprendidos.
# ! Motivo: regra do painel (uma aba por análise, números só dos JSON); a corrida 20 é a quinta análise da Fase 4.
def secao_biblioteca(bibl: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões e itens de leitura à vista reescritos sem b = / c = e sem p; a regra R5 passa a dizer "N passaram a acertar e M passaram a errar".
    # ! Motivo: o texto à vista trazia b e c soltos, que o Eric pediu para tirar; os mesmos números aparecem agora na frase, e o teste de painel confere a frase nova.
    fontes_ = fontes(["<code>resultados_alvo/fase4/biblioteca.json</code> e <code>.md</code> (<code>avaliar_fase4.py --biblioteca</code>, com <code>--check</code>; blocos <code>tb_f4_biblioteca_*</code>)",
                      "<code>executar_fase4.py --modo biblioteca</code> (<code>biblioteca_fase4.py</code>: os 13 filtros em código da decisão 65, a operação de correção, a recuperação por id, a regra R5; "
                      "<code>sonda_correcao.py --recuperacao-por-id</code>; relatórios v2 por caso em <code>fase4_biblioteca/relatorios/</code>)",
                      "roadmap §2.12 e §4.2; plano aprovado da Fase 4, seções 3.7, 5 (regras R4 e R5) e 6; fichas 32 e 26; decisão 65"])
    vazio = {"resumo": None, "filtros": [], "reavaliacao": None, "correcao": None}
    if not bibl or not bibl.get("resumo") or not bibl["resumo"].get("casos"):
        html_ = f'''<section id="biblioteca" hidden>
<h1>Biblioteca em produção: o que o agente propõe passa pelos filtros, melhora os inéditos e o ciclo de correção marca o que foi corrigido?</h1>
<p class="lead">A corrida 20 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/biblioteca.json</code>, gerado por <code>avaliar_fase4.py --biblioteca</code> depois de <code>executar_fase4.py --modo biblioteca --saida fase4_biblioteca</code> (pacote P5 do plano aprovado, com modelo, noite C).</p>
{cartoes_corridas(road, numeros=["20"], sufixo="-bib")}
{fontes_}
</section>'''
        return vazio, html_
    r = bibl["resumo"]
    lote = bibl.get("lote") or {}
    reav = bibl.get("reavaliacao")
    corr = bibl.get("correcao")
    sonda = bibl.get("sonda")
    rec_ = bibl.get("recuperacao") or {}
    filtros_ = [{"filtro": x["filtro"], "recusas": x["recusas"]} for x in bibl.get("filtros") or []]
    mais_barra = max(filtros_, key=lambda x: x["recusas"]) if filtros_ and any(x["recusas"] for x in filtros_) else None
    sem_rec = rec_.get("aprendidos_sem_recuperacao") or []
    dados_js = {"resumo": {k: r.get(k) for k in ("casos", "da_tela", "do_fixture", "acertos_diagnostico", "acerto_pct", "propostas", "aceitas", "abstencoes", "para_revisao",
                                                 "recusadas_p5", "recusadas_fase3", "inferencias", "segundos")},
                "filtros": filtros_, "reavaliacao": ({k: reav.get(k) for k in ("n", "b", "c", "acerto_base_pct", "acerto_novo_pct", "veredito", "p_mcnemar")} if reav else None),
                "correcao": ({k: corr.get(k) for k in ("universo", "desligados", "marcados", "acertos", "falsos_positivos", "perdidos", "precisao_pct", "revocacao_pct", "kappa")} if corr else None)}
    itens_kpi = [
        ("Edições no lote", f'{r["aceitas"]} de {r["propostas"]}',
         f'propostas nos {r["casos"]} casos de aprendizado; em {r["abstencoes"]} o modelo respondeu NENHUMA (sem proposta)'),
        ("Barradas e seguradas", f'{r["recusadas_p5"] + r["para_revisao"]} pelos filtros do P5',
         f'{r["recusadas_p5"]} recusadas pelos 13 filtros em código; {r["para_revisao"]} seguradas para revisão humana'),
        ("Regra R5: o lote melhora os inéditos?", f'{reav["veredito"]}: {reav["b"]} passaram a acertar, {reav["c"]} a errar' if reav else "não medida",
         f'acerto {fmt(reav["acerto_base_pct"])}% com a cópia curada e {fmt(reav["acerto_novo_pct"])}% com o lote, nos {reav["n"]} inéditos pareados' if reav else "sem reavaliação"),
        ("Regra R4, ciclo de correção", f'precisão {fmt(corr["precisao_pct"])}%, revocação {fmt(corr["revocacao_pct"])}%' if corr and corr.get("precisao_pct") is not None else
         (f'{corr["marcados"]} marcada(s) de {corr["desligados"]} desligado(s)' if corr else "não medida"),
         f'{corr["marcados"]} marcada(s) como corrigido em {corr["universo"]} casos; {corr["acertos"]} certa(s), {corr["falsos_positivos"]} sem razão, {corr["perdidos"]} perdida(s)' if corr else "sem ciclo de correção"),
        ("Sonda com recuperação por id", f'{sonda["mudaram_proposta"]} de {sonda["casos"] - sonda["sem_sonda_anterior"]} mudaram a proposta' if sonda and sonda["casos"] > sonda["sem_sonda_anterior"] else (f'{sonda["casos"]} casos' if sonda else "não repetida"),
         f'{sonda["mencionam_correcao"]} mencionam a correção; {sonda["abstencoes"]} NENHUMA; {sonda["com_verbete_por_id"]} com verbete pelo id; {sonda["sem_sonda_anterior"]} sem sonda anterior' if sonda else "a sonda de 28/09 não foi repetida"),
        ("Verbetes aprendidos (ficha 32)", f'{len(sem_rec)} de {len(rec_.get("aprendidos_na_calibracao") or {})} nunca recuperados',
         f'na calibração com k = {r.get("k")}; nesta corrida {rec_.get("casos_com_verbete_por_id", 0)} caso(s) receberam verbete pelo id'),
    ]
    tab_filtros = tabela(["Filtro em código (decisão 65)", "Propostas barradas ou seguradas"], [[f"<code>{esc(x['filtro'])}</code>", x["recusas"]] for x in filtros_], raw=True)
    tab_lote = tabela(["Verbete", "Operação", "Caso", "Peso", "Granularidade"],
                      [[f"<code>{esc(e['verbete'])}</code>", esc(e["operacao"]), f"<code>{esc(e['caso'])}</code>", e.get("peso"), esc(e.get("granularidade") or "")] for e in lote.get("lista") or []], raw=True)
    tab_rev = tabela(["Verbete", "Operação", "Caso", "Peso"], [[f"<code>{esc(e['verbete'])}</code>", esc(e["operacao"]), f"<code>{esc(e['caso'])}</code>", e.get("peso")] for e in lote.get("revisao") or []], raw=True)
    tab_corr = tabela(["Caso", "Modo", "Verbetes", "Modo desligado", "Reproduziu antes", "Passou depois", "Fio mudou", "Árvore mudou", "Marcado", "Motivo"],
                      [[f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['modo'])}</code>", ", ".join(f"<code>{esc(v)}</code>" for v in c.get("verbetes") or []), "sim" if c["desligado"] else "não",
                        "sim" if c["reproduziu_antes"] else "não", "sim" if c["passou_depois"] else "não", "sim" if c["ha_diff_http"] else "não", "sim" if c["ha_diff_arvore"] else "não",
                        "sim" if c["marcado"] else "não", esc(c.get("motivo") or "")] for c in (corr or {}).get("por_caso") or []], raw=True)
    tab_sonda = tabela(["Caso", "Rótulo agora", "Acertou", "Propostas", "Aceitas", "NENHUMA", "Motivos", "Menciona a correção", "Verbetes pelo id", "Rótulo em 28/09", "Propostas em 28/09", "Mudou"],
                       [[f"<code>{esc(x['caso'])}</code>", esc(x["rotulo"] or ""), "sim" if x["acertou"] else "não", x["n_propostas"], x["n_aceitas"], "sim" if x["abstencao"] else "não",
                         ", ".join(f"<code>{esc(m)}</code>" for m in x["motivos"]) or "nenhum", "sim" if x["menciona_correcao"] else "não", ", ".join(f"<code>{esc(v)}</code>" for v in x["por_id"]) or "nenhum",
                         esc(x["rotulo_anterior"] or "n/d"), x["n_propostas_anterior"] if x["n_propostas_anterior"] is not None else "n/d",
                         "sem sonda anterior" if x["mudou_proposta"] is None else ("sim" if x["mudou_proposta"] else "não")] for x in (sonda or {}).get("por_caso") or []], raw=True)
    tab_rec = tabela(["Verbete aprendido", f"Vezes na calibração (k = {r.get('k')})", "Vezes pelo id nesta corrida"],
                     [[f"<code>{esc(v)}</code>", n, (rec_.get("verbetes_por_id") or {}).get(v, 0)] for v, n in sorted((rec_.get("aprendidos_na_calibracao") or {}).items())], raw=True)
    tab_casos = tabela(["Caso", "Origem", "Rótulo", "Acertou", "Selo", "Propostas", "Aceitas", "Para revisão", "Recusadas", "NENHUMA", "Pelo id", "Verbetes editados"],
                       [[f"<code>{esc(c['caso'])}</code>", esc(c["origem"] or ""), esc(c["rotulo"] or ""), "sim" if c["acertou"] else "não", esc(c["selo"] or ""), c["n_propostas"], c["n_aceitas"], c["para_revisao"],
                         ", ".join(f"<code>{esc(m)}</code>" for m in c.get("recusadas") or []), "sim" if c["abstencao"] else "não", ", ".join(f"<code>{esc(v)}</code>" for v in c.get("recuperacao_por_id") or []),
                         ", ".join(f"<code>{esc(v)}</code>" for v in c.get("verbetes_editados") or [])] for c in bibl.get("casos") or []], raw=True)
    lead = (f'Na corrida 20, o modelo propôs {r["propostas"]} edições nos {r["casos"]} casos de aprendizado e {r["aceitas"]} entraram no lote; os filtros em código barraram {r["recusadas_p5"]} e '
            f'seguraram {r["para_revisao"]} para revisão humana (o validador da Fase 3 recusou {r["recusadas_fase3"]} antes). '
            + (f'Nos {reav["n"]} inéditos, o lote {"entra" if reav["veredito"] == "aceito" else "fica em espera"} pela regra R5: b = {reav["b"]} passaram a acertar e c = {reav["c"]} passaram a errar '
               f'({fmt(reav["acerto_base_pct"])}% para {fmt(reav["acerto_novo_pct"])}% de acerto). ' if reav else "A regra R5 não foi medida. ")
            + (f'No ciclo de correção, a marca corrigido teve precisão {fmt(corr["precisao_pct"])}% e revocação {fmt(corr["revocacao_pct"])}% contra os {corr["desligados"]} casos com o modo desligado (regra R4). '
               if corr and corr.get("precisao_pct") is not None else (f'No ciclo de correção, {corr["marcados"]} de {corr["desligados"]} casos desligados foram marcados. ' if corr else ""))
            + (f'Na sonda repetida com recuperação por id, {sonda["mudaram_proposta"]} caso(s) mudaram a proposta em relação a 28/09 e {sonda["mencionam_correcao"]} mencionam a correção registrada.' if sonda else ""))
    leitura_ = leitura([
        f"<strong>Lote e filtros.</strong> {r['aceitas']} edições entraram (peso {lote.get('peso', 0)}); "
        + (f"o filtro que mais barrou foi <code>{esc(mais_barra['filtro'])}</code> ({mais_barra['recusas']})" if mais_barra else "nenhum filtro do P5 barrou proposta")
        + f" (blocos <code>tb_f4_biblioteca_filtros</code> e <code>tb_f4_biblioteca_rejeicoes</code>); {r['abstencoes']} abstenções contam como saída válida.",
        (f"<strong>Regra R5.</strong> Nos {reav['n']} inéditos, {reav['b']} passaram a acertar e {reav['c']} passaram a errar: {reav['veredito']} (bloco <code>tb_f4_biblioteca_reavaliacao</code>); a base é {esc(reav.get('origem_da_base') or 'n/d')}."
         if reav else "<strong>Regra R5.</strong> Não medida."),
        (f"<strong>Regra R4.</strong> {corr['marcados']} marcadas, {corr['acertos']} certas, {corr['falsos_positivos']} marcadas sem razão e {corr['perdidos']} perdidas em {corr['universo']} casos com sintoma antes "
         f"(bloco <code>tb_f4_biblioteca_correcao</code>); concordância além do acaso (kappa) {fmt(corr['kappa'], 3) if corr.get('kappa') is not None else 'n/d'}." if corr else "<strong>Regra R4.</strong> Não medida."),
        (f"<strong>Sonda.</strong> {sonda['casos']} casos reapresentados com os verbetes do próprio caso no contexto: {sonda['mudaram_proposta']} mudaram a proposta, {sonda['mencionam_correcao']} mencionam a correção, "
         f"{sonda['abstencoes']} abstiveram-se (bloco <code>tb_f4_biblioteca_sonda</code>)." if sonda else "<strong>Sonda.</strong> Não repetida."),
        f"<strong>Ficha 32.</strong> {len(sem_rec)} verbetes aprendidos nunca entraram num contexto da calibração ({', '.join(f'<code>{esc(v)}</code>' for v in sem_rec) or 'nenhum'}); "
        "a decisão da ficha os manda para <code>aprendidos_em_espera/</code> (<code>biblioteca_fase4.py --espera</code>, comando do Eric).",
        "<strong>O que não muda sozinho.</strong> A biblioteca de produção só recebe o lote por <code>biblioteca_fase4.py --promover</code>, depois da planilha de revisão humana preenchida (porta final da decisão 65).",
    ])
    html_ = f'''<section id="biblioteca" hidden>
<h1>Biblioteca em produção: o que o agente propõe passa pelos filtros, melhora os inéditos e o ciclo de correção marca o que foi corrigido?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>O que cada filtro barrou</h2>
<p>Os 13 filtros em código da decisão 65, na ordem fixa; a regra dos 40% segura (não recusa) a nota em verbete presente em 40% ou mais dos contextos da calibração.</p>
<div class="chart"><canvas id="g-bib-filtros"></canvas></div>
{tab_filtros}
<h2>Regra R5: o lote nos inéditos</h2>
<div class="chart"><canvas id="g-bib-reavaliacao"></canvas></div>
{detalhes(f"Edições do lote ({lote.get('edicoes', 0)})", tab_lote)}
{detalhes(f"Seguradas para revisão humana ({lote.get('para_revisao', 0)})", tab_rev)}
<h2>Regra R4: o ciclo de correção</h2>
{tab_corr}
<h2>A sonda de 28/09 repetida com recuperação por id</h2>
{tab_sonda}
{detalhes("Verbetes aprendidos: recuperação na calibração e pelo id", tab_rec)}
{detalhes(f"Caso a caso ({len(bibl.get('casos') or [])})", tab_casos)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["20"], sufixo="-bib")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ Fase 4: ensaio dos cenários da Fase 5 (corrida 21)

# ! Alteração de IA - Revisar: (04/11/2026, Fase 4, pacote P6) a aba "Cenários da Fase 5", lida de
# resultados_alvo/fase4/cenarios.json (avaliar_fase4.py --cenarios): Task Success com intervalo de Wilson e MTTR com intervalo
# por reamostragem, no geral, por tipo e por cenário, a ficha da falha de cada cenário (o que a detecção acusou), o tempo por
# execução com a estimativa da Fase 5 e o protocolo da linha de base manual.
# ! Motivo: regra do painel (uma aba por análise, números só dos JSON); a corrida 21 é a sexta análise da Fase 4, e a ficha da
# falha de cada cenário é o que o protocolo da linha de base manual entrega ao integrante.
# ! Alteração de IA - Revisar: (04/11/2026, corrida 21b) secao_cenarios recebe também a leitura da repetição (cenarios_v2.json): com ela, os
# números principais são os da 21b, o gráfico do MTTR mostra as duas corridas, entra a tabela "As duas corridas" e a execução sem Task
# Success aparece com o nome da corrida.
# ! Motivo: a 21b roda com a correção da cura e é a leitura vigente do ensaio; a 21 é o registro de como o defeito apareceu, e o painel,
# onde o Eric decide, tem de mostrar as duas, como a aba "Tela e fixture" faz com as corridas 18 e 18b.
def secao_cenarios(cen_: dict | None, cen_v2: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos com "chegou ao resultado (Task Success)" e "tempo até o resultado (MTTR)", sem Wilson nem reamostragem.
    # ! Motivo: o texto à vista trazia siglas e nomes de método estatístico que o Eric pediu para tirar; o título "Execuções sem Task Success" passou a "Execuções que não chegaram ao resultado" e o teste do painel foi ajustado.
    protocolo = ("<p>A linha de base manual da Fase 5 segue o protocolo em <code>Documentacao/memorial/5-metodo-e-ferramental/protocolo-linha-de-base-manual.md</code>: "
                 "três integrantes, cada um nos dez cenários numa ordem sorteada com semente fixa, com a falha ligada pelo ajudante "
                 "<code>linha_de_base_manual.py</code> (as mesmas funções da corrida) e a planilha <code>planilha-linha-de-base-manual.csv</code>.</p>")
    fontes_ = fontes([("<code>resultados_alvo/fase4/cenarios.json</code> e <code>.md</code> (<code>avaliar_fase4.py --cenarios</code>, com <code>--check</code>; blocos <code>tb_f4_cenarios_*</code>); "
                       "a repetição com a correção da cura em <code>cenarios_v2.json</code> (<code>--nome cenarios_v2</code>)"),
                      ("<code>executar_fase4.py --modo cenarios</code> (catálogo <code>cenarios_fase4.CENARIOS_DO_ENSAIO</code>; cronômetro <code>mttr_monotonico</code>; "
                       "conferência do diagnóstico <code>diagnostico_conferido</code>; relatórios v2 por execução em <code>fase4_ensaio/relatorios/</code> e <code>fase4_ensaio_v2/relatorios/</code>)"),
                      "protocolo da linha de base manual; roadmap §2.13 e §2.14 (corridas 21 e 21b); plano aprovado da Fase 4, seções 3.9 e 5 (P6); fichas 35 e 36, decisão 79"])
    vazio = {"geral": None, "por_tipo": [], "por_cenario": []}
    if not cen_ or not (cen_.get("geral") or {}).get("n"):
        html_ = f'''<section id="cenarios" hidden>
<h1>Cenários da Fase 5: quanto tempo o agente leva da detecção ao resultado e em quantos cenários acerta?</h1>
<p class="lead">A corrida 21 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/cenarios.json</code>, gerado por <code>avaliar_fase4.py --cenarios</code> depois de <code>rodar_fase4.ps1 -Modo cenarios -Saida fase4_ensaio -Repeticoes 1</code> (pacote P6 do plano aprovado, com modelo, de dia).</p>
{protocolo}
{cartoes_corridas(road, numeros=["21", "21b"], sufixo="-cen")}
{fontes_}
</section>'''
        return vazio, html_
    anterior = None
    if cen_v2 and (cen_v2.get("geral") or {}).get("n"):
        anterior, cen_ = cen_, cen_v2
    antes = {x["cenario"]: x for x in (anterior or {}).get("por_cenario") or []}
    g, t = cen_["geral"], cen_.get("tempo") or {}
    cond, det = cen_.get("condicoes") or {}, cen_.get("deteccao") or {}
    nav, banco = cen_.get("navegador") or {}, cen_.get("banco") or {}
    por_tipo = {x["tipo"]: x for x in cen_.get("por_tipo") or []}

    def nd(v, casas: int = 1) -> str:
        return "n/d" if v is None else fmt(v, casas)

    def ts(x: dict) -> str:
        return f'{x["sucessos"]} de {x["n"]}'

    def faixa(lo, hi, unidade: str) -> str:
        return "sem intervalo" if lo is None else f"{nd(lo)} a {nd(hi)}{unidade}"

    dados_js = {"geral": {k: g.get(k) for k in ("n", "sucessos", "task_success_pct", "mttr_media_s")},
                "por_tipo": [{k: x.get(k) for k in ("tipo", "n", "sucessos", "mttr_media_s")} for x in cen_.get("por_tipo") or []],
                "por_cenario": [{**{k: x.get(k) for k in ("cenario", "tipo", "n", "sucessos", "mttr_media_s")}, "mttr_anterior": (antes.get(x["cenario"]) or {}).get("mttr_media_s")}
                                for x in cen_.get("por_cenario") or []],
                "duas_corridas": bool(anterior)}
    itens_kpi = [("Chegou ao resultado (Task Success)", ts(g), f'{nd(g["task_success_pct"])}% das {g["n"]} execuções; margem de incerteza de {faixa(g["wilson_lo_pct"], g["wilson_hi_pct"], "%")}')]
    itens_kpi.append(("Tempo até o resultado (MTTR), média", f'{nd(g["mttr_media_s"])} s', f'margem de incerteza de {faixa(g["mttr_ic_lo_s"], g["mttr_ic_hi_s"], " s")}; mediana {nd(g["mttr_mediana_s"])} s'))
    for tipo, nome in (("contrato", "Contrato (ficha 35)"), ("localizador", "Localizador")):
        if tipo in por_tipo:
            x = por_tipo[tipo]
            itens_kpi.append((nome, ts(x), f'chegaram ao resultado; tempo médio {nd(x["mttr_media_s"])} s ({faixa(x["mttr_ic_lo_s"], x["mttr_ic_hi_s"], " s")})'))
    itens_kpi.append(("Tempo por execução", f'{nd(t.get("segundos_media"))} s', f'{t.get("execucoes")} execuções em {nd(t.get("segundos_total"))} s; a Fase 5 levaria {nd(t.get("estimativa_fase5_h"), 2)} h'))
    itens_kpi.append(("Detecção", f'{sum(det.values())} de {g["n"]}', f'{det.get("conferencia_do_roteiro", 0)} pelo roteiro, {det.get("contrato_no_fio", 0)} pelo fio (regra R1), {det.get("passo_do_localizador", 0)} pelo localizador'))
    tab_tipo = tabela(["Tipo", "Execuções", "Task Success", "Task Success (%)", "Wilson 95% (%)", "MTTR médio (s)", "Reamostragem 95% (s)", "MTTR mediano (s)"],
                      [[esc(x["tipo"]), x["n"], x["sucessos"], nd(x["task_success_pct"]), faixa(x["wilson_lo_pct"], x["wilson_hi_pct"], ""), nd(x["mttr_media_s"]),
                        faixa(x["mttr_ic_lo_s"], x["mttr_ic_hi_s"], ""), nd(x["mttr_mediana_s"])] for x in cen_.get("por_tipo") or []], raw=True)
    # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) a ficha da falha sai da tabela por cenário para uma tabela própria.
    # ! Motivo: com os dados reais a tabela passava da largura da página e a coluna da ficha, a que o protocolo da linha de base manual usa, ficava fora da vista.
    tab_cen = tabela(["Cenário", "Tipo", "Classe", "Causa esperada", "Execuções", "Task Success", "MTTR médio (s)", "Rótulos do diagnóstico", "Segundos por execução"],
                     [[f"<code>{esc(x['cenario'])}</code>", esc(x["tipo"]), x.get("classe"), f"<code>{esc(x.get('causa_esperada') or '')}</code>", x["n"], x["sucessos"], nd(x["mttr_media_s"]),
                       ", ".join(f"<code>{esc(k)}</code> {v}" for k, v in (x.get("rotulos") or {}).items()), nd(x.get("segundos_media"))] for x in cen_.get("por_cenario") or []], raw=True)
    tab_fichas = tabela(["Cenário", "O que a detecção acusou"],
                        [[f"<code>{esc(x['cenario'])}</code>", esc(" / ".join(x.get("fichas_da_falha") or []) or "n/d")] for x in cen_.get("por_cenario") or []], raw=True)
    # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) as execuções sem Task Success, com o rótulo e a falha da cura.
    # ! Motivo: na corrida 21 a tabela por cenário só mostrava o zero do login; quem decide pelo painel precisa ver que o diagnóstico acertou
    # e que a cura falhou, e a explicação fica no roadmap, mostrado no cartão da corrida.
    sem_ts = [("21", x) for x in (anterior or {}).get("sem_task_success") or []] + [("21b" if anterior else "21", x) for x in cen_.get("sem_task_success") or []]
    bloco_sem = ""
    if sem_ts:
        tab_sem = tabela(["Corrida", "Cenário", "Repetição", "Tipo", "Detectou", "Rótulo do diagnóstico", "Causa esperada", "Falha da cura", "Segundos"],
                         [[n_, f"<code>{esc(x['cenario'])}</code>", x.get("repeticao"), esc(x["tipo"]), "sim" if x.get("detectou") else "não", f"<code>{esc(x.get('rotulo') or 'n/d')}</code>",
                           f"<code>{esc(x.get('causa_esperada') or '')}</code>", f"<code>{esc(x.get('falha_da_cura') or 'n/d')}</code>", nd(x.get("segundos"))] for n_, x in sem_ts], raw=True)
        bloco_sem = f'<h2>Execuções que não chegaram ao resultado (sem Task Success)</h2>\n<p>Bloco <code>tb_f4_cenarios_sem_sucesso</code>; a explicação de cada uma fica no roadmap, no cartão da corrida abaixo.</p>\n{tab_sem}'
    bloco_duas = ""
    itens_duas: list[str] = []
    if anterior:
        por = cen_.get("por_cenario") or []
        mesmo = sum(1 for x in por if (antes.get(x["cenario"]) or {}).get("rotulos") == x.get("rotulos"))
        tab_duas = tabela(["Cenário", "Tipo", "Task Success 21", "Task Success 21b", "MTTR 21 (s)", "MTTR 21b (s)", "Segundos 21", "Segundos 21b", "Mesmo rótulo"],
                          [[f"<code>{esc(x['cenario'])}</code>", esc(x["tipo"]), (antes.get(x["cenario"]) or {}).get("sucessos"), x["sucessos"], nd((antes.get(x["cenario"]) or {}).get("mttr_media_s")),
                            nd(x["mttr_media_s"]), nd((antes.get(x["cenario"]) or {}).get("segundos_media")), nd(x.get("segundos_media")),
                            "sim" if (antes.get(x["cenario"]) or {}).get("rotulos") == x.get("rotulos") else "não"] for x in por], raw=True)
        bloco_duas = f'<h2>As duas corridas, cenário a cenário</h2>\n<p>A corrida 21, antes da correção da cura, e a 21b, depois dela: blocos <code>tb_f4_cenarios_por_cenario</code> de <code>cenarios.md</code> e <code>cenarios_v2.md</code>.</p>\n{tab_duas}'
        itens_duas = [(f"<strong>As duas corridas.</strong> Na corrida 21 chegaram ao resultado {ts(anterior['geral'])} execuções e, na 21b, com os candidatos da cura verificados numa página refeita até o passo que falhou, {ts(g)}. "
                       f"A mesma causa respondida em {mesmo} de {len(por)} cenários. O tempo por execução passou de {nd((anterior.get('tempo') or {}).get('segundos_media'))} s a {nd(t.get('segundos_media'))} s. A explicação está no roadmap, §2.13 e §2.14.")]
    ct, lc = por_tipo.get("contrato"), por_tipo.get("localizador")
    abertura = (f'Na repetição do ensaio (corrida 21b: {cond.get("repeticoes")} repetição dos dez cenários da ficha 36, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), já com a correção da cura, '
                f'o agente teve Task Success em {ts(g)} execuções, contra {ts(anterior["geral"])} na corrida 21, e MTTR médio de ' if anterior else
                f'No ensaio da corrida 21 ({cond.get("repeticoes")} repetição dos dez cenários da ficha 36, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), '
                f'o agente teve Task Success em {ts(g)} execuções e MTTR médio de ')
    lead = (abertura + f'{nd(g["mttr_media_s"])} s da detecção ao fim do cronômetro'
            + (f'; no contrato, {ts(ct)}, e no localizador, {ts(lc)}' if ct and lc else "")
            + f'. Cada execução levou {nd(t.get("segundos_media"))} s em média, o que põe a Fase 5 (dez cenários com cinco repetições) em {nd(t.get("estimativa_fase5_h"), 2)} h de máquina.')
    leitura_ = leitura([
        *itens_duas,
        ("<strong>O que o cronômetro mede.</strong> No contrato (ficha 35), da detecção ao diagnóstico conferido em código (quatro linhas, causa dentro das 23, campo existente no caso), "
         "e chegar ao resultado (Task Success) é acertar a causa e o campo; no localizador, da detecção à reexecução validada, descontada a restauração do banco, e chegar ao resultado é aplicar a cura com o roteiro concluído sem erro."),
        (f"<strong>Condições.</strong> Navegador {', '.join(esc(v) for v in nav.get('versoes') or []) or 'n/d'} em todas as execuções ({'uma versão só' if nav.get('unica') else 'versões diferentes'}); "
         f"banco restaurado e conferido por hash no começo de cada repetição ({'o mesmo hash em todas' if banco.get('unico') else 'hashes diferentes'})."),
        "<strong>Ensaio, não Fase 5.</strong> Uma repetição serve para dimensionar a noite da Fase 5 e conferir o protocolo; as margens de incerteza com uma execução por cenário são largas e não sustentam comparação.",
        "<strong>Linha de base manual.</strong> A coluna \"O que a detecção acusou\" é a ficha da falha que o integrante recebe na sessão, a mesma frase que a detecção do agente acusou.",
    ])
    html_ = f'''<section id="cenarios" hidden>
<h1>Cenários da Fase 5: quanto tempo o agente leva da detecção ao resultado e em quantos cenários acerta?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Tempo até o resultado (MTTR) por cenário</h2>
<div class="chart"><canvas id="g-cen-mttr"></canvas></div>
<h2>Chegou ao resultado (Task Success), por cenário</h2>
<div class="chart"><canvas id="g-cen-ts"></canvas></div>
{tab_tipo}
{bloco_sem}
{bloco_duas}
<h2>Cenário a cenário</h2>
<p>Blocos <code>tb_f4_cenarios_resumo</code>, <code>tb_f4_cenarios_por_tipo</code>, <code>tb_f4_cenarios_por_cenario</code> e <code>tb_f4_cenarios_tempo</code> de <code>{"cenarios_v2.md" if anterior else "cenarios.md"}</code>.</p>
{tab_cen}
<h2>A ficha da falha de cada cenário</h2>
<p>O que a detecção do agente acusou: a frase que o integrante recebe na sessão da linha de base manual.</p>
{tab_fichas}
<h2>A linha de base manual</h2>
{protocolo}
<h2>As corridas no roadmap</h2>
{cartoes_corridas(road, numeros=["21", "21b"], sufixo="-cen")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ Fase 4: fechamento da fase (pacote P8)

# ! Alteração de IA - Revisar: (05/11/2026, Fase 4, pacote P8) a aba "Fechamento da fase": a tabela das regras (seção 10) e as seções 1, 11, 12 e 15 lidas do relatório da fase, os cartões lidos dos JSON das leituras vigentes (tela_v2, cura, cenarios_v2, leitura_revisao_trilha) e as fichas abertas.
# ! Motivo: o plano previa uma aba da fase (seção 3.8), e as sete abas por análise não dizem o que fechou, o que ficou como limitação e o que depende do Eric. Ele decide pelo painel, não pelo Markdown. Nenhum número é digitado aqui.
ESTADOS_REGRA = {"cumprida": ("Cumprida", "concluida"), "ressalva": ("Cumprida com ressalva", "andamento"), "medida": ("Medida", "outro"), "nao": ("Não cumprida", "nao_cumprida")}


def _classe_regra(estado: str) -> str:
    e = estado.strip().lower()
    if e.startswith("não cumprida") or e.startswith("nao cumprida"):
        return "nao"
    if "ressalva" in e:
        return "ressalva"
    return "cumprida" if e.startswith("cumprida") else "medida"


def _celula_regra(estado: str) -> str:
    """O chip com o estado e, abaixo dele, o que vem depois dos dois-pontos: um chip longo não quebra linha e esprime as outras colunas."""
    classe = _classe_regra(estado)
    resto = estado.partition(":")[2].strip()
    return chip(ESTADOS_REGRA[classe][1], ESTADOS_REGRA[classe][0]) + (f'<br><span class="nota">{pt.inline(resto)}</span>' if resto else "")


# ! Alteração de IA - Revisar: (05/11/2026, decisões 90 a 92) as corridas da Fase 4 que o roadmap ainda não marca como feitas viram um cartão de número, uma frase na resposta e os cartões de corrida, e a seção 13 do relatório fica à vista.
# ! Motivo: com as fichas 42 a 45 fechadas, a aba dizia só "nenhuma ficha aberta", como se não restasse nada, e as corridas 18c, 21c, 23 e 24 ainda vão rodar. Lidas pelo estado no roadmap, elas saem da lista sozinhas quando a linha passar a `feita`.
def _corridas_que_faltam_f4(road: dict | None) -> list[str]:
    """As corridas da Fase 4 (da 16 em diante) que o roadmap ainda não marca como feitas."""
    faltam = []
    for c in (road or {}).get("corridas", []):
        m = re.match(r"\d+", c.numero)
        if m and int(m.group()) >= 16 and c.classe != "feita":
            faltam.append(c.numero)
    return faltam


def _lista_em_frase(itens: list[str]) -> str:
    return " e ".join(itens) if len(itens) < 3 else ", ".join(itens[:-1]) + " e " + itens[-1]


def secao_fechamento_f4(relatorio_md: str | None, pend: list, md_doc_para_html, tela: dict | None = None, cura: dict | None = None, cenarios: dict | None = None, revisao: dict | None = None,
                        road: dict | None = None, cartoes_corridas=None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) três cartões (tela, cura, cenários) reescritos sem "b + c", "rótulo", MTTR e Task Success soltos.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; os números são os mesmos, lidos dos mesmos JSON.
    titulo = "Fechamento da Fase 4: o agente na tela fez o que o plano pediu?"
    if not relatorio_md:
        return {"contagem": {}, "fichas_abertas": 0}, (f'<section id="fechamentof4" hidden>\n<h1>{titulo}</h1>\n<p class="lead">O relatório da fase ainda não existe: '
                                                       '<code>Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md</code> sai do pacote P8.</p>\n</section>')
    md = pt.sem_comentarios(relatorio_md)
    secs = {t.split(".")[0]: c for t, c in pt.secoes(md) if t and t[0].isdigit()}
    cab, linhas, _ = pt.primeira_tabela(secs["10"])
    col = {c: i for i, c in enumerate(cab)}
    cont = Counter(_classe_regra(r[col["Estado"]]) for r in linhas)
    nomes_nao = [r[col["Regra"]] for r in linhas if _classe_regra(r[col["Estado"]]) == "nao"]
    abertas = [f for b in pend for f in b.fichas if f.aberta]
    faltam = _corridas_que_faltam_f4(road)
    trs = "".join(
        f'<tr data-valor="{_classe_regra(r[col["Estado"]])}"><td>{pt.inline(r[col["Regra"]])}</td><td>{pt.inline(r[col["O que ela pede"]])}</td><td>{esc(r[col["Corrida"]])}</td>'
        f'<td>{pt.inline(r[col["Resultado"]])}</td><td>{_celula_regra(r[col["Estado"]])}</td></tr>'
        for r in linhas)
    tab = ('<div class="filtros filtro-tabela" data-alvo="tab-regras-f4" role="group" aria-label="Filtro das regras">'
           f'<button type="button" data-valor="todos" aria-pressed="true">Todas ({len(linhas)})</button>'
           + "".join(f'<button type="button" data-valor="{k}" aria-pressed="false">{esc(ESTADOS_REGRA[k][0])} ({cont[k]})</button>' for k in ESTADOS_REGRA if cont[k])
           + '</div><div class="tabela" id="tab-regras-f4"><table><thead><tr><th>Regra</th><th>O que ela pede</th><th>Corrida</th><th>Resultado</th><th>Estado</th></tr></thead>'
           f'<tbody>{trs}</tbody></table></div>')
    lista = "".join(f'<li><a href="#{f.id_html}" data-ir="pendencias|{f.id_html}"><span class="numero">{f.numero}</span> {pt.inline(f.titulo)}</a>'
                    f'<br><span class="nota">Recomendação: {pt.inline(f.campos.get("Recomendação", "n/d"))}</span></li>' for f in abertas)
    itens_kpi = [("Regras cumpridas", f'{cont["cumprida"] + cont["ressalva"]} de {len(linhas)}', f'{cont["ressalva"]} com ressalva, indicada na coluna Estado' + (f'; {cont["medida"]} só medida, sem limite fixado' if cont["medida"] else "")),
                 ("Não cumpridas", str(cont["nao"]), " e ".join(nomes_nao) or "nenhuma")]
    if tela:
        r = tela["resumo"]
        itens_kpi.append(("Mesma causa na tela e no caso escrito", f'{r["concordam"]} de {r["casos"]}', f'corrida 18b; só um lado acerta em {r["discordantes"]}, limite {r["limite_r2"]}; limitação declarada'))
    if cura:
        r = cura["resumo"]
        itens_kpi.append(("Quebras curadas em código", f'{r["curadas"]} de {r["execucoes"]}', f'corrida 19, sem modelo; mediana {fmt(r["mttr_mediana_s"], 3)} s até o resultado; os 100% vêm do desenho'))
    if cenarios:
        g = cenarios["geral"]
        itens_kpi.append(("Cenários que chegaram ao resultado (Task Success)", f'{g["sucessos"]} de {g["n"]}', f'corrida 21b; média de {fmt(g["mttr_media_s"], 1)} s até o resultado; uma repetição, sem linha de base'))
    if revisao:
        r = revisao["resumo"]
        itens_kpi.append(("Medida com revisor humano", "não feita", f'{r["respostas_do_revisor"]} resposta do Eric e {r["pareceres_aprovados"]} pareceres do Claude aprovados'))
    if faltam:
        itens_kpi.append(("Corridas que faltam antes da Fase 5", str(len(faltam)), f'{_lista_em_frase(faltam)}, pedidas pelas respostas às fichas 42 a 44'))
    itens_kpi.append(("Decisões do Eric em aberto", str(len(abertas)), "fichas na aba Pendências; não impedem a Fase 5" if abertas else "nenhuma ficha aberta"))
    resposta = (f'Em parte. Das {len(linhas)} regras, {cont["cumprida"]} {"foi cumprida" if cont["cumprida"] == 1 else "foram cumpridas"} sem ressalva, {cont["ressalva"]} com ressalva'
                + (f', {cont["medida"]} só medida' if cont["medida"] else "")
                + f' e {cont["nao"]} não: {" e ".join(nomes_nao) or "nenhuma"}. A medida com revisor humano da especificação da trilha não foi feita e fica como limitação declarada (decisão 87).'
                + (f' Faltam {len(abertas)} decisões do Eric, que não impedem a Fase 5.' if abertas else "")
                + (f' Antes da Fase 5 faltam as corridas {_lista_em_frase(faltam)}, e as leituras delas podem mudar estes números.' if faltam else ""))
    html_ = f'''<section id="fechamentof4" hidden>
<h1>{titulo}</h1>
<p class="lead">{pt.inline(resposta)}</p>
{kpis(itens_kpi)}
<h2>O que depende do Eric</h2>
{"<ol class='lista-eric'>" + lista + "</ol>" if abertas else ("<p>Nenhuma ficha aberta. Os pré-requisitos das corridas abaixo dizem o que ainda depende dele.</p>" if faltam else "<p>Nenhuma ficha aberta.</p>")}
{"<h2>O que falta antes da Fase 5</h2>" + cartoes_corridas(road, numeros=faltam, sufixo="-f4") if faltam and cartoes_corridas else ""}
<h2>O que o plano previa e não saiu</h2>
{md_doc_para_html(secs.get("13", ""))}
<h2>As regras, uma a uma</h2>
{tab}
{detalhes("O que a fase perguntou e o que respondeu (relatório, seção 1)", md_doc_para_html(secs.get("1", "")))}
{detalhes("Limitações declaradas (relatório, seção 12)", md_doc_para_html(secs.get("12", "")))}
{detalhes("O que a Fase 4 entrega à Fase 5 (relatório, seção 11)", md_doc_para_html(secs.get("11", "")))}
{detalhes("O que a próxima versão do documento do TCC precisa carregar (relatório, seção 15)", md_doc_para_html(secs.get("15", "")))}
{fontes(["<code>3-resultados-e-analises/fase-4-relatorio.md</code>, seções 1, 10, 11, 12, 13 e 15, com os blocos <code>tb_f4_*</code> colados por <code>avaliar_fase4.py --colar</code>", "<code>resultados_alvo/fase4/tela_v2.json</code>, <code>cura.json</code>, <code>cenarios_v2.json</code> e <code>leitura_revisao_trilha.json</code>", "<code>pendencias.md</code> (fichas abertas)", "<code>roadmap.md</code>, §2 (as corridas que faltam, pelo estado)", "anexo de <code>claude-memoria/plano-aprovado-fase-4.md</code> (desvios do plano)"])}
</section>'''
    return {"contagem": dict(cont), "fichas_abertas": len(abertas)}, html_


# ------------------------------------------------------------------ Fase 4: avaliação da própria trilha (corrida 22)

# ! Alteração de IA - Revisar: (04/11/2026, Fase 4, pacote P7) a aba "Avaliação da trilha", lida de resultados_alvo/fase4/trilha.json
# (avaliar_fase4.py --trilha): TPR x TNR de cada sinal da trilha contra os erros reais (o principal é a divergência do nó; acaso
# 0,25), as intervenções com o limite inferior, a repetição da base, a sonda de pós-racionalização, as três mutações contra o nó
# previsto (verbete trocado: recuperacao; contrato alterado: poda; seletor quebrado: cura), o seletor roteiro a roteiro, a amostra
# dos relatórios da sessão de revisão e a tabela caso a caso; sem o arquivo, o estado vazio com o cartão da corrida.
# ! Motivo: regra do painel (uma aba por análise, números só dos JSON); a corrida 22 é a sétima análise da Fase 4 e o Eric decide
# pelo painel se a trilha vale como prova (especificação da trilha, seção 12).
# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) a aba ganhou a divergência só por gatilho e o selo baixo nos cartões, os intervalos de
# Wilson, o controle da sonda e a tabela das inferências de mesmo prompt; `revisao_preenchida` guarda a tabela caso a caso até a planilha da sessão de
# revisão estar preenchida, e o texto das mutações diz que os 100% são esperados por construção.
# ! Motivo: a sessão de revisão é às cegas e este painel é publicado e é o que o Eric lê: a tabela diz quais relatórios estão certos. Com só 5 erros, um
# número sem intervalo engana; e dizer "100% no nó previsto" sem dizer que o nó sai em código da entrada mutada faria parecer um resultado do modelo.
def secao_trilha(tri: dict | None, road: dict, cartoes_corridas, revisao_preenchida: bool = False, rev: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos, o parágrafo "O que a aba mede" e itens de leitura à vista reescritos sem TPR x TNR, Wilson, "gatilho", "poda" e "rótulo" soltos.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; o cartão das mutações perdeu o detalhe por tipo, que já está no gráfico e na tabela, e os números seguem lidos do JSON.
    fontes_ = fontes(["<code>resultados_alvo/fase4/trilha.json</code> e <code>.md</code> (<code>avaliar_fase4.py --trilha</code>, com <code>--check</code>; blocos <code>tb_f4_trilha_*</code>); "
                      "a planilha da sessão de revisão em <code>resultados_alvo/fase4/revisao_trilha.md</code>, os relatórios dela em <code>resultados_alvo/fase4/relatorios_revisao_trilha/</code>, a pré-análise do Claude em <code>resultados_alvo/fase4/pre_analise_revisao_trilha.md</code> e a leitura em <code>resultados_alvo/fase4/leitura_revisao_trilha.json</code> (<code>avaliar_fase4.py --revisao</code>, blocos <code>tb_f4_revisao_*</code>)",
                      "<code>executar_fase4.py --modo avaliacao_trilha</code> (<code>avaliacao_trilha.py</code>: os nós <code>poda</code> e <code>recuperacao</code> em código, as quatro "
                      "intervenções de <code>diagnostico_ao_vivo.py</code>, a sonda, as mutações e o diff de <code>trilha.diff_contra_referencia</code>)",
                      "especificação da trilha, seções 5, 6.1, 9 e 12; plano aprovado da Fase 4, seções 5 (P7) e 6 (corrida 22); roadmap §2.15; ficha 39"])
    o_que_mede = ("<p>Três perguntas da especificação da trilha (seção 12), respondidas sem gabarito no agente e com gabarito só na leitura: (a) a divergência que a trilha "
                  "sinaliza coincide com os erros reais? A medida é a nota que sobe quando o sinal pega os erros e deixa os acertos em paz (TPR x TNR); um sinal jogado ao acaso dá 0,25. (b) Quando a "
                  "falha é injetada de propósito (um verbete trocado na busca, o contrato alterado no corte em código do que o modelo lê, o seletor quebrado na cura), o primeiro nó que diverge da trilha "
                  "da base é o nó previsto? (c) A FONTE só justifica a resposta depois de dada (pós-racionalização)? Um trecho que afirma a causa respondida é plantado num verbete entregue que a FONTE não citou, "
                  "e a sonda mede se ela passa a citá-lo com a mesma causa respondida. Depois da corrida, uma sessão de revisão com o Eric, de até 12 relatórios (até 6 certos e até 6 errados, "
                  "sorteados com semente fixa), mede o tempo até a decisão, a localização do erro e a adesão apropriada.</p>")
    vazio = {"sinais": [], "mutacoes": [], "resumo": None}
    if not tri or not (tri.get("resumo") or {}).get("casos"):
        html_ = f'''<section id="trilha" hidden>
<h1>Avaliação da trilha: ela aponta os erros reais e o passo certo quando a falha é injetada?</h1>
<p class="lead">A corrida 22 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/trilha.json</code>, gerado por <code>avaliar_fase4.py --trilha</code> depois de <code>rodar_fase4.ps1 -Modo avaliacao_trilha -Saida fase4_trilha</code> (noite D do plano aprovado, com modelo).</p>
{o_que_mede}
{cartoes_corridas(road, numeros=["22"], sufixo="-tri")}
{fontes_}
</section>'''
        return vazio, html_
    r, so, fo, rep, cond = tri["resumo"], tri.get("sonda") or {}, tri.get("fonte") or {}, tri.get("repeticao") or {}, tri.get("condicoes") or {}
    sinais = tri.get("sinais") or []
    mutacoes = tri.get("mutacoes") or []
    por_tipo = {m["tipo"]: m for m in mutacoes}
    sel = tri.get("seletor") or {}
    amostra = tri.get("amostra_revisao") or []
    intervencoes = tri.get("intervencoes") or []
    inter = {x["tipo"]: x for x in intervencoes}
    pares = tri.get("mesmo_prompt") or []
    par_troca = next((x for x in pares if x["par"] == "verbete_trocado_e_troca"), None)
    por_sinal = {s["sinal"]: s for s in sinais}
    principal, gat, selo = por_sinal.get("divergencia"), por_sinal.get("por_gatilho"), por_sinal.get("selo_baixo")

    def nd(v, casas: int = 2) -> str:
        return "n/d" if v is None else fmt(v, casas)

    def de(a, b) -> str:
        return f"{a} de {b}"

    def wilson_(ic) -> str:
        return "n/d" if not ic else f"{fmt(ic[0])} a {fmt(ic[1])}"

    def pegou(s: dict | None, verbo: str = "pegou") -> str:
        return "n/d" if not s else f"{verbo} {s['vp']} de {s['erros']} erros e acusou {s['fp']} de {s['acertos']} acertos"

    texto = [m for m in mutacoes if m["tipo"] != "seletor_quebrado"]
    prev_texto, apl_texto = sum(m["previsto"] for m in texto), sum(m["aplicaveis"] for m in texto)
    prev_total, apl_total = sum(m["previsto"] for m in mutacoes), sum(m["aplicaveis"] for m in mutacoes)
    dados_js = {"sinais": [{k: s.get(k) for k in ("sinal", "tpr", "tnr", "produto")} for s in sinais],
                "mutacoes": [{k: m.get(k) for k in ("tipo", "previsto", "outro_no", "sem_divergencia", "sem_alvo")} for m in mutacoes],
                "resumo": {k: r.get(k) for k in ("casos", "acertos", "erros", "tpr", "tnr", "produto")}}
    previstas = cond.get("inferencias_previstas")
    itens_kpi = [("Nota da divergência, com todas as intervenções", nd(r.get("produto")), f'{pegou(principal)}; o acaso dá {fmt(r.get("acaso"), 2)}'),
                 ("Nota só pelo aviso de checagem extra, como o agente roda", nd((gat or {}).get("produto")), f'{pegou(gat, "pegaria")} (contado, não rodado assim)'),
                 ("Nota do selo baixo, sem inferência a mais", nd((selo or {}).get("produto")), f'{pegou(selo)}'),
                 ("Acerto nos casos", de(r["acertos"], r["casos"]), f'{nd(r.get("acerto_pct"), 1)}% no caso escrito; {cond.get("modelo") or ""}, Ollama {cond.get("versao_ollama") or "n/d"}'),
                 ("Falhas injetadas que apontaram o nó previsto", de(prev_total, apl_total), "esperado por construção: o nó sai em código da entrada mutada (ver a leitura)"),
                 ("FONTE que só justifica a resposta (pós-racionalização)", f'{nd(so.get("taxa_pct"), 1)}%', f'{de(so.get("pos_racionalizacao"), so.get("com_alvo"))} casos citaram o verbete plantado; sem plantar, {de(so.get("controle_cita", 0), so.get("controle_n", 0))}'),
                 ("Inferências", str(r.get("inferencias")), f'{previstas} previstas; a diferença são as mutações de contrato sem alvo' if previstas is not None else "")]
    tab_sinais = tabela(["Sinal", "O que é", "Pegou (VP)", "Deixou passar (FN)", "Acusou acerto (FP)", "Deixou em paz (VN)", "TPR", "TNR", "TPR x TNR", "TPR, Wilson 95% (%)", "TNR, Wilson 95% (%)"],
                        [[f"<code>{esc(s['sinal'])}</code>", esc(s.get("descricao") or ""), s["vp"], s["fn"], s["fp"], s["vn"], nd(s["tpr"]), nd(s["tnr"]), nd(s["produto"]), wilson_(s.get("ic_tpr")), wilson_(s.get("ic_tnr"))] for s in sinais], raw=True)
    tab_inter = tabela(["Intervenção", "O que é", "Rodou em", "Mudou o rótulo", "Só limite inferior", "Queda média de p"],
                       [[f"<code>{esc(x['tipo'])}</code>", esc(x.get("descricao") or ""), x["n"], x["mudou_rotulo"], x["limite_inferior"], nd(x.get("queda_media_p"))] for x in intervencoes], raw=True)
    tab_pares = tabela(["Par de inferências", "O que é", "Pares", "Mesmo prompt", "Mesma resposta", "Mesma FONTE", "Mesmo rótulo"],
                       [[f"<code>{esc(x['par'])}</code>", esc(x.get("descricao") or ""), x["n"], x["mesmo_prompt"], x["mesma_resposta"], x["mesma_fonte"], x["mesmo_rotulo"]] for x in pares], raw=True)
    tab_mut = tabela(["Mutação", "Nó previsto", "Casos", "Aplicáveis", "Sem alvo", "Apontou o nó previsto", "Apontou outro nó", "Sem divergência", "Rótulo mudou", "Previsto (%)"],
                     [[f"<code>{esc(m['tipo'])}</code>", f"<code>{esc(m['no_previsto'])}</code>", m["casos"], m["aplicaveis"], m["sem_alvo"], m["previsto"], m["outro_no"], m["sem_divergencia"],
                       m["rotulo_mudou"], nd(m.get("previsto_pct"), 1)] for m in mutacoes], raw=True)
    tab_sel = tabela(["Roteiro", "Modo mutado", "Cura dourada", "Cura mutada", "Rótulo dourado", "Rótulo mutado", "Primeiro nó divergente", "Previsto (cura)"],
                     [[f"<code>{esc(x['roteiro'])}</code>", f"<code>{esc(x.get('modo_mutado') or '')}</code>",
                       f"<code>{esc(x['estrategia_dourada'])}</code>" if x.get("curada_dourada") else "sem cura", f"<code>{esc(x['estrategia_mutada'])}</code>" if x.get("curada_mutada") else "sem cura",
                       f"<code>{esc(x.get('rotulo_dourado') or 'n/d')}</code>", f"<code>{esc(x.get('rotulo_mutado') or 'n/d')}</code>",
                       f"<code>{esc(x['primeiro_no'])}</code>" if x.get("primeiro_no") else "sem divergência", "sim" if x.get("aponta_o_previsto") else ("não" if x.get("aponta_o_previsto") is False else "n/d")]
                      for x in sel.get("roteiros") or []], raw=True)
    # ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) a lista dos casos da amostra só entra depois da sessão; antes, a aba aponta para a página da sessão.
    # ! Motivo: o nome e a classe dizem a família do defeito e estreitam a causa verdadeira, e a posição na lista é a mesma da página, que mostra só um nome neutro.
    tab_amostra = (tabela(["Posição", "Caso", "Classe", "Relatório"], [[x["posicao"], f"<code>{esc(x['caso'])}</code>", x.get("classe"), f"<code>{esc(x['relatorio'])}</code>"] for x in amostra], raw=True)
                   if revisao_preenchida else
                   ('<p class="nota">A lista dos casos entra aqui depois da sessão: o nome e a classe dizem a família do defeito, e a posição na lista é a mesma da '
                    f'<a href="{URL_SESSAO_REVISAO}" target="_blank" rel="noopener">página da sessão de revisão</a>, que mostra só um nome neutro.</p>'))
    if revisao_preenchida:
        tab_casos = tabela(["Caso", "Classe", "Gabarito", "Rótulo", "Resultado", "p", "Selo", "Falha", "Divergência", "Por gatilho", "Remoção ou troca", "Sem documentação", "Limite inferior", "Sonda", "Verbete trocado", "Contrato alterado"],
                           [[f"<code>{esc(c['caso'])}</code>", c.get("classe"), f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c.get('rotulo') or 'n/d')}</code>", "certo" if c["acerto"] else "errado",
                             nd(c.get("p_rotulo")), esc(c.get("selo") or "n/d"), esc(c.get("falha") or ""), "sim" if c["sinais"]["divergencia"] else "não", "sim" if c["sinais"].get("por_gatilho") else "não",
                             "sim" if c["sinais"]["remocao_ou_troca"] else "não", "sim" if c["sinais"]["sem_documentacao"] else "não", c.get("limite_inferior"), esc(c.get("sonda") or ""), esc(c.get("verbete_trocado") or ""),
                             esc(c.get("contrato_alterado") or "")] for c in tri.get("casos") or []], raw=True)
        bloco_casos = detalhes("Caso a caso (bloco tb_f4_trilha_casos)", tab_casos)
    else:
        bloco_casos = ('<p class="nota">A tabela com o resultado de cada caso entra nesta aba depois da sessão de revisão, quando a planilha <code>revisao_trilha.md</code> estiver preenchida: '
                       'a sessão é às cegas, e a tabela diria quais relatórios estão certos. Por isso também vale não abrir <code>trilha.md</code> nem <code>trilha.json</code> antes dela.</p>')
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 86) o bloco da sessão: quem decidiu cada relatório, o parecer do Claude contra o gabarito, o caso a caso e o aviso de que a medida com revisor humano não foi feita.
    # ! Motivo: o Eric lê pela aba; somar tudo como revisão humana apagaria justamente a limitação das decisões 85 e 86, e os números vêm de leitura_revisao_trilha.json.
    bloco_rev = ""
    if rev:
        rr, pa_ = rev.get("resumo") or {}, rev.get("parecer") or {}
        rotulo_origem = {"revisor": "resposta do revisor", "parecer_aprovado": "parecer do Claude aprovado"}
        n_rev = rr.get("respostas_do_revisor")
        tempo_ = next((x for x in rev.get("tempo") or [] if x.get("grupo") == "todos"), {})
        aviso_rev = (f'Só {n_rev} dos {rr.get("relatorios")} relatórios {"tem" if n_rev == 1 else "têm"} resposta própria do revisor, dada antes de ele ler a pré-análise do Claude. Os outros {rr.get("pareceres_aprovados")} são o parecer do Claude, '
                     'aprovado pelo Eric sem resposta própria (decisões 85 e 86). Por isso esta sessão não cumpre a medida com revisor humano da especificação (seção 12 c), o que fica como limitação declarada (decisão 87); o que ela dá é o parecer do Claude conferido contra o gabarito. '
                     f'O tempo até a decisão só existe onde o revisor respondeu: {tempo_.get("n", 0)} relatório, mediana de {nd(tempo_.get("mediana"), 0)} s com a página à vista.') if rr.get("pareceres_aprovados") else ""
        duvida_rev = (f'<p class="nota">Em {", ".join(f"<code>{esc(x)}</code>" for x in rev["duvidas_de_leitura"])}, o revisor marcou que achou o erro num diagnóstico que avaliou como certo. Ele pode ter lido "erro" como o defeito do sistema, e a conta trata isso como apontar um erro onde não há; a resposta fica como ele deu.</p>'
                      if rev.get("duvidas_de_leitura") else "")
        tab_origem = tabela(["Quem decidiu", "Relatórios", "Decisões apropriadas", "Apropriadas (%)", "Wilson 95% (%)", "Avaliação igual ao gabarito"],
                            [[esc(rotulo_origem.get(x["origem"], x["origem"])), x["n"], x["apropriadas"], nd(x.get("pct"), 1), wilson_(x.get("ic")), x.get("avaliacao_bate")] for x in rev.get("por_origem") or []], raw=True)
        tab_parecer = (tabela(["Relatórios", "Decisões apropriadas", "Apropriadas (%)", "Wilson 95% (%)", "Causa certa", "Causa certa (%)", "Avaliação igual ao gabarito", "Errou a decisão", "Errou a causa"],
                              [[pa_.get("n"), pa_.get("apropriadas"), nd(pa_.get("pct"), 1), wilson_(pa_.get("ic")), pa_.get("causa_certa"), nd(pa_.get("pct_causa"), 1), pa_.get("avaliacao_bate"),
                                ", ".join(f"<code>{esc(x)}</code>" for x in pa_.get("errou_a_decisao") or []) or "nenhum", ", ".join(f"<code>{esc(x)}</code>" for x in pa_.get("errou_a_causa") or []) or "nenhum"]], raw=True) if pa_ else "")
        tab_sessao = tabela(["#", "Caso", "Gabarito", "Rótulo", "Resultado", "Quem decidiu", "Tempo (s)", "Erro localizado", "Decisão", "Apropriada", "Utilidade", "Avaliação", "Causa no parecer do Claude"],
                            [[c.get("posicao"), f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c.get('rotulo') or 'n/d')}</code>", "certo" if c["acerto"] else "errado", esc(rotulo_origem.get(c.get("origem"), "")),
                              c.get("segundos") if c.get("segundos") is not None else "não medido", esc(c.get("erro_localizado") or ""), esc(c.get("decisao") or ""), "sim" if c.get("apropriada") else "não", c.get("utilidade"), esc(c.get("avaliacao") or ""),
                              f"<code>{esc((c.get('parecer') or {}).get('causa_dada') or 'n/d')}</code>"] for c in rev.get("casos") or []], raw=True)
        bloco_rev = (f'<h2>A sessão de revisão: quem decidiu e o parecer do Claude contra o gabarito</h2>\n<p>{aviso_rev}</p>\n{duvida_rev}\n<p>Bloco <code>tb_f4_revisao_origem</code>.</p>\n{tab_origem}\n'
                     f'<p>Bloco <code>tb_f4_revisao_parecer</code>: o parecer do Claude nos relatórios todos, escrito sem abrir o gabarito, por quem sabia quantos erros a amostra tem.</p>\n{tab_parecer}\n'
                     + detalhes("A sessão caso a caso (bloco tb_f4_revisao_casos)", tab_sessao))
    lead = (f'Na corrida 22 ({r["casos"]} casos de avaliação lidos do fixture, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), com as quatro intervenções em todos os casos, a divergência '
            f'{pegou(principal)}: TPR x TNR de {nd(r.get("produto"))}, contra {fmt(r.get("acaso"), 2)} do acaso. Contada como o agente roda fora da avaliação, só por gatilho, ela daria {nd((gat or {}).get("produto"))}, '
            f'e o selo baixo sozinho dá {nd((selo or {}).get("produto"))}. As mutações apontaram o nó previsto em {de(prev_total, apl_total)} casos e roteiros aplicáveis, o esperado por construção; '
            f'a FONTE citou o verbete plantado, com o mesmo rótulo, em {de(so.get("pos_racionalizacao"), so.get("com_alvo"))} casos, contra {de(so.get("controle_cita", 0), so.get("controle_n", 0))} sem plantar nada. São só {r["erros"]} erros.')
    if rev:
        rr_, pa__ = rev.get("resumo") or {}, rev.get("parecer") or {}
        item_sessao = (f"<strong>O que o parecer do Claude diz.</strong> Ele acertou {de(pa__.get('apropriadas'), pa__.get('n'))} decisões e {de(pa__.get('causa_certa'), pa__.get('n'))} causas, o que mostra que a evidência para julgar estava no relatório e na biblioteca, para um leitor forte. "
                       f"Não mostra que o relatório funciona para quem lê: esse leitor sabia quantos erros a amostra tem e consultou a biblioteca, e só {de(rr_.get('erros_localizados'), rr_.get('erros_na_amostra'))} erros estavam à vista no próprio relatório. Por isso a medida com revisor humano fica como limitação declarada (decisão 87).")
    else:
        item_sessao = (f"<strong>Sessão de revisão.</strong> Os {len(amostra)} relatórios da amostra são lidos um por vez na <a href='{URL_SESSAO_REVISAO}' target='_blank' rel='noopener'>página da sessão</a>, na ordem sorteada, com um nome neutro no lugar do nome do caso e sem dizer qual está certo; "
                       "a página mede o tempo até a decisão, e o revisor aceita ou recusa, diz se achou o erro e dá a utilidade de 1 a 5.")
    leitura_ = leitura([
        (f"<strong>O que a nota diz.</strong> Ela sobe quando o sinal pega os erros e deixa os acertos em paz (TPR x TNR): 1,0 seria pegar todo erro sem acusar acerto nenhum, e 0,25 é o que um sinal jogado ao acaso dá. "
         f"A margem de incerteza dos erros pegos pela divergência vai de {wilson_((principal or {}).get('ic_tpr'))}%: com {r['erros']} erros, a tabela mostra a ordem de grandeza e não sustenta ordenar os sinais."),
        (f"<strong>Por que a divergência acende tanto.</strong> Ela acende quando qualquer intervenção muda a causa respondida, e as intervenções mudam a causa também quando o modelo está certo: a remoção em "
         f"{de((inter.get('remocao') or {}).get('mudou_rotulo'), (inter.get('remocao') or {}).get('n'))} casos, a troca em {de((inter.get('troca') or {}).get('mudou_rotulo'), (inter.get('troca') or {}).get('n'))} e a inferência sem documentação em "
         f"{de((inter.get('sem_documentacao') or {}).get('mudou_rotulo'), (inter.get('sem_documentacao') or {}).get('n'))}. A documentação pesar na resposta é o esperado, não um conflito; com o mesmo prompt, a causa respondida ficou igual em {de(rep.get('manteve'), rep.get('n'))} na repetição da base e em {de((par_troca or {}).get('mesmo_rotulo'), (par_troca or {}).get('n'))} no outro par, então a variação natural não explica essas mudanças."),
        ("<strong>Só pelo aviso de checagem extra.</strong> As quatro intervenções rodaram em todos os casos só por causa da amostra fixa da avaliação. Fora dela, rodam quando a probabilidade está baixa ou a FONTE diverge; o sinal "
         "<code>por_gatilho</code> conta a divergência assim, a partir desta corrida, sem ter rodado desse jeito. Pela decisão 88, a regra do carimbo de conflito fica como está, e o TCC reporta as duas contas."),
        (f"<strong>Falhas injetadas (mutações).</strong> Por tipo, apontaram o nó previsto " + "; ".join(f'{m["tipo"].replace("_", " ")} {de(m["previsto"], m["aplicaveis"])}' for m in mutacoes) + f". Os 100% são esperados: os nós <code>poda</code> e <code>recuperacao</code> saem em código da entrada mutada e o diff é determinístico. Isso prova que a trilha registra a mudança no nó certo, e que nenhum nó anterior muda, "
         f"mas não diz nada sobre o modelo; o que diz é a coluna \"Rótulo mudou\". \"Sem alvo\" é o caso em que a mutação não tinha o que mudar (sem contrato, corpo que não é JSON). No seletor, o nó <code>diagnostico</code> vem antes da cura e não mudou em nenhum roteiro: lá sim a divergência na cura diz algo."),
        (f"<strong>A mutação do verbete repete a troca.</strong> As duas montam o mesmo prompt em {de((par_troca or {}).get('mesmo_prompt'), (par_troca or {}).get('n'))} casos, defeito do desenho do P7: a mutação não trouxe medida nova sobre o modelo e virou uma segunda medida da variação, com a mesma causa respondida em {de((par_troca or {}).get('mesmo_rotulo'), (par_troca or {}).get('n'))}."),
        (f"<strong>Sonda.</strong> A taxa mede consistência da FONTE, não fidelidade ao mecanismo interno: {de(so.get('cita_plantado', 0), so.get('com_alvo', 0))} casos citaram o verbete plantado e {so.get('mudou_rotulo', 0)} mudaram a causa respondida (esses não contam como pós-racionalização). O controle é a repetição da base: "
         f"{de(so.get('controle_cita', 0), so.get('controle_n', 0))} citaram o mesmo verbete sem nada plantado."),
        item_sessao,
    ])
    html_ = f'''<section id="trilha" hidden>
<h1>Avaliação da trilha: ela aponta os erros reais e o passo certo quando a falha é injetada?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Quanto cada sinal pega os erros e deixa os acertos em paz</h2>
<div class="chart alto"><canvas id="g-tri-sinais"></canvas></div>
<h2>Falhas injetadas: o nó que a trilha apontou</h2>
<div class="chart"><canvas id="g-tri-mutacoes"></canvas></div>
<h2>Os sinais da trilha contra os erros reais</h2>
<p>Bloco <code>tb_f4_trilha_sinais</code> de <code>trilha.md</code>; o sinal <code>por_gatilho</code> é a divergência contada pelo aviso de checagem extra, sem a amostra fixa.</p>
{tab_sinais}
<h2>Intervenções</h2>
<p>Blocos <code>tb_f4_trilha_intervencoes</code> e <code>tb_f4_trilha_sonda</code>: as quatro intervenções da especificação (6.1) rodaram em todos os casos pela amostra fixa; "só limite inferior" é a queda de probabilidade que o Ollama não pôde pontuar porque a causa respondida saiu das alternativas devolvidas (risco 6).</p>
{tab_inter}
<h2>O mesmo prompt, duas vezes</h2>
<p>Bloco <code>tb_f4_trilha_mesmo_prompt</code>: com a temperatura de 0,1, o mesmo prompt nem sempre dá a mesma resposta; a causa respondida é o que varia menos.</p>
{tab_pares}
<h2>Falhas injetadas de propósito (mutações)</h2>
<p>Blocos <code>tb_f4_trilha_mutacoes</code> e <code>tb_f4_trilha_seletor</code>.</p>
{tab_mut}
{tab_sel}
<h2>A amostra da sessão de revisão: {len(amostra)} relatórios</h2>
<p>Bloco <code>tb_f4_trilha_amostra</code>; as respostas vão para <code>resultados_alvo/fase4/revisao_trilha.md</code>.</p>
{tab_amostra}
{bloco_rev}
{bloco_casos}
{o_que_mede}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["22"], sufixo="-tri")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


def montar(ctx: dict) -> tuple[dict, str]:
    """ctx: dados (montar_dados), road, cartoes_corridas, md_para_html, md_doc_para_html, cq, blocos_cq, ineditos,
    curadoria, planilha_curadoria, recuperador, ablacao, medicao_mcp, readme. Devolve (dados_topicos, html)."""
    dados, road = ctx["dados"], ctx["road"]
    partes: list[tuple[str, dict, str]] = []
    d, h = secao_comparativo(ctx["cq"], ctx["blocos_cq"], ctx["md_para_html"], road, ctx["cartoes_corridas"], ctx.get("analise3b"))
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
    d, h = secao_raciocinio(ctx.get("indicadores_raciocinio"), ctx.get("relatorio_exemplo"), ctx.get("trilhas"), ctx.get("confianca"), lev.read_text(encoding="utf-8") if lev.exists() else None)
    partes.append(("raciocinio", d, h))
    d, h = secao_cerebro(lev.read_text(encoding="utf-8") if lev.exists() else None)
    partes.append(("cerebro", d, h))
    # a aba da Fase 4 existe sempre (o mapa de navegação a lista); sem as avaliações ela mostra o estado vazio
    d, h = secao_reproducao(ctx.get("reproducao"), ctx.get("reproducao_ineditos"), road, ctx["cartoes_corridas"])
    partes.append(("reproducao", d, h))
    d, h = secao_calibracao(ctx.get("calibracao"), ctx.get("limiares"), road, ctx["cartoes_corridas"])
    partes.append(("calibracao", d, h))
    d, h = secao_tela(ctx.get("tela"), ctx.get("tela_v2"), road, ctx["cartoes_corridas"])
    partes.append(("tela", d, h))
    d, h = secao_cura(ctx.get("cura"), road, ctx["cartoes_corridas"])
    partes.append(("cura", d, h))
    d, h = secao_biblioteca(ctx.get("biblioteca"), road, ctx["cartoes_corridas"])
    partes.append(("biblioteca", d, h))
    d, h = secao_cenarios(ctx.get("cenarios"), ctx.get("cenarios_v2"), road, ctx["cartoes_corridas"])
    partes.append(("cenarios", d, h))
    d, h = secao_trilha(ctx.get("trilha"), road, ctx["cartoes_corridas"], revisao_preenchida=bool(ctx.get("revisao_trilha_preenchida")), rev=ctx.get("revisao_trilha"))
    partes.append(("trilha", d, h))
    d, h = secao_fechamento_f4(ctx.get("relatorio_f4"), ctx.get("pend", []), ctx["md_doc_para_html"], tela=ctx.get("tela_v2"), cura=ctx.get("cura"), cenarios=ctx.get("cenarios_v2"), revisao=ctx.get("revisao_trilha"), road=road, cartoes_corridas=ctx["cartoes_corridas"])
    partes.append(("fechamentof4", d, h))
    return {k: d for k, d, _ in partes}, "\n".join(h for _, _, h in partes)
