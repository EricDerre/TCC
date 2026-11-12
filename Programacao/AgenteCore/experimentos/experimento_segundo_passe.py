#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (10/11/2026, ficha 66 opção b, decisão 120) com a corrida 26, um experimento em texto que não muda o agente: só nos casos
# das corridas 22 (os 36 oficiais de avaliação) e 24 (os 36 inéditos da ficha 27) em que um sinal em código acendeu na primeira resposta (o selo baixo, que é a
# etiqueta de confiança baixa pela probabilidade da causa respondida, ou a FONTE divergente, que acende quando o modelo cita um verbete fora dos três entregues ou quando
# nenhum dos três trata da causa respondida), o agente recebe um segundo pedido de diagnóstico, uma única vez: o mesmo prompt congelado, o mesmo modelo e os três
# verbetes seguintes da mesma busca (as posições 4 a 6) no lugar dos três primeiros. A primeira resposta de cada caso é a que a corrida de referência gravou e não é
# repetida. Traz a seleção dos casos (`casos_com_sinal`), os verbetes seguintes (`seguintes`), a regra de escolha entre as duas respostas (`escolher`), a prévia sem
# modelo (`previa`), a corrida (`rodar`, modo `segundo_passe` de executar_fase4.py) e a leitura (`resumir` e `render`, por avaliar_fase4.py --segundo_passe).
# ! Motivo: a pesquisa da ficha 64 (levantamento §6.16.4 e §6.16.5) concluiu que pedir ao modelo que reveja a própria resposta com o mesmo contexto troca mais resposta
# certa por errada, e que a forma com apoio é outra: disparo por sinal em código, uma volta só, contexto novo que sai do código e escolha por regra em código. O Eric
# escolheu medir essa forma antes da Fase 5, sem tocar no agente. Por isso o código é novo: o prompt (`estrategias.py`), a busca (`recuperacao.py`), a biblioteca de
# produção e o diagnóstico (`diagnostico_ao_vivo.py`) entram só para leitura; os verbetes seguintes chegam ao diagnóstico do agente pelo parâmetro `extras`, que já
# existe, com k = 0. O que a decisão deixava em aberto foi fechado antes do código, com a prévia sem modelo: (1) o segundo pedido leva só os verbetes seguintes, porque
# juntar os três primeiros repete o contexto da primeira resposta e passa do limite de tokens do prompt que as corridas da tela usam em quase todos os casos; (2) entram
# três verbetes, o mesmo k do primeiro pedido e da calibração do selo; com dois o alcance é o mesmo, mas o k sairia do calibrado; (3) a regra de escolha deixa a primeira
# resposta, salvo quando a segunda dá outra causa da lista, não acende nenhum dos dois sinais e tem probabilidade maior. A regra de escolha e a do veredito ficam
# escritas aqui e testadas antes de a corrida rodar, para o resultado não escolher a régua.
"""Corrida 26: o segundo passe do diagnóstico, só nos casos com sinal das corridas 22 e 24, com os verbetes seguintes da mesma busca. Em texto, sem navegador.

Uso (em Programacao/AgenteCore/experimentos, com RESULTADOS_DIR=resultados_alvo):
  python experimento_segundo_passe.py --previa [--check]   a prévia sem modelo: os casos com sinal, o que o segundo pedido alcança e o tamanho do prompt
                                                           (resultados_alvo/fase4/segundo_passe_previa.{json,md})
A corrida roda por rodar_fase4.ps1 -Modo segundo_passe -Saida fase4_segundo_passe (a fila rodar_fila_pre_fase5.ps1 roda a ponte da versão do Ollama e a corrida 25
antes) e a leitura por avaliar_fase4.py --segundo_passe --saida fase4_segundo_passe.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import biblioteca as bib
import caminhos
import corridas_em_texto as ct
import diagnostico_ao_vivo as dv
import estrategias
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import executar_fase3b as e3b
import experimento_sem_notas as esn
import pre_fase4 as pf
import recuperacao as rec
import trilha as tr
from taxonomia import CAUSAS_RAIZ

CORRIDA = 26
NOME, PREFIXO = "segundo_passe", "tb_f4_segpasse_"
NOME_PREVIA = "segundo_passe_previa"
ALFA = 0.05                                   # o corte do teste pareado, fixado antes da corrida (decisão 120; o mesmo da decisão 116)
VERBETES_SEGUINTES = ct.K_DO_EXPERIMENTO      # 3: o segundo pedido entrega o mesmo número de verbetes do primeiro (regra R8, k = 3)
BANCOS = esn.BANCOS
NOME_DO_BANCO = esn.NOME_DO_BANCO
# Onde está o nó de diagnóstico da primeira resposta de cada banco: na corrida 22 o nó que vale é o da inferência de base, cuja trilha termina em "@base".
TRILHAS = {"avaliacao": {"arquivo": "trilha_avaliacao.jsonl", "sufixo": "@base"}, "ineditos": {"arquivo": "trilha_ineditos.jsonl", "sufixo": ""}}
GRUPOS_DE_SINAL = ("só o selo baixo", "só a FONTE divergente", "os dois sinais")
# Onde está o verbete da causa certa: entre os três que o primeiro pedido entregou, entre os que o segundo entrega, ou em nenhum dos dois.
ALCANCES = ("entre os três do primeiro pedido", "entre os seguintes", "fora dos dois pedidos")
EFEITOS = ("consertaria", "estragaria", "continua certo", "continua errado")
# Os motivos da regra de escolha, na ordem em que ela confere; só o último troca a resposta.
MOTIVOS = ("a segunda resposta não traz uma causa da lista",
           "as duas respostas dão a mesma causa",
           "a segunda resposta cai no selo baixo",
           "a segunda resposta acende a FONTE divergente",
           "a probabilidade da segunda não passa a da primeira",
           "a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior")
ARQ_DO_LIMITE = "prompt_tela_blocos.json"     # resultados_alvo/fase4: o limite de tokens do prompt na tela (o maior da calibração mais 10%, plano da Fase 4, seção 3.3)


# ------------------------------------------------------------------ as primeiras respostas e os sinais

def sinais_do_no(caminho: Path, sufixo: str) -> dict[str, dict]:
    """caso -> os dois sinais que o agente gravou no nó de diagnóstico da trilha (`selo_baixo` é o gatilho da probabilidade; `fonte_divergente`, o da FONTE) e a falha
    do nó. Com `sufixo`, só as trilhas que terminam nele (a inferência de base da corrida 22); sem ele, as que não têm "@"."""
    saida = {}
    for e in executar_bateria.ler_jsonl(caminho):
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
        g = d.get("gatilhos") or {}
        saida[nome] = {"selo_baixo": bool(g.get("probabilidade")), "fonte_divergente": bool(g.get("fonte_divergente")), "falha": d.get("falha")}
    return saida


def primeiras_respostas(modelo: str = dv.MODELO_PADRAO) -> dict[str, dict]:
    """A primeira resposta de cada caso, lida das corridas de referência (a 22 nos oficiais, a 24 nos inéditos): o registro do diagnóstico, a linha com a
    probabilidade e o selo, e os dois sinais que o agente gravou. Nada é recalculado, e nenhuma primeira resposta é repetida."""
    refs = esn.referencias(modelo)
    saida = {}
    for banco in BANCOS:
        conf = esn.REFERENCIAS[banco]
        nos = sinais_do_no(caminhos.fase3(conf["saida"])["raiz"] / TRILHAS[banco]["arquivo"], TRILHAS[banco]["sufixo"])
        linhas = {l["caso"]: l for l in refs[banco]["linhas"]}
        casos = {}
        for r in refs[banco]["registros"]:
            cid = r["caso"]
            if cid not in nos or cid not in linhas:
                raise SystemExit(f"corrida {conf['corrida']}: o caso {cid} tem registro, mas falta a linha de resumo ou o nó de diagnóstico na trilha de {conf['saida']}")
            casos[cid] = {"registro": r, "linha": linhas[cid], "sinais": {k: nos[cid][k] for k in ("selo_baixo", "fonte_divergente")}, "falha": nos[cid]["falha"]}
        saida[banco] = {"corrida": conf["corrida"], "casos": casos}
    return saida


def grupo_do_sinal(sinais: dict) -> str | None:
    """Em que grupo o caso cai pelos sinais da primeira resposta; None quando nenhum acendeu (o caso não tem segundo passe)."""
    selo, fonte = bool(sinais.get("selo_baixo")), bool(sinais.get("fonte_divergente"))
    if selo and fonte:
        return GRUPOS_DE_SINAL[2]
    if selo:
        return GRUPOS_DE_SINAL[0]
    return GRUPOS_DE_SINAL[1] if fonte else None


def casos_com_sinal(limite: int = 0, primeiras: dict | None = None) -> list[tuple[str, dict, dict]]:
    """(banco, caso, primeira resposta) dos casos em que um sinal acendeu, na ordem da corrida: os oficiais e depois os inéditos; com `limite`, os N primeiros de cada
    banco (fumaça). O caso vem inteiro do banco de casos; quem chama tira o gabarito antes de entregá-lo ao agente."""
    primeiras = primeiras or primeiras_respostas()
    saida = []
    for banco, casos in esn.casos_por_banco().items():
        do_banco = [(banco, c, primeiras[banco]["casos"][c["id"]]) for c in casos
                    if c["id"] in primeiras[banco]["casos"] and grupo_do_sinal(primeiras[banco]["casos"][c["id"]]["sinais"])]
        saida += do_banco[:limite] if limite else do_banco
    return saida


# ------------------------------------------------------------------ o segundo pedido

def seguintes(indice: rec.Indice, caso: dict, gravados: list[str], n: int = VERBETES_SEGUINTES) -> list[dict]:
    """Os `n` verbetes seguintes da mesma busca: os que a busca do agente põe logo abaixo dos que o primeiro pedido entregou. Para a corrida (SystemExit) se a busca
    de agora não devolver, na mesma ordem, os verbetes que a corrida de referência gravou: aí os seguintes não seriam os da mesma busca."""
    ordem = [v for _, v in rec.pontuar(indice, dv.caso_da_busca(caso))]
    k = len(gravados)
    agora = [v["id"] for v in ordem[:k]]
    if agora != list(gravados):
        raise SystemExit(f"caso {caso['id']}: a busca de agora devolve {agora} e a corrida de referência gravou {list(gravados)}; os verbetes seguintes não seriam os da "
                         "mesma busca (a biblioteca de produção mudou depois da corrida?)")
    return ordem[k:k + n]


def prompt_do_segundo_passe(verbetes: list[dict], indice: rec.Indice, caso: dict, prox: list[dict]) -> tuple[dict, str]:
    """O contexto e o prompt do segundo pedido: o prompt congelado do diagnóstico com os verbetes seguintes no lugar dos que a busca entregaria. Entram pelo parâmetro
    `extras` de `diagnostico_ao_vivo.montar_prompt` com k = 0, que é como `diagnostico_ao_vivo.diagnosticar` os recebe na corrida."""
    return dv.montar_prompt(verbetes, indice, caso, 0, extras=prox)


def limite_de_tokens() -> tuple[int | None, str | None]:
    """O limite de tokens do prompt que as corridas da tela usam (o maior prompt da calibração mais 10%) e de onde ele vem; (None, None) sem o arquivo."""
    arq = caminhos.RESULTADOS / "fase4" / ARQ_DO_LIMITE
    if not arq.exists():
        return None, None
    limite = json.loads(arq.read_text(encoding="utf-8")).get("limite") or {}
    return limite.get("tokens"), limite.get("origem")


# ------------------------------------------------------------------ a regra de escolha e a regra do veredito

def escolher(primeira: dict, segunda: dict) -> dict:
    """A regra de escolha entre as duas respostas, em código e fixada antes da corrida. Cada resposta traz `rotulo` (a causa lida), `p_rotulo` (a probabilidade do
    primeiro token da causa) e os dois sinais (`selo_baixo`, `fonte_divergente`). Fica a primeira, salvo quando a segunda dá outra causa da lista, não acende nenhum dos
    dois sinais e tem probabilidade maior que a da primeira. Devolve qual fica e o motivo, um de `MOTIVOS`."""
    if not segunda.get("rotulo") or segunda["rotulo"] not in CAUSAS_RAIZ:
        return {"fica": "primeira", "motivo": MOTIVOS[0]}
    if segunda["rotulo"] == primeira.get("rotulo"):
        return {"fica": "primeira", "motivo": MOTIVOS[1]}
    if segunda.get("selo_baixo"):
        return {"fica": "primeira", "motivo": MOTIVOS[2]}
    if segunda.get("fonte_divergente"):
        return {"fica": "primeira", "motivo": MOTIVOS[3]}
    p1, p2 = primeira.get("p_rotulo"), segunda.get("p_rotulo")
    # a primeira sem causa lida não tem probabilidade: conta como a menor possível
    if p2 is None or (p1 is not None and p2 <= p1):
        return {"fica": "primeira", "motivo": MOTIVOS[4]}
    return {"fica": "segunda", "motivo": MOTIVOS[5]}


def texto_da_escolha() -> str:
    return ("A resposta final de cada caso é escolhida por regra em código: fica a primeira resposta, salvo quando a segunda dá outra causa da lista, não acende nenhum dos "
            "dois sinais (não cai no selo baixo, e algum verbete entregue no segundo pedido trata da causa respondida, com a FONTE dentro dos entregues) e tem probabilidade "
            "maior que a da primeira; só então fica a segunda.")


def texto_da_regra() -> str:
    corte = f"{ALFA:.2f}".replace(".", ",")
    return (f"Regra fixada antes da corrida (decisão 120). {texto_da_escolha()} A diferença entre a resposta final e a primeira sai do ruído quando o teste pareado exato "
            f"(McNemar, bilateral) dá p abaixo de {corte}, com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Fora "
            "disso a diferença fica dentro do ruído e o agente não muda; se sair do ruído, mudar o agente é outra decisão.")


def consertos_para_sair_do_ruido() -> int:
    """Quantos erros o segundo passe teria de consertar, sem perder nenhum acerto, para o teste pareado exato passar do corte."""
    b = 1
    while avaliar.mcnemar_exato(b, 0) >= ALFA:
        b += 1
    return b


def _veredito(b: int, c: int, p: float, completo: bool, pareavel: bool | None) -> tuple[bool | None, str]:
    if not completo:
        return None, "sem veredito: a corrida não cobriu todos os casos com sinal"
    if pareavel is None:
        return None, "sem veredito: a versão do Ollama desta corrida não tem ponte registrada, e as primeiras respostas vieram de outra versão"
    if not pareavel:
        return None, "sem veredito: a ponte da versão do Ollama desta corrida não é pareável com a Fase 3, e a comparação com as primeiras respostas não vale"
    if p < ALFA:
        return True, "sai do ruído, a favor do segundo passe" if b > c else "sai do ruído, contra o segundo passe"
    return False, "dentro do ruído"


# ------------------------------------------------------------------ a leitura

def _alcance(gabarito: str, primeiros: list[str], segundos: list[str]) -> str:
    if gabarito in primeiros:
        return ALCANCES[0]
    return ALCANCES[1] if gabarito in segundos else ALCANCES[2]


def _conta(sub: list[dict]) -> dict:
    """As contas de um grupo de casos com segundo passe: o que a segunda resposta sozinha faria e o que a regra de escolha fez."""
    return {"casos": len(sub), "erros_primeira": sum(1 for i in sub if not i["acerto_primeira"]), "acertos_primeira": sum(1 for i in sub if i["acerto_primeira"]),
            "acertos_segunda": sum(1 for i in sub if i["acerto_segunda"]), "mesmo_rotulo": sum(1 for i in sub if i["rotulo_segunda"] == i["rotulo_primeira"]),
            "consertaria": sum(1 for i in sub if i["efeito_da_segunda"] == EFEITOS[0]), "estragaria": sum(1 for i in sub if i["efeito_da_segunda"] == EFEITOS[1]),
            "trocas": sum(1 for i in sub if i["fica"] == "segunda"), "b": sum(1 for i in sub if i["mudou"] == "ganho"), "c": sum(1 for i in sub if i["mudou"] == "perda")}


def resumir(registros: list[dict], linhas: list[dict], casos: dict[str, list[dict]], primeiras: dict, condicoes: dict | None, ponte: dict | None = None,
            corrida: str | None = None, gerado_em: str | None = None) -> dict:
    """O segundo passe contra a primeira resposta de cada caso com sinal: o que a segunda resposta sozinha consertaria e estragaria, o que a regra de escolha troca, o
    teste pareado e a regra do ruído, por sinal, por banco e pelo alcance do verbete da causa certa. O gabarito entra só aqui, pelo id do caso."""
    condicoes = condicoes or {}
    por_id = {c["id"]: (banco, c) for banco, lista in casos.items() for c in lista}
    extras = {l["caso"]: l for l in linhas}
    itens = []
    for r in registros:
        if r["caso"] not in por_id:
            continue
        banco, c = por_id[r["caso"]]
        primeira = (primeiras.get(banco) or {}).get("casos", {}).get(r["caso"])
        if primeira is None:
            continue
        g = c["gabarito"]["causa_raiz"]
        reg1, lin1, x = primeira["registro"], primeira.get("linha") or {}, extras.get(r["caso"], {})
        rot1, rot2 = ct.rotulo_lido(reg1.get("resposta")), ct.rotulo_lido(r.get("resposta"))
        acerto1, acerto2 = rot1 == g, rot2 == g
        # sem a linha de resumo do segundo passe os sinais dele são desconhecidos: contam como acesos, e a regra deixa a primeira
        escolha = escolher({"rotulo": rot1, "p_rotulo": lin1.get("p_rotulo"), **primeira["sinais"]},
                           {"rotulo": rot2, "p_rotulo": x.get("p_rotulo"), "selo_baixo": bool(x.get("selo_baixo", True)), "fonte_divergente": bool(x.get("fonte_divergente", True))})
        rot_final = rot2 if escolha["fica"] == "segunda" else rot1
        acerto_final = rot_final == g
        ids1, ids2 = list(reg1.get("verbetes_ids") or []), list(r.get("verbetes_ids") or [])
        efeito = (EFEITOS[2] if acerto2 else EFEITOS[1]) if acerto1 else (EFEITOS[0] if acerto2 else EFEITOS[3])
        itens.append({"caso": r["caso"], "banco": banco, "classe": c.get("classe"), "nivel": c.get("nivel"), "gabarito": g, "sinal": grupo_do_sinal(primeira["sinais"]),
                      "rotulo_primeira": rot1, "acerto_primeira": acerto1, "p_primeira": lin1.get("p_rotulo"), "selo_primeira": lin1.get("selo"), "verbetes_primeira": ids1,
                      "rotulo_segunda": rot2, "acerto_segunda": acerto2, "p_segunda": x.get("p_rotulo"), "selo_segunda": x.get("selo"),
                      "selo_baixo_segunda": x.get("selo_baixo"), "fonte_divergente_segunda": x.get("fonte_divergente"), "verbetes_segunda": ids2,
                      "alcance": _alcance(g, ids1, ids2), "efeito_da_segunda": efeito, "fica": escolha["fica"], "motivo": escolha["motivo"], "rotulo_final": rot_final,
                      "acerto_final": acerto_final, "mudou": "ganho" if acerto_final and not acerto1 else ("perda" if acerto1 and not acerto_final else ""),
                      "tokens_entrada": r.get("tokens_entrada"), "tokens_entrada_primeira": reg1.get("tokens_entrada"), "segundos": r.get("segundos"),
                      "segundos_primeira": reg1.get("segundos")})

    def acertos_da_primeira(banco: str) -> int:
        do_banco = (primeiras.get(banco) or {}).get("casos", {})
        return sum(1 for c in casos.get(banco, []) if c["id"] in do_banco and ct.rotulo_lido(do_banco[c["id"]]["registro"].get("resposta")) == c["gabarito"]["causa_raiz"])

    def com_sinal(banco: str) -> int:
        do_banco = (primeiras.get(banco) or {}).get("casos", {})
        return sum(1 for c in casos.get(banco, []) if c["id"] in do_banco and grupo_do_sinal(do_banco[c["id"]]["sinais"]))

    total_de_casos = sum(len(v) for v in casos.values())
    previstos = sum(com_sinal(b) for b in casos)
    acertos_primeira = sum(acertos_da_primeira(b) for b in casos)
    completo = len(itens) == previstos and previstos > 0 and not condicoes.get("parcial")
    versao = condicoes.get("versao_ollama")
    versoes_ref = {x["registro"].get("versao_ollama") for b in primeiras.values() for x in b.get("casos", {}).values()}
    mesma_versao = versao is not None and versoes_ref == {versao}
    pareavel = True if mesma_versao else (bool(ponte.get("pareavel")) if ponte else None)
    total = _conta(itens)
    p = avaliar.mcnemar_exato(total["b"], total["c"])
    sai, veredito = _veredito(total["b"], total["c"], p, completo, pareavel)
    limite = condicoes.get("limite_de_tokens")

    def de_maior_probabilidade(i: dict) -> bool:
        return i["rotulo_segunda"] is not None and i["p_segunda"] is not None and (i["p_primeira"] is None or i["p_segunda"] > i["p_primeira"])

    def linha_da_regra(nome: str, fica_a_segunda) -> dict:
        b = sum(1 for i in itens if fica_a_segunda(i) and i["acerto_segunda"] and not i["acerto_primeira"])
        c = sum(1 for i in itens if fica_a_segunda(i) and i["acerto_primeira"] and not i["acerto_segunda"])
        return {"regra": nome, "trocas": sum(1 for i in itens if fica_a_segunda(i) and i["rotulo_segunda"] != i["rotulo_primeira"]), "b": b, "c": c,
                "acertos": acertos_primeira + b - c, "p": avaliar.mcnemar_exato(b, c)}

    por_regra = [linha_da_regra("sempre a primeira (o agente de hoje)", lambda i: False), linha_da_regra("sempre a segunda", lambda i: True),
                 linha_da_regra("a de maior probabilidade, sem olhar os sinais", de_maior_probabilidade),
                 linha_da_regra("a regra fixada antes da corrida", lambda i: i["fica"] == "segunda")]
    # em `por_banco`, `casos` é o banco inteiro e `segundos_passes` são os casos dele que tiveram o segundo pedido
    por_banco = []
    for banco in BANCOS:
        if banco not in primeiras:
            continue
        conta = _conta([i for i in itens if i["banco"] == banco])
        por_banco.append({"banco": banco, "referencia": f"corrida {primeiras[banco]['corrida']}", "casos": len(casos.get(banco, [])), "com_sinal": com_sinal(banco),
                          "segundos_passes": conta["casos"], "acertos_primeira_no_banco": acertos_da_primeira(banco), **{k: v for k, v in conta.items() if k != "casos"}})
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "corrida": corrida, "numero": CORRIDA}, "condicoes": condicoes,
            "regra": {"alfa": ALFA, "texto": texto_da_regra(), "escolha": texto_da_escolha(), "pareavel": pareavel, "mesma_versao_das_referencias": mesma_versao, "ponte": ponte},
            "resumo": {"casos": total_de_casos, "com_sinal": previstos, "segundos_passes": len(itens), "acertos_primeira": acertos_primeira,
                       "acertos_final": acertos_primeira + total["b"] - total["c"], "erros_primeira_com_sinal": total["erros_primeira"],
                       "acertos_primeira_com_sinal": total["acertos_primeira"], "acertos_segunda": total["acertos_segunda"], "mesmo_rotulo": total["mesmo_rotulo"],
                       "consertaria": total["consertaria"], "estragaria": total["estragaria"], "trocas": total["trocas"], "b": total["b"], "c": total["c"],
                       "saldo": total["b"] - total["c"], "p": p, "ganhos": sorted(i["caso"] for i in itens if i["mudou"] == "ganho"),
                       "perdas": sorted(i["caso"] for i in itens if i["mudou"] == "perda"), "completo": completo, "sai_do_ruido": sai, "veredito": veredito,
                       "tokens_entrada_mediana": ct._mediana([i["tokens_entrada"] for i in itens]),
                       "tokens_entrada_mediana_primeira": ct._mediana([i["tokens_entrada_primeira"] for i in itens]),
                       "tokens_entrada_maximo": max((i["tokens_entrada"] for i in itens if isinstance(i["tokens_entrada"], (int, float))), default=None),
                       "limite_de_tokens": limite,
                       "acima_do_limite": sum(1 for i in itens if isinstance(i["tokens_entrada"], (int, float)) and i["tokens_entrada"] > limite) if limite else None,
                       "segundos_mediana": ct._mediana([i["segundos"] for i in itens]), "segundos_mediana_primeira": ct._mediana([i["segundos_primeira"] for i in itens]),
                       "segundos_no_total": round(sum(i["segundos"] or 0 for i in itens), 1)},
            "por_sinal": [{"sinal": g, **_conta([i for i in itens if i["sinal"] == g])} for g in GRUPOS_DE_SINAL],
            "por_banco": por_banco,
            "por_alcance": [{"alcance": a, **_conta([i for i in itens if i["alcance"] == a])} for a in ALCANCES],
            "por_regra": por_regra,
            "motivos": [{"motivo": m, "casos": sum(1 for i in itens if i["motivo"] == m), "troca": m == MOTIVOS[-1]} for m in MOTIVOS],
            "casos": itens}


def _lista(ids: list[str]) -> str:
    return ", ".join(f"`{i}`" for i in ids) or "nenhum"


def _n(v) -> str:
    """O número como vai ao texto: a mediana que é um inteiro sai sem a casa decimal (1277, e não 1277,0); o resto segue o formato das outras leituras."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return ct._n(v)


