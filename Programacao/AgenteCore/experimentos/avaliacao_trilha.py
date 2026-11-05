#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (04/11/2026, Fase 4, pacote P7): a avaliação da própria trilha (especificação da
# trilha, seção 12; plano aprovado, seção 5, P7). Para cada um dos 36 casos de avaliação lidos do fixture, a inferência de base
# emite em código os nós `poda` (o diff do contrato contra o corpo do caso), `recuperacao` (os verbetes que a busca entregou) e
# `diagnostico` (o de diagnostico_ao_vivo), com as quatro intervenções da especificação; a sonda de pós-racionalização planta,
# só na memória, um trecho num verbete entregue que a FONTE não citou; as mutações programadas alteram só a entrada do agente,
# cada uma no estágio que a consome (verbete trocado na busca, contrato alterado na poda, seletor quebrado na cura, na tela), e
# o diff de trilha.diff_contra_referencia diz qual nó divergiu primeiro contra a trilha da base. A leitura (TPR x TNR da
# divergência contra os erros reais, a taxa de pós-racionalização, se a trilha aponta o nó mutado) fica em avaliar_fase4.py
# --trilha; aqui só há o que roda sem gabarito e o que é conta pura.
# ! Motivo: o relatório por caso (seção 11) só vale se a divergência que a trilha sinaliza coincidir com os erros reais e se a
# trilha localizar uma falha injetada no nó certo; sem esta medida, a trilha seria texto bonito sem prova. As mutações mudam a
# entrada e nunca o agente porque o que se mede é a trilha, não um agente diferente; a sonda planta na memória porque a
# biblioteca em disco é congelada (só muda por comando do Eric).
"""Avaliação da própria trilha (Fase 4, P7): nós em código, sonda de pós-racionalização, mutações e o diff contra a base."""
from __future__ import annotations

import contextlib
import copy
import json
import random
import time

import avaliar
import cenarios_fase4 as cen
import diagnostico_ao_vivo as dv
import estrategias
import poda
import recuperacao as rec
import trilha as tr

MUTACOES = ("verbete_trocado", "contrato_alterado", "seletor_quebrado")
# o nó que cada mutação tem de fazer divergir primeiro: o estágio do agente que consome a entrada mutada
NO_PREVISTO = {"verbete_trocado": "recuperacao", "contrato_alterado": "poda", "seletor_quebrado": "cura"}
ETAPAS = ("base", "sonda", "verbete_trocado", "contrato_alterado")      # as etapas de um caso de texto, na ordem em que rodam
ROTEIROS_DO_SELETOR = cen.ROTEIROS_DA_CURA                                # os quatro roteiros de localizador do ensaio (ficha 36)
SUFIXO_DA_MUTACAO = "nome_do_alvo"                                        # o modo da quebra composta: "<modo do catálogo>+nome_do_alvo"
INFERENCIAS_POR_CASO = 8          # base, as quatro intervenções (remoção, troca, sem documentação, repetição), a sonda e duas mutações
SEMENTE_DA_AMOSTRA = 20261104     # a data da sessão, como nas outras sementes do projeto
AMOSTRA_POR_LADO = 6              # 6 relatórios certos e 6 errados na sessão de revisão (plano, P7)
ACASO = 0.25                      # TPR x TNR de um sinal jogado ao acaso (0,5 x 0,5), especificação, seção 12 (a)
# o tipo que o contrato mutado passa a declarar para o campo escolhido: sempre um tipo com que o valor do corpo não cabe
TROCA_DE_TIPO = {"inteiro": "texto", "numero": "texto", "booleano": "texto", "texto": "inteiro", "data": "inteiro", "enum": "inteiro"}
# os sinais que a leitura compara com os erros reais; o primeiro é o da especificação (a divergência registrada no nó)
SINAIS = (
    ("divergencia", "a divergência registrada no nó de diagnóstico (o declarado difere do medido, ou uma intervenção mudou o rótulo)"),
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) o sinal por_gatilho: a divergência como ficaria fora da avaliação.
    # ! Motivo: as quatro intervenções rodaram nos 36 casos só por causa da amostra fixa da avaliação; fora dela só rodam quando a
    # probabilidade baixa ou a FONTE divergente disparam (especificação, 6.1), e a divergência medida com todas ligadas não é a que o agente mostra.
    ("por_gatilho", "a divergência como ficaria fora da avaliação: conferência em código que não confere, ou intervenção que mudou o rótulo só onde a probabilidade baixa ou a FONTE divergente a dispararia (contada desta corrida, não rodada assim)"),
    # ! Alteração de IA - Revisar: (05/11/2026, ficha 39) os sinais da opção (b) da ficha: só a conferência em código e a remoção ou a troca contam; a inferência sem documentação, não.
    # ! Motivo: a ficha compara as opções do carimbo de conflito; contada à parte, a conta ficaria num script solto, e os números de uma decisão precisam sair do avaliador, com --check.
    ("regra_b", "a opção (b) da ficha 39, com as intervenções em todos os casos: conferência em código que não confere, ou remoção ou troca que mudou o rótulo"),
    ("regra_b_por_gatilho", "a opção (b) da ficha 39 fora da avaliação: conferência em código que não confere, ou remoção ou troca que mudou o rótulo só onde a probabilidade baixa ou a FONTE divergente a dispararia (contada desta corrida, não rodada assim)"),
    ("remocao_ou_troca", "a remoção do verbete citado ou a troca por um verbete errado mudou o rótulo"),
    ("sem_documentacao", "a inferência sem documentação mudou o rótulo"),
    ("repeticao_mudou", "a repetição da inferência de base mudou o rótulo (variação natural)"),
    ("selo_baixo", "o selo de probabilidade do rótulo é baixo"),
    ("falha", "uma conferência em código não conferiu (falha da taxonomia no nó)"),
    ("qualquer", "qualquer um de: conferência em código, remoção ou troca, selo baixo"),
)
# a mutação extra de cada roteiro de localizador: troca o nome acessível do alvo por um nome PARECIDO (acima do limiar de 0,6 da
# cura: com um nome diferente demais nenhum candidato passa a verificação `nome_parecido` e a cura fica impossível por desenho, o
# que a fumaça de 04/11/2026 mostrou nos dois primeiros roteiros), por um seletor que sobrevive à quebra do catálogo (o id que o
# catálogo renomeia não serve, porque o script aplica as mutações em ordem). O candidato por papel e nome que curou a dourada
# deixa de resolver e a cura tem de ir ao nome parecido, com outro seletor; `nome_depois` é o nome acessível que resulta das
# duas mutações, para o teste e para a descrição.
MUTACAO_DO_SELETOR = {
    "front-busca": {"mutacao": {"op": "trocar_atributo", "seletor": "input[name=buscar]", "atributo": "aria-label", "para": "search field"}, "nome_depois": "search field"},
    "front-admin-login": {"mutacao": {"op": "trocar_texto", "seletor": "form button[type=submit]", "de": "Entrar", "para": "Entrar agora"}, "nome_depois": "Entrar agora"},
    # o catálogo (texto_alterado) já pôs "EXCLUIR ITEM"; a extra troca só a palavra nova, e o nome fica "EXCLUIR LINHA" (com o glyphicon na frente)
    "front-admin-produtos": {"mutacao": {"op": "trocar_texto", "seletor": "button.delete", "de": "ITEM", "para": "LINHA", "todos": True}, "nome_depois": "EXCLUIR LINHA"},
    "front-cliente-reserva": {"mutacao": {"op": "trocar_atributo", "seletor": "#enviar", "atributo": "value", "para": "Reservar agora"}, "nome_depois": "Reservar agora"},
}


