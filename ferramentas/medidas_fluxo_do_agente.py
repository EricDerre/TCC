#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (10/11/2026), só de leitura: junta num arquivo as medidas do repositório que a rodada 7
# da pesquisa cita para as três ideias do Eric sobre o fluxo do agente (ficha 64). Lê os JSON já gravados das corridas 16
# (calibração), 20 (biblioteca em produção), 22 (avaliação da trilha), 23 (exemplar e rótulos) e 24 (inéditos em texto), a prévia
# da corrida 25, as taxas do modelo nesta máquina, a planilha de revisão do lote e a tabela da Fase 2-A, e faz uma conta nova, sem
# modelo: refaz a busca de cada um dos 72 casos (os 36 oficiais e os 36 inéditos) com a biblioteca de produção e diz em que posição
# da lista ficou o verbete da causa certa, cruzando isso com o selo de confiança e com os dois gatilhos que o agente já calcula
# (probabilidade baixa e FONTE divergente). Grava `dados/pesquisa-fluxo-do-agente/medidas_do_repositorio.json`; `--check` regera e
# compara. Nada do agente é alterado e nada é gravado em `resultados_alvo/`.
# ! Motivo: a ficha 64 pede pesquisa sobre o raciocínio em passos, o ciclo de reavaliação e um segundo momento do modelo só para a
# documentação, e o veredito de cada ideia depende do que o repositório já mediu. A regra é nenhum número digitado à mão: o
# levantamento §6.16, a proposta de desenho e a aba do painel leem deste arquivo. A conta da posição responde uma pergunta que
# nenhuma corrida respondeu: nos erros em que o verbete certo não chegou ao modelo, uma segunda busca com mais verbetes o traria?
# A busca é código (BM25 com sinais), então dá para saber sem rodar o modelo, desde que a busca refeita devolva os mesmos três
# verbetes que a corrida gravou; o script confere isso caso a caso e para se não bater.
"""Uso:
    python ferramentas/medidas_fluxo_do_agente.py            grava medidas_do_repositorio.json
    python ferramentas/medidas_fluxo_do_agente.py --check    regera e compara com o arquivo gravado (sem a data de geração)
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
# ! Alteração de IA - Revisar: o script aponta o harness para `resultados_alvo` antes de importar qualquer módulo dele, sem trocar um valor que já esteja definido.
# ! Motivo: `caminhos.py` lê a variável RESULTADOS_DIR na importação; sem ela, a partição oficial dos 36 casos de avaliação é procurada em `resultados/fase3/`
# (a pasta da máquina de desenvolvimento) e a leitura para com "sem particao.json". Todas as corridas citadas aqui são da máquina-alvo.
os.environ.setdefault("RESULTADOS_DIR", "resultados_alvo")

RAIZ = Path(__file__).resolve().parents[1]
EXP = RAIZ / "Programacao" / "AgenteCore" / "experimentos"
RES = EXP / "resultados_alvo"
F4 = RES / "fase4"
DADOS = RAIZ / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "dados" / "pesquisa-fluxo-do-agente"
SAIDA = DADOS / "medidas_do_repositorio.json"
RELATORIO_2A = RAIZ / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-2a-relatorio-por-modelo.md"
MODELO = "qwen2.5:7b"
PASTA_DO_MODELO = "qwen2.5_7b"
FAIXAS = ("1 a 3", "4 a 5", "6 a 10", "acima de 10")
SEM_VERBETE = "sem verbete da causa"
# ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) o nome dado ao caso cujo nó de diagnóstico não gravou falha nenhuma.
# ! Motivo: a separação da FONTE divergente pela falha gravada precisa de um nome para o caso sem o campo, para a soma das linhas fechar com os disparos do gatilho.
SEM_FALHA = "sem falha gravada"
VERBETES_DO_SEGUNDO_PASSE = (5, 10)
# ! Alteração de IA - Revisar: o tamanho de um raciocínio em passos, em tokens, usado só para converter em segundos desta máquina.
# ! Motivo: é um número da literatura, não do projeto: cerca de 240 tokens no Qwen2.5 de 3B (236,4) e no Llama 3.1 de 8B (241,5), nas duas fontes do levantamento
# §6.16.1 que medem modelo aberto pequeno; fica declarado aqui para a conta em segundos sair do script, e não da mão.
TOKENS_DE_UM_RACIOCINIO = 240
# ! Alteração de IA - Revisar: o orçamento, em tokens, da ficha curta do caso que a proposta de desenho do analista de documentação descreve.
# ! Motivo: é parâmetro de desenho, não medida: o prompt do diagnóstico tem cerca de 1.190 tokens na mediana, dos quais cerca de 620 são os três verbetes, de modo
# que o caso e as instruções ocupam perto de 570; uma ficha de 400 tokens cabe o caso, a resposta do agente, as conferências e a decisão da pessoa. Declarado aqui
# para a conta do custo de cada cenário de entrada sair do script.
FICHA_DO_CASO_TOKENS = 400
# de onde vem cada caso das duas corridas cruzadas: a leitura (acerto, selo), os registros (os três verbetes entregues) e a trilha
# (os gatilhos do nó de diagnóstico); na corrida 22 o nó que vale é o da inferência de base, cuja trilha termina em "@base"
CORRIDAS = {
    "24": {"banco": "ineditos", "leitura": "ineditos.json", "pasta": "fase4_ineditos", "registros": "ineditos.jsonl", "trilha": "trilha_ineditos.jsonl", "sufixo": ""},
    "22": {"banco": "avaliacao", "leitura": "trilha.json", "pasta": "fase4_trilha", "registros": f"{PASTA_DO_MODELO}/diagnosticos__base.jsonl", "trilha": "trilha_avaliacao.jsonl", "sufixo": "@base"},
}


# ------------------------------------------------------------------ contas puras (testadas com casos inventados)

def mediana(valores: list) -> float | None:
    vals = [v for v in valores if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return statistics.median(vals) if vals else None


def faixa_da_posicao(posicao: int | None) -> str:
    """A faixa em que cai a posição do verbete da causa certa na lista da busca: os três entregues, o que um contexto de 5 ou de 10
    verbetes alcançaria, e o que fica além disso."""
    if posicao is None:
        return SEM_VERBETE
    if posicao <= 3:
        return FAIXAS[0]
    if posicao <= 5:
        return FAIXAS[1]
    return FAIXAS[2] if posicao <= 10 else FAIXAS[3]


def cruzar(casos: list[dict]) -> dict:
    """O cruzamento, caso a caso, do acerto com o selo, com os dois gatilhos e com a posição do verbete certo. Cada caso traz `caso`,
    `acerto`, `selo`, `gatilho_probabilidade`, `gatilho_fonte` e `posicao` (1 é o primeiro da busca; até 3 chegou ao modelo).
    O teto de um segundo passe conta os erros em que um gatilho acendeu, o verbete certo não estava entre os três entregues e
    estaria entre os N primeiros: é o máximo que um segundo passe com N verbetes poderia consertar, não uma previsão."""
    erros = [c for c in casos if not c["acerto"]]
    presentes = [c for c in casos if c["posicao"] is not None and c["posicao"] <= 3]
    ausentes = [c for c in casos if c not in presentes]

    def disparou(c: dict, quais: tuple[str, ...]) -> bool:
        return any(c[q] for q in quais)

    gatilhos = []
    for nome, quais in (("selo baixo", ("gatilho_probabilidade",)), ("FONTE divergente", ("gatilho_fonte",)),
                        ("selo baixo ou FONTE divergente", ("gatilho_probabilidade", "gatilho_fonte"))):
        acesos = [c for c in casos if disparou(c, quais)]
        pegos = sum(1 for c in acesos if not c["acerto"])
        gatilhos.append({"gatilho": nome, "disparos": len(acesos), "erros_pegos": pegos, "acertos_incomodados": len(acesos) - pegos, "erros_perdidos": len(erros) - pegos})
    algum = ("gatilho_probabilidade", "gatilho_fonte")
    teto = []
    for n in VERBETES_DO_SEGUNDO_PASSE:
        ao_alcance = sum(1 for c in erros if disparou(c, algum) and c["posicao"] is not None and 3 < c["posicao"] <= n)
        teto.append({"verbetes": n, "disparos": gatilhos[-1]["disparos"], "erros_ao_alcance": ao_alcance, "erros_fora_do_alcance": len(erros) - ao_alcance})
    # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) os casos com a FONTE divergente saem também separados pela falha que o nó de diagnóstico gravou.
    # ! Motivo: o gatilho da FONTE junta duas conferências de `diagnostico_ao_vivo.REGRAS_DA_FONTE_DIVERGENTE` (a FONTE cita um verbete fora dos três entregues; nenhum verbete
    # entregue trata da causa respondida), e a proposta de desenho do analista de documentação só trata a segunda como lacuna da documentação. O texto atribuía os casos a ela
    # sem ter medido. A falha gravada é a da primeira conferência que não confere, na ordem de `FALHA_POR_REGRA`; o caso sem o campo entra como "sem falha gravada".
    com_fonte = [c for c in casos if c["gatilho_fonte"]]
    por_falha = [{"falha": f, "casos": sum(1 for c in com_fonte if (c.get("falha") or SEM_FALHA) == f),
                  "acertos": sum(1 for c in com_fonte if (c.get("falha") or SEM_FALHA) == f and c["acerto"]),
                  "erros": sum(1 for c in com_fonte if (c.get("falha") or SEM_FALHA) == f and not c["acerto"])}
                 for f in sorted({c.get("falha") or SEM_FALHA for c in com_fonte})]
    return {
        "casos": len(casos), "acertos": len(casos) - len(erros), "erros": len(erros),
        "verbete_certo_no_contexto": {"presente": {"casos": len(presentes), "acertos": sum(1 for c in presentes if c["acerto"])},
                                      "ausente": {"casos": len(ausentes), "acertos": sum(1 for c in ausentes if c["acerto"])}},
        "erros_sem_o_verbete_certo": sum(1 for c in erros if c in ausentes),
        "posicao_do_verbete_certo": [{"faixa": f, "casos": sum(1 for c in casos if faixa_da_posicao(c["posicao"]) == f),
                                      "erros": sum(1 for c in erros if faixa_da_posicao(c["posicao"]) == f)} for f in FAIXAS],
        "gatilhos": gatilhos,
        "fonte_divergente_por_falha": por_falha,
        "teto_de_um_segundo_passe": teto,
        "lista_de_erros": [{**{k: c.get(k) for k in ("caso", "gabarito", "rotulo", "selo", "posicao", "gatilho_probabilidade", "gatilho_fonte")},
                            "faixa": faixa_da_posicao(c["posicao"])} for c in erros],
    }


# ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) função nova: cruza a decisão de uma pessoa sobre cada relatório (aceitar ou recusar) com o acerto do
# diagnóstico e com o gatilho da FONTE divergente do mesmo caso.
# ! Motivo: a proposta de desenho do analista de documentação dizia que os diagnósticos certos que o analista de QA recusou na sessão de revisão da corrida 24 eram os que
# nenhum verbete entregue sustentava, sem número medido; a conta sai daqui. Para com SystemExit se um relatório revisado não existir na corrida, porque a soma deixaria de fechar.
def decisao_e_fonte_divergente(casos: list[dict], revisao: list[dict]) -> dict:
    """`casos` são os da corrida (`caso`, `acerto`, `gatilho_fonte`, `falha`); `revisao` são os relatórios decididos (`caso`, `decisao`, em que recusar é "recusar").
    Devolve, dos acertos e dos erros com a FONTE divergente, quantos a pessoa recusou, e os diagnósticos certos recusados separados pelo gatilho e pela falha gravada."""
    por_caso = {c["caso"]: c for c in casos}
    faltam = [r["caso"] for r in revisao if r["caso"] not in por_caso]
    if faltam:
        raise SystemExit(f"a revisão traz relatórios que não estão na corrida: {', '.join(faltam)}")
    linhas = [{**por_caso[r["caso"]], "recusou": r.get("decisao") == "recusar"} for r in revisao]
    certos_recusados = [l for l in linhas if l["acerto"] and l["recusou"]]
    falhas = sorted({l.get("falha") or SEM_FALHA for l in certos_recusados})

    def quantos(acerto: bool, recusou: bool | None = None) -> int:
        return sum(1 for l in linhas if l["gatilho_fonte"] and l["acerto"] == acerto and (recusou is None or l["recusou"] == recusou))

    return {"acertos_com_a_fonte_divergente": quantos(True), "acertos_com_a_fonte_divergente_recusados": quantos(True, True),
            "certos_recusados_com_a_fonte_divergente": sum(1 for l in certos_recusados if l["gatilho_fonte"]),
            "certos_recusados_sem_a_fonte_divergente": sum(1 for l in certos_recusados if not l["gatilho_fonte"]),
            "certos_recusados_por_falha": [{"falha": f, "casos": sum(1 for l in certos_recusados if (l.get("falha") or SEM_FALHA) == f)} for f in falhas],
            "erros_com_a_fonte_divergente": quantos(False), "erros_com_a_fonte_divergente_recusados": quantos(False, True)}


# ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) função nova: dos verbetes novos de um lote, quantos nenhum caso com gabarito leria.
# ! Motivo: o mapa do levantamento dizia que nenhum caso leria os verbetes novos da corrida 20; a conta por edição mostra que um deles teria um leitor, e a frase
# passa a citar o número medido em vez de um "nenhum" escrito à mão.
def verbetes_novos_do_lote(por_edicao: list[dict]) -> dict:
    """`por_edicao` é a lista do portão da busca (`operacao`, `casos_que_leriam_a_edicao`). Conta só as edições de operação `novo_verbete`."""
    leitores = [e["casos_que_leriam_a_edicao"] for e in por_edicao if e.get("operacao") == "novo_verbete"]
    return {"edicoes": len(leitores), "que_nenhum_caso_leria": sum(1 for n in leitores if n == 0), "com_algum_caso": sum(1 for n in leitores if n > 0),
            "casos_que_os_leriam_no_total": sum(leitores)}


def p_pareado_exato(b: int, c: int) -> float:
    """O p bilateral do teste pareado exato (McNemar pela binomial) para b casos ganhos e c perdidos, a mesma conta que as leituras das corridas usam."""
    import math
    n = b + c
    if n == 0:
        return 1.0
    cauda = sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n
    return min(1.0, round(2 * cauda, 4))


# ------------------------------------------------------------------ prévia: o rótulo respondido contradito por um fato medido em código

# ! Alteração de IA - Revisar: cinco conferências de exemplo, só de leitura, que dizem quando o rótulo que o modelo respondeu é contradito por um fato que o código
# mede no próprio caso: "corpo vazio" com corpo que tem texto; "corpo não é JSON" e "resposta truncada" com corpo que é um JSON inteiro; "coleção no lugar de objeto"
# com o corpo na forma que a rota devolve (lista em /api/produtos, objeto em /api/produtos/7) e sem lista dentro de campo simples; "tipo divergente" com todos os
# campos no tipo do contrato. Não fazem parte do agente: servem para dimensionar, nos registros gravados, a forma da lista de conferência que não mexe no prompt.
# ! Motivo: o veredito da ideia 1 (ficha 64) diz que a lista de conferência cabe depois da resposta, como conferência em código; sem um número, a recomendação de
# medi-la seria só opinião. As cinco foram escritas olhando os erros das corridas 22 e 24, e por isso a medida também sai separada para os casos de aprendizado da
# corrida 16, que não foram olhados. Cada conferência é testada contra o gabarito: ela nunca pode contradizer o rótulo num caso em que ele é a causa certa.
_ROTA_DE_DETALHE = __import__("re").compile(r"/api/[a-z_]+/\d+")
_ROTA_CONHECIDA = __import__("re").compile(r"\bGET\s+/api/(produtos|pedidos)\b")


def corpo_do_caso(caso: dict) -> tuple[str, object]:
    """O corpo da resposta do caso como o código o lê: "sem corpo", "vazio", "invalido" (não é um JSON inteiro) ou "ok" com o valor lido."""
    corpo = (caso.get("entrada") or {}).get("corpo")
    if corpo is None:
        return "sem corpo", None
    if isinstance(corpo, (dict, list)):
        return "ok", corpo
    texto = str(corpo).strip()
    if not texto:
        return "vazio", None
    try:
        return "ok", json.loads(texto)
    except ValueError:
        return "invalido", None


def _itens(valor: object) -> list[dict]:
    return [x for x in (valor if isinstance(valor, list) else [valor]) if isinstance(x, dict)]


def _tipos_do_contrato(caso: dict) -> dict[str, set[str]]:
    sys.path.insert(0, str(EXP))
    import recuperacao as rec
    return rec._parse_contrato(str((caso.get("entrada") or {}).get("contrato") or ""))


def _tipo_do_valor(v: object) -> str:
    sys.path.insert(0, str(EXP))
    import recuperacao as rec
    return rec._TIPO_JSON.get(type(v), "outro")


def contradiz_corpo_vazio(caso: dict) -> bool:
    return corpo_do_caso(caso)[0] in ("ok", "invalido")


def contradiz_corpo_que_nao_e_json(caso: dict) -> bool:
    return corpo_do_caso(caso)[0] == "ok"


def contradiz_colecao_no_lugar_de_objeto(caso: dict) -> bool:
    """O rótulo diz que veio uma coleção onde se esperava um objeto (ou o contrário). É contradito quando a rota é conhecida, o corpo veio na forma que ela devolve
    e nenhum campo que o contrato dá como simples traz uma lista ou um objeto."""
    estado, valor = corpo_do_caso(caso)
    requisicao = str((caso.get("entrada") or {}).get("requisicao") or "")
    if estado != "ok" or not _ROTA_CONHECIDA.search(requisicao):
        return False
    espera_objeto = bool(_ROTA_DE_DETALHE.search(requisicao))
    if isinstance(valor, dict) != espera_objeto or not isinstance(valor, (dict, list)):
        return False
    contrato = _tipos_do_contrato(caso)
    return not any(isinstance(v, (list, dict)) and not ({"lista", "objeto"} & contrato.get(campo, set())) for item in _itens(valor) for campo, v in item.items())


def contradiz_tipo_divergente(caso: dict) -> bool:
    """O rótulo diz que um campo veio com o tipo trocado. É contradito quando o corpo é um JSON inteiro, há contrato, e todo campo do contrato presente no corpo
    tem um dos tipos que o contrato aceita."""
    estado, valor = corpo_do_caso(caso)
    contrato = _tipos_do_contrato(caso)
    itens = _itens(valor)
    if estado != "ok" or not contrato or not itens:
        return False
    return all(_tipo_do_valor(v) in contrato[campo] for item in itens for campo, v in item.items() if campo in contrato)


CONFERENCIAS_DO_ROTULO = {
    "corpo_vazio": contradiz_corpo_vazio,
    "corpo_nao_e_json": contradiz_corpo_que_nao_e_json,
    "resposta_truncada": contradiz_corpo_que_nao_e_json,
    "colecao_no_lugar_de_objeto": contradiz_colecao_no_lugar_de_objeto,
    "tipo_divergente": contradiz_tipo_divergente,
}


def rotulo_contradito(caso: dict, rotulo: str | None) -> bool:
    """O rótulo respondido tem conferência e o fato medido no caso o contradiz."""
    conferencia = CONFERENCIAS_DO_ROTULO.get(rotulo or "")
    return bool(conferencia and conferencia(caso))


def previa_da_conferencia(casos: dict[str, dict], respostas: list[dict]) -> dict:
    """Aplica as conferências às respostas gravadas de uma corrida. `respostas` traz `caso`, `rotulo` e `acerto`. Devolve quantos erros têm o rótulo contradito,
    quantos acertos teriam (tem de ser zero), e quantos erros responderam um rótulo que tem conferência."""
    erros = [r for r in respostas if not r["acerto"]]
    acertos = [r for r in respostas if r["acerto"]]
    contraditos = [r for r in erros if rotulo_contradito(casos[r["caso"]], r.get("rotulo"))]
    return {"casos": len(respostas), "erros": len(erros), "erros_com_rotulo_conferivel": sum(1 for r in erros if r.get("rotulo") in CONFERENCIAS_DO_ROTULO),
            "erros_contraditos": len(contraditos), "acertos_contraditos": sum(1 for r in acertos if rotulo_contradito(casos[r["caso"]], r.get("rotulo"))),
            "lista": [{"caso": r["caso"], "rotulo": r.get("rotulo"), "gabarito": casos[r["caso"]]["gabarito"]["causa_raiz"]} for r in contraditos]}


def _previa_da_conferencia_nas_corridas() -> dict:
    """A prévia nas três corridas em texto que têm a resposta gravada: a calibração (corrida 16, 90 casos, com os 54 de aprendizado à parte), a base da corrida 22
    (36 oficiais) e a corrida 24 (36 inéditos). Antes, confere cada conferência contra o gabarito e para se alguma contradisser o rótulo num caso em que ele é o certo."""
    sys.path.insert(0, str(EXP))
    import executar_fase3b as e3b
    import experimento_sem_notas as esn
    casos = {c["id"]: c for c in list(e3b.TODOS_OS_CASOS) + list(esn.casos_por_banco()["ineditos"])}
    do_rotulo = [c for c in casos.values() if c["gabarito"]["causa_raiz"] in CONFERENCIAS_DO_ROTULO]
    falsos = [c["id"] for c in do_rotulo if rotulo_contradito(c, c["gabarito"]["causa_raiz"])]
    if falsos:
        raise SystemExit(f"uma conferência contradiz o rótulo em caso cujo gabarito é esse rótulo: {falsos}")
    cal = _json(F4 / "calibracao.json")
    do_k = next(x for x in cal["por_k"] if x["k"] == cal["r8"]["k"])
    c16 = [{"caso": c["caso"], "rotulo": c.get("rotulo"), "acerto": bool(c["acerto"]), "particao": c.get("particao")} for c in do_k["casos"]]
    c22 = [{"caso": c["caso"], "rotulo": c.get("rotulo"), "acerto": bool(c["acerto"])} for c in _json(F4 / "trilha.json")["casos"]]
    c24 = [{"caso": c["caso"], "rotulo": c.get("rotulo"), "acerto": bool(c["acerto"])} for c in _json(F4 / "ineditos.json")["casos"]]
    corridas = [("corrida 16, os 90 casos da calibração", c16), ("corrida 16, só os 54 casos de aprendizado", [r for r in c16 if r["particao"] == "aprendizado"]),
                ("corrida 22, os 36 oficiais de avaliação", c22), ("corrida 24, os 36 inéditos", c24)]
    return {"conferencias": list(CONFERENCIAS_DO_ROTULO), "quantas": len(CONFERENCIAS_DO_ROTULO), "casos_cujo_gabarito_tem_conferencia": len(do_rotulo), "desses_contraditos": len(falsos),
            "por_corrida": [{"corrida": nome, **previa_da_conferencia(casos, respostas)} for nome, respostas in corridas],
            "fonte": ("as respostas gravadas em resultados_alvo/fase4/calibracao.json (por_k, k = 3), trilha.json e ineditos.json (campo casos), e a entrada de cada caso nos "
                      "bancos de casos; as conferências são medidas_fluxo_do_agente.CONFERENCIAS_DO_ROTULO, escritas para esta prévia, fora do agente")}


def linha_da_fase_2a(relatorio: str, modelo: str) -> dict:
    """A linha de um modelo na tabela da seção 3 do relatório da Fase 2-A (prompt direto contra prompt em etapas), com os textos das
    células como estão no relatório."""
    secao = relatorio[relatorio.index("## 3. Estratégias de prompt"):]
    for l in secao.splitlines():
        if l.startswith(f"| `{modelo}` |"):
            cel = [c.strip().replace("**", "") for c in l.strip().strip("|").split("|")]
            return {"modelo": modelo, "linear": cel[1], "estagios_compilador": cel[2], "estagios_dominio": cel[3], "linear_x_compilador": cel[4], "linear_x_dominio": cel[5]}
        if l.startswith("## ") and not l.startswith("## 3."):
            break
    raise SystemExit(f"linha de {modelo} não encontrada na seção 3 do relatório da Fase 2-A")


# ------------------------------------------------------------------ leitura dos arquivos das corridas

def _json(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"))


def _jsonl(caminho: Path) -> list[dict]:
    return [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]


def _gatilhos_da_trilha(caminho: Path, sufixo: str) -> dict[str, dict]:
    """caso -> os gatilhos do nó de diagnóstico da trilha e, na chave `falha`, a falha que o nó gravou (na corrida 22, só o da inferência de base)."""
    saida = {}
    for e in _jsonl(caminho):
        d = e.get("dados") or {}
        if e.get("tipo") != "decisao" or d.get("decisao") != "diagnostico":
            continue
        nome = str(e.get("trilha", "")).split("/")[-1]
        if sufixo:
            if not nome.endswith(sufixo):
                continue
            nome = nome[: -len(sufixo)]
        elif "@" in nome:
            continue
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) leva junto a falha gravada no nó (`dados.falha`).
        # ! Motivo: é ela que diz qual das duas conferências da FONTE não conferiu (`citacao_fora_do_contexto` ou `causa_sem_verbete_que_a_trate`); o gatilho sozinho não diz.
        saida[nome] = {**(d.get("gatilhos") or {}), "falha": d.get("falha")}
    return saida


def _posicoes(banco: str) -> dict[str, dict]:
    """caso -> a posição do verbete da causa certa na busca refeita agora com a biblioteca de produção, e os três primeiros ids.
    A busca é a do agente (`recuperacao.pontuar` sobre `diagnostico_ao_vivo.caso_da_busca`), só lida; o verbete da causa certa é o
    que tem o id igual à causa do gabarito, a mesma definição de `ineditos.json` e da prévia da corrida 25."""
    sys.path.insert(0, str(EXP))
    import biblioteca as bib
    import diagnostico_ao_vivo as dv
    import executar_fase4 as ex
    import experimento_sem_notas as esn
    import recuperacao as rec
    verbetes = bib.carregar(dv.PASTA_CURADA)
    indice = rec.Indice(verbetes)
    saida = {}
    for c in esn.casos_por_banco()[banco]:
        ordem = [v["id"] for _, v in rec.pontuar(indice, dv.caso_da_busca(ex.fixture_sem_gabarito(c)))]
        causa = c["gabarito"]["causa_raiz"]
        saida[c["id"]] = {"posicao": ordem.index(causa) + 1 if causa in ordem else None, "tres_primeiros": ordem[:3], "verbetes": len(ordem)}
    return saida


# ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) passa a devolver também a lista dos casos lidos, cada um com a falha gravada no nó de diagnóstico.
# ! Motivo: o cruzamento com a decisão do analista de QA na sessão de revisão da corrida 24 (`decisao_e_fonte_divergente`) precisa do caso a caso, que antes ficava só
# dentro desta função; a lista não entra no arquivo de medidas, só as contas feitas sobre ela.
def ler_corrida(numero: str) -> tuple[dict, list[dict]]:
    """O cruzamento de uma das duas corridas com a busca refeita, e os casos lidos. Para se a busca de agora não devolver os três verbetes gravados."""
    conf = CORRIDAS[numero]
    leitura = _json(F4 / conf["leitura"])
    registros = {r["caso"]: r for r in _jsonl(RES / conf["pasta"] / conf["registros"])}
    gatilhos = _gatilhos_da_trilha(RES / conf["pasta"] / conf["trilha"], conf["sufixo"])
    posicoes = _posicoes(conf["banco"])
    casos, iguais = [], 0
    for c in leitura["casos"]:
        cid = c["caso"]
        if cid not in registros or cid not in gatilhos or cid not in posicoes:
            raise SystemExit(f"corrida {numero}: o caso {cid} não está nos registros, na trilha ou no banco de casos")
        gravados = list(registros[cid].get("verbetes_ids") or [])[:3]
        iguais += posicoes[cid]["tres_primeiros"] == gravados
        g = gatilhos[cid]
        casos.append({"caso": cid, "gabarito": c.get("gabarito"), "rotulo": c.get("rotulo"), "acerto": bool(c["acerto"]), "selo": c.get("selo"),
                      "gatilho_probabilidade": bool(g.get("probabilidade")), "gatilho_fonte": bool(g.get("fonte_divergente")), "posicao": posicoes[cid]["posicao"],
                      "falha": g.get("falha")})
    if iguais != len(casos):
        raise SystemExit(f"corrida {numero}: a busca refeita devolve os três verbetes gravados em {iguais} de {len(casos)} casos; a biblioteca de produção mudou "
                         "depois da corrida, e a posição do verbete certo deixaria de ser a da corrida")
    cond = leitura.get("condicoes") or {}
    return ({**cruzar(casos), "busca_refeita_igual": iguais, "verbetes_na_biblioteca": next(iter(posicoes.values()))["verbetes"],
             "hash_da_biblioteca": (cond.get("biblioteca") or {}).get("hash"), "versao_ollama": cond.get("versao_ollama"),
             "por_selo": [{"selo": s, "casos": sum(1 for c in casos if c["selo"] == s), "erros": sum(1 for c in casos if c["selo"] == s and not c["acerto"])} for s in ("alto", "medio", "baixo")]},
            casos)


def _medianas(registros: list[dict], campos: tuple[str, ...]) -> dict:
    return {c: mediana([r.get(c) for r in registros]) for c in campos}


def _tamanho_dos_textos(pasta: Path) -> dict:
    """Quantos arquivos de texto por caso há numa pasta de relatórios ou de árvores e a mediana de caracteres (sem o índice)."""
    tamanhos = [len(p.read_text(encoding="utf-8")) for p in sorted(pasta.glob("*.md")) if p.name != "INDICE.md"]
    return {"arquivos": len(tamanhos), "chars_mediana": mediana(tamanhos)}


def _revisao_do_lote(planilha: Path) -> dict:
    """A contagem dos vereditos da planilha de revisão humana do lote da corrida 20, pela mesma leitura que a promoção usa."""
    sys.path.insert(0, str(EXP))
    import biblioteca_fase4 as b4
    vered = b4.vereditos_da_planilha(planilha.read_text(encoding="utf-8"))
    por_veredito = Counter(aval for aval, _ in vered.values())
    por_operacao = Counter((chave[2], aval) for chave, (aval, _) in vered.items())
    return {"edicoes_revisadas": len(vered), "por_veredito": {v: por_veredito.get(v, 0) for v in b4.VEREDITOS_DA_REVISAO},
            "por_operacao": [{"operacao": op, **{v: por_operacao.get((op, v), 0) for v in b4.VEREDITOS_DA_REVISAO}} for op in sorted({o for o, _ in por_operacao})],
            "fonte": "resultados_alvo/fase4_biblioteca/revisao_do_lote.md, coluna Avaliação, lida por biblioteca_fase4.vereditos_da_planilha"}


def _conferencias_em_codigo() -> dict:
    """As regras com que o código confere a resposta do modelo depois que ela sai (a lista de conferência que já existe), lidas de diagnostico_ao_vivo."""
    sys.path.insert(0, str(EXP))
    import diagnostico_ao_vivo as dv
    return {"regras": list(dv.FALHA_POR_REGRA), "quantas": len(dv.FALHA_POR_REGRA), "fonte": "Programacao/AgenteCore/experimentos/diagnostico_ao_vivo.py, FALHA_POR_REGRA"}


def _filtros_em_codigo() -> dict:
    """Quantos códigos de recusa tem o validador da Fase 3, quantos filtros tem a Fase 4 e quantas propostas o formato de hoje aceita por caso, lidos do código."""
    sys.path.insert(0, str(EXP))
    import biblioteca_fase4 as b4
    import evolucao_biblioteca as evo
    return {"codigos_do_validador_da_fase_3": len(evo.CODIGOS_REJEICAO), "filtros_da_fase_4": len(b4.FILTROS), "propostas_por_caso": evo.MAX_PROPOSTAS_POR_CASO,
            "parcela_da_regra_dos_40_pct": round(100 * b4.PARCELA_PARA_REVISAO), "fonte": "evolucao_biblioteca.CODIGOS_REJEICAO e MAX_PROPOSTAS_POR_CASO; biblioteca_fase4.FILTROS e PARCELA_PARA_REVISAO"}


def em_forma_de_instrucao(texto: str, verbos: tuple[str, ...]) -> bool:
    """O texto de uma proposta começa por um verbo de instrução ("Adicionar", "Corrigir"), em vez de afirmar um fato sobre o sistema."""
    return str(texto or "").strip().startswith(verbos)


def contar_forma_de_instrucao(propostas: list[dict], revisadas: list[dict], verbos: tuple[str, ...], vereditos: tuple[str, ...]) -> dict:
    """Quantas propostas vêm em forma de instrução. `propostas` traz `texto` e `destino` (aceita, para revisão ou recusada); `revisadas`
    traz `texto` e `veredito` (o da revisão humana do lote)."""
    def n(itens: list[dict]) -> int:
        return sum(1 for x in itens if em_forma_de_instrucao(x["texto"], verbos))

    passaram = [p for p in propostas if p["destino"] != "recusada"]
    return {"propostas": len(propostas), "em_forma_de_instrucao": n(propostas), "passaram_nos_filtros": len(passaram), "passaram_em_forma_de_instrucao": n(passaram),
            "por_veredito": [{"veredito": v, "edicoes": sum(1 for r in revisadas if r["veredito"] == v), "em_forma_de_instrucao": n([r for r in revisadas if r["veredito"] == v])} for v in vereditos]}


def _forma_de_instrucao_na_corrida_20() -> dict:
    """A forma de instrução nas 92 propostas da corrida 20 e nas 20 que a pessoa revisou; os verbos são os da prévia da corrida 25."""
    sys.path.insert(0, str(EXP))
    import biblioteca_fase4 as b4
    import experimento_sem_notas as esn
    propostas = []
    for r in _jsonl(RES / "fase4_biblioteca" / PASTA_DO_MODELO / "propostas__E101.jsonl"):
        for bloco, decisao in zip(r.get("propostas_parseadas") or [], r.get("decisoes") or []):
            propostas.append({"texto": (bloco.get("campos") or {}).get("TEXTO", ""), "destino": "aceita" if decisao.get("aceita") else "para revisão" if decisao.get("para_revisao") else "recusada"})
    vered = b4.vereditos_da_planilha((RES / "fase4_biblioteca" / "revisao_do_lote.md").read_text(encoding="utf-8"))
    revisadas = [{"texto": chave[3], "veredito": aval} for chave, (aval, _) in vered.items()]
    return {**contar_forma_de_instrucao(propostas, revisadas, esn.VERBOS_DE_INSTRUCAO, b4.VEREDITOS_DA_REVISAO), "verbos": list(esn.VERBOS_DE_INSTRUCAO),
            "fonte": ("resultados_alvo/fase4_biblioteca/qwen2.5_7b/propostas__E101.jsonl (campo TEXTO de cada proposta e a decisão dos filtros) e revisao_do_lote.md; "
                      "os verbos são experimento_sem_notas.VERBOS_DE_INSTRUCAO")}


def efeito_na_busca(antes: dict[str, list[str]], depois: dict[str, list[str]], certo: dict[str, str], verbete: str) -> dict:
    """O que uma edição muda na busca: em quantos casos os três verbetes entregues mudam, em quantos o verbete da causa certa entra ou
    sai dos três, e em quantos casos o verbete editado fica entre os três (os casos em que o modelo leria a edição). `antes` e `depois`
    são caso -> os três ids; `certo` é caso -> o id do verbete da causa certa."""
    mudam = [c for c in antes if antes[c] != depois[c]]
    return {"casos_em_que_os_tres_verbetes_mudam": len(mudam),
            "verbete_certo_entra": sum(1 for c in mudam if certo[c] not in antes[c] and certo[c] in depois[c]),
            "verbete_certo_sai": sum(1 for c in mudam if certo[c] in antes[c] and certo[c] not in depois[c]),
            "casos_que_leriam_a_edicao": sum(1 for c in depois if verbete in depois[c])}


def _portao_da_busca_no_lote() -> dict:
    """Aplica, uma a uma, as edições do lote da corrida 20 a uma cópia temporária da biblioteca de antes do lote e refaz a busca dos
    casos com gabarito (os 90 oficiais e os 36 inéditos da ficha 27): é a conferência que um portão por edição faria sem modelo.
    Nada é gravado fora da pasta temporária."""
    import tempfile
    sys.path.insert(0, str(EXP))
    import biblioteca as bib
    import diagnostico_ao_vivo as dv
    import evolucao_biblioteca as evo
    import executar_fase3b as e3b
    import executar_fase4 as ex
    import experimento_sem_notas as esn
    import recuperacao as rec
    casos = list(e3b.TODOS_OS_CASOS) + list(esn.casos_por_banco()["ineditos"])
    certo = {c["id"]: c["gabarito"]["causa_raiz"] for c in casos}
    consultas = {c["id"]: dv.caso_da_busca(ex.fixture_sem_gabarito(c)) for c in casos}
    base = RES / "fase4_biblioteca" / "bibliotecas" / PASTA_DO_MODELO / "epoca-100"
    lote = _json(RES / "fase4_biblioteca" / "lote.json")

    def tres(pasta: Path) -> dict[str, list[str]]:
        indice = rec.Indice(bib.carregar(pasta))
        return {cid: [v["id"] for _, v in rec.pontuar(indice, consulta)[:3]] for cid, consulta in consultas.items()}

    antes = tres(base)
    edicoes = []
    for e in list(lote.get("edicoes") or []) + list(lote.get("para_revisao") or []):
        with tempfile.TemporaryDirectory() as tmp:
            copia = Path(tmp) / "biblioteca"
            evo.copiar_biblioteca(base, copia)
            evo._limpar_gerados(copia)
            evo.aplicar_edicao(copia, e)
            efeito = efeito_na_busca(antes, tres(copia), certo, e["verbete"])
        edicoes.append({"caso": e.get("caso"), "verbete": e.get("verbete"), "operacao": e.get("operacao"), **efeito})
    sem_efeito = sum(1 for x in edicoes if x["casos_em_que_os_tres_verbetes_mudam"] == 0)
    ligados = [x["casos_que_leriam_a_edicao"] for x in edicoes]
    return {"casos_com_gabarito": len(casos), "edicoes": len(edicoes), "edicoes_que_nao_mudam_a_busca_de_nenhum_caso": sem_efeito,
            "edicoes_que_mudam_a_busca": len(edicoes) - sem_efeito, "verbete_certo_entra_no_total": sum(x["verbete_certo_entra"] for x in edicoes),
            "verbete_certo_sai_no_total": sum(x["verbete_certo_sai"] for x in edicoes), "edicoes_que_nenhum_caso_leria": sum(1 for n in ligados if n == 0),
            "casos_que_leriam_a_edicao_mediana": mediana(ligados), "casos_que_leriam_a_edicao_maximo": max(ligados) if ligados else None,
            "verbete_com_mais_casos": max(edicoes, key=lambda x: x["casos_que_leriam_a_edicao"])["verbete"] if edicoes else None,
            "casos_que_leriam_a_edicao_soma": sum(ligados), "verbetes_novos": verbetes_novos_do_lote(edicoes), "por_edicao": edicoes,
            "fonte": ("resultados_alvo/fase4_biblioteca/lote.json (as 19 edições aceitas e a segurada) aplicadas uma a uma, por evolucao_biblioteca.aplicar_edicao, a uma cópia "
                      "temporária de bibliotecas/qwen2.5_7b/epoca-100 (a biblioteca de antes do lote); a busca é recuperacao.pontuar nos 90 casos oficiais e nos 36 inéditos da ficha 27")}


# ------------------------------------------------------------------ o arquivo de medidas

def montar(gerado_em: str | None = None) -> dict:
    taxas = _json(F4 / "taxas_progresso.json")["por_modelo"][MODELO]
    prefill, geracao = taxas["prefill_tokens_por_s"]["mediana"], taxas["geracao_tokens_por_s"]["mediana"]
    cal = _json(F4 / "calibracao.json")
    k_da_calibracao = cal["r8"]["k"]
    do_k = next(x for x in cal["por_k"] if x["k"] == k_da_calibracao)
    exp = _json(F4 / "experimento_prompt.json")
    tri = _json(F4 / "trilha.json")
    bibl = _json(F4 / "biblioteca.json")
    ined = _json(F4 / "ineditos.json")
    previa = _json(F4 / "sem_notas_previa.json")
    rev = _json(F4 / "leitura_revisao_v3.json")
    fechamento = _json(EXP.parent / "biblioteca_producao" / "fechamento.json")
    curadoria = _json(EXP.parent / "biblioteca_producao" / "curadoria.json")
    corrida_25 = F4 / "sem_notas.json"
    propostas = _jsonl(RES / "fase4_biblioteca" / PASTA_DO_MODELO / "propostas__E101.jsonl")
    diagnosticos = _jsonl(RES / "fase4_biblioteca" / PASTA_DO_MODELO / "diagnosticos__L100.jsonl")
    reavaliacao = _jsonl(RES / "fase4_biblioteca" / PASTA_DO_MODELO / "reavaliacao__E101.jsonl")
    campos = ("tokens_entrada", "tokens_saida", "prefill_ms", "geracao_ms", "segundos")
    med_prop, med_diag = _medianas(propostas, campos), _medianas(diagnosticos, campos)
    relatorios, arvores = _tamanho_dos_textos(RES / "fase4_ineditos" / "relatorios_v3"), _tamanho_dos_textos(RES / "fase4_ineditos" / "arvores")
    chars_por_token = taxas["chars_por_token"]["mediana"]

    def em_tokens(chars: float | None) -> int | None:
        return None if chars is None else round(chars / chars_por_token)

    def segundos_de_leitura(tokens: float | None) -> float | None:
        return None if tokens is None else round(tokens / prefill, 1)

    sinais = {s["sinal"]: s for s in tri["sinais"]}

    def sinal(nome: str) -> dict:
        s = sinais[nome]
        return {k: s[k] for k in ("vp", "fn", "fp", "vn", "tpr", "tnr", "produto", "acaso")}

    sonda20 = bibl["sonda"]
    com_sonda_anterior = sonda20["casos"] - sonda20["sem_sonda_anterior"]
    (cruzamento_22, _), (cruzamento_24, casos_24) = ler_corrida("22"), ler_corrida("24")
    os_72 = somar_cruzamentos([cruzamento_22, cruzamento_24])
    # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) a decisão do analista de QA em cada relatório da corrida 24, cruzada com o acerto e com a FONTE divergente.
    # ! Motivo: dá o número medido para a frase da proposta de desenho sobre os diagnósticos certos recusados; para aqui se a soma não fechar com a contagem de recusas
    # que `leitura_revisao_v3.json` já traz em `adesao`, porque aí as duas leituras estariam falando de casos diferentes.
    certos_recusados = next(g["recusou"] for g in rev["adesao"] if g["grupo"] == "diagnóstico certo")
    decisao_e_fonte = decisao_e_fonte_divergente(casos_24, rev["casos"])
    if decisao_e_fonte["certos_recusados_com_a_fonte_divergente"] + decisao_e_fonte["certos_recusados_sem_a_fonte_divergente"] != certos_recusados:
        raise SystemExit("os diagnósticos certos recusados contados caso a caso não somam os de `adesao` em leitura_revisao_v3.json")
    segundos_do_diagnostico = ined["resumo"]["segundos_mediana"]
    portao = _portao_da_busca_no_lote()
    relatorios = {**relatorios, "tokens_estimados": em_tokens(relatorios["chars_mediana"])}
    arvores = {**arvores, "tokens_estimados": em_tokens(arvores["chars_mediana"])}
    return {
        "_tag": ("! Alteração de IA - Revisar: arquivo gerado por ferramentas/medidas_fluxo_do_agente.py (10/11/2026): as medidas do repositório que a rodada 7 da "
                 "pesquisa cita para as três ideias do Eric sobre o fluxo do agente (ficha 64), copiadas dos JSON das corridas 16, 20, 22, 23 e 24, da prévia da corrida "
                 "25, das taxas do modelo nesta máquina e da planilha de revisão do lote, mais o cruzamento, sem modelo, do acerto com o selo, os gatilhos e a posição do "
                 "verbete da causa certa na busca refeita. NÃO editar à mão: `--check` compara com o regerado."),
        "_motivo": ("! Motivo: o levantamento §6.16, a proposta de desenho do analista de documentação e a aba do painel não podem trazer número digitado à mão; cada bloco "
                    "diz no campo `fonte` de que arquivo e de que campo saiu, e a conta da posição só vale porque a busca refeita devolve os três verbetes gravados em "
                    "todos os casos (campo `busca_refeita_igual`)."),
        "gerado_por": "ferramentas/medidas_fluxo_do_agente.py",
        "gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"),
        "maquina": {
            "modelo": MODELO, "registros": taxas["n"], "prefill_tokens_por_s": prefill, "geracao_tokens_por_s": geracao,
            "tokens_gerados_mediana": taxas["tokens_saida"]["mediana"], "tokens_do_prompt_mediana": taxas["tokens_entrada"]["mediana"], "chars_por_token": chars_por_token,
            "segundos_por_100_tokens_gerados": round(100 / geracao, 1), "segundos_por_100_tokens_lidos": round(100 / prefill, 1),
            # 240 tokens é o tamanho do raciocínio em passos medido em modelos de 3B a 8B nas fontes F03 e F05 do tópico r7-raciocinio-em-passos-em-modelo-pequeno
            "tokens_de_um_raciocinio_em_passos_na_literatura": TOKENS_DE_UM_RACIOCINIO, "segundos_de_um_raciocinio_em_passos": round(TOKENS_DE_UM_RACIOCINIO / geracao, 1),
            "fonte": "resultados_alvo/fase4/taxas_progresso.json, por_modelo.qwen2.5:7b (medianas dos 120 registros das corridas 18d, 21d e 24)",
        },
        "ideia_1": {
            "fase_2a": {**linha_da_fase_2a(RELATORIO_2A.read_text(encoding="utf-8"), MODELO),
                        "fonte": "3-resultados-e-analises/fase-2a-relatorio-por-modelo.md, seção 3, linha do qwen2.5:7b (90 casos; b/c e p do teste pareado exato)"},
            "conferencias_em_codigo": _conferencias_em_codigo(),
            "conferencia_depois_da_resposta": _previa_da_conferencia_nas_corridas(),
            "experimento_em_texto": {"inferencias": do_k["n"], "minutos": round(do_k["n"] * exp["base"]["segundos_mediana"] / 60),
                                     "fonte": "os casos da calibração (calibracao.json, por_k) vezes a mediana de segundos por caso da corrida 16 (experimento_prompt.json, base.segundos_mediana)"},
            "corrida_23": {"base_acertos": exp["base"]["acertos"], "casos": exp["base"]["n"],
                           "condicoes": [{k: c.get(k) for k in ("condicao", "acertos", "b", "c", "p_mcnemar", "trocas_de_rotulo", "tokens_entrada_mediana", "segundos_mediana")} for c in exp["por_condicao"]],
                           "base_tokens_entrada_mediana": exp["base"]["tokens_entrada_mediana"], "base_segundos_mediana": exp["base"]["segundos_mediana"],
                           "fonte": "resultados_alvo/fase4/experimento_prompt.json, base e por_condicao"},
            "calibracao": {"casos": do_k["n"], "k": k_da_calibracao, "auroc_da_probabilidade": do_k["sinais"]["p_rotulo"]["auroc"], "auroc_ic95": do_k["sinais"]["p_rotulo"]["ic95"],
                           "erros": do_k["sinais"]["p_rotulo"]["erros"], "por_selo": [{k: s[k] for k in ("selo", "casos", "certos", "errados", "erro_pct")} for s in cal["por_selo"]],
                           "leitura": cal["limiares"]["leitura"], "baixo_ate": cal["limiares"]["baixo_ate"], "alto_a_partir_de": cal["limiares"]["alto_a_partir_de"],
                           "fonte": "resultados_alvo/fase4/calibracao.json, por_k (k = 3), por_selo e limiares"},
        },
        "ideia_2": {
            "corrida_22": {
                "casos": tri["resumo"]["casos"], "acertos": tri["resumo"]["acertos"], "erros": tri["resumo"]["erros"],
                "divergencia": sinal("divergencia"), "divergencia_por_gatilho": sinal("por_gatilho"), "selo_baixo": sinal("selo_baixo"),
                "intervencoes": [{k: i[k] for k in ("tipo", "n", "mudou_rotulo")} for i in tri["intervencoes"]],
                "repeticao": tri["repeticao"], "sonda": {k: tri["sonda"][k] for k in ("casos", "cita_plantado", "mudou_rotulo", "pos_racionalizacao", "taxa_pct", "controle_cita", "controle_pct")},
                "segundos_por_caso_com_as_intervencoes": tri["resumo"]["segundos_por_caso_media"], "segundos_da_inferencia_de_base": tri["resumo"]["segundos_base_mediana"],
                "cruzamento": cruzamento_22,
                "fonte": "resultados_alvo/fase4/trilha.json (resumo, sinais, intervencoes, repeticao, sonda); o cruzamento usa fase4_trilha/qwen2.5_7b/diagnosticos__base.jsonl e trilha_avaliacao.jsonl",
            },
            "corrida_24": {**cruzamento_24, "por_classe": ined["por_classe"], "segundos_mediana": segundos_do_diagnostico,
                           "fonte": "resultados_alvo/fase4/ineditos.json (casos, verbete_certo, por_classe, resumo), fase4_ineditos/ineditos.jsonl e trilha_ineditos.jsonl; a posição vem da busca refeita"},
            "os_72_casos": {**os_72, "minutos_a_mais_dos_disparos": round(os_72["disparos"] * segundos_do_diagnostico / 60, 1),
                            # o melhor cenário de um segundo passe: todos os erros ao alcance consertados e nenhum acerto perdido
                            "p_do_melhor_cenario": [{"verbetes": t["verbetes"], "ganhos": t["erros_ao_alcance"], "perdas": 0, "p": p_pareado_exato(t["erros_ao_alcance"], 0)}
                                                    for t in os_72["teto_de_um_segundo_passe"]],
                            "casos_com_disparo_pct": round(100 * os_72["disparos"] / os_72["casos"], 1),
                            "fonte": "a soma dos cruzamentos das corridas 22 e 24; os minutos são os disparos vezes a mediana de segundos por diagnóstico da corrida 24"},
            "corrida_16_numero_de_verbetes": {
                "por_k": [{k: x[k] for k in ("k", "n", "acertos", "acuracia_balanceada_pct", "segundos_mediana", "tokens_entrada_mediana", "tokens_entrada_max")} for x in cal["por_k"]],
                "par": {k: cal["r8"]["par"][k] for k in ("n_comuns", "b", "c", "p_mcnemar", "rotulos_diferentes")}, "motivo": cal["r8"]["motivo"],
                "fonte": "resultados_alvo/fase4/calibracao.json, por_k e r8 (os mesmos 90 casos com 3 e com 5 verbetes)"},
            "corrida_20_sonda": {"casos": sonda20["casos"], "com_proposta_anterior": com_sonda_anterior, "mudaram_a_proposta": sonda20["mudaram_proposta"],
                                 "mencionam_a_correcao": sonda20["mencionam_correcao"], "fonte": "resultados_alvo/fase4/biblioteca.json, sonda"},
        },
        "ideia_3": {
            "corrida_20": {
                **{k: bibl["resumo"][k] for k in ("casos", "acertos_diagnostico", "propostas", "aceitas", "para_revisao", "recusadas_p5", "recusadas_fase3", "taxa_de_rejeicao_pct", "abstencoes")},
                "aceitas_por_tipo": bibl["lote"]["aceitas_por_tipo"], "filtros": bibl["filtros"], "rejeicoes_do_validador_da_fase_3": bibl["rejeicoes"]["fase3"],
                "rejeicoes_dos_filtros_do_p5": bibl["rejeicoes"]["p5"],
                "reavaliacao": {k: bibl["reavaliacao"][k] for k in ("n", "b", "c", "acerto_base", "acerto_novo", "veredito")},
                "teto_de_tokens_da_proposta": bibl["condicoes"]["teto_proposta"],
                "fonte": "resultados_alvo/fase4/biblioteca.json (resumo, lote, filtros, rejeicoes, reavaliacao, condicoes)",
            },
            "revisao_do_lote": _revisao_do_lote(RES / "fase4_biblioteca" / "revisao_do_lote.md"),
            "forma_de_instrucao": _forma_de_instrucao_na_corrida_20(),
            "portao_da_busca_no_lote": portao,
            "custo_dos_portoes": {
                "segundos_por_diagnostico": segundos_do_diagnostico,
                "diagnosticos_do_portao_por_edicao": portao["casos_que_leriam_a_edicao_soma"],
                "horas_do_portao_por_edicao": round(portao["casos_que_leriam_a_edicao_soma"] * segundos_do_diagnostico / 3600, 1),
                "minutos_dos_72_casos": round(72 * segundos_do_diagnostico / 60),
                "fonte": ("os diagnósticos do portão por edição são a soma de `casos_que_leriam_a_edicao` das 20 edições do lote da corrida 20; o tempo usa a mediana de segundos "
                          "por diagnóstico da corrida 24 (ineditos.json, resumo.segundos_mediana)")},
            "cenarios_do_analista": _cenarios_do_analista(med_prop, relatorios, arvores, propostas, prefill, geracao, chars_por_token),
            "promocao": {"mantidas": fechamento["mantidas"], "removidas": len(fechamento["removidas"]), "politica": fechamento["politica"], "hash": fechamento["hash"],
                         "verbetes": fechamento["n_verbetes"], "verbetes_novos": fechamento["n_verbetes_novos"], "notas": fechamento["n_notas"], "retificacoes": fechamento["n_retificacoes"],
                         "aprendidos_em_espera": len(fechamento.get("aprendidos_em_espera") or []), "fonte": "Programacao/AgenteCore/biblioteca_producao/fechamento.json"},
            "curadoria_da_fase_3": {"edicoes_na_epoca": curadoria["edicoes_na_epoca"], "mantidas": curadoria["mantidas"], "removidas": len(curadoria["removidas"]),
                                    "fonte": "Programacao/AgenteCore/biblioteca_producao/curadoria.json (a cópia curada da biblioteca da Fase 3, 29/09/2026)"},
            "notas_do_modelo": {**{k: previa["biblioteca"][k] for k in ("verbetes_producao", "verbetes_com_notas", "notas_retiradas", "notas_em_forma_de_instrucao", "verbetes_retirados",
                                                                         "tokens_estimados_producao", "tokens_estimados_sem_notas")},
                                "contextos_que_mudam": previa["resumo"]["contextos_que_mudam"], "casos": previa["resumo"]["casos"], "com_aprendido_na_referencia": previa["resumo"]["com_aprendido_na_referencia"],
                                "fonte": "resultados_alvo/fase4/sem_notas_previa.json, biblioteca e resumo (a prévia sem modelo da corrida 25)"},
            "custo_da_proposta": {
                "inferencias": len(propostas), "proposta": med_prop, "diagnostico": med_diag,
                "segundos_sem_reaproveitar_o_prompt": round(med_prop["tokens_entrada"] / prefill + med_prop["tokens_saida"] / geracao, 1),
                "reavaliacao_do_lote": {"inferencias": len(reavaliacao), "segundos_mediana": mediana([r.get("segundos") for r in reavaliacao]),
                                        "minutos_no_total": round(sum(r.get("segundos") or 0 for r in reavaliacao) / 60, 1)},
                "fonte": ("resultados_alvo/fase4_biblioteca/qwen2.5_7b/propostas__E101.jsonl, diagnosticos__L100.jsonl e reavaliacao__E101.jsonl (medianas); "
                          "`segundos_sem_reaproveitar_o_prompt` é a conta com as taxas da máquina para o mesmo tamanho de entrada e de saída lido do zero"),
            },
            "o_que_o_analista_leria": {
                "relatorio_v3": {**relatorios, "tokens_estimados": em_tokens(relatorios["chars_mediana"]), "segundos_de_leitura": segundos_de_leitura(em_tokens(relatorios["chars_mediana"]))},
                "arvore_de_decisao": {**arvores, "tokens_estimados": em_tokens(arvores["chars_mediana"]), "segundos_de_leitura": segundos_de_leitura(em_tokens(arvores["chars_mediana"]))},
                "fonte": "resultados_alvo/fase4_ineditos/relatorios_v3/*.md e arvores/*.md (mediana de caracteres), divididos por chars_por_token e pela taxa de prefill",
            },
            "revisao_humana_v3": {k: rev["resumo"][k] for k in ("relatorios", "adesao_apropriada", "adesao_pct", "erros_na_corrida", "erros_localizados", "utilidade_mediana")}
            | {"certos_recusados": certos_recusados,
               "errados_recusados": next(g["recusou"] for g in rev["adesao"] if g["grupo"] == "diagnóstico errado")}
            | decisao_e_fonte
            | {"fonte": ("resultados_alvo/fase4/leitura_revisao_v3.json, resumo e adesao (a sessão de revisão da corrida 24, com um analista de QA); o cruzamento com a FONTE "
                         "divergente usa `casos` do mesmo arquivo (a decisão por relatório) e o nó de diagnóstico de fase4_ineditos/trilha_ineditos.jsonl (o gatilho e a falha gravada)")},
            "filtros_em_codigo": _filtros_em_codigo(),
            "corrida_25": ({"rodou": True, "resumo": _json(corrida_25).get("resumo"), "fonte": "resultados_alvo/fase4/sem_notas.json, resumo"} if corrida_25.exists()
                           else {"rodou": False, "fonte": "resultados_alvo/fase4/sem_notas.json ainda não existe: a corrida 25 espera o Eric"}),
        },
    }


def somar_cruzamentos(cruzamentos: list[dict]) -> dict:
    """A soma de dois ou mais cruzamentos (as corridas 22 e 24 juntas): casos, erros, o que os dois gatilhos pegam e o teto do segundo passe."""
    algum = [c["gatilhos"][-1] for c in cruzamentos]
    # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) a soma leva também os disparos da FONTE divergente e a separação deles pela falha gravada.
    # ! Motivo: a ficha 66 e o veredito da ideia 2 descrevem o segundo sinal pelos casos das duas corridas juntas; o total por falha sai daqui, e não de uma soma de cabeça.
    linhas = [x for c in cruzamentos for x in c.get("fonte_divergente_por_falha") or []]
    por_falha = [{"falha": f, **{k: sum(x[k] for x in linhas if x["falha"] == f) for k in ("casos", "acertos", "erros")}} for f in sorted({x["falha"] for x in linhas})]
    return {"disparos_da_fonte_divergente": sum(c["gatilhos"][1]["disparos"] for c in cruzamentos), "fonte_divergente_por_falha": por_falha,
            **_soma_basica(cruzamentos, algum)}


def _soma_basica(cruzamentos: list[dict], algum: list[dict]) -> dict:
    """As contas que `somar_cruzamentos` já fazia antes da separação pela falha: casos, erros, o que os dois gatilhos juntos pegam e o teto do segundo passe."""
    return {"casos": sum(c["casos"] for c in cruzamentos), "erros": sum(c["erros"] for c in cruzamentos),
            "erros_sem_o_verbete_certo": sum(c["erros_sem_o_verbete_certo"] for c in cruzamentos),
            "disparos": sum(g["disparos"] for g in algum), "erros_pegos": sum(g["erros_pegos"] for g in algum),
            "acertos_incomodados": sum(g["acertos_incomodados"] for g in algum), "erros_perdidos": sum(g["erros_perdidos"] for g in algum),
            "teto_de_um_segundo_passe": [{"verbetes": n, "erros_ao_alcance": sum(t["erros_ao_alcance"] for c in cruzamentos for t in c["teto_de_um_segundo_passe"] if t["verbetes"] == n)}
                                         for n in VERBETES_DO_SEGUNDO_PASSE]}


def _cenarios_do_analista(med_prop: dict, relatorios: dict, arvores: dict, propostas: list[dict], prefill: float, geracao: float, chars_por_token: float) -> dict:
    """Quanto custaria, nesta máquina, uma chamada do analista de documentação conforme o que ele recebe para ler. As entradas são medidas (a proposta de hoje, o
    relatório v3, a árvore de decisão, um verbete e o bloco de instruções) ou o orçamento declarado da ficha curta; a conta é tokens lidos pela taxa de leitura mais
    tokens escritos pela taxa de escrita."""
    sys.path.insert(0, str(EXP))
    import biblioteca as bib
    import diagnostico_ao_vivo as dv
    import estrategias
    verbete = round(mediana([len(bib.render(v)) for v in bib.carregar(dv.PASTA_CURADA)]) / chars_por_token)
    instrucoes = round(len(estrategias._FORMATO_PROPOSTA) / chars_por_token)
    por_proposta = round(mediana([r["tokens_saida"] / r["n_propostas"] for r in propostas if r.get("n_propostas") and r.get("tokens_saida")]))

    def custo(entrada: float, saida: float) -> float:
        return round(entrada / prefill + saida / geracao, 1)

    def cenario(nome: str, leitura: float, saida: float) -> dict:
        entrada = round(leitura + verbete + instrucoes)
        return {"cenario": nome, "tokens_lidos": entrada, "tokens_escritos": saida, "segundos": custo(entrada, saida), "minutos": round(custo(entrada, saida) / 60, 1)}

    cenarios = [cenario("relatório v3 inteiro", relatorios["tokens_estimados"], por_proposta), cenario("árvore de decisão", arvores["tokens_estimados"], por_proposta),
                cenario("ficha curta do caso", FICHA_DO_CASO_TOKENS, por_proposta)]
    return {"verbete_tokens": verbete, "instrucoes_tokens": instrucoes, "tokens_por_proposta": por_proposta, "ficha_curta_tokens": FICHA_DO_CASO_TOKENS,
            "medido_hoje": {"tokens_lidos": med_prop["tokens_entrada"], "tokens_escritos": med_prop["tokens_saida"], "segundos": med_prop["segundos"], "minutos": round(med_prop["segundos"] / 60, 1)},
            "cenarios": cenarios,
            "experimento_em_texto": {"inferencias": len(propostas), "minutos_com_a_ficha_curta": round(len(propostas) * cenarios[-1]["segundos"] / 60),
                                     "minutos_como_a_proposta_de_hoje": round(len(propostas) * med_prop["segundos"] / 60)},
            "fonte": ("a entrada de cada cenário é o texto do caso (relatorios_v3/*.md e arvores/*.md da corrida 24, ou o orçamento declarado da ficha curta) mais um verbete "
                      "(mediana de biblioteca.render sobre a biblioteca de produção) e o bloco de instruções (estrategias._FORMATO_PROPOSTA), em tokens estimados por "
                      "chars_por_token; a saída é uma proposta (mediana de tokens_saida por proposta em propostas__E101.jsonl); a conta usa as taxas de `maquina`")}


def _sem_data(d: dict) -> dict:
    return {k: v for k, v in d.items() if k != "gerado_em"}


def check() -> int:
    if not SAIDA.exists():
        print("--check: medidas_do_repositorio.json ainda não foi gravado")
        return 1
    gravado = _json(SAIDA)
    if _sem_data(montar(gravado.get("gerado_em"))) == _sem_data(gravado):
        print("--check: medidas_do_repositorio.json idêntico ao regerado")
        return 0
    print("--check: medidas_do_repositorio.json DIFERE do regerado (um arquivo de origem mudou; regere com o script)")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    dado = montar()
    DADOS.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(dado, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for numero in ("22", "24"):
        c = dado["ideia_2"][f"corrida_{numero}"]
        c = c.get("cruzamento", c)
        print(f"corrida {numero}: {c['erros']} erros em {c['casos']} casos; sem o verbete certo entre os três: {c['erros_sem_o_verbete_certo']}; "
              f"busca refeita igual em {c['busca_refeita_igual']} de {c['casos']}")
    print(f"gravado: {SAIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
