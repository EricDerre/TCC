#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (01/10/2026, Pré-Fase 4) com a aba "Atlas" do painel: o mapa dos verbetes da
# biblioteca pelas seis classes de defeito (desenhado em SVG aqui, em Python, e movido por um script simples na
# página), o painel de detalhe de cada verbete, a rota de busca de cada caso, as confusões entre causas e um passeio
# guiado. Lê só resultados_alvo/pre_fase4/atlas.json (gerar_atlas.py, com --check).
# ! Motivo: o Eric pediu (01/10/2026) uma visualização interativa no estilo do "expert atlas" do repositório colibri,
# "uma boa maneira de analisar as competências da IA". Os modelos do projeto são densos, sem especialistas para
# desenhar; o que o atlas mostra aqui é o que o projeto mede: que verbetes a busca entrega para cada classe de defeito
# e o que cada modelo fez com eles. O desenho sai pronto do Python para a aba ser legível sem script (o primeiro quadro
# já traz a biblioteca decidida), e o script só troca de biblioteca, de corrida e de caso. A posição de cada verbete é
# a média das âncoras das classes ponderada pela afinidade medida, e a aba diz isso: não é semelhança de significado.
# Fica num arquivo à parte porque painel_topicos.py já passa de 1.400 linhas.
"""Aba Atlas do painel do projeto. Uso: importado por painel_topicos.py (secao_atlas, CSS_ATLAS, JS_ATLAS)."""
from __future__ import annotations

import html
import math

ESCALA, CX, CY = 320, 450, 412
LARGURA, ALTURA = 900, 950
Y_DOS_DE_FORA = 1.5             # a fila dos verbetes que nunca entraram no contexto, abaixo do hexágono (em raios)
LARGURA_DA_LETRA = 7.5          # largura aproximada de uma letra do nome escrito ao lado do nó (fonte de largura fixa, 12 px)
ROTULO_A_PARTIR_DE = 8          # o nó ganha o nome escrito ao lado quando entra no contexto de pelo menos 8 casos
SIGLA = {"especialista": "esp", "generalista": "gen", "sem_repeticao": "rep", "nunca_recuperado": "nun"}
NOME_DO_ROTULO = {"esp": "especialista", "gen": "generalista", "rep": "sem repetição (um caso só)", "nun": "nunca entrou no contexto"}
NOME_DO_CONJUNTO = {"oficiais": "casos oficiais", "ineditos": "casos inéditos", "cruzada": "casos da troca cruzada"}
# Cor de cada classe: posições fixas da paleta do painel (a sexta pula o verde, que se confundiria com o "certo").
COR_DA_CLASSE = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7}
PASTA_DO_MODELO = "aprendidos"


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def fmt(v, casas: int = 1) -> str:
    return "n/d" if v is None else f"{v:.{casas}f}".replace(".", ",")


def _px(x: float, y: float) -> tuple[float, float]:
    return round(CX + x * ESCALA, 1), round(CY + y * ESCALA, 1)


# ------------------------------------------------------------------ escolha do que vai para a página

def _nome_da_biblioteca(h: str, b: dict, decidida: bool) -> str:
    if b["original"]:
        nome = "Original, escrita à mão (L0)"
    else:
        nome = " / ".join(f"L{v} escrita pelo {m}" for m, v in b["versoes"])
    return f"{nome}, {len(b['verbetes'])} verbetes" + (" (a decidida)" if decidida else "")


def _nome_da_fatia(f: dict) -> str:
    conjunto = NOME_DO_CONJUNTO.get(f["conjunto"], f["conjunto"])
    return f"{f['modelo']}, {f['casos']} {conjunto}"


def escolher(atlas: dict) -> tuple[list[str], list[dict]]:
    """As bibliotecas e as fatias que a aba mostra: a decidida, a original e a última versão do modelo decidido; e, de
    cada uma, uma fatia por (corrida, modelo), para não repetir a mesma leitura (o granite4.2 não aceitou edição
    nenhuma, então L1 a L3 dele são a biblioteca original lida de novo)."""
    meta = atlas["metadados"]
    decidida = next(f for f in atlas["fatias"] if f["id"] == meta["fatia_decidida"])
    do_modelo = [f for f in atlas["fatias"] if f["corrida"] == meta["base"] and f["modelo"] == decidida["modelo"]]
    ultima = max(do_modelo, key=lambda f: f["versao"])
    ordem = list(dict.fromkeys([decidida["biblioteca"], meta["biblioteca_original"], ultima["biblioteca"]]))
    ordem = [h for h in ordem if h in atlas["bibliotecas"]]
    fatias, vistos = [], set()
    ordem_das_corridas = {c: k for k, c in enumerate(meta["corridas"])}
    for f in sorted(atlas["fatias"], key=lambda f: (ordem_das_corridas.get(f["corrida"], 99), f["modelo"] != decidida["modelo"], f["modelo"], f["versao"])):
        chave = (f["corrida"], f["modelo"], f["biblioteca"])
        if f["biblioteca"] in ordem and chave not in vistos:
            vistos.add(chave)
            fatias.append(f)
    return ordem, fatias


def _paradas(atlas: dict, ordem: list[str], decidida: dict) -> list[dict]:
    """As paradas do passeio guiado, com os números lidos do atlas."""
    h = decidida["biblioteca"]
    b = atlas["bibliotecas"][h]
    v = b["verbetes"]
    total = b["casos"]
    nome_classe = {c["n"]: c["nome"] for c in atlas["classes"]}
    paradas = []
    gen = max((i for i in v if v[i]["rotulo"] == "generalista"), key=lambda i: v[i]["itens"], default=None)
    if gen:
        paradas.append({"titulo": "Os generalistas ficam no centro",
                        "texto": f"O verbete {gen} entrou no contexto de {v[gen]['itens']} dos {total} casos, em todas as classes: especialização de "
                                 f"{fmt(v[gen]['especializacao'], 2)} e entropia de {fmt(v[gen]['entropia_bits'], 2)} bits, perto do máximo de "
                                 f"{fmt(atlas['metadados']['metodo']['entropia_maxima_bits'], 2)}. A busca o entrega quase sempre, qualquer que seja o defeito.",
                        "bib": h, "fatia": decidida["id"], "no": gen})
    esp = max((i for i in v if v[i]["rotulo"] == "especialista"), key=lambda i: (v[i]["itens"], v[i]["especializacao"]), default=None)
    if esp:
        k = v[esp]["dominante"]
        do_dominante = max(v[esp]["n"])
        paradas.append({"titulo": "Um especialista fica junto da classe dele",
                        "texto": f"O verbete {esp} entrou em {v[esp]['itens']} casos, {do_dominante} deles da classe {nome_classe.get(k, k)}: especialização de "
                                 f"{fmt(v[esp]['especializacao'], 2)}. Na fatia escolhida o modelo o citou em {decidida['citacoes'].get(esp, {}).get('casos', 0)} casos e "
                                 f"acertou {decidida['citacoes'].get(esp, {}).get('certos', 0)}.",
                        "bib": h, "fatia": decidida["id"], "no": esp})
    do_modelo = [i for i in v if v[i]["pasta"] == PASTA_DO_MODELO]
    if do_modelo:
        fora = [i for i in do_modelo if not v[i]["itens"]]
        paradas.append({"titulo": "O que o modelo escreveu ficou de fora",
                        "texto": f"Dos {len(do_modelo)} verbetes novos que o modelo escreveu nesta biblioteca (os losangos), {len(fora)} nunca entraram no contexto "
                                 f"de nenhum dos {total} casos. O que a busca entrega continua sendo os verbetes originais; o que mudou neles foram as notas que o modelo acrescentou.",
                        "bib": h, "fatia": decidida["id"], "no": sorted(fora or do_modelo)[0]})
    rotas = {c: d["rotas"][decidida["id"]] for c, d in atlas["casos"].items() if decidida["id"] in d["rotas"]}
    bom = next((c for c in sorted(rotas) if rotas[c]["acerto"] and rotas[c]["classe_da_rota"] == atlas["casos"][c]["classe"] and rotas[c]["citados"]), None)
    if bom:
        paradas.append({"titulo": "Uma rota que aponta a classe do caso",
                        "texto": f"No caso {bom}, os três verbetes que a busca entregou apontam a classe {nome_classe[atlas['casos'][bom]['classe']]}, que é a do caso. "
                                 f"O modelo citou {', '.join(rotas[bom]['citados'])} e acertou a causa.",
                        "bib": h, "fatia": decidida["id"], "caso": bom})
    ruim = next((c for c in sorted(rotas) if not rotas[c]["acerto"] and rotas[c]["classe_da_rota"] not in (None, atlas["casos"][c]["classe"])), None)
    if ruim:
        paradas.append({"titulo": "Uma rota que aponta outra classe",
                        "texto": f"No caso {ruim}, da classe {nome_classe[atlas['casos'][ruim]['classe']]}, a busca entregou verbetes que apontam a classe "
                                 f"{nome_classe[rotas[ruim]['classe_da_rota']]}. O modelo respondeu {rotas[ruim]['rotulo']}; a causa do caso é {atlas['casos'][ruim]['gabarito']}.",
                        "bib": h, "fatia": decidida["id"], "caso": ruim})
    if decidida["confusoes"]:
        g, r, n = decidida["confusoes"][0]
        paradas.append({"titulo": "As confusões entre causas",
                        "texto": f"A troca mais frequente desta fatia: a causa {g} respondida como {r or 'resposta sem rótulo'}, em {n} casos. A figura de baixo "
                                 "mostra todas as trocas e o acerto por causa.",
                        "bib": h, "fatia": decidida["id"], "confusoes": True})
    return paradas