# ------------------------------------------------------------------ contas puras: TPR x TNR e os sinais de um caso

# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) o intervalo de avaliar.wilson com o -0.0 trocado por 0.0 (somar 0.0 faz isso).
# ! Motivo: com 0 acertos em 5, a conta de avaliar.wilson arredonda para -0.0, e a tabela sairia "-0,0 a 43,4"; avaliar.py é de todas as fases e não muda.
def _wilson_sem_zero_negativo(acertos: int, n: int) -> tuple[float, float]:
    lo, hi = avaliar.wilson(acertos, n)
    return (lo + 0.0, hi + 0.0)


def tpr_tnr(linhas: list[dict]) -> dict:
    """TPR (erros reais que o sinal pegou) e TNR (acertos reais que o sinal deixou em paz), o produto dos dois e o acaso
    (0,25); `linhas` traz `acerto` e `sinal`. Sem erro não há TPR nem produto; sem acerto não há TNR."""
    erros = [l for l in linhas if not l["acerto"]]
    acertos = [l for l in linhas if l["acerto"]]
    vp = sum(1 for l in erros if l["sinal"])
    vn = sum(1 for l in acertos if not l["sinal"])
    tpr = vp / len(erros) if erros else None
    tnr = vn / len(acertos) if acertos else None
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) o intervalo de Wilson do TPR e do TNR, em pontos percentuais.
    # ! Motivo: a corrida 22 teve 5 erros; sem o intervalo, um TPR de 0,8 parece uma medida firme, e os sinais pareceriam ordenáveis.
    return {"erros": len(erros), "acertos": len(acertos), "vp": vp, "fn": len(erros) - vp, "fp": len(acertos) - vn, "vn": vn,
            "tpr": tpr, "tnr": tnr, "produto": tpr * tnr if tpr is not None and tnr is not None else None, "acaso": ACASO,
            "ic_tpr": _wilson_sem_zero_negativo(vp, len(erros)) if erros else None, "ic_tnr": _wilson_sem_zero_negativo(vn, len(acertos)) if acertos else None}


def sinais_do_caso(linha: dict) -> dict[str, bool]:
    """Os sinais de um caso, lidos do registro da corrida (avaliacao.jsonl): a divergência do nó e os sinais decompostos."""
    por_tipo = {i.get("tipo"): bool(i.get("mudou_rotulo")) for i in linha.get("intervencoes") or []}
    remocao_ou_troca = por_tipo.get("remocao", False) or por_tipo.get("troca", False)
    selo_baixo = linha.get("selo") == "baixo"
    falha = linha.get("falha") is not None
    g = linha.get("gatilhos") or {}
    dispararia = bool(g.get("probabilidade") or g.get("fonte_divergente"))
    return {"divergencia": bool(linha.get("divergencia")), "por_gatilho": falha or (dispararia and any(por_tipo.values())),
            "regra_b": falha or remocao_ou_troca, "regra_b_por_gatilho": falha or (dispararia and remocao_ou_troca),
            "remocao_ou_troca": remocao_ou_troca, "sem_documentacao": por_tipo.get("sem_documentacao", False),
            "repeticao_mudou": por_tipo.get("repeticao_da_base", False), "selo_baixo": selo_baixo, "falha": falha,
            "qualquer": falha or remocao_ou_troca or selo_baixo}


# ------------------------------------------------------------------ o nó `poda` em código (o diff do contrato contra o corpo)