def _posicoes_em_palavras(posicoes: list[int] | None) -> str:
    posicoes = list(posicoes or [])
    if not posicoes:
        return "n/d"
    return f"posição {posicoes[0]}" if len(posicoes) == 1 else f"posições {posicoes[0]} a {posicoes[-1]}"


def render(dado: dict) -> str:
    r, regra, cond = dado["resumo"], dado["regra"], dado.get("condicoes") or {}
    n, p = _n, ct._p
    ponte = regra.get("ponte")
    if regra.get("mesma_versao_das_referencias"):
        sobre_a_ponte = "A corrida rodou na mesma versão do Ollama das corridas de referência, e a ponte não entra."
    elif ponte:
        sobre_a_ponte = (f"A corrida rodou em outra versão do Ollama que as corridas de referência; a ponte dessa versão (`{ponte.get('corrida')}`) deu b = {n(ponte.get('b'))} e "
                         f"c = {n(ponte.get('c'))} em {n(ponte.get('n'))} casos, {'pareável' if ponte.get('pareavel') else 'não pareável'} com a Fase 3 (limite {n(ponte.get('limite'))}).")
    else:
        sobre_a_ponte = "A corrida rodou em outra versão do Ollama que as corridas de referência, e essa versão não tem ponte registrada."
    posicoes = _posicoes_em_palavras(cond.get("posicoes"))
    sobre_o_limite = (f" {n(r['acima_do_limite'])} dos {n(r['segundos_passes'])} segundos pedidos passaram do limite de {n(r['limite_de_tokens'])} tokens que o plano da Fase 4 fixa "
                      "para o prompt na tela.") if r.get("limite_de_tokens") else ""
    texto = [(f"Só nos casos das corridas 22 (os oficiais de avaliação) e 24 (os inéditos da ficha 27) em que um sinal em código acendeu na primeira resposta, o selo baixo ou a FONTE "
              f"divergente, o agente recebeu um segundo pedido de diagnóstico, uma única vez: o mesmo prompt congelado, o mesmo modelo e os {n(cond.get('verbetes_seguintes'))} verbetes "
              f"seguintes da mesma busca ({posicoes}) no lugar dos três primeiros. A primeira resposta é a que a corrida de referência gravou e não foi repetida, e o segundo pedido não "
              f"fala dela. São {n(r['com_sinal'])} casos com sinal em {n(r['casos'])} (corrida {CORRIDA}, decisão 120)."),
             "", regra["texto"], "", f"Veredito: {r['veredito']}. {sobre_a_ponte}",
             "", (f"Se a segunda resposta valesse sempre, ela consertaria {n(r['consertaria'])} dos {n(r['erros_primeira_com_sinal'])} erros com sinal e estragaria {n(r['estragaria'])} dos "
                  f"{n(r['acertos_primeira_com_sinal'])} acertos com sinal; a causa respondida foi a mesma em {n(r['mesmo_rotulo'])} casos. Pela regra de escolha, a resposta trocou em "
                  f"{n(r['trocas'])} casos: {n(r['b'])} passaram a acertar e {n(r['c'])} passaram a errar, e o agente iria de {n(r['acertos_primeira'])} a {n(r['acertos_final'])} acertos em "
                  f"{n(r['casos'])}. O segundo pedido teve mediana de {n(r['tokens_entrada_mediana'])} tokens de entrada, contra {n(r['tokens_entrada_mediana_primeira'])} do primeiro nos "
                  f"mesmos casos, e de {n(r['segundos_mediana'])} s por caso.{sobre_o_limite}")]

    def linha_do_grupo(nome: str, x: dict) -> list[str]:
        return [nome, n(x["casos"]), n(x["erros_primeira"]), n(x["acertos_primeira"]), n(x["consertaria"]), n(x["estragaria"]), n(x["mesmo_rotulo"]), n(x["trocas"]), n(x["b"]), n(x["c"])]

    cab_grupo = ["Casos com segundo passe", "Erros na primeira resposta", "Acertos na primeira resposta", "A segunda consertaria", "A segunda estragaria", "Mesma causa nas duas",
                 "Trocas pela regra", "Passaram a acertar (b)", "Passaram a errar (c)"]
    blocos = [
        a3b.tab(f"{PREFIXO}resumo", ["Casos", "Com sinal", "Segundos passes feitos", "Acertos da primeira resposta", "Acertos da resposta final", "A segunda consertaria",
                                    "A segunda estragaria", "Mesma causa nas duas", "Trocas pela regra", "Passaram a acertar (b)", "Passaram a errar (c)", "Saldo", "p do teste pareado",
                                    "Tokens de entrada (mediana) no segundo pedido", "Tokens de entrada (mediana) no primeiro", "Acima do limite de tokens", "Segundos (mediana) no segundo pedido",
                                    "Veredito"],
                [[n(r["casos"]), n(r["com_sinal"]), n(r["segundos_passes"]), n(r["acertos_primeira"]), n(r["acertos_final"]), n(r["consertaria"]), n(r["estragaria"]), n(r["mesmo_rotulo"]),
                  n(r["trocas"]), n(r["b"]), n(r["c"]), n(r["saldo"]), p(r["p"]), n(r["tokens_entrada_mediana"]), n(r["tokens_entrada_mediana_primeira"]), n(r["acima_do_limite"]),
                  n(r["segundos_mediana"]), r["veredito"]]]),
        a3b.tab(f"{PREFIXO}sinal", ["Sinal aceso na primeira resposta", *cab_grupo], [linha_do_grupo(x["sinal"], x) for x in dado["por_sinal"]]),
        a3b.tab(f"{PREFIXO}banco", ["Banco", "Primeira resposta", "Casos do banco", "Com sinal", *cab_grupo],
                [[NOME_DO_BANCO.get(x["banco"], x["banco"]), x["referencia"], n(x["casos"]), n(x["com_sinal"]), *linha_do_grupo("", {**x, "casos": x["segundos_passes"]})[1:]]
                 for x in dado["por_banco"]] or [["sem casos"] + [""] * 12]),
        a3b.tab(f"{PREFIXO}alcance", ["Onde está o verbete da causa certa", *cab_grupo], [linha_do_grupo(x["alcance"], x) for x in dado["por_alcance"]]),
        a3b.tab(f"{PREFIXO}regras", ["Se a escolha fosse", "Trocas de causa", "Passariam a acertar (b)", "Passariam a errar (c)", "Acertos nos casos todos", "p do teste pareado"],
                [[x["regra"], n(x["trocas"]), n(x["b"]), n(x["c"]), n(x["acertos"]), p(x["p"])] for x in dado["por_regra"]]),
        a3b.tab(f"{PREFIXO}motivos", ["O que a regra de escolha achou", "Casos", "Fica"], [[x["motivo"], n(x["casos"]), "a segunda" if x["troca"] else "a primeira"] for x in dado["motivos"]]),
        a3b.tab(f"{PREFIXO}casos", ["Caso", "Banco", "Sinal", "Gabarito", "Primeira resposta", "Certa", "Probabilidade", "Segunda resposta", "Certa", "Probabilidade", "Selo da segunda",
                                   "FONTE divergente na segunda", "A segunda sozinha", "Fica", "Motivo", "Mudou", "Verbete da causa certa", "Verbetes do segundo pedido",
                                   "Tokens de entrada do segundo pedido"],
                [[f"`{i['caso']}`", i["banco"], n(i["sinal"]), f"`{i['gabarito']}`", f"`{i['rotulo_primeira']}`", "sim" if i["acerto_primeira"] else "não", p(i["p_primeira"]),
                  f"`{i['rotulo_segunda']}`", "sim" if i["acerto_segunda"] else "não", p(i["p_segunda"]), n(i["selo_segunda"]),
                  "n/d" if i["fonte_divergente_segunda"] is None else ("sim" if i["fonte_divergente_segunda"] else "não"), i["efeito_da_segunda"], f"a {i['fica']}", i["motivo"],
                  i["mudou"], i["alcance"], _lista(i["verbetes_segunda"]), n(i["tokens_entrada"])] for i in dado["casos"]] or [["nenhum"] + [""] * 18]),
    ]
    cab = pf.cabecalho(f"O segundo passe do diagnóstico, só nos casos com sinal (corrida {CORRIDA})", "avaliar_fase4.py --segundo_passe", f"`{dado['metadados'].get('corrida')}`",
                       dado["metadados"]["gerado_em"][:10])
    return "\n".join(cab + [""] + texto + [""] + blocos) + "\n"