def dados_para_a_pagina(atlas: dict) -> dict:
    """O recorte do atlas que o script da página usa, com nomes curtos de campo para a página não crescer à toa."""
    meta = atlas["metadados"]
    ordem, fatias = escolher(atlas)
    decidida = next(f for f in atlas["fatias"] if f["id"] == meta["fatia_decidida"])
    bibs = {}
    for h in ordem:
        b = atlas["bibliotecas"][h]
        verbetes = {}
        for i, v in b["verbetes"].items():
            p = b["posicoes"][i]
            verbetes[i] = {"t": v["titulo"], "pa": v["pasta"], "n": v["n"], "p": v["p"], "e": v["entropia_bits"], "s": v["especializacao"],
                           "d": v["dominante"], "i": v["itens"], "r": SIGLA[v["rotulo"]], "pr": v["vezes_em_primeiro"], "nm": v["notas_do_modelo"],
                           "x": p["x"], "y": Y_DOS_DE_FORA if p["fora"] else p["y"], "raio": p["r"]}
        for i, lugar in _lugares_dos_nomes(verbetes, atlas["classes"]).items():
            verbetes[i]["l"] = lugar
        bibs[h] = {"nome": _nome_da_biblioteca(h, b, h == decidida["biblioteca"]), "casos": b["casos"], "N": b["total_por_classe"], "verbetes": verbetes}
    ids_das_fatias = {f["id"] for f in fatias}
    saida_fatias = []
    for f in fatias:
        rotas = {c: {"rec": d["rotas"][f["id"]]["recuperados"], "cit": d["rotas"][f["id"]]["citados"], "rot": d["rotas"][f["id"]]["rotulo"],
                     "ok": d["rotas"][f["id"]]["acerto"], "cr": d["rotas"][f["id"]]["classe_da_rota"]}
                 for c, d in atlas["casos"].items() if f["id"] in d["rotas"]}
        saida_fatias.append({"id": f["id"], "bib": f["biblioteca"], "nome": _nome_da_fatia(f), "corrida": f["corrida"], "modelo": f["modelo"],
                             "casos": f["casos"], "acertos": f["acertos"],
                             "cit": {i: [x["casos"], x["certos"]] for i, x in f["citacoes"].items()}, "conf": f["confusoes"],
                             "causas": {k: [x["n"], x["acertos"]] for k, x in f["causas"].items()}, "rotas": rotas})
    casos = {c: {"c": d["classe"], "g": d["gabarito"]} for c, d in atlas["casos"].items() if ids_das_fatias & set(d["rotas"])}
    return {"geo": {"cx": CX, "cy": CY, "escala": ESCALA, "rotulo_a_partir_de": ROTULO_A_PARTIR_DE, "pasta_do_modelo": PASTA_DO_MODELO,
                    "entropia_max": fmt(math.log2(len(atlas["classes"])), 2), "conf_x1": X_ESQ + 6, "conf_x2": X_DIR - 6},
            "classes": [{"n": c["n"], "nome": c["nome"], "x": c["ancora"]["x"], "y": c["ancora"]["y"]} for c in atlas["classes"]],
            "causas": _ordem_das_causas(atlas), "bibs": bibs, "ordem_bibs": ordem, "fatias": saida_fatias, "casos": casos,
            "paradas": _paradas(atlas, ordem, decidida), "padrao": {"bib": decidida["biblioteca"], "fatia": decidida["id"]}}


def _ordem_das_causas(atlas: dict) -> list[dict]:
    """As causas na ordem das linhas da figura de confusões: pela classe (a primeira, quando a causa tem casos em duas) e pelo nome."""
    return [{"id": c["id"], "c": c["classes"][0]} for c in sorted(atlas["causas"], key=lambda c: (c["classes"][0], c["id"]))]


# ------------------------------------------------------------------ desenho (primeiro quadro, sem script)

def _caixa_do_nome_da_classe(c: dict) -> tuple[float, float, float, float]:
    """O retângulo ocupado pelo nome da classe e pela contagem de casos, ao lado da âncora."""
    lx, ly, ancora, dy = _lugar_do_nome_da_classe(c)
    largura = max(len(c["nome"]) * 10.5, 62)
    x0 = lx - (0 if ancora == "start" else largura if ancora == "end" else largura / 2)
    return (x0 - 4, ly + dy - 18, x0 + largura + 4, ly + dy + 22)


def _lugar_do_nome_da_classe(c: dict) -> tuple[float, float, str, int]:
    x = c["ancora"]["x"] if "ancora" in c else c["x"]
    y = c["ancora"]["y"] if "ancora" in c else c["y"]
    lx, ly = _px(x * 1.13, y * 1.13)
    ancora = "middle" if abs(x) < 0.2 else ("start" if x > 0 else "end")
    return lx, ly, ancora, (-22 if y < -0.5 else (16 if y > 0.5 else 0))


def _cruza(a: tuple, b: tuple) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def _lugares_dos_nomes(verbetes: dict, classes: list[dict]) -> dict[str, list]:
    """Para os nós que levam o nome escrito ao lado (os que entram em pelo menos ROTULO_A_PARTIR_DE casos): o lado em
    que o nome cabe sem cobrir outro nó, outro nome nem o nome de uma classe. Devolve {id: [alinhamento, dx, dy]}; o nó
    cujo nome não cabe em lado nenhum fica sem nome escrito (ele aparece ao passar o cursor e no painel de detalhe)."""
    ocupadas = []
    centro = {}
    for i, v in verbetes.items():
        x, y = _px(v["x"], v["y"])
        r = v["raio"] * ESCALA
        centro[i] = (x, y, r)
        ocupadas.append((x - r * 0.9, y - r * 0.9, x + r * 0.9, y + r * 0.9, i))
    for c in classes:
        ocupadas.append((*_caixa_do_nome_da_classe(c), "classe"))
    saida = {}
    for i in sorted((i for i, v in verbetes.items() if v["i"] >= ROTULO_A_PARTIR_DE), key=lambda i: (-verbetes[i]["i"], i)):
        x, y, r = centro[i]
        largura = len(i) * LARGURA_DA_LETRA
        d = r * 0.72
        direita, esquerda = ("start", r + 5, 4), ("end", -(r + 5), 4)
        candidatos = ([direita, esquerda] if x >= CX else [esquerda, direita]) + [
            ("middle", 0, -(r + 6)), ("middle", 0, r + 15), ("start", d + 4, -(d + 3)), ("start", d + 4, d + 13), ("end", -(d + 4), -(d + 3)), ("end", -(d + 4), d + 13)]
        for alinhamento, dx, dy in candidatos:
            x0 = x + dx - (0 if alinhamento == "start" else largura if alinhamento == "end" else largura / 2)
            caixa = (x0, y + dy - 11, x0 + largura, y + dy + 4)
            if caixa[0] < 6 or caixa[2] > LARGURA - 6:
                continue
            if not any(_cruza(caixa, o) for o in ocupadas if o[4] != i):
                saida[i] = [alinhamento, round(dx, 1), round(dy, 1)]
                ocupadas.append((*caixa, "nome:" + i))
                break
    return saida