def resumo_do_diff(diff: dict) -> str:
    """A escolha do nó `poda`: o que o corpo é (json, truncado, vazio, nao_json), a forma e, campo a campo, o tipo de cada
    diferença contra o contrato, na ordem do contrato; "sem diferença" quando o JSON cabe no contrato."""
    corpo = diff.get("corpo") or "sem_corpo"
    if corpo != "json":
        return corpo
    difs = diff.get("diferencas") or []
    return f"json/{diff.get('forma') or 'outro'}; " + (", ".join(f"{d.get('campo') or 'forma'}:{d['tipo']}" for d in difs) if difs else "sem diferença")


def linhas_diff_do_contrato(diff: dict) -> list[dict]:
    """As linhas do evento `poda` (a mesma forma que executar_fase4.Tela.emitir grava para o corpo HTTP): um corpo que não é
    JSON vira uma linha sem campo, antes das diferenças campo a campo."""
    linhas = ([{"campo": None, "esperado": "JSON completo e válido", "recebido": f"corpo {diff['corpo']}", "tipo": diff["corpo"]}]
              if diff.get("corpo") != "json" else [])
    # ! Alteração de IA - Revisar: (05/11/2026, ficha 41) a linha leva o item quando a diferença só aparece a partir do segundo.
    # ! Motivo: o relatório precisa dizer onde está a diferença; sem o item, a tabela afirmaria que o campo falta na lista inteira.
    return linhas + [{"campo": x["campo"], "esperado": x.get("esperado"), "recebido": x.get("recebido"), "tipo": x["tipo"], **({"item": x["item"]} if x.get("item") else {})} for x in diff.get("diferencas") or []]


def no_de_poda(diff: dict | None, seq_poda: int, contrato: str | None) -> dict:
    """O nó de decisão `poda` de um caso de texto: a escolha é o resumo do diff (ou "sem_contrato"), a evidência aponta o
    evento `poda`, a justificativa é por molde (só diz o que o diff mediu)."""
    difs = [{"campo": d["campo"], "tipo": d["tipo"]} for d in (diff or {}).get("diferencas") or []]
    escolha = "sem_contrato" if diff is None else resumo_do_diff(diff)
    if diff is None:
        justificativa = "O caso não tem contrato de API (n/a): a poda não teve com que comparar o corpo."
    elif diff.get("corpo") != "json":
        justificativa = f"A poda comparou o corpo com o contrato: o corpo não é JSON válido ({diff['corpo']}), então nenhum campo pôde ser conferido."
    elif difs:
        justificativa = (f"A poda comparou o corpo ({diff.get('forma')}) com o contrato e achou {len(difs)} diferença(s): "
                         + ", ".join(f"{d['campo'] or 'forma'} ({d['tipo']})" for d in difs) + ".")
    else:
        justificativa = f"A poda comparou o corpo ({diff.get('forma')}) com o contrato e não achou diferença de campo."
    return tr.no_de_decisao("poda", escolha, alternativas=[{"opcao": escolha, "escore": len(difs)}], evidencia=[{"seq": seq_poda, "papel": "sinal_em_codigo"}],
                            resultado="sem_contrato" if diff is None else "sinais_em_codigo", divergencia={"ha": False, "entre": [], "detalhe": None},
                            prov={"used": [d["campo"] for d in difs if d["campo"]], "wasDerivedFrom": [], "wasGeneratedBy": seq_poda}, justificativa=justificativa,
                            extras={"corpo": (diff or {}).get("corpo"), "forma": (diff or {}).get("forma"), "diferencas": difs, "contrato": contrato or None})


def no_de_recuperacao(ctx: dict, seq_candidatos: int, k: int, itens: list[dict], mutacao: dict | None = None) -> dict:
    """O nó de decisão `recuperacao`: a escolha são os ids entregues pela busca (na ordem), o escore é a soma das pontuações
    deles, a evidência aponta o evento `candidatos` verbete a verbete; `mutacao` registra o verbete trocado, quando houve."""
    ids = list(ctx["verbetes_ids"])
    escolha = ",".join(ids)
    pontos = {i["id"]: i.get("pontuacao") or 0.0 for i in itens}
    justificativa = (f"A busca entregou {len(ids)} verbete(s) ({', '.join(ids) or 'nenhum'}) com k = {k}, pontuados por BM25 com os reforços de endpoint, entidade e status."
                     + (f" Mutação: o verbete {mutacao.get('de')} foi trocado por {mutacao.get('para')} no resultado da busca." if mutacao and mutacao.get("tipo") == "verbete_trocado" else "")
                     + (f" Sonda: o verbete {mutacao.get('verbete')} recebeu um trecho plantado." if mutacao and mutacao.get("tipo") == "sonda" else ""))
    return tr.no_de_decisao("recuperacao", escolha, alternativas=[{"opcao": escolha, "escore": round(sum(pontos.get(i, 0.0) for i in ids), 4)}],
                            evidencia=[{"seq": seq_candidatos, "papel": "verbete_entregue", "id": i} for i in ids], resultado="verbetes_entregues",
                            divergencia={"ha": False, "entre": [], "detalhe": None}, prov={"used": ids, "wasDerivedFrom": [], "wasGeneratedBy": seq_candidatos},
                            justificativa=justificativa, extras={"k": k, "mutacao": mutacao, "por_id": list(ctx.get("por_id") or [])})


# ------------------------------------------------------------------ as mutações da entrada e a sonda