def ler(saida: str, modelo: str = dv.MODELO_PADRAO) -> dict:
    """Tudo o que a leitura precisa: os registros e as linhas do segundo passe, os casos com o gabarito, as primeiras respostas e a ponte da versão em que a corrida rodou."""
    import executar_fase4 as ex
    raiz, slug = caminhos.fase3(saida)["raiz"], executar_fase3._slug(modelo)
    arq_cond = raiz / "condicoes_fase4.json"
    condicoes = json.loads(arq_cond.read_text(encoding="utf-8")) if arq_cond.exists() else {}
    versao = condicoes.get("versao_ollama")
    return {"registros": executar_bateria.ler_jsonl(raiz / slug / f"diagnosticos__{NOME}.jsonl"), "linhas": executar_bateria.ler_jsonl(raiz / f"{NOME}.jsonl"),
            "casos_por_banco": esn.casos_por_banco(), "primeiras": primeiras_respostas(modelo), "condicoes": condicoes,
            "ponte": ex.ultima_ponte(ex.carregar_pontes(gravar=False), versao) if versao else None}


# ------------------------------------------------------------------ a prévia sem modelo

# Os desenhos do segundo pedido que a prévia mede lado a lado: quantos verbetes seguintes entram e se os três primeiros voltam. Só um é o da corrida.
_DESENHOS = (
    {"desenho": "2 seguintes (posições 4 e 5), no lugar dos três primeiros", "seguintes": 2, "com_os_primeiros": False,
     "motivo": "descartado: alcança os mesmos erros com um prompt menor, mas o pedido sai do k = 3 em que o selo foi calibrado"},
    {"desenho": "3 seguintes (posições 4 a 6), no lugar dos três primeiros", "seguintes": 3, "com_os_primeiros": False,
     "motivo": "escolhido: contexto novo, com o mesmo k = 3 do primeiro pedido e da calibração do selo"},
    {"desenho": "os três primeiros mais 2 seguintes (5 verbetes)", "seguintes": 2, "com_os_primeiros": True,
     "motivo": "descartado: repete o contexto da primeira resposta e passa do limite de tokens; a corrida 16 já mediu 5 verbetes para todos os casos (5 ganhos, 8 perdas)"},
    {"desenho": "os três primeiros mais 3 seguintes (6 verbetes)", "seguintes": 3, "com_os_primeiros": True,
     "motivo": "descartado: repete o contexto da primeira resposta e passa do limite de tokens em todos os casos"},
    {"desenho": "7 seguintes (posições 4 a 10), no lugar dos três primeiros", "seguintes": 7, "com_os_primeiros": False,
     "motivo": "descartado: alcança mais erros, mas o prompt quase dobra e fica fora do tamanho em que o selo foi calibrado"},
)