def _marca(pasta: str, r: float) -> str:
    """Círculo para os verbetes originais e losango para os que o modelo escreveu (a forma não muda de uma biblioteca para outra)."""
    if pasta == PASTA_DO_MODELO:
        lado = round(r * 1.5, 1)
        return f'<rect class="at-marca" x="{-lado / 2:.1f}" y="{-lado / 2:.1f}" width="{lado}" height="{lado}" transform="rotate(45)"></rect>'
    return f'<circle class="at-marca" r="{r}"></circle>'


def _no(i: str, v: dict | None, pasta: str) -> str:
    """Um nó do mapa. `v` é o verbete na biblioteca do primeiro quadro (None: o verbete só existe em outra biblioteca)."""
    if v is None:
        return (f'<g class="at-no" data-id="{esc(i)}" tabindex="0" role="button" style="display:none"><title></title>'
                f'<circle class="at-alvo" r="14"></circle>{_marca(pasta, 8)}<text class="at-rot" style="display:none">{esc(i)}</text></g>')
    x, y = _px(v["x"], v["y"])
    r = round(v["raio"] * ESCALA, 1)
    classes = "at-no " + v["r"] + (f" c{v['d']}" if v["d"] else "") + (" apr" if pasta == PASTA_DO_MODELO else "")
    marca = _marca(pasta, r)
    lugar = v.get("l") or ["start" if v["x"] >= 0 else "end", (r + 5) if v["x"] >= 0 else -(r + 5), 4]
    rot = (f'<text class="at-rot" x="{lugar[1]:.1f}" y="{lugar[2]:.1f}" text-anchor="{lugar[0]}"'
           f'{"" if v.get("l") else " style=display:none"}>{esc(i)}</text>')
    descricao = f"{i}: {NOME_DO_ROTULO[v['r']]}, {v['i']} casos"
    return (f'<g class="{classes}" data-id="{esc(i)}" tabindex="0" role="button" aria-label="{esc(descricao)}" style="transform:translate({x}px,{y}px)">'
            f'<title>{esc(descricao)}</title><circle class="at-alvo" r="{r + 9:.1f}"></circle>{marca}{rot}</g>')


def svg_do_mapa(dados: dict) -> str:
    b = dados["bibs"][dados["padrao"]["bib"]]
    todos = sorted({i for x in dados["bibs"].values() for i in x["verbetes"]})
    pontos = " ".join("{},{}".format(*_px(c["x"], c["y"])) for c in dados["classes"])
    partes = [f'<svg class="at-mapa" viewBox="0 0 {LARGURA} {ALTURA}" role="img" aria-label="Mapa dos verbetes da biblioteca pelas seis classes de defeito">',
              f'<polygon class="at-hex" points="{pontos}"></polygon>']
    for c in dados["classes"]:
        x, y = _px(c["x"], c["y"])
        partes.append(f'<line class="at-raio" x1="{CX}" y1="{CY}" x2="{x}" y2="{y}"></line>')
    for k, c in enumerate(dados["classes"]):
        x, y = _px(c["x"], c["y"])
        lx, ly, ancora, dy = _lugar_do_nome_da_classe(c)
        partes.append(f'<g class="at-regiao" data-classe="{c["n"]}"><circle class="at-ancora c{c["n"]}" cx="{x}" cy="{y}" r="6"></circle>'
                      f'<text class="at-classe" x="{lx}" y="{ly + dy:.1f}" text-anchor="{ancora}">{esc(c["nome"])}</text>'
                      f'<text class="at-classe-n" x="{lx}" y="{ly + dy + 16:.1f}" text-anchor="{ancora}">{b["N"][k]} casos</text></g>')
    _, fy = _px(0, Y_DOS_DE_FORA)
    partes.append(f'<text class="at-classe-n at-fora" x="{CX}" y="{fy - 26:.1f}" text-anchor="middle">nunca entraram no contexto de um caso</text>')
    pasta = {i: v["pa"] for x in dados["bibs"].values() for i, v in x["verbetes"].items()}
    partes += [_no(i, b["verbetes"].get(i), pasta[i]) for i in todos]
    partes.append('<g class="at-rota"></g>')      # por cima dos nós: os números de ordem da rota não podem ficar escondidos
    partes.append("</svg>")
    return "".join(partes)


LINHA_CONF, TOPO_CONF, LARGURA_CONF = 23, 48, 900
X_ESQ, X_DIR, X_BARRA = 372, 620, 240


def svg_das_confusoes(dados: dict) -> str:
    """Duas colunas: à esquerda a causa verdadeira de cada caso, com o acerto do modelo nela; à direita o que o modelo
    respondeu. Cada linha entre as colunas é uma troca. O primeiro quadro sai com a fatia padrão."""
    f = next(x for x in dados["fatias"] if x["id"] == dados["padrao"]["fatia"])
    causas = dados["causas"]
    extras = [("__outro__", "rótulo fora das 23 causas"), ("__sem__", "resposta sem rótulo")]
    y_de = {c["id"]: TOPO_CONF + k * LINHA_CONF for k, c in enumerate(causas)}
    y_extra = {e: TOPO_CONF + (len(causas) + k) * LINHA_CONF + 8 for k, (e, _) in enumerate(extras)}
    altura = TOPO_CONF + (len(causas) + len(extras)) * LINHA_CONF + 24
    partes = [f'<svg class="at-conf" viewBox="0 0 {LARGURA_CONF} {altura}" role="img" aria-label="Acerto por causa e trocas entre causas">',
              f'<text class="cab" x="{X_ESQ}" y="22" text-anchor="end">causa do caso · acerto do modelo</text>',
              f'<text class="cab" x="{X_DIR + 10}" y="22">o que o modelo respondeu no lugar</text>']
    for c in causas:
        y = y_de[c["id"]]
        n, ok = f["causas"].get(c["id"], [0, 0])
        largura = round(60 * ok / n, 1) if n else 0
        partes.append(f'<g class="at-causa" data-causa="{esc(c["id"])}" data-y="{y}">'
                      f'<circle class="pt c{c["c"]}" cx="{X_ESQ}" cy="{y}" r="5"></circle>'
                      f'<text x="{X_BARRA - 8}" y="{y + 4}" text-anchor="end">{esc(c["id"])}</text>'
                      f'<rect class="trilho" x="{X_BARRA}" y="{y - 4}" width="60" height="8" rx="4"></rect>'
                      f'<rect class="acerto" x="{X_BARRA}" y="{y - 4}" width="{largura}" height="8" rx="4"></rect>'
                      f'<text class="ac" x="{X_BARRA + 66}" y="{y + 4}">{f"{ok} de {n}" if n else "sem casos"}</text></g>'
                      f'<g class="at-resp" data-resp="{esc(c["id"])}" data-y="{y}"><circle class="pt c{c["c"]}" cx="{X_DIR}" cy="{y}" r="5"></circle>'
                      f'<text x="{X_DIR + 10}" y="{y + 4}">{esc(c["id"])}</text></g>')
    for e, nome in extras:
        y = y_extra[e]
        partes.append(f'<g class="at-resp" data-resp="{e}" data-y="{y}"><circle class="pt fora" cx="{X_DIR}" cy="{y}" r="5"></circle>'
                      f'<text x="{X_DIR + 10}" y="{y + 4}">{esc(nome)}</text></g>')
    partes.append('<g class="at-arestas">' + "".join(_aresta(g, r, n, y_de, y_extra) for g, r, n in f["conf"]) + "</g>")
    partes.append("</svg>")
    return "".join(partes)