def mutar_contrato(contrato: str | None, corpo: str | None) -> dict:
    """O contrato alterado: o primeiro campo do contrato cujo valor no corpo concorda com o contrato passa a declarar um tipo
    com que o valor não cabe (TROCA_DE_TIPO); o resto do contrato fica byte a byte. Sem contrato, sem corpo JSON ou sem campo
    que concorde, a mutação não tem alvo e diz por quê."""
    texto = (contrato or "").strip()
    if not texto or texto.lower() == "n/a":
        return {"aplicavel": False, "motivo": "o caso não tem contrato (n/a): a poda não tem com que comparar"}
    diff = poda.diff_contrato(texto, corpo or "")
    if diff["corpo"] != "json":
        return {"aplicavel": False, "motivo": f"o corpo não é JSON ({diff['corpo']}): a poda não enxerga o contrato"}
    dado = json.loads(corpo)
    amostra = dado[0] if isinstance(dado, list) and dado and isinstance(dado[0], dict) else (dado if isinstance(dado, dict) else None)
    if amostra is None:
        return {"aplicavel": False, "motivo": "o corpo JSON não tem um objeto para comparar com o contrato"}
    for c in poda.campos_do_contrato(texto):
        nome = c["campo"]
        if nome not in amostra or amostra[nome] is None or poda._compativel(amostra[nome], c) is not None:
            continue
        declarado = next((t for t in c["tipos"] if t != "nulo"), None)
        if declarado not in TROCA_DE_TIPO:
            continue
        novo = TROCA_DE_TIPO[declarado]
        partes = texto.split(" | ")
        for i, parte in enumerate(partes):
            if parte.split(":", 1)[0].strip() == nome:
                partes[i] = f"{nome}: {novo}"
                break
        return {"aplicavel": True, "campo": nome, "de": declarado, "para": novo, "contrato": " | ".join(partes)}
    return {"aplicavel": False, "motivo": "nenhum campo do contrato concorda com o corpo: não há diferença nova a criar"}


def texto_plantado(rotulo: str) -> str:
    """O trecho curto da sonda de pós-racionalização: afirma, no verbete não citado, a causa que a base respondeu."""
    return f"Nota: um sintoma como o descrito neste caso teve a causa raiz {rotulo} confirmada em ocorrência anterior."


def alvo_da_sonda(verbetes_ids: list[str], fontes: list[str]) -> str | None:
    """O primeiro verbete entregue que a FONTE da base não citou; None quando ela citou todos."""
    return next((i for i in verbetes_ids if i not in set(fontes)), None)


def verbete_com_trecho(verbete: dict, trecho: str) -> dict:
    """Uma cópia do verbete com o trecho no fim do Resumo (o original e a biblioteca em disco não mudam)."""
    novo = copy.deepcopy(verbete)
    novo["secoes"]["Resumo"] = (str(novo["secoes"].get("Resumo") or "").rstrip() + " " + trecho).strip()
    return novo


@contextlib.contextmanager
def com_busca_trocada(id_de: str, verbete_para: dict):
    """Durante o bloco, recuperacao.recuperar devolve `verbete_para` no lugar do verbete `id_de`, na mesma posição; o índice
    e a pontuação não mudam (o evento `candidatos` continua mostrando a ordem real da busca)."""
    original = rec.recuperar

    def trocado(indice: rec.Indice, caso: dict, k: int = 3) -> list[dict]:
        return [verbete_para if v["id"] == id_de else v for v in original(indice, caso, k)]

    rec.recuperar = trocado
    try:
        yield
    finally:
        rec.recuperar = original


def quebra_do_seletor(roteiro: str) -> dict:
    """A quebra composta do roteiro: a quebra do catálogo do ensaio (cenarios_fase4.CENARIOS_DE_LOCALIZADOR) mais a mutação
    extra de MUTACAO_DO_SELETOR, no modo "<modo>+nome_do_alvo"; o alvo, o localizador e o passo são os da quebra do catálogo."""
    c = next((x for x in cen.CENARIOS_DE_LOCALIZADOR if x["cenario"] == roteiro), None)
    if c is None or roteiro not in MUTACAO_DO_SELETOR:
        raise KeyError(f"{roteiro!r} não é um roteiro de localizador do ensaio")
    q = cen.quebra(roteiro, c["modo"])
    extra = dict(MUTACAO_DO_SELETOR[roteiro]["mutacao"])
    nome_depois = MUTACAO_DO_SELETOR[roteiro]["nome_depois"]
    return {**q, "modo": f"{c['modo']}+{SUFIXO_DA_MUTACAO}", "mutacoes": list(q["mutacoes"]) + [extra], "nome_depois": nome_depois,
            "descricao": q["descricao"] + f'; a mutação extra troca o nome acessível do alvo por "{nome_depois}" (parecido, acima do limiar da cura), '
                                          "para o candidato que curou a dourada deixar de resolver"}


# ------------------------------------------------------------------ o diff entre duas trilhas da mesma corrida

def nos_da_trilha(eventos: list[dict], tid: str) -> list[dict]:
    """Os nós de decisão da trilha `tid`, na ordem: decisão e escolha."""
    return [{"decisao": e["dados"].get("decisao"), "escolha": e["dados"].get("escolha")} for e in eventos if e.get("trilha") == tid and e["tipo"] == "decisao"]


def _escolha_da_cura_com_seletor(e: dict) -> dict:
    """Uma cópia do evento de decisão em que a escolha do nó `cura` leva também o seletor aplicado ("estratégia (seletor)")."""
    d = e["dados"]
    if d.get("decisao") != "cura":
        return e
    aplicado = next((a for a in d.get("alternativas") or [] if a.get("aplicado")), None)
    escolha = f"{d.get('escolha')} ({aplicado.get('seletor')})" if aplicado and aplicado.get("seletor") else d.get("escolha")
    return {**e, "dados": {**d, "escolha": escolha}}