def previa(gerado_em: str | None = None) -> dict:
    """Sem modelo: quais casos têm segundo passe, que verbetes o segundo pedido entrega, em quantos erros o verbete da causa certa fica ao alcance, quantos acertos
    perdem o verbete da causa certa e quanto mede o prompt contra o limite da tela. A busca e a montagem do prompt são código, então dá para saber antes da corrida o
    que ela consegue enxergar; a conta do teto diz se o teste pareado teria como passar do corte."""
    import executar_fase4 as ex
    verbetes = bib.carregar(dv.PASTA_CURADA)
    indice = rec.Indice(verbetes)
    primeiras = primeiras_respostas()
    casos = esn.casos_por_banco()
    limite, origem_do_limite = limite_de_tokens()
    limiares = dv.carregar_limiares() or {}
    itens, por_desenho = [], {d["desenho"]: {"alcance": 0, "tokens": []} for d in _DESENHOS}
    refeita = contexto_igual = 0
    erros_sem_sinal = erros_no_total = 0
    for banco in BANCOS:
        for c in casos[banco]:
            primeira = primeiras[banco]["casos"].get(c["id"])
            if primeira is None:
                continue
            g = c["gabarito"]["causa_raiz"]
            reg = primeira["registro"]
            acerto = ct.rotulo_lido(reg.get("resposta")) == g
            erros_no_total += not acerto
            grupo = grupo_do_sinal(primeira["sinais"])
            if grupo is None:
                erros_sem_sinal += not acerto
                continue
            caso_f = ex.fixture_sem_gabarito(c)
            ordem = [v for _, v in rec.pontuar(indice, dv.caso_da_busca(caso_f))]
            ids = [v["id"] for v in ordem]
            gravados = list(reg.get("verbetes_ids") or [])
            refeita += ids[:len(gravados)] == gravados
            posicao = ids.index(g) + 1 if g in ids else None
            ctx1, prompt1 = dv.montar_prompt(verbetes, indice, caso_f, len(gravados))
            contexto_igual += executar_fase3._sha12(ctx1["texto"]) == reg.get("contexto_sha256")
            razao = (reg.get("tokens_entrada") or 0) / len(prompt1)
            k = len(gravados)
            for d in _DESENHOS:
                _, prompt_d = dv.montar_prompt(verbetes, indice, caso_f, k if d["com_os_primeiros"] else 0, extras=ordem[k:k + d["seguintes"]])
                por_desenho[d["desenho"]]["tokens"].append(round(len(prompt_d) * razao))
                por_desenho[d["desenho"]]["alcance"] += (not acerto) and posicao is not None and k < posicao <= k + d["seguintes"]
            prox = seguintes(indice, caso_f, gravados) if ids[:k] == gravados else ordem[k:k + VERBETES_SEGUINTES]
            _, prompt2 = prompt_do_segundo_passe(verbetes, indice, caso_f, prox)
            tokens2 = round(len(prompt2) * razao)
            itens.append({"caso": c["id"], "banco": banco, "sinal": grupo, "gabarito": g, "rotulo_primeira": ct.rotulo_lido(reg.get("resposta")), "acerto_primeira": acerto,
                          "p_primeira": (primeira.get("linha") or {}).get("p_rotulo"), "selo_primeira": (primeira.get("linha") or {}).get("selo"),
                          "posicao_do_verbete_certo": posicao, "alcance": _alcance(g, ids[:k], [v["id"] for v in prox]), "primeiros": ids[:k], "seguintes": [v["id"] for v in prox],
                          "posicoes": list(range(k + 1, k + 1 + len(prox))), "tokens_primeira": reg.get("tokens_entrada"), "tokens_estimados": tokens2,
                          "acima_do_limite": bool(limite and tokens2 > limite), "segundos_estimados": round((reg.get("segundos") or 0) * len(prompt2) / len(prompt1), 1)})

    def quantos(condicao) -> int:
        return sum(1 for i in itens if condicao(i))

    erros = [i for i in itens if not i["acerto_primeira"]]
    acertos = [i for i in itens if i["acerto_primeira"]]
    ao_alcance = sum(1 for i in erros if i["alcance"] == ALCANCES[1])
    tokens2 = [i["tokens_estimados"] for i in itens]
    tokens1 = [i["tokens_primeira"] for i in itens]
    ks = sorted({len(i["primeiros"]) for i in itens})
    k_do_primeiro = ks[0] if ks else VERBETES_SEGUINTES
    alternativas = []
    for d in _DESENHOS:
        t = por_desenho[d["desenho"]]["tokens"]
        alternativas.append({"desenho": d["desenho"], "escolhido": d["seguintes"] == VERBETES_SEGUINTES and not d["com_os_primeiros"],
                             "verbetes_no_pedido": d["seguintes"] + (k_do_primeiro if d["com_os_primeiros"] else 0),
                             "erros_ao_alcance": por_desenho[d["desenho"]]["alcance"], "tokens_estimados_mediana": ct._mediana(t), "tokens_estimados_maximo": max(t, default=None),
                             "acima_do_limite": sum(1 for v in t if limite and v > limite), "motivo": d["motivo"]})
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "numero": CORRIDA},
            "desenho": {"verbetes_seguintes": VERBETES_SEGUINTES, "posicoes": list(range(ks[0] + 1, ks[0] + 1 + VERBETES_SEGUINTES)) if ks else [], "k_do_primeiro_pedido": ks[0] if len(ks) == 1 else ks,
                        "limite_de_tokens": limite, "origem_do_limite": origem_do_limite, "biblioteca": evo.hash_biblioteca(dv.PASTA_CURADA),
                        "versao_ollama_das_referencias": sorted({str(x["registro"].get("versao_ollama")) for b in primeiras.values() for x in b["casos"].values()}),
                        "selo_baixo_ate": limiares.get("baixo_ate"), "selo_alto_a_partir_de": limiares.get("alto_a_partir_de"),
                        # os nomes dos grupos e dos alcances, para o painel montar os gráficos sem repetir as listas
                        "grupos_de_sinal": list(GRUPOS_DE_SINAL), "alcances": list(ALCANCES),
                        "tokens_estimados_como": "caracteres do prompt do segundo pedido vezes a razão de tokens por caractere do primeiro pedido do mesmo caso"},
            "resumo": {"casos": sum(len(casos[b]) for b in BANCOS), "com_sinal": len(itens), "so_selo_baixo": quantos(lambda i: i["sinal"] == GRUPOS_DE_SINAL[0]),
                       "so_fonte_divergente": quantos(lambda i: i["sinal"] == GRUPOS_DE_SINAL[1]), "os_dois_sinais": quantos(lambda i: i["sinal"] == GRUPOS_DE_SINAL[2]),
                       "erros": erros_no_total, "erros_com_sinal": len(erros), "erros_sem_sinal": erros_sem_sinal, "acertos_com_sinal": len(acertos),
                       "busca_refeita_igual": refeita, "contexto_do_primeiro_pedido_refeito_igual": contexto_igual,
                       "erros_ao_alcance": ao_alcance, "erros_com_o_verbete_certo_ja_entregue": sum(1 for i in erros if i["alcance"] == ALCANCES[0]),
                       "erros_fora_do_alcance": sum(1 for i in erros if i["alcance"] == ALCANCES[2]),
                       "acertos_que_perdem_o_verbete_certo": sum(1 for i in acertos if i["alcance"] == ALCANCES[0]),
                       "acertos_com_o_verbete_certo_entre_os_seguintes": sum(1 for i in acertos if i["alcance"] == ALCANCES[1]),
                       "acertos_sem_o_verbete_certo_nos_dois": sum(1 for i in acertos if i["alcance"] == ALCANCES[2]),
                       "p_do_melhor_cenario": avaliar.mcnemar_exato(ao_alcance, 0), "consertos_para_sair_do_ruido": consertos_para_sair_do_ruido(),
                       "tokens_mediana_do_primeiro_pedido": ct._mediana(tokens1), "acima_do_limite_no_primeiro_pedido": sum(1 for v in tokens1 if limite and v and v > limite),
                       "tokens_estimados_mediana": ct._mediana(tokens2), "tokens_estimados_maximo": max(tokens2, default=None), "acima_do_limite": quantos(lambda i: i["acima_do_limite"]),
                       "inferencias": len(itens), "minutos_estimados": round(sum(i["segundos_estimados"] for i in itens) / 60)},
            "por_sinal": [{"sinal": g, "casos": quantos(lambda i, g=g: i["sinal"] == g), "erros": sum(1 for i in erros if i["sinal"] == g), "acertos": sum(1 for i in acertos if i["sinal"] == g),
                           "erros_ao_alcance": sum(1 for i in erros if i["sinal"] == g and i["alcance"] == ALCANCES[1]),
                           "acertos_que_perdem_o_verbete_certo": sum(1 for i in acertos if i["sinal"] == g and i["alcance"] == ALCANCES[0])} for g in GRUPOS_DE_SINAL],
            "por_banco": [{"banco": b, "referencia": f"corrida {primeiras[b]['corrida']}", "casos": len(casos[b]), "com_sinal": quantos(lambda i, b=b: i["banco"] == b),
                           "erros_com_sinal": sum(1 for i in erros if i["banco"] == b), "acertos_com_sinal": sum(1 for i in acertos if i["banco"] == b),
                           "erros_ao_alcance": sum(1 for i in erros if i["banco"] == b and i["alcance"] == ALCANCES[1])} for b in BANCOS],
            "alternativas": alternativas, "casos": itens, "regra": texto_da_regra()}