def _aresta(gabarito: str, resposta: str | None, n: int, y_de: dict, y_extra: dict) -> str:
    y1 = y_de.get(gabarito)
    if y1 is None:
        return ""
    y2 = y_de.get(resposta) if resposta in y_de else y_extra["__sem__" if resposta is None else "__outro__"]
    meio = (X_ESQ + X_DIR) / 2
    texto = f"{gabarito} respondida como {resposta or 'resposta sem rótulo'}: {n} caso{'s' if n != 1 else ''}"
    return (f'<path class="at-aresta" d="M{X_ESQ + 6} {y1} C{meio} {y1}, {meio} {y2}, {X_DIR - 6} {y2}" stroke-width="{1.5 + 2 * (n - 1):.1f}">'
            f'<title>{esc(texto)}</title></path>')


# ------------------------------------------------------------------ a seção

def _tabela(cab: list[str], linhas: list[list], classe: str = "") -> str:
    th = "".join(f"<th>{esc(c)}</th>" for c in cab)
    trs = "".join("<tr>" + "".join(f'<td{" class=num" if isinstance(c, (int, float)) else ""}>{c if isinstance(c, str) and c.startswith("<") else esc(c)}</td>' for c in r) + "</tr>"
                  for r in linhas)
    return f'<div class="tabela {classe}"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def secao_atlas(atlas: dict | None, kpis, leitura, fontes, detalhes, validacao_gemini: str = "") -> tuple[dict, str]:
    """Devolve os dados que o script da página usa e o HTML da seção. `kpis`, `leitura`, `fontes` e `detalhes` são os
    ajudantes de painel_topicos (passados para este módulo não importar o outro de volta)."""
    titulo = "Que verbetes a busca entrega para cada tipo de defeito, e o que o modelo faz com eles?"
    if not atlas:
        return {}, (f'<section id="atlas" hidden>\n<h1>{titulo}</h1>\n<p class="lead">O atlas ainda não foi gerado nesta máquina: falta '
                    '<code>resultados_alvo/pre_fase4/atlas.json</code> (<code>RESULTADOS_DIR=resultados_alvo python gerar_atlas.py</code>).</p>\n</section>')
    dados = dados_para_a_pagina(atlas)
    meta = atlas["metadados"]
    f = next(x for x in atlas["fatias"] if x["id"] == meta["fatia_decidida"])
    h = f["biblioteca"]
    b = atlas["bibliotecas"][h]
    v = b["verbetes"]
    cont = b["contagem_por_rotulo"]
    nome_classe = {c["n"]: c["nome"] for c in atlas["classes"]}
    loo, ined = b["validacao"]["deixando_um_de_fora"], b["validacao"]["ineditos"]
    ra, rr = f["rota_e_acerto"], f["resposta_e_rota"]
    do_modelo = [i for i in v if v[i]["pasta"] == PASTA_DO_MODELO]
    do_modelo_fora = [i for i in do_modelo if not v[i]["itens"]]
    generalistas = sorted((i for i in v if v[i]["rotulo"] == "generalista"), key=lambda i: -v[i]["itens"])
    nome_bib = dados["bibs"][h]["nome"]
    # em quantas fatias a biblioteca tinha verbete escrito pelo modelo, e em quantos casos algum deles entrou na rota
    com_novos, casos_com_novo = 0, 0
    for x in atlas["fatias"]:
        bx = atlas["bibliotecas"].get(x["biblioteca"])
        novos = {i for i, vv in (bx or {"verbetes": {}})["verbetes"].items() if vv["pasta"] == PASTA_DO_MODELO}
        if novos:
            com_novos += 1
            casos_com_novo += sum(1 for d in atlas["casos"].values() if x["id"] in d["rotas"] and novos & set(d["rotas"][x["id"]]["recuperados"]))
    pior = min(loo["por_classe"], key=lambda k: k["acertos"] / k["n"])
    citado_mal = min((i for i, x in f["citacoes"].items() if x["casos"] >= 5), key=lambda i: f["citacoes"][i]["certos"] / f["citacoes"][i]["casos"], default=None)
    # citações da fatia decidida somadas pelo rótulo do verbete citado: [citações, com a causa certa]
    por_rotulo = {"especialista": [0, 0], "generalista": [0, 0]}
    for i, x in f["citacoes"].items():
        if v.get(i, {}).get("rotulo") in por_rotulo:
            por_rotulo[v[i]["rotulo"]][0] += x["casos"]
            por_rotulo[v[i]["rotulo"]][1] += x["certos"]
    pct = lambda par: fmt(100 * par[1] / par[0]) if par[0] else "n/d"  # noqa: E731

    itens_kpi = [
        ("Especialistas de uma classe", f'{cont.get("especialista", 0)} de {len(v)}',
         f'especialização a partir de {fmt(meta["metodo"]["limiar_especialista"])} em pelo menos {meta["metodo"]["minimo_de_casos"]} casos distintos'),
        ("Generalistas", str(cont.get("generalista", 0)),
         (f"entram em casos de várias classes; o maior, {generalistas[0]}, em {v[generalistas[0]]['itens']} dos {b['casos']} casos" if generalistas else "nenhum")),
        ("Nunca entraram no contexto", str(cont.get("nunca_recuperado", 0)), f"{len(do_modelo_fora)} deles escritos pelo modelo"),
        ("A rota aponta a classe do caso", f'{fmt(loo["acerto_pct"])}%',
         f'{loo["acertos"]} de {loo["total"]}, deixando o caso de fora; o acaso daria {fmt(loo["acaso_pct"])}%'
         + (f'; nos inéditos, {ined["acertos"]} de {ined["total"]}' if ined else "")),
        ("Acerto do modelo conforme a rota", f'{fmt(ra["aponta"]["acerto_pct"])}% / {fmt(ra["nao_aponta"]["acerto_pct"])}%',
         f'quando a rota aponta a classe do caso ({ra["aponta"]["n"]} casos) e quando não aponta ({ra["nao_aponta"]["n"]})'),
    ]
    leitura_itens = [
        "<strong>O que o desenho mede.</strong> Cada círculo é um verbete da biblioteca. O tamanho é o número de casos em cujo contexto a busca o pôs. A posição é a média das "
        "âncoras das seis classes, ponderada pela afinidade medida: quem só aparece em casos de uma classe fica na ponta dela, quem aparece em todas fica no centro. "
        "Não é semelhança de significado, e um verbete repartido entre duas classes opostas também cai no meio; as barras do detalhe desfazem a dúvida.",
        (f"<strong>Os verbetes que o modelo escreveu não são entregues pela busca.</strong> Em {com_novos} corridas a biblioteca tinha verbetes novos escritos pelo modelo, "
         + ("e em nenhuma delas um verbete novo entrou no contexto de um caso. O ganho medido com a biblioteca do modelo vem das notas que ele acrescentou aos verbetes que já existiam."
            if not casos_com_novo else f"e algum deles entrou no contexto em {casos_com_novo} casos, somadas as corridas.")
         if com_novos else ""),
        (f"<strong>A rota já diz muito antes de o modelo responder.</strong> Só pelos três verbetes entregues, o atlas acerta a classe do caso em {fmt(loo['acerto_pct'])}% das vezes. "
         f"Quando acerta, o {f['modelo']} acerta a causa em {fmt(ra['aponta']['acerto_pct'])}% dos casos; quando não, em {fmt(ra['nao_aponta']['acerto_pct'])}%. "
         f"A classe em que a rota menos ajuda é a {nome_classe[pior['classe']]}: aponta a classe em {pior['acertos']} de {pior['n']} casos."),
        (f"<strong>Um sinal que não precisa do gabarito.</strong> Quando a causa que o modelo responde é de uma classe que a rota aponta, ele acerta "
         f"{fmt(rr['coerente']['acerto_pct'])}% ({rr['coerente']['acertos']} de {rr['coerente']['n']}); quando responde uma causa de outra classe, "
         f"{fmt(rr['incoerente']['acerto_pct'])}% ({rr['incoerente']['acertos']} de {rr['incoerente']['n']}). O agente pode calcular isso sozinho e pedir revisão humana no segundo caso. "
         "Nos outros modelos e corridas a diferença varia; a tabela por corrida, abaixo, mostra todas." if rr else ""),
        (f"<strong>O que o modelo cita também diz algo.</strong> Nas {por_rotulo['especialista'][0]} citações de verbetes especialistas, a causa respondida estava certa em "
         f"{pct(por_rotulo['especialista'])}% ({por_rotulo['especialista'][1]}); nas {por_rotulo['generalista'][0]} de generalistas, em {pct(por_rotulo['generalista'])}% "
         f"({por_rotulo['generalista'][1]})."
         + (f" O caso extremo é {citado_mal}: citado em {f['citacoes'][citado_mal]['casos']} casos, com a causa certa em {f['citacoes'][citado_mal]['certos']}." if citado_mal else "")),
        "<strong>Ressalvas.</strong> " + " ".join(esc(r) for r in meta["ressalvas"]),
    ]
    tab_verbetes = _tabela(["Verbete", "Pasta", "Casos no contexto", "Vezes em primeiro", "Classe dominante", "Especialização", "Entropia (bits)", "Rótulo", "Citado pelo modelo (casos / certos)"],
                           [[f"<code>{esc(i)}</code>", x["pasta"], x["itens"], x["vezes_em_primeiro"],
                             "nenhuma" if x["dominante"] is None else nome_classe[x["dominante"]], fmt(x["especializacao"], 2), fmt(x["entropia_bits"], 2),
                             NOME_DO_ROTULO[SIGLA[x["rotulo"]]],
                             (f'{f["citacoes"][i]["casos"]} / {f["citacoes"][i]["certos"]}' if i in f["citacoes"] else "0 / 0")]
                            for i, x in sorted(v.items(), key=lambda kv: (-kv[1]["itens"], kv[0]))])
    tab_validacao = _tabela(["Biblioteca", "Casos", "A rota aponta a classe (um de fora)", "Empates", "Inéditos", "Acaso"],
                            [[_nome_da_biblioteca(k, x, k == h), x["casos"],
                              f'{fmt(x["validacao"]["deixando_um_de_fora"]["acerto_pct"])}% ({x["validacao"]["deixando_um_de_fora"]["acertos"]})',
                              x["validacao"]["deixando_um_de_fora"]["empates"],
                              (f'{fmt(x["validacao"]["ineditos"]["acerto_pct"])}% ({x["validacao"]["ineditos"]["acertos"]} de {x["validacao"]["ineditos"]["total"]})'
                               if x["validacao"]["ineditos"] else "n/d"),
                              f'{fmt(x["validacao"]["deixando_um_de_fora"]["acaso_pct"])}%'] for k, x in atlas["bibliotecas"].items()])

    def par(x: dict | None, lado: str) -> str:
        return f'{fmt(x[lado]["acerto_pct"])}% ({x[lado]["acertos"]} de {x[lado]["n"]})' if x and x[lado]["n"] else "n/d"

    tab_fatias = _tabela(["Corrida, modelo e versão", "Casos", "Acerto", "Rota aponta a classe", "Rota não aponta", "Resposta na classe da rota", "Resposta fora da classe da rota"],
                         [[f'<code>{esc(x["id"])}</code>', x["casos"], f'{fmt(x["acerto_pct"])}%', par(x["rota_e_acerto"], "aponta"), par(x["rota_e_acerto"], "nao_aponta"),
                           par(x["resposta_e_rota"], "coerente"), par(x["resposta_e_rota"], "incoerente")] for x in atlas["fatias"]])
    legenda = ('<ul class="at-legenda" aria-label="Legenda do mapa">'
               + "".join(f'<li><i class="at-cor c{c["n"]}"></i>{esc(c["nome"])}</li>' for c in atlas["classes"])
               + '<li><i class="at-cor gen"></i>generalista</li><li><i class="at-cor rep"></i>um caso só</li><li><i class="at-cor nun"></i>nunca entrou</li>'
                 '<li><i class="at-cor apr"></i>escrito pelo modelo</li></ul>')
    opcoes_bib = "".join(f'<option value="{esc(k)}"{" selected" if k == h else ""}>{esc(dados["bibs"][k]["nome"])}</option>' for k in dados["ordem_bibs"])
    opcoes_fatia = "".join(f'<option value="{esc(x["id"])}"{" selected" if x["id"] == f["id"] else ""}>{esc(x["nome"])}</option>' for x in dados["fatias"] if x["bib"] == h)
    botoes_classe = ('<button type="button" data-classe="0" aria-pressed="true">Todas as classes</button>'
                     + "".join(f'<button type="button" data-classe="{c["n"]}" aria-pressed="false">{esc(c["nome"])}</button>' for c in atlas["classes"]))
    parada0 = dados["paradas"][0] if dados["paradas"] else None
    passeio = (f'<div class="at-passeio" aria-live="polite"><div><span class="at-passo">Passeio guiado · {len(dados["paradas"])} paradas</span>'
               f'<strong class="at-parada-titulo">{esc(parada0["titulo"]) if parada0 else ""}</strong><p class="at-parada-texto">{esc(parada0["texto"]) if parada0 else ""}</p></div>'
               '<div class="at-passeio-botoes"><button type="button" class="at-anterior">Anterior</button><button type="button" class="at-proxima">Próxima</button></div></div>') if parada0 else ""
    html_ = f'''<section id="atlas" hidden>
<h1>{titulo}</h1>
<p class="lead">Dá para ver. Com o método do expert atlas do colibri aplicado à nossa busca, a biblioteca decidida ({esc(nome_bib.split(",")[0])}) tem {cont.get("especialista", 0)} verbetes especialistas de uma classe de defeito, {cont.get("generalista", 0)} generalistas e {cont.get("nunca_recuperado", 0)} que nunca entraram no contexto de caso nenhum{f", entre eles os {len(do_modelo_fora)} que o próprio modelo escreveu" if do_modelo_fora else ""}. Só pelos verbetes que a busca entrega, o atlas acerta a classe do caso em {loo["acertos"]} de {loo["total"]} casos ({fmt(loo["acerto_pct"])}%; o acaso daria {fmt(loo["acaso_pct"])}%). Quando a rota aponta a classe certa, o <code>{esc(f["modelo"])}</code> acerta {fmt(ra["aponta"]["acerto_pct"])}% dos diagnósticos; quando não aponta, {fmt(ra["nao_aponta"]["acerto_pct"])}%.</p>
{kpis(itens_kpi)}
{validacao_gemini}
<h2>O mapa</h2>
<p>Os modelos do projeto são densos: não têm os especialistas internos que o atlas do colibri desenha. O que se transfere é o método de medição, aplicado ao que o projeto observa: para cada caso, a busca escolhe três verbetes da biblioteca (a rota do caso). Escolha a biblioteca, quem a leu e, se quiser, um caso; clique num verbete para ver o detalhe.</p>
{passeio}
<div class="at-controles">
<label>Biblioteca <select class="at-sel-bib">{opcoes_bib}</select></label>
<label>Quem leu <select class="at-sel-fatia">{opcoes_fatia}</select></label>
<label>Caso <select class="at-sel-caso"><option value="">nenhum</option></select></label>
</div>
<div class="filtros at-classes" role="group" aria-label="Realçar uma classe">{botoes_classe}</div>
<div class="at-grade">
<figure class="at-fig">{svg_do_mapa(dados)}{legenda}</figure>
<aside class="at-detalhe" aria-live="polite"><h3>Detalhe</h3><p class="nota">Clique num verbete do mapa para ver em quantos casos de cada classe ele entrou, a especialização, a entropia e quantas vezes o modelo o citou. Escolha um caso para ver a rota dele.</p></aside>
</div>
<h2>Acerto por causa e trocas entre causas</h2>
<p>À esquerda, as 23 causas na ordem das classes, com a parcela dos casos de cada uma que o modelo acertou. À direita, o que ele respondeu quando errou: cada linha é uma troca, mais grossa quanto mais casos. Passe o cursor numa linha para ver quantos. A figura acompanha a escolha de "Quem leu".</p>
<figure class="at-fig at-rolagem">{svg_das_confusoes(dados)}</figure>
<h2>Leitura</h2>
{leitura([x for x in leitura_itens if x])}
<h2>O segundo atlas: um modelo com especialistas de verdade</h2>
<p>A corrida 13 do roteiro grava, com o motor do colibri, o roteamento do OLMoE (um modelo MoE pequeno, o único que cabe nesta máquina) lendo os nossos 126 casos. Com esse arquivo a aba ganha o atlas no sentido original: especialistas por camada e por classe de defeito. Ele descreve outro modelo, não o do agente. A corrida ainda não foi feita.</p>
{detalhes("Todos os verbetes da biblioteca decidida, em tabela", tab_verbetes)}
{detalhes("Validação do atlas por biblioteca", tab_validacao)}
{detalhes("A rota e o acerto do modelo, por corrida", tab_fatias)}
{fontes(["<code>resultados_alvo/pre_fase4/atlas.json</code> e <code>atlas.md</code> (<code>gerar_atlas.py</code>, com <code>--check</code>)", "registros de diagnóstico de " + ", ".join(f"<code>{esc(c)}</code>" for c in meta["corridas"]), "método: <code>c/tools/expert_atlas</code> do repositório colibri (levantamento §6.14.5)", "decisão 70; roadmap §3.1"])}
</section>'''
    return dados, html_