def diff_entre_trilhas(eventos: list[dict], tid_referencia: str, tid_nova: str, cura_pelo_seletor: bool = False) -> dict:
    """O diff de trilha.diff_contra_referencia entre duas trilhas do mesmo arquivo (relidas sob um id comum): o primeiro nó
    divergente (posição, decisão, esperado e obtido) ou None quando as sequências de nós são iguais. Com `cura_pelo_seletor`,
    o nó `cura` é comparado pela estratégia e pelo seletor aplicado (a mutação do seletor pode levar a cura à mesma estratégia
    com outro seletor, como no roteiro cuja dourada já cura por nome parecido)."""
    ref = [dict(e, trilha="comparada") for e in eventos if e.get("trilha") == tid_referencia and e["tipo"] == "decisao"]
    nova = [dict(e, trilha="comparada") for e in eventos if e.get("trilha") == tid_nova and e["tipo"] == "decisao"]
    if cura_pelo_seletor:
        ref, nova = [_escolha_da_cura_com_seletor(e) for e in ref], [_escolha_da_cura_com_seletor(e) for e in nova]
    d = tr.diff_contra_referencia(nova, ref)
    div = None
    if d["divergencias"]:
        x = d["divergencias"][0]
        div = {"posicao": x["posicao"], "decisao": (x["esperado"] or x["obtido"] or {}).get("decisao"), "esperado": x["esperado"], "obtido": x["obtido"]}
    elif not ref and nova:
        # a referência não tem nó nenhum: o primeiro nó da nova já é a divergência
        div = {"posicao": 1, "decisao": nova[0]["dados"].get("decisao"), "esperado": None,
               "obtido": {"decisao": nova[0]["dados"].get("decisao"), "escolha": nova[0]["dados"].get("escolha")}}
    return {"primeiro_no_divergente": div, "nos_referencia": nos_da_trilha(eventos, tid_referencia), "nos_nova": nos_da_trilha(eventos, tid_nova)}


# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) leituras_da_trilha: por caso, o que só a trilha guarda: a FONTE e a resposta
# da repetição da base e a comparação da mutação do verbete com a intervenção de troca (mesmo prompt, mesma resposta, mesma FONTE).
# ! Motivo: a repetição é o controle da sonda de pós-racionalização (a FONTE cita o mesmo verbete sem nada plantado?), e a corrida 22 mostrou
# que a mutação do verbete monta o mesmo prompt da troca; avaliacao.jsonl não guarda a resposta das intervenções, e os dois fatos têm de
# sair de script para entrar na leitura.
def leituras_da_trilha(eventos: list[dict], blobs: dict) -> dict[str, dict]:
    """{id do caso: controle da sonda e comparação da mutação com a troca}; valor None onde a inferência não rodou ou o blob não está à mão."""
    por = tr.por_trilha(eventos)
    saida: dict[str, dict] = {}
    for tid, evs in por.items():
        if not str(tid).endswith("@base"):
            continue
        inf = {e["dados"].get("etapa"): e["dados"] for e in evs if e["tipo"] == "inferencia"}
        base, rep, troca = inf.get("diagnostico"), inf.get("intervencao:repeticao_da_base"), inf.get("intervencao:troca")
        item = {"fonte_na_repeticao": None, "repeticao_mesma_resposta": None, "repeticao_mesma_fonte": None,
                "troca_mesmo_prompt": None, "troca_mesma_resposta": None, "troca_mesma_fonte": None}
        texto_base = blobs.get(base["resposta"]) if base else None
        texto_rep = blobs.get(rep["resposta"]) if rep else None
        if texto_base is not None and texto_rep is not None:
            fonte_rep = avaliar.extrair(texto_rep)["fonte_ids"]
            item.update(fonte_na_repeticao=fonte_rep, repeticao_mesma_resposta=texto_base == texto_rep, repeticao_mesma_fonte=avaliar.extrair(texto_base)["fonte_ids"] == fonte_rep)
        mutada = por.get(str(tid)[:-len("@base")] + "@verbete_trocado") or []
        prompt_m = next((e["dados"] for e in mutada if e["tipo"] == "prompt"), None)
        inf_m = next((e["dados"] for e in mutada if e["tipo"] == "inferencia"), None)
        texto_troca = blobs.get(troca["resposta"]) if troca else None
        texto_m = blobs.get(inf_m["resposta"]) if inf_m else None
        if troca and prompt_m and texto_troca is not None and texto_m is not None:
            item.update(troca_mesmo_prompt=troca.get("prompt") == prompt_m.get("sha"), troca_mesma_resposta=texto_troca == texto_m,
                        troca_mesma_fonte=avaliar.extrair(texto_troca)["fonte_ids"] == avaliar.extrair(texto_m)["fonte_ids"])
        saida[str(tid).rsplit("/", 1)[-1].split("@")[0]] = item
    return saida


def aponta_o_previsto(primeiro_no: dict | None, tipo: str) -> bool | None:
    """A trilha apontou o nó previsto para a mutação? None sem divergência (não há o que apontar)."""
    if primeiro_no is None:
        return None
    return primeiro_no.get("decisao") == NO_PREVISTO[tipo]


# ------------------------------------------------------------------ as etapas de um caso de texto (com o modelo)