def render_previa(dado: dict) -> str:
    d, r, n, p = dado["desenho"], dado["resumo"], _n, ct._p
    posicoes = _posicoes_em_palavras(d["posicoes"])
    texto = [(f"Sem modelo. Dos {n(r['casos'])} casos das corridas 22 e 24, um sinal em código acendeu na primeira resposta de {n(r['com_sinal'])}: {n(r['so_selo_baixo'])} só com o selo "
              f"baixo, {n(r['so_fonte_divergente'])} só com a FONTE divergente e {n(r['os_dois_sinais'])} com os dois. Neles estão {n(r['erros_com_sinal'])} dos {n(r['erros'])} erros das duas "
              f"corridas e {n(r['acertos_com_sinal'])} acertos; os outros {n(r['erros_sem_sinal'])} erros não acendem sinal e não têm segundo passe. A corrida {CORRIDA} faz um segundo "
              f"pedido por caso com sinal, com os {n(d['verbetes_seguintes'])} verbetes seguintes da mesma busca ({posicoes}) no lugar dos três primeiros. A busca refeita agora devolve os "
              f"três verbetes gravados em {n(r['busca_refeita_igual'])} dos {n(r['com_sinal'])} casos, e o contexto do primeiro pedido se refaz igual em "
              f"{n(r['contexto_do_primeiro_pedido_refeito_igual'])}."),
             "", (f"O que a corrida consegue enxergar. Dos {n(r['erros_com_sinal'])} erros com sinal, o verbete da causa certa fica entre os seguintes em {n(r['erros_ao_alcance'])}; em "
                  f"{n(r['erros_com_o_verbete_certo_ja_entregue'])} ele já estava entre os três do primeiro pedido, e em {n(r['erros_fora_do_alcance'])} fica fora dos dois pedidos. Dos "
                  f"{n(r['acertos_com_sinal'])} acertos com sinal, {n(r['acertos_que_perdem_o_verbete_certo'])} tinham o verbete da causa certa entre os três primeiros e deixam de recebê-lo "
                  f"no segundo pedido. No melhor cenário, com os {n(r['erros_ao_alcance'])} erros ao alcance consertados e nenhum acerto perdido, o teste pareado exato dá p = "
                  f"{p(r['p_do_melhor_cenario'])}; para passar do corte seriam precisos {n(r['consertos_para_sair_do_ruido'])} consertos sem nenhuma perda. O resultado não tem como sair do "
                  "ruído: a corrida serve para contar quantos erros o segundo passe conserta e quantas respostas certas ele estraga."),
             "", (f"O tamanho do prompt. O segundo pedido tem mediana estimada de {n(r['tokens_estimados_mediana'])} tokens (máximo {n(r['tokens_estimados_maximo'])}), contra "
                  f"{n(r['tokens_mediana_do_primeiro_pedido'])} do primeiro nos mesmos casos; {n(r['acima_do_limite'])} dos {n(r['com_sinal'])} passam do limite de {n(d['limite_de_tokens'])} "
                  f"tokens que o plano da Fase 4 fixa para o prompt na tela (no primeiro pedido dos mesmos casos, que é em texto, o número acima do limite era "
                  f"{n(r['acima_do_limite_no_primeiro_pedido'])}). Pelo tempo das corridas de referência, as {n(r['inferencias'])} inferências levam cerca de "
                  f"{n(r['minutos_estimados'])} minutos."),
             "", dado["regra"]]
    blocos = [
        a3b.tab(f"{PREFIXO}previa_resumo", ["Casos", "Com sinal", "Erros com sinal", "Acertos com sinal", "Erros sem sinal", "Erros com o verbete certo entre os seguintes",
                                           "Erros com o verbete certo já entregue", "Erros com o verbete certo fora dos dois pedidos", "Acertos que perdem o verbete certo",
                                           "p do melhor cenário", "Consertos para sair do ruído", "Tokens estimados (mediana)", "Acima do limite de tokens", "Minutos estimados"],
                [[n(r["casos"]), n(r["com_sinal"]), n(r["erros_com_sinal"]), n(r["acertos_com_sinal"]), n(r["erros_sem_sinal"]), n(r["erros_ao_alcance"]),
                  n(r["erros_com_o_verbete_certo_ja_entregue"]), n(r["erros_fora_do_alcance"]), n(r["acertos_que_perdem_o_verbete_certo"]), p(r["p_do_melhor_cenario"]),
                  n(r["consertos_para_sair_do_ruido"]), n(r["tokens_estimados_mediana"]), n(r["acima_do_limite"]), n(r["minutos_estimados"])]]),
        a3b.tab(f"{PREFIXO}previa_sinal", ["Sinal aceso na primeira resposta", "Casos", "Erros", "Acertos", "Erros com o verbete certo entre os seguintes", "Acertos que perdem o verbete certo"],
                [[x["sinal"], n(x["casos"]), n(x["erros"]), n(x["acertos"]), n(x["erros_ao_alcance"]), n(x["acertos_que_perdem_o_verbete_certo"])] for x in dado["por_sinal"]]),
        a3b.tab(f"{PREFIXO}previa_banco", ["Banco", "Primeira resposta", "Casos do banco", "Com sinal", "Erros com sinal", "Acertos com sinal", "Erros com o verbete certo entre os seguintes"],
                [[NOME_DO_BANCO.get(x["banco"], x["banco"]), x["referencia"], n(x["casos"]), n(x["com_sinal"]), n(x["erros_com_sinal"]), n(x["acertos_com_sinal"]), n(x["erros_ao_alcance"])]
                 for x in dado["por_banco"]]),
        a3b.tab(f"{PREFIXO}previa_alternativas", ["Desenho do segundo pedido", "Verbetes no pedido", "Erros com o verbete certo ao alcance", "Tokens estimados (mediana)",
                                                 "Tokens estimados (máximo)", "Acima do limite de tokens", "O que ficou"],
                [[x["desenho"], n(x["verbetes_no_pedido"]), n(x["erros_ao_alcance"]), n(x["tokens_estimados_mediana"]), n(x["tokens_estimados_maximo"]), n(x["acima_do_limite"]), x["motivo"]]
                 for x in dado["alternativas"]]),
        a3b.tab(f"{PREFIXO}previa_casos", ["Caso", "Banco", "Sinal", "Gabarito", "Primeira resposta", "Certa", "Probabilidade", "Posição do verbete da causa certa na busca",
                                          "Verbete da causa certa", "Verbetes do primeiro pedido", "Verbetes do segundo pedido", "Tokens do primeiro pedido", "Tokens estimados do segundo"],
                [[f"`{i['caso']}`", i["banco"], i["sinal"], f"`{i['gabarito']}`", f"`{i['rotulo_primeira']}`", "sim" if i["acerto_primeira"] else "não", p(i["p_primeira"]),
                  n(i["posicao_do_verbete_certo"]), i["alcance"], _lista(i["primeiros"]), _lista(i["seguintes"]), n(i["tokens_primeira"]), n(i["tokens_estimados"])] for i in dado["casos"]]
                or [["nenhum"] + [""] * 12]),
    ]
    cab = pf.cabecalho(f"Prévia sem modelo da corrida {CORRIDA}: o que o segundo passe do diagnóstico alcança", "experimento_segundo_passe.py --previa",
                       "`biblioteca_producao/`, `fase4_trilha` e `fase4_ineditos`", dado["metadados"]["gerado_em"][:10])
    return "\n".join(cab + [""] + texto + [""] + blocos) + "\n"