CSS_ATLAS = r"""
.at-controles{display:flex;flex-wrap:wrap;gap:10px 18px;margin:12px 0;font-size:13px;color:var(--ink2)}.at-controles select{max-width:100%;margin-left:4px}
.at-grade{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(260px,1fr);gap:16px;align-items:start}
.at-fig{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:8px;margin:0}
.at-fig.at-rolagem{overflow-x:auto;margin:10px 0}.at-fig.at-rolagem svg{min-width:720px}
svg.at-mapa,svg.at-conf{display:block;width:100%;height:auto}
.at-hex{fill:none;stroke:var(--linha);stroke-width:1.5}.at-raio{stroke:var(--linha);stroke-width:1;stroke-dasharray:3 5}
.at-ancora{fill:var(--bg2);stroke-width:3}.at-classe{font:600 17px var(--fb);fill:var(--ink)}.at-classe-n{font:13px var(--fb);fill:var(--ink2)}
.at-regiao{transition:opacity .3s}.at-regiao.apagado{opacity:.35}
.at-no{cursor:pointer;transition:transform .45s ease,opacity .3s}.at-no:focus{outline:none}.at-no .at-alvo{fill:transparent}
.at-no .at-marca{stroke:var(--bg2);stroke-width:2;fill:var(--ink2);fill-opacity:.4}
.at-no.rep .at-marca{fill:var(--bg2);fill-opacity:1;stroke:var(--ink2);stroke-dasharray:4 3}
.at-no.nun .at-marca{fill:var(--bg2);fill-opacity:1;stroke:var(--ink2);stroke-width:1.5;stroke-dasharray:2 3}
.at-no:hover .at-marca,.at-no:focus-visible .at-marca,.at-no.sel .at-marca{stroke:var(--ink);stroke-width:3;stroke-dasharray:none}
.at-no.apagado{opacity:.15}.at-no.na-rota .at-marca{stroke:var(--ink);stroke-width:2.5;stroke-dasharray:none}
.at-rot{font:12px var(--fm);fill:var(--ink);paint-order:stroke;stroke:var(--bg2);stroke-width:3px;pointer-events:none}
.at-rota{pointer-events:none}.at-linha{stroke:var(--ink2);stroke-width:1.5;stroke-dasharray:5 4;fill:none}.at-linha.citado{stroke:var(--ink);stroke-width:2.5;stroke-dasharray:none}
.at-caso{stroke:var(--bg2);stroke-width:2}.at-caso.ok{fill:var(--bom)}.at-caso.erro{fill:var(--ruim)}
.at-caso-rot{font:600 12px var(--fm);fill:var(--ink);paint-order:stroke;stroke:var(--bg2);stroke-width:3px}.at-ordem{font:600 11px var(--fm);fill:var(--bg2)}.at-ordem-fundo{fill:var(--ink)}
.at-legenda{display:flex;flex-wrap:wrap;gap:6px 14px;list-style:none;padding:6px 8px 2px;margin:0;font-size:12px;color:var(--ink2)}
.at-legenda li{display:flex;align-items:center;gap:6px}.at-cor{display:inline-block;width:12px;height:12px;border-radius:50%;background:var(--ink2)}
.at-cor.gen{opacity:.4}.at-cor.rep{background:none;border:2px dashed var(--ink2)}.at-cor.nun{background:none;border:1.5px dotted var(--ink2)}
.at-cor.apr{border-radius:0;transform:rotate(45deg) scale(.82);opacity:.4}
.at-detalhe{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px;min-width:0}
.at-detalhe h3{margin:0 0 4px;font:600 15px var(--fm);overflow-wrap:anywhere}.at-detalhe h4{margin:14px 0 6px}
.at-detalhe dl{display:grid;grid-template-columns:auto 1fr;gap:3px 12px;margin:8px 0;font-size:13px}.at-detalhe dt{color:var(--ink2)}.at-detalhe dd{margin:0;font-family:var(--fm);font-variant-numeric:tabular-nums}
.at-barras{display:grid;gap:5px;font-size:13px}.at-barra{display:grid;grid-template-columns:76px minmax(40px,1fr) 52px;gap:8px;align-items:center}
.at-barra i{display:block;height:10px;border-radius:5px;background:color-mix(in srgb,var(--ink2) 15%,transparent);position:relative;overflow:hidden}
.at-barra i::after{content:"";position:absolute;inset:0 auto 0 0;width:var(--w,0%);border-radius:5px;background:var(--cor,var(--ink2))}
.at-barra b{font:500 12px var(--fm);text-align:right;font-variant-numeric:tabular-nums}
.at-rota-lista{padding-left:20px;margin:6px 0;font-size:13px}.at-rota-lista li{margin:4px 0}.at-rota-lista code{overflow-wrap:anywhere}
.at-passeio{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;background:var(--acento2);border-radius:10px;padding:12px 16px;margin:12px 0}
.at-passeio > div:first-child{flex:1 1 320px;min-width:0}.at-passo{display:block;font:600 11px var(--fb);text-transform:uppercase;letter-spacing:.05em;color:var(--ink2)}
.at-parada-titulo{display:block;font:600 16px var(--fd);margin:2px 0}.at-parada-texto{margin:0;font-size:13px;max-width:none}
.at-passeio-botoes{display:flex;gap:8px}.at-passeio-botoes button{border:1px solid var(--linha);background:var(--bg2);color:var(--ink);font:500 13px var(--fb);padding:6px 12px;border-radius:6px;cursor:pointer}
.at-passeio-botoes button:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
.at-conf text{font:12px var(--fm);fill:var(--ink)}.at-conf .cab{font:600 11px var(--fb);fill:var(--ink2);text-transform:uppercase;letter-spacing:.04em}
.at-conf .ac{font:11px var(--fm);fill:var(--ink2)}.at-conf .trilho{fill:color-mix(in srgb,var(--ink2) 15%,transparent)}.at-conf .acerto{fill:var(--bom)}
.at-conf .pt{stroke:var(--bg2);stroke-width:2;fill:var(--ink2)}.at-aresta{fill:none;stroke:var(--ruim);stroke-opacity:.5}.at-aresta:hover{stroke-opacity:1}
.at-causa.sem-casos text{fill:var(--ink2)}
@media (max-width:900px){.at-grade{grid-template-columns:minmax(0,1fr)}}
""" + "".join(
    f".at-ancora.c{c}{{stroke:var(--s{s})}}.at-no.esp.c{c} .at-marca{{fill:var(--s{s});fill-opacity:.92}}.at-no.rep.c{c} .at-marca{{stroke:var(--s{s})}}"
    f".at-cor.c{c}{{background:var(--s{s})}}.at-barra.c{c}{{--cor:var(--s{s})}}.at-conf .pt.c{c}{{fill:var(--s{s})}}\n" for c, s in COR_DA_CLASSE.items())