def _entrada_e_poda(trilha: tr.Trilha, tid: str, caso: dict, etapa: str, mutacao: dict | None, ts: str) -> tuple[int, int, dict, dict | None]:
    """Os eventos `entrada` (o texto do caso como vai ao prompt) e `poda` (o diff do contrato contra o corpo) e o nó `poda`;
    um caso sem contrato (n/a) ganha o nó com "sem_contrato" e um evento de poda sem diff."""
    e = caso["entrada"]
    contrato = str(e.get("contrato") or "").strip()
    corpo = e.get("corpo") or ""
    s_ent = trilha.evento("entrada", tid, {"caso": caso["id"], "classe": caso.get("classe"), "nivel": caso.get("nivel"), "origem": "fixture", "etapa": etapa,
                                           "texto": trilha.blob(estrategias._dados_do_caso(caso), "caso"), "mutacao": mutacao}, "ao_vivo", ts=ts)
    diff = None if (not contrato or contrato.lower() == "n/a") else poda.diff_contrato(contrato, corpo)
    linhas = linhas_diff_do_contrato(diff) if diff is not None else []
    s_poda = trilha.evento("poda", tid, {"alvo": "corpo_http", "antes": {"chars": len(corpo)}, "depois": {"chars": len(corpo)}, "regras": ["diff_contra_contrato"],
                                         "sha": trilha.blob(corpo, "corpo_podado"), "diff": linhas, "sem_contrato": diff is None}, "ao_vivo", pai=s_ent, ts=ts)
    no = no_de_poda(diff, s_poda, contrato if diff is not None else None)
    trilha.decisao(tid, no, pai=s_poda, ts=ts)
    return s_ent, s_poda, no, diff


def _diagnosticar_etapa(trilha: tr.Trilha, tid: str, caso: dict, verbetes: list[dict], indice: rec.Indice, *, etapa: str, mutacao: dict | None, k: int,
                        modelo: str, comum: dict, limiares: dict | None, top: int, teto: int, ts: str, intervencoes: str = "desligadas", amostra=()) -> dict:
    """Uma etapa de um caso de texto: entrada, poda e o nó `poda`, depois diagnostico_ao_vivo.diagnosticar com o nó
    `recuperacao` emitido pelo gancho apos_candidatos (entre os candidatos e o prompt) e o nó `diagnostico` no fim."""
    _, s_poda, no_poda, diff = _entrada_e_poda(trilha, tid, caso, etapa, mutacao, ts)
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) o corpo que não é JSON só entra como sinal em código quando está truncado ou vazio.
    # ! Motivo: nos fixtures, nao_json é o corpo escrito em texto corrido ("POST devolveu ..."): vem de como o caso foi escrito, não da falha, e a justificativa
    # gravada nos 5 casos assim da corrida 22 atribuiu a resposta a esse "sinal". O nó `poda` continua registrando o que o código leu.
    evidencia = [{"seq": s_poda, "papel": "sinal_em_codigo"}] if no_poda.get("diferencas") or (diff is not None and diff.get("corpo") in ("truncado", "vazio")) else []

    def apos_candidatos(info: dict) -> None:
        trilha.decisao(tid, no_de_recuperacao(info["ctx"], info["seq_candidatos"], k, info["itens"], mutacao=mutacao), pai=info["seq_candidatos"], ts=ts)

    sv = dv.diagnosticar(trilha, tid, caso, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares, intervencoes=intervencoes, amostra=amostra,
                         top=top, teto=teto, evidencia=evidencia, ts=ts, apos_candidatos=apos_candidatos)
    sv["fontes"] = [f["valor"] for f in sv["decl"]["fontes"]]
    return sv


def _intervencao_resumida(i: dict) -> dict:
    return {chave: i.get(chave) for chave in ("tipo", "verbete", "verbete_errado", "rotulo_antes", "rotulo_depois", "mudou_rotulo", "p_antes", "p_depois",
                                               "limite_inferior", "p_rotulo_novo", "segundos")}


def rodar_base(trilha: tr.Trilha, tid: str, caso: dict, verbetes: list[dict], indice: rec.Indice, *, k: int, modelo: str, comum: dict, limiares: dict | None,
               top: int, teto: int, amostra=(), ts: str, intervencoes: str = "por_gatilho") -> dict:
    """A inferência de base de um caso (a trilha de referência das mutações): os nós `poda`, `recuperacao` e `diagnostico`,
    as intervenções por gatilho (na corrida 22 os 36 casos estão na amostra fixa, então as quatro rodam) e a linha do caso."""
    sv = _diagnosticar_etapa(trilha, tid, caso, verbetes, indice, etapa="base", mutacao=None, k=k, modelo=modelo, comum=comum, limiares=limiares, top=top, teto=teto,
                             ts=ts, intervencoes=intervencoes, amostra=amostra)
    no = sv["no"]
    rodadas = [_intervencao_resumida(i) for i in sv["intervencoes"]]
    repeticao = next((i for i in rodadas if i["tipo"] == "repeticao_da_base"), None)
    nos = nos_da_trilha(trilha.eventos, tid)
    linha = {"caso": caso["id"], "classe": caso.get("classe"), "nivel": caso.get("nivel"), "rotulo": no["escolha"], "p_rotulo": no["confianca"]["p_rotulo"],
             "selo": no["confianca"]["selo"], "falha": no["falha"], "divergencia": bool(no["divergencia"]["ha"]), "gatilhos": sv["gatilhos"], "intervencoes": rodadas,
             "intervencoes_puladas": no.get("intervencoes_puladas"), "repeticao_manteve": (not repeticao["mudou_rotulo"]) if repeticao else None,
             "fontes": sv["fontes"], "verbetes_entregues": list(sv["ctx"]["verbetes_ids"]), "nos_base": [[n["decisao"], n["escolha"]] for n in nos],
             "segundos_base": sv["registro"]["segundos"], "tokens_entrada": sv["registro"]["tokens_entrada"], "segundos_etapa": sv["segundos_total"]}
    return {"registro": sv["registro"], "lateral": sv["lateral"], "no": no, "sv": sv, "ctx": sv["ctx"], "fontes": sv["fontes"], "rotulo": no["escolha"],
            "linha": linha, "tid": tid, "caso": caso}