# ------------------------------------------------------------------ a corrida

def rodar(args: argparse.Namespace) -> int:
    """Corrida 26: um segundo pedido de diagnóstico por caso com sinal das corridas 22 e 24, pelo diagnóstico do agente, com os verbetes seguintes da mesma busca, o
    prompt congelado e os limiares da calibração. Não escreve fora da pasta da corrida e não repete nenhuma primeira resposta. Relançar retoma do caso em que parou."""
    import executar_fase4 as ex
    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = ex._marcador(saida / "fase4.log")
    t0 = time.monotonic()
    inicio = time.strftime("%Y-%m-%dT%H:%M:%S")
    modelo, slug = args.modelo, executar_fase3._slug(args.modelo)
    parcial = bool(args.casos)
    versao, segue = ct._guardas(args, marco)
    if not segue:
        return 2
    try:
        primeiras = primeiras_respostas(modelo)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    faltam = [f"corrida {x['corrida']}" for x in primeiras.values() if not x["casos"]]
    if faltam:
        marco(f"!! faltam os registros das primeiras respostas ({', '.join(faltam)}) em {caminhos.RESULTADOS}")
        return 2
    registros_ref = [x["registro"] for b in primeiras.values() for x in b["casos"].values()]
    ponte = ex.ultima_ponte(ex.carregar_pontes(gravar=False), versao)
    if {r.get("versao_ollama") for r in registros_ref} != {versao}:
        ok, motivo = esn.segue_depois_da_ponte(ponte, parcial)
        marco(("" if ok else "!! ") + motivo)
        if not ok:
            return 2
    limiares = dv.carregar_limiares(Path(args.limiares) if args.limiares else None)
    if limiares is None:
        marco("!! sem limiares.json (regra R7): a regra de escolha precisa do selo da segunda resposta; rode --modo calibracao antes")
        return 2
    ks = {r.get("k") for r in registros_ref} | {limiares.get("k")}
    if ks != {VERBETES_SEGUINTES}:
        marco(f"!! o desenho da corrida supõe k = {VERBETES_SEGUINTES} no primeiro pedido e na calibração, e os registros trazem {sorted(ks, key=str)}")
        return 2
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a biblioteca de produção em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    pasta_bib = saida / "bibliotecas" / slug / f"epoca-{dv.VERSAO_CURADA}"
    try:
        hash_bib = e3b._preparar_copia(dv.PASTA_CURADA, pasta_bib)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    hashes_ref = {r.get("biblioteca_versao") for r in registros_ref}
    if hashes_ref != {hash_bib}:
        marco(f"!! a biblioteca de produção ({hash_bib}) não é a que as primeiras respostas leram ({sorted(hashes_ref, key=str)}); os verbetes seguintes não seriam os da mesma busca")
        return 2
    verbetes = bib.carregar(pasta_bib)
    indice = rec.Indice(verbetes)
    itens = casos_com_sinal(args.casos, primeiras)
    if not itens:
        marco("!! nenhum caso com sinal nas corridas de referência")
        return 2
    caso0 = ex.fixture_sem_gabarito(itens[0][1])
    try:
        ctx0, prompt0 = prompt_do_segundo_passe(verbetes, indice, caso0, seguintes(indice, caso0, itens[0][2]["registro"]["verbetes_ids"]))
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    hash_fixo = dv.hash_prompt_fixo(verbetes, ctx0, caso0, prompt0)
    for r in esn.REFERENCIAS.values():
        arq = caminhos.fase3(r["saida"])["raiz"] / "condicoes_fase4.json"
        fixo_ref = json.loads(arq.read_text(encoding="utf-8")).get("hash_prompt_fixo") if arq.exists() else None
        if fixo_ref and fixo_ref != hash_fixo:
            marco(f"!! a parte fixa do prompt ({hash_fixo}) não é a da corrida {r['corrida']} ({fixo_ref}); a comparação não vale")
            return 2
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    arq_diag, arq_lat, arq_resumo, arq_trilha = pasta_reg / f"diagnosticos__{NOME}.jsonl", pasta_reg / f"logprobs__{NOME}.jsonl", saida / f"{NOME}.jsonl", saida / f"trilha_{NOME}.jsonl"
    try:
        ex._conferir_versao_das_linhas([arq_diag], versao)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    feitos = {r["caso"] for r in executar_bateria.ler_jsonl(arq_resumo)}
    limite, origem_do_limite = limite_de_tokens()
    posicoes = list(range(VERBETES_SEGUINTES + 1, 2 * VERBETES_SEGUINTES + 1))
    condicoes = {"modo": NOME, "corrida": CORRIDA, "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": 0, "verbetes_seguintes": VERBETES_SEGUINTES,
                 "posicoes": posicoes, "limiares": limiares, "casos": len(itens), "casos_por_banco": {b: sum(1 for x, _, _ in itens if x == b) for b in BANCOS}, "parcial": parcial,
                 "top_logprobs": args.top, "teto_tokens": args.teto, "hash_prompt_fixo": hash_fixo, "hash_indice": dv.hash_indice(indice), "limite_de_tokens": limite,
                 "origem_do_limite": origem_do_limite,
                 "biblioteca": {"hash": hash_bib, "origem": "Programacao/AgenteCore/biblioteca_producao"},
                 "primeiras_respostas": {b: {"corrida": r["corrida"], "saida": r["saida"]} for b, r in esn.REFERENCIAS.items()},
                 "como_os_verbetes_entram": ("pelo parâmetro extras de diagnostico_ao_vivo.diagnosticar, com k = 0: no registro oficial o campo k fica 0 e, na trilha, o evento candidatos traz os "
                                             "verbetes do pedido em por_id; as posições deles na busca estão na linha de resumo de cada caso"),
                 "ponte": ponte, "regra": texto_da_regra()}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO {NOME}: Ollama {versao}, {modelo}, biblioteca de produção ({hash_bib}), verbetes das posições {posicoes[0]} a {posicoes[-1]} da busca; {len(itens)} casos com sinal; "
          f"{len(feitos)} já feito(s)")
    digest, versao_ollama = e3b._preparar_modelo(modelo)
    if versao_ollama != versao:
        marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
        return 2
    comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": dv.VERSAO_CURADA + 1, "biblioteca_epoca": dv.VERSAO_CURADA,
             "biblioteca_versao": hash_bib, "particao": None}
    if arq_trilha.exists() and feitos:
        trilha = tr.Trilha.carregar(arq_trilha)
        trilha.pasta_blobs = saida / "blobs"
    else:
        trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
        trilha.corrida(tr.cabecalho_de_corrida(modelo=modelo, versao_ollama=versao, inicio=inicio, quantizacao=dv.quantizacao_do_modelo(modelo), top_logprobs=args.top,
                                               leitura_da_probabilidade=dv.LEITURA_DA_PROBABILIDADE, hash_biblioteca=hash_bib, hash_prompt_fixo=hash_fixo, hash_indice=dv.hash_indice(indice),
                                               corrida=args.saida, etapas_registradas=["recuperacao", "prompt", "diagnostico"],
                                               etapas_nao_registradas=["roteiro", "interceptacao", "poda", "cura", "edicao_biblioteca", "intervencao"],
                                               extras={"modo": NOME, "k": 0, "verbetes_seguintes": VERBETES_SEGUINTES, "posicoes": posicoes, "limiares": limiares,
                                                       "como_os_verbetes_entram": condicoes["como_os_verbetes_entram"]}), ts=inicio)

    def _loop() -> None:
        for n, (banco, caso, primeira) in enumerate(itens, 1):
            if caso["id"] in feitos:
                continue
            caso_f = ex.fixture_sem_gabarito(caso)
            prox = seguintes(indice, caso_f, primeira["registro"]["verbetes_ids"])
            tid = f"{args.saida}/{slug}/{caso['id']}"
            ts = time.strftime("%Y-%m-%dT%H:%M:%S")
            trilha.evento("entrada", tid, {"caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"], "origem": "fixture", "texto": trilha.blob(estrategias._dados_do_caso(caso_f), "caso"),
                                           "segundo_passe": {"sinais_da_primeira": primeira["sinais"], "posicoes": posicoes, "verbetes": [v["id"] for v in prox]}}, "ao_vivo", ts=ts)
            sv = dv.diagnosticar(trilha, tid, caso_f, verbetes, indice, k=0, modelo=modelo, comum=comum, limiares=limiares, intervencoes="desligadas", top=args.top, teto=args.teto, ts=ts,
                                 extras=prox)
            executar_fase3._gravar(arq_diag, sv["registro"])
            executar_fase3._gravar(arq_lat, sv["lateral"])
            confianca = sv["no"]["confianca"]
            executar_fase3._gravar(arq_resumo, {"caso": caso["id"], "banco": banco, "sinais_da_primeira": primeira["sinais"], "posicoes": posicoes, "verbetes_ids": sv["registro"]["verbetes_ids"],
                                                "p_rotulo": confianca.get("p_rotulo"), "selo": confianca.get("selo"), "selo_baixo": bool(sv["gatilhos"]["probabilidade"]),
                                                "fonte_divergente": bool(sv["gatilhos"]["fonte_divergente"]), "falha": sv["no"].get("falha"), "segundos": sv["registro"]["segundos"]})
            trilha.gravar(arq_trilha)
            ex._conferir_versao(versao)
            marco(f"[{n}/{len(itens)}] {banco} {caso['id']}: {sv['no']['escolha']} (p {confianca.get('p_rotulo')}, selo {confianca.get('selo')}, FONTE divergente "
                  f"{'sim' if sv['gatilhos']['fonte_divergente'] else 'não'}; {sv['registro']['segundos']} s)")

    try:
        e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    trilha.fechar(time.strftime("%Y-%m-%dT%H:%M:%S"))
    trilha.gravar(arq_trilha)
    marco(f"FIM {NOME}: {len(itens)} casos com sinal; duração {time.monotonic() - t0:.0f} s; trilha {arq_trilha.stat().st_size} bytes")
    return 0


# ------------------------------------------------------------------ linha de comando

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--previa", action="store_true", help=f"grava a prévia sem modelo em resultados_alvo/fase4/{NOME_PREVIA}.json e .md")
    ap.add_argument("--check", action="store_true", help="com --previa: regera e compara com o gravado, sem gravar")
    args = ap.parse_args(argv)
    if args.previa:
        import avaliar_fase4 as av
        dado = previa()
        return pf.fechar(NOME_PREVIA, dado, render_previa(dado), f"{PREFIXO}previa_", check=args.check, pasta=caminhos.RESULTADOS / "fase4", doc=av.RELATORIO)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