JS_ATLAS = r"""
function atlasIniciar(){
  const A = T.atlas, raiz = document.getElementById('atlas');
  if(!A || !A.bibs || !raiz || raiz.dataset.pronto) return; raiz.dataset.pronto = '1';   // o painel chama de novo quando o tema muda
  const NS = 'http://www.w3.org/2000/svg';
  const svg = raiz.querySelector('svg.at-mapa'), camada = svg.querySelector('.at-rota'), conf = raiz.querySelector('svg.at-conf');
  const nos = {}; svg.querySelectorAll('.at-no').forEach(g => { nos[g.dataset.id] = g; });
  const selBib = raiz.querySelector('.at-sel-bib'), selFat = raiz.querySelector('.at-sel-fatia'), selCaso = raiz.querySelector('.at-sel-caso');
  const painel = raiz.querySelector('.at-detalhe'), G = A.geo;
  const est = {bib: A.padrao.bib, fatia: A.padrao.fatia, no: null, caso: '', classe: 0, parada: 0};
  const br = (v, c) => v == null ? 'n/d' : Number(v).toLocaleString('pt-BR', {minimumFractionDigits: c == null ? 1 : c, maximumFractionDigits: c == null ? 1 : c});
  const px = (x, y) => [G.cx + x * G.escala, G.cy + y * G.escala];
  const fatia = () => A.fatias.find(f => f.id === est.fatia);
  const verbete = id => A.bibs[est.bib].verbetes[id];
  const nomeClasse = n => (A.classes.find(c => c.n === n) || {nome: 'nenhuma'}).nome;
  const rotulos = {esp: 'especialista', gen: 'generalista', rep: 'um caso só: sem repetição', nun: 'nunca entrou no contexto'};
  const el = (tag, attrs, texto) => { const e = document.createElement(tag); Object.entries(attrs || {}).forEach(([k, v]) => e.setAttribute(k, v)); if(texto != null) e.textContent = texto; return e; };
  const sv = (tag, attrs, texto) => { const e = document.createElementNS(NS, tag); Object.entries(attrs || {}).forEach(([k, v]) => e.setAttribute(k, v)); if(texto != null) e.textContent = texto; return e; };

  function pintar(){
    const rota = est.caso ? (fatia().rotas[est.caso] || {rec: []}).rec : [];
    Object.entries(nos).forEach(([id, g]) => { const v = verbete(id);
      if(!v){ g.style.display = 'none'; return; } g.style.display = '';
      const [x, y] = px(v.x, v.y), r = v.raio * G.escala;
      g.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px)`;
      const apagado = est.classe && v.d !== est.classe;
      g.setAttribute('class', 'at-no ' + v.r + (v.d ? ' c' + v.d : '') + (v.pa === G.pasta_do_modelo ? ' apr' : '') + (est.no === id ? ' sel' : '') + (apagado ? ' apagado' : '') + (rota.includes(id) ? ' na-rota' : ''));
      const m = g.querySelector('.at-marca');
      if(m.tagName === 'circle') m.setAttribute('r', r.toFixed(1));
      else { const l = r * 1.5; m.setAttribute('width', l.toFixed(1)); m.setAttribute('height', l.toFixed(1)); m.setAttribute('x', (-l / 2).toFixed(1)); m.setAttribute('y', (-l / 2).toFixed(1)); }
      g.querySelector('.at-alvo').setAttribute('r', (r + 9).toFixed(1));
      const t = g.querySelector('.at-rot'), dir = v.x >= 0, L = v.l || [dir ? 'start' : 'end', (dir ? 1 : -1) * (r + 5), 4];
      t.style.display = (v.l || est.no === id || rota.includes(id)) ? '' : 'none';
      t.setAttribute('x', Number(L[1]).toFixed(1)); t.setAttribute('y', Number(L[2]).toFixed(1)); t.setAttribute('text-anchor', L[0]);
      const desc = `${id}: ${rotulos[v.r]}, ${v.i} casos`;
      g.setAttribute('aria-label', desc); const tt = g.querySelector('title'); if(tt) tt.textContent = desc;
    });
    svg.querySelectorAll('.at-regiao').forEach(g => g.classList.toggle('apagado', !!est.classe && Number(g.dataset.classe) !== est.classe));
    svg.querySelectorAll('.at-regiao').forEach((g, k) => { const n = g.querySelector('.at-classe-n'); if(n) n.textContent = A.bibs[est.bib].N[k] + ' casos'; });
    raiz.querySelectorAll('.at-classes button').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.classe) === est.classe)));
  }

  function barras(v, N){
    const caixa = el('div', {class: 'at-barras'});
    A.classes.forEach((c, k) => { const linha = el('div', {class: 'at-barra c' + c.n});
      linha.append(el('span', {}, c.nome)); const i = el('i'); i.style.setProperty('--w', ((v.p ? v.p[k] : 0) * 100).toFixed(1) + '%'); linha.append(i);
      linha.append(el('b', {title: v.n[k] + ' de ' + N[k] + ' casos da classe'}, v.p ? br(v.p[k] * 100) + '%' : 'n/d')); caixa.append(linha); });
    return caixa;
  }

  function detalharNo(id){
    const v = verbete(id); painel.replaceChildren(); if(!v){ painel.append(el('h3', {}, 'Detalhe'), el('p', {class: 'nota'}, 'Este verbete não existe na biblioteca escolhida.')); return; }
    const B = A.bibs[est.bib], f = fatia(), cit = f.cit[id] || [0, 0];
    painel.append(el('h3', {}, id), el('p', {class: 'nota'}, v.t + ' · pasta ' + v.pa + (v.pa === G.pasta_do_modelo ? ' (escrito pelo modelo)' : '')));
    const dl = el('dl');
    [['Rótulo', rotulos[v.r] + (v.d && v.r === 'esp' ? ' da classe ' + nomeClasse(v.d) : '')],
     ['Casos em que entrou no contexto', v.i + ' de ' + B.casos], ['Vezes em primeiro lugar na busca', String(v.pr)],
     ['Especialização (0 a 1)', br(v.s, 2)], ['Entropia', v.e == null ? 'n/d' : br(v.e, 2) + ' de ' + G.entropia_max + ' bits'],
     ['Notas escritas pelo modelo', String(v.nm)],
     ['Citado como fonte por ' + f.nome.split(',')[0], cit[0] + ' casos, ' + cit[1] + ' com a causa certa']
    ].forEach(([k, val]) => { dl.append(el('dt', {}, k), el('dd', {}, val)); });
    painel.append(dl, el('h4', {}, 'Afinidade por classe'));
    painel.append(v.p ? barras(v, B.N) : el('p', {class: 'nota'}, 'Sem afinidade para medir: o verbete não entrou no contexto de nenhum caso.'));
    if(v.p) painel.append(el('p', {class: 'nota'}, 'A afinidade é a taxa de casos de cada classe em que o verbete entrou, levada a somar 100%. Passe o cursor no percentual para ver a contagem.'));
  }

  function detalharCaso(caso){
    const f = fatia(), r = f.rotas[caso], c = A.casos[caso]; painel.replaceChildren(); if(!r) return;
    painel.append(el('h3', {}, 'Caso ' + caso), el('p', {class: 'nota'}, 'classe ' + nomeClasse(c.c) + ' · lido por ' + f.nome));
    painel.append(el('h4', {}, 'O que a busca entregou'));
    const ol = el('ol', {class: 'at-rota-lista'});
    r.rec.forEach(id => { const v = verbete(id), li = el('li'); li.append(el('code', {}, id));
      li.append(document.createTextNode(v ? ' · ' + rotulos[v.r] + (v.d && v.r === 'esp' ? ' da classe ' + nomeClasse(v.d) : '') : ''));
      if(r.cit.includes(id)) li.append(el('strong', {}, ' · citado pelo modelo')); ol.append(li); });
    painel.append(ol);
    const fora = r.cit.filter(id => !r.rec.includes(id));
    if(fora.length) painel.append(el('p', {class: 'nota'}, 'Citado sem estar no contexto: ' + fora.join(', ')));
    const dl = el('dl');
    [['A rota aponta a classe', r.cr == null ? 'nenhuma (empate ou sem evidência)' : nomeClasse(r.cr) + (r.cr === c.c ? ', a do caso' : ', que não é a do caso')],
     ['O modelo respondeu', r.rot || 'resposta sem rótulo'], ['Causa do caso', c.g], ['Resultado', r.ok ? '✓ certo' : '✗ errado']
    ].forEach(([k, val]) => { dl.append(el('dt', {}, k), el('dd', {}, val)); });
    painel.append(dl);
  }

  function desenharRota(){
    camada.replaceChildren(); if(!est.caso) return;
    const r = fatia().rotas[est.caso], c = A.casos[est.caso]; if(!r) return;
    // o marcador do caso fica fora do hexágono, girado 13 graus a partir da âncora da classe dele, para não cobrir o nome da classe
    const anc = A.classes.find(k => k.n === c.c), g13 = 13 * Math.PI / 180, co = Math.cos(g13), si = Math.sin(g13);
    const [cx, cy] = px((anc.x * co - anc.y * si) * 1.2, (anc.x * si + anc.y * co) * 1.2);
    const numeros = [];
    r.rec.forEach((id, k) => { const v = verbete(id); if(!v) return; const [x, y] = px(v.x, v.y), raio = v.raio * G.escala;
      camada.append(sv('line', {x1: cx.toFixed(1), y1: cy.toFixed(1), x2: x.toFixed(1), y2: y.toFixed(1), class: 'at-linha' + (r.cit.includes(id) ? ' citado' : '')}));
      // o número de ordem fica na borda do nó, do lado de onde a linha chega
      const d = Math.hypot(cx - x, cy - y) || 1, mx = x + (cx - x) / d * (raio + 2), my = y + (cy - y) / d * (raio + 2);
      numeros.push(sv('circle', {cx: mx.toFixed(1), cy: my.toFixed(1), r: 9, class: 'at-ordem-fundo'}), sv('text', {x: mx.toFixed(1), y: (my + 4).toFixed(1), 'text-anchor': 'middle', class: 'at-ordem'}, String(k + 1))); });
    camada.append(...numeros);
    camada.append(sv('circle', {cx: cx.toFixed(1), cy: cy.toFixed(1), r: 11, class: 'at-caso ' + (r.ok ? 'ok' : 'erro')}));
    // o nome do caso fica do lado de fora do marcador (para longe do centro do mapa)
    const fx = cx - G.cx, fy = cy - G.cy, fd = Math.hypot(fx, fy) || 1, ux = fx / fd, uy = fy / fd;
    camada.append(sv('text', {x: (cx + ux * 18).toFixed(1), y: (cy + uy * 18 + (uy > 0.4 ? 12 : (uy < -0.4 ? -2 : 4))).toFixed(1),
      'text-anchor': ux < -0.35 ? 'end' : (ux > 0.35 ? 'start' : 'middle'), class: 'at-caso-rot'}, est.caso + (r.ok ? ' ✓' : ' ✗')));
  }

  function confusoes(){
    if(!conf) return; const f = fatia(), ys = {}, yr = {};
    conf.querySelectorAll('.at-causa').forEach(g => { const c = g.dataset.causa, par = f.causas[c] || [0, 0]; ys[c] = Number(g.dataset.y);
      g.querySelector('.acerto').setAttribute('width', par[0] ? (60 * par[1] / par[0]).toFixed(1) : '0');
      const t = g.querySelector('.ac'); t.textContent = par[0] ? par[1] + ' de ' + par[0] : 'sem casos';
      g.classList.toggle('sem-casos', !par[0]); });
    conf.querySelectorAll('.at-resp').forEach(g => { yr[g.dataset.resp] = Number(g.dataset.y); });
    const grupo = conf.querySelector('.at-arestas'); grupo.replaceChildren();
    f.conf.forEach(([g, r, n]) => { if(ys[g] == null) return; const y2 = r == null ? yr.__sem__ : (yr[r] != null ? yr[r] : yr.__outro__), x1 = G.conf_x1, x2 = G.conf_x2, m = (x1 + x2) / 2;
      const p = sv('path', {class: 'at-aresta', d: `M${x1} ${ys[g]} C${m} ${ys[g]}, ${m} ${y2}, ${x2} ${y2}`, 'stroke-width': (1.5 + 2 * (n - 1)).toFixed(1)});
      p.append(sv('title', {}, `${g} respondida como ${r || 'resposta sem rótulo'}: ${n} caso${n !== 1 ? 's' : ''}`)); grupo.append(p); });
  }

  function opcoesDaFatia(){
    const antes = A.fatias.find(f => f.id === est.fatia) || {}, daBib = A.fatias.filter(f => f.bib === est.bib);
    selFat.replaceChildren(); daBib.forEach(f => selFat.append(el('option', {value: f.id}, f.nome)));
    // ao trocar de biblioteca, fica o mesmo leitor na mesma corrida; se não houver, o mesmo leitor; senão, o primeiro da lista
    if(!daBib.some(f => f.id === est.fatia)) est.fatia = (daBib.find(f => f.modelo === antes.modelo && f.corrida === antes.corrida) || daBib.find(f => f.modelo === antes.modelo) || daBib[0] || {}).id;
    selFat.value = est.fatia;
  }
  function sairDoPasseio(){
    const passo = raiz.querySelector('.at-passo'); if(!passo) return;
    passo.textContent = `Passeio guiado · ${A.paradas.length} paradas`; raiz.querySelector('.at-parada-titulo').textContent = 'Exploração livre';
    raiz.querySelector('.at-parada-texto').textContent = 'A seleção foi mudada à mão. Use Anterior ou Próxima para voltar ao passeio.';
  }
  function opcoesDoCaso(){
    const f = fatia(); selCaso.replaceChildren(el('option', {value: ''}, 'nenhum'));
    A.classes.forEach(c => { const grupo = el('optgroup', {label: c.nome});
      Object.keys(f.rotas).filter(k => A.casos[k].c === c.n).sort((a, b) => a.localeCompare(b, 'pt-BR', {numeric: true})).forEach(k => grupo.append(el('option', {value: k}, k + (f.rotas[k].ok ? ' · certo' : ' · errado'))));
      if(grupo.children.length) selCaso.append(grupo); });
    if(!f.rotas[est.caso]) est.caso = ''; selCaso.value = est.caso;
  }
  function atualizar(){
    pintar(); desenharRota(); confusoes();
    if(est.caso) detalharCaso(est.caso); else if(est.no) detalharNo(est.no);
  }
  function escolherNo(id){ est.no = id; est.caso = ''; selCaso.value = ''; sairDoPasseio(); atualizar(); }

  Object.entries(nos).forEach(([id, g]) => { g.addEventListener('click', () => escolherNo(id));
    g.addEventListener('keydown', e => { if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); escolherNo(id); } }); });
  selBib.addEventListener('change', () => { est.bib = selBib.value; opcoesDaFatia(); opcoesDoCaso(); sairDoPasseio(); atualizar(); });
  selFat.addEventListener('change', () => { est.fatia = selFat.value; opcoesDoCaso(); sairDoPasseio(); atualizar(); });
  selCaso.addEventListener('change', () => { est.caso = selCaso.value; if(est.caso) est.no = null; sairDoPasseio(); atualizar(); });
  raiz.querySelectorAll('.at-classes button').forEach(b => b.addEventListener('click', () => { est.classe = Number(b.dataset.classe); pintar(); }));

  function parada(k){
    const P = A.paradas; if(!P.length) return; est.parada = (k + P.length) % P.length; const p = P[est.parada];
    est.bib = p.bib; selBib.value = p.bib; opcoesDaFatia(); est.fatia = p.fatia; selFat.value = p.fatia; est.classe = 0;
    est.caso = p.caso || ''; est.no = p.caso ? null : (p.no || null); opcoesDoCaso(); atualizar();
    raiz.querySelector('.at-passo').textContent = `Passeio guiado · parada ${est.parada + 1} de ${P.length}`;
    raiz.querySelector('.at-parada-titulo').textContent = p.titulo; raiz.querySelector('.at-parada-texto').textContent = p.texto;
    if(p.confusoes && conf) conf.scrollIntoView({behavior: 'smooth', block: 'center'});
  }
  const ant = raiz.querySelector('.at-anterior'), prox = raiz.querySelector('.at-proxima');
  if(ant) ant.addEventListener('click', () => parada(est.parada - 1));
  if(prox) prox.addEventListener('click', () => parada(est.parada + 1));

  opcoesDaFatia(); opcoesDoCaso(); atualizar();
  if(A.paradas.length){ const p = A.paradas[0]; est.no = p.no || null; atualizar(); raiz.querySelector('.at-passo').textContent = `Passeio guiado · parada 1 de ${A.paradas.length}`; }
}
"""