def rodar_sonda(trilha: tr.Trilha, tid: str, caso: dict, verbetes: list[dict], indice: rec.Indice, base: dict, *, k: int, modelo: str, comum: dict,
                limiares: dict | None, top: int, teto: int, ts: str) -> dict:
    """A sonda de pós-racionalização (especificação, seção 5): o trecho de texto_plantado entra, só na memória, no Resumo do
    primeiro verbete entregue que a FONTE da base não citou; uma inferência; a FONTE passar a citar o verbete plantado com o
    mesmo rótulo é a pós-racionalização. Sem rótulo de base ou sem verbete não citado, a sonda não roda e diz por quê."""
    ids = list(base["ctx"]["verbetes_ids"])
    vazio = {"aplicavel": False, "verbete": None, "trecho": None, "cita_plantado": None, "mudou_rotulo": None, "rotulo_depois": None, "fonte_antes": list(base["fontes"]),
             "fonte_depois": None, "pos_racionalizacao": None, "p_depois": None, "motivo": None, "segundos": None}
    if base["rotulo"] is None:
        return {"registro": None, "lateral": None, "sv": None, "linha": {**vazio, "motivo": "a inferência de base não tem rótulo (sem a linha CAUSA_RAIZ)"}}
    alvo = alvo_da_sonda(ids, base["fontes"])
    if alvo is None:
        return {"registro": None, "lateral": None, "sv": None, "linha": {**vazio, "motivo": "a FONTE da base citou todos os verbetes entregues: não há verbete não citado para plantar"}}
    trecho = texto_plantado(base["rotulo"])
    por_id = {v["id"]: v for v in verbetes}
    plantado = verbete_com_trecho(por_id[alvo], trecho)
    verbetes_sonda = [plantado if v["id"] == alvo else v for v in verbetes]
    caso_sonda = {**caso, "id": f"{caso['id']}@sonda"}
    mutacao = {"tipo": "sonda", "verbete": alvo, "trecho": trecho}
    with com_busca_trocada(alvo, plantado):
        sv = _diagnosticar_etapa(trilha, tid, caso_sonda, verbetes_sonda, indice, etapa="sonda", mutacao=mutacao, k=k, modelo=modelo, comum=comum, limiares=limiares,
                                 top=top, teto=teto, ts=ts)
    rotulo_depois = sv["no"]["escolha"]
    cita = alvo in sv["fontes"]
    linha = {**vazio, "aplicavel": True, "verbete": alvo, "trecho": trecho, "cita_plantado": cita, "mudou_rotulo": rotulo_depois != base["rotulo"], "rotulo_depois": rotulo_depois,
             "fonte_depois": list(sv["fontes"]), "pos_racionalizacao": cita and rotulo_depois == base["rotulo"], "p_depois": sv["no"]["confianca"]["p_rotulo"],
             "segundos": sv["registro"]["segundos"]}
    return {"registro": sv["registro"], "lateral": sv["lateral"], "sv": sv, "linha": linha}


def rodar_mutacao(trilha: tr.Trilha, tid: str, tipo: str, caso: dict, verbetes: list[dict], indice: rec.Indice, base: dict, *, k: int, modelo: str, comum: dict,
                  limiares: dict | None, top: int, teto: int, ts: str) -> dict:
    """Uma mutação programada de um caso de texto (verbete trocado na busca ou contrato alterado): uma inferência sem
    intervenções, a trilha diffada contra a base e o nó que divergiu primeiro contra o previsto."""
    if tipo not in ("verbete_trocado", "contrato_alterado"):
        raise ValueError(f"mutação de texto desconhecida: {tipo!r} (o seletor quebrado roda na tela)")
    vazio = {"aplicavel": False, "detalhe": None, "motivo": None, "no_previsto": NO_PREVISTO[tipo], "primeiro_no_divergente": None, "aponta_o_previsto": None,
             "rotulo_depois": None, "mudou_rotulo": None, "p_depois": None, "segundos": None}
    ids = list(base["ctx"]["verbetes_ids"])
    if tipo == "verbete_trocado":
        citadas = [f for f in base["fontes"] if f in ids]
        alvo = citadas[0] if citadas else (ids[0] if ids else None)
        errado = dv.verbete_errado(indice, caso, base["rotulo"], excluir=ids) if alvo else None
        if alvo is None or errado is None:
            motivo = "a busca não entregou verbete nenhum" if alvo is None else "a biblioteca não tem verbete de erro com outra causa fora do contexto"
            return {"registro": None, "lateral": None, "sv": None, "linha": {**vazio, "motivo": motivo}}
        detalhe = {"de": alvo, "para": errado["id"], "alvo": "citado" if citadas else "primeiro_entregue"}
        caso_m = {**caso, "id": f"{caso['id']}@{tipo}"}
        with com_busca_trocada(alvo, errado):
            sv = _diagnosticar_etapa(trilha, tid, caso_m, verbetes, indice, etapa=tipo, mutacao={"tipo": tipo, **detalhe}, k=k, modelo=modelo, comum=comum,
                                     limiares=limiares, top=top, teto=teto, ts=ts)
    else:
        m = mutar_contrato(caso["entrada"].get("contrato"), caso["entrada"].get("corpo"))
        if not m["aplicavel"]:
            return {"registro": None, "lateral": None, "sv": None, "linha": {**vazio, "motivo": m["motivo"]}}
        detalhe = {"campo": m["campo"], "de": m["de"], "para": m["para"], "contrato": m["contrato"]}
        caso_m = copy.deepcopy(caso)
        caso_m["id"] = f"{caso['id']}@{tipo}"
        caso_m["entrada"]["contrato"] = m["contrato"]
        sv = _diagnosticar_etapa(trilha, tid, caso_m, verbetes, indice, etapa=tipo, mutacao={"tipo": tipo, **detalhe}, k=k, modelo=modelo, comum=comum,
                                 limiares=limiares, top=top, teto=teto, ts=ts)
    d = diff_entre_trilhas(trilha.eventos, base["tid"], tid)
    div = d["primeiro_no_divergente"]
    rotulo_depois = sv["no"]["escolha"]
    linha = {**vazio, "aplicavel": True, "detalhe": detalhe, "primeiro_no_divergente": div, "aponta_o_previsto": aponta_o_previsto(div, tipo), "rotulo_depois": rotulo_depois,
             "mudou_rotulo": rotulo_depois != base["rotulo"], "p_depois": sv["no"]["confianca"]["p_rotulo"], "segundos": sv["registro"]["segundos"]}
    return {"registro": sv["registro"], "lateral": sv["lateral"], "sv": sv, "linha": linha}


def linha_do_caso(base: dict, sonda: dict, mutacoes: dict[str, dict], segundos_total: float | None = None) -> dict:
    """A linha de avaliacao.jsonl de um caso: a base, a sonda e as mutações de texto."""
    return {**base["linha"], "sonda": sonda["linha"], "mutacoes": {tipo: m["linha"] for tipo, m in mutacoes.items()}, "segundos_total": segundos_total}


# ------------------------------------------------------------------ o seletor quebrado, na tela (as partes puras)

def lado_do_seletor(d: dict, sv: dict | None, nos: list[dict]) -> dict:
    """O que uma execução do roteiro deixa (a dourada ou a mutada): a quebra, a cura, o diagnóstico do meio e os nós."""
    e = d.get("escolha") or {}
    ap = e.get("aplicado") if isinstance(e.get("aplicado"), dict) else None
    no = (sv or {}).get("no") or {}
    return {"quebrou": bool(d.get("quebrou")), "fora_do_alvo": bool(d.get("fora_do_alvo")), "curado": bool(e.get("curado")), "estrategia": (ap or {}).get("estrategia"),
            "seletor_curado": (ap or {}).get("seletor"), "falha": e.get("falha"), "mesmo_elemento": e.get("mesmo_elemento"), "reexecucoes": e.get("reexecucoes"),
            "rotulo": no.get("escolha"), "p_rotulo": ((no.get("confianca") or {}).get("p_rotulo")), "selo": ((no.get("confianca") or {}).get("selo")),
            "mttr_s": d.get("mttr_s"), "segundos_cura": d.get("segundos_cura"), "nos": [[n["decisao"], n["escolha"]] for n in nos]}


def registro_do_seletor(roteiro: str, cenario_: dict, quebra_dourada: dict, quebra_mutada: dict, dourada: dict, mutada: dict, diff: dict, segundos: float | None) -> dict:
    """A linha de seletor.jsonl de um roteiro: os dois lados e o primeiro nó divergente contra o previsto (cura)."""
    div = diff["primeiro_no_divergente"]
    return {"roteiro": roteiro, "cenario_id": cenario_["id"], "modo_dourado": quebra_dourada["modo"], "modo_mutado": quebra_mutada["modo"], "extra": quebra_mutada["mutacoes"][-1],
            "dourada": dourada, "mutada": mutada, "primeiro_no_divergente": div, "no_previsto": NO_PREVISTO["seletor_quebrado"],
            "aponta_o_previsto": aponta_o_previsto(div, "seletor_quebrado"), "segundos": segundos}


# ------------------------------------------------------------------ contas da noite e a amostra da sessão de revisão

def inferencias_previstas(casos: int, roteiros: int = 4) -> int:
    """Quantas inferências a corrida faz: INFERENCIAS_POR_CASO por caso de texto e duas por roteiro de localizador (a
    dourada e a mutada, cada uma com o diagnóstico entre a detecção e a cura)."""
    return casos * INFERENCIAS_POR_CASO + roteiros * 2


def amostra_de_revisao(linhas: list[dict]) -> list[dict]:
    """Até 6 casos certos e 6 errados sorteados com a semente fixa e embaralhados juntos: os relatórios da sessão de revisão
    com o Eric (plano, P7). `linhas` traz `caso` e `acerto`; a ordem de saída não revela o acerto."""
    rng = random.Random(SEMENTE_DA_AMOSTRA)
    certos = sorted((l for l in linhas if l["acerto"]), key=lambda l: l["caso"])
    errados = sorted((l for l in linhas if not l["acerto"]), key=lambda l: l["caso"])
    amostra = rng.sample(certos, min(AMOSTRA_POR_LADO, len(certos))) + rng.sample(errados, min(AMOSTRA_POR_LADO, len(errados)))
    rng.shuffle(amostra)
    return amostra


def agora() -> str:
    return cen.agora()


def cronometro() -> float:
    return time.monotonic()
