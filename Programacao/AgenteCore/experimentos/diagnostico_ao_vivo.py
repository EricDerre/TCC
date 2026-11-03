#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (27/10/2026, Fase 4, pacote P3): o diagnóstico ao vivo do agente. Monta o
# contexto da busca sem gabarito (a irmã do ramo A2 de recuperacao.contexto), o prompt congelado de
# estrategias.linear_com_biblioteca, faz UMA inferência com as probabilidades por token (sondar_logprobs.com_logprobs
# em volta de executar_fase3.inferir_com_repeticao), monta o registro com as 37 chaves oficiais, lê a probabilidade no
# primeiro token do rótulo depois de CAUSA_RAIZ:, roda as conferências em código (trilha.verificar sem gabarito e
# trilha.conferencias_fase4), dá o selo pelos limiares de resultados_alvo/fase4/limiares.json (ficha 31), decide os
# gatilhos de intervenção (probabilidade baixa, FONTE divergente, amostra fixa), roda as intervenções quando pedidas
# (remoção do verbete citado por um marcador neutro, troca por um verbete errado, inferência sem documentação e a
# repetição da inferência de base) e emite na trilha v2 os eventos candidatos, prompt, inferencia, declaracao,
# verificacao, intervencao e o nó de decisão `diagnostico` (trilha.no_de_decisao), com a justificativa e o contraste
# pelo molde de gerar_relatorio_raciocinio. Nada aqui lê o gabarito do caso; nenhum arquivo congelado muda.
# ! Motivo: plano aprovado da Fase 4, seção 3.5 e pacote P3; especificação da trilha, seções 4.2 (nó), 5
# (conferências), 6.1 (intervenções e gatilhos), 6.3 e 14 (probabilidade lida no primeiro token do rótulo) e 7
# (justificativa por molde); fichas 26 (a probabilidade manda no gatilho), 30 (k = 3 e 5) e 31 (os 30% de menor
# probabilidade são o selo baixo). O registro mantém as 37 chaves porque toda análise anterior (avaliar.py,
# analisar_confianca.py) lê esse formato; o que a Fase 4 acrescenta vai para a trilha e para a linha lateral de
# probabilidades, como a corrida 12 já fazia.
"""Diagnóstico ao vivo da Fase 4 (pacote P3): contexto sem gabarito, prompt congelado, probabilidade do rótulo, selo,
gatilhos, intervenções e o nó de decisão na trilha v2."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import statistics
import time
from pathlib import Path

import analisar_confianca as conf
import avaliar
import biblioteca as bib
import caminhos
import cliente_ollama as oll
import estrategias
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import gerar_relatorio_raciocinio as grr
import recuperacao as rec
import sonda_confianca as sc
import sondar_logprobs as sl
import trilha as tr

MODELO_PADRAO = "qwen2.5:7b"
PASTA_CURADA = sc.PASTA_CURADA          # Programacao/AgenteCore/biblioteca_producao (L1 curada, só leitura)
VERSAO_CURADA = sc.VERSAO_CURADA        # 100 nos arquivos; "L1 curada" para pessoas
ROTULO_CURADA = sc.ROTULO_CURADA
TOP_LOGPROBS = 20
TETO_TOKENS = 600
LEITURA_DA_PROBABILIDADE = "primeiro_token_do_rotulo"
MEDIDA_DO_SELO = "p_rotulo"
PARCELA_BAIXA = 0.3                     # ficha 31 (a): os 30% de menor probabilidade são o selo baixo e o gatilho
INTERVENCOES = ("remocao", "troca", "sem_documentacao", "repeticao_da_base")
MODOS_DE_INTERVENCAO = ("desligadas", "por_gatilho")
# O marcador que entra no lugar do verbete removido: mantém a forma de um verbete (linha de título entre colchetes e um
# parágrafo), para o formato do prompt não mudar; o id é inventado de propósito, para o modelo não ter o que citar.
MARCADOR_NEUTRO = ("[verbete-removido] Verbete retirado para o teste de intervenção\n"
                   "Este verbete foi removido do contexto; não há conteúdo a consultar aqui.")
# As 37 chaves do registro oficial, na ordem em que executar_fase3.diagnosticar as grava (arquivo congelado).
CHAVES_OFICIAIS = ("modelo", "digest", "versao_ollama", "maquina", "caso", "classe", "nivel", "estrategia", "condicao", "fase", "tipo",
                   "epoca", "biblioteca_epoca", "biblioteca_versao", "particao", "k", "contexto_sha256", "notas_no_contexto",
                   "verbetes_novos_no_contexto", "contexto_estourou", "verbetes_ids", "verbete_ouro", "causa_plantada", "chars_contexto",
                   "gabarito", "teto_tokens", "segundos", "tokens_entrada", "tokens_saida", "carga_ms", "prefill_ms", "geracao_ms",
                   "total_ms", "resposta", "somente_cpu", "modelos_residentes", "memoria_mb")
_CHAVES_DA_INFERENCIA = ("segundos", "tokens_entrada", "tokens_saida", "carga_ms", "prefill_ms", "geracao_ms", "total_ms", "resposta")
_CHAVES_DO_AMBIENTE = ("somente_cpu", "modelos_residentes", "memoria_mb")
# Conferência em código que não confere -> falha da taxonomia (trilha.TAXONOMIA_DE_FALHAS), na ordem de prioridade: a
# primeira regra desta lista que não confere dá a falha do nó.
FALHA_POR_REGRA = {"quatro_linhas_presentes": "formato_das_quatro_linhas", "rotulo_no_conjunto": "rotulo_fora_da_taxonomia",
                   "fonte_existe_na_biblioteca": "citacao_inexistente", "fonte_estava_no_contexto": "citacao_fora_do_contexto",
                   "rotulo_sustentado_por_verbete_do_contexto": "causa_sem_verbete_que_a_trate", "campo_existe_no_caso": "campo_errado"}
DETALHE_DA_REGRA = {"quatro_linhas_presentes": "faltam na resposta as linhas {ausentes}",
                    "rotulo_no_conjunto": "a causa respondida {alvo} está fora das 23 permitidas",
                    "fonte_existe_na_biblioteca": "a FONTE cita o verbete {alvo}, que não existe na biblioteca",
                    "fonte_estava_no_contexto": "a FONTE cita o verbete {alvo}, fora do contexto entregue",
                    "rotulo_sustentado_por_verbete_do_contexto": "nenhum verbete entregue trata da causa respondida {alvo}",
                    "campo_existe_no_caso": "o campo apontado ({alvo}) não aparece no caso"}
# "FONTE divergente" da especificação (6.1): cita verbete fora do contexto ou nenhum verbete do contexto trata da causa.
REGRAS_DA_FONTE_DIVERGENTE = ("fonte_estava_no_contexto", "rotulo_sustentado_por_verbete_do_contexto")


def agora() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def caminho_dos_limiares() -> Path:
    """resultados_alvo/fase4/limiares.json (regra R7), lido na hora porque RESULTADOS_DIR pode mudar nos testes."""
    return caminhos.RESULTADOS / "fase4" / "limiares.json"


# ------------------------------------------------------------------ contexto e prompt (sem gabarito)

def contexto_ao_vivo(verbetes: list[dict], indice: rec.Indice, caso: dict, k: int = 3, extras=()) -> dict:
    """O ramo A2 de recuperacao.contexto sem pedir gabarito: os k verbetes que a busca entrega, no mesmo envelope; o
    verbete de ouro e a causa plantada ficam None, porque o agente não sabe a resposta.
    ! Alteração de IA - Revisar: (03/11/2026, P5) `extras` são verbetes recuperados pelo id do caso (ficha 32 e o ciclo
    de correção: as notas `[E1 · <caso> · …]` e o caso de origem dos verbetes aprendidos), postos DEPOIS dos k da busca,
    sem repetir os que a busca já entregou; os ids deles ficam em `por_id`.
    ! Motivo: a sonda de 28/09/2026 (roadmap §3) mostrou que a busca por palavras não trazia as notas ligadas ao caso
    reapresentado; os k da busca continuam na frente para o contexto de um caso sem notas ser byte a byte o de antes."""
    sel = rec.recuperar(indice, caso, k)
    ids = [v["id"] for v in sel]
    por_id = [v for v in extras if v["id"] not in ids]
    todos = sel + por_id
    return {"texto": rec._envelope(todos), "verbetes_ids": [v["id"] for v in todos], "verbete_ouro": None, "causa_plantada": None,
            "por_id": [v["id"] for v in por_id]}


def montar_prompt(verbetes: list[dict], indice: rec.Indice, caso: dict, k: int = 3, extras=()) -> tuple[dict, str]:
    """O contexto ao vivo e o prompt congelado (estrategias.linear_com_biblioteca): byte a byte o mesmo que
    executar_fase3.contexto_e_prompt monta para um caso gravado com a mesma entrada (com `extras`, os verbetes
    recuperados pelo id do caso entram depois dos k da busca)."""
    ctx = contexto_ao_vivo(verbetes, indice, caso, k, extras)
    return ctx, estrategias.linear_com_biblioteca(caso, ctx["texto"])


def hash_prompt_fixo(verbetes: list[dict], ctx: dict, caso: dict, prompt: str) -> str:
    """O hash da parte fixa do prompt (instrução e formato das quatro linhas), lida pela repartição de
    trilha.partes_do_prompt: é o que o cabeçalho da corrida declara para provar que o prompt não mudou (ficha 34)."""
    partes = tr.partes_do_prompt(verbetes, ctx, caso, prompt)
    return tr.sha("".join(p["antes"] + p["texto"] for p in partes if p["papel"] in ("instrucao", "formato")))


def hash_indice(indice: rec.Indice) -> str:
    """O hash do índice BM25 (ids e tokens indexados de cada verbete), para o cabeçalho da corrida."""
    return tr.sha(json.dumps([[v["id"] for v in indice.verbetes], indice.docs], ensure_ascii=False))


def quantizacao_do_modelo(modelo: str) -> str | None:
    """A quantização declarada pelo Ollama em /api/show (None quando ele não responde)."""
    try:
        return oll._post("/api/show", {"model": modelo}, timeout=60).get("details", {}).get("quantization_level")
    except Exception:  # noqa: BLE001 - metadado: a corrida não para por isso
        return None


# ------------------------------------------------------------------ inferência e registro

def inferir(modelo: str, prompt: str, teto: int, caso_id: str, top: int = TOP_LOGPROBS, etapa: str = "diagnóstico") -> tuple[dict, dict]:
    """Uma inferência com as probabilidades por token: a chamada de sempre (cliente_ollama.gerar, repetida por
    executar_fase3.inferir_com_repeticao quando o Ollama falha) com `logprobs` e `top_logprobs` acrescentados pelo
    gancho da Pré-Fase 4. Devolve o dicionário de 8 chaves de `gerar` e a captura crua (resposta com os tokens)."""
    capturas: list = []
    with sl.com_logprobs(top, capturas, exigir=True):
        r = executar_fase3.inferir_com_repeticao(modelo, prompt, teto, caso_id, etapa)
    if not capturas:
        raise RuntimeError(f"caso {caso_id}: inferência sem captura das probabilidades")
    executar_bateria.guarda_tokens_reais(r.get("tokens_entrada", 0), teto, etapa)
    return r, capturas[-1]


def registro_oficial(modelo: str, caso: dict, verbetes: list[dict], ctx: dict, prompt: str, r: dict, comum: dict, ambiente: dict) -> dict:
    """O registro de diagnóstico com exatamente as 37 chaves oficiais, na ordem de executar_fase3.diagnosticar; para o
    caso ao vivo, `gabarito`, `verbete_ouro` e `causa_plantada` ficam None e `fase` é "4"."""
    por_id = {v["id"]: v for v in verbetes}
    recuperados = [por_id[i] for i in ctx["verbetes_ids"] if i in por_id]
    particao = comum.get("particao")
    particao_do_caso = (evo.particao_de(particao, caso["id"]) if isinstance(particao, dict) and caso["id"] in particao.get("casos", {})
                        else "avaliacao")
    teto = comum.get("teto_tokens", TETO_TOKENS)
    registro = {"modelo": modelo, "digest": comum["digest"], "versao_ollama": comum["versao_ollama"], "maquina": comum["maquina"],
                "caso": caso["id"], "classe": caso.get("classe"), "nivel": caso.get("nivel"),
                "estrategia": executar_fase3.ESTRATEGIA, "condicao": executar_fase3.CONDICAO, "fase": "4", "tipo": "diagnostico",
                "epoca": comum.get("epoca", VERSAO_CURADA + 1), "biblioteca_epoca": comum.get("biblioteca_epoca", VERSAO_CURADA),
                "biblioteca_versao": comum["biblioteca_versao"], "particao": particao_do_caso, "k": comum["k"],
                "contexto_sha256": executar_fase3._sha12(ctx["texto"]),
                "notas_no_contexto": sum(len(bib.notas(v)) for v in recuperados),
                "verbetes_novos_no_contexto": [v["id"] for v in recuperados if v["pasta"] == evo.PASTA_APRENDIDOS],
                "contexto_estourou": executar_fase3._estourou(r.get("tokens_entrada", 0), teto),
                "verbetes_ids": list(ctx["verbetes_ids"]), "verbete_ouro": ctx.get("verbete_ouro"), "causa_plantada": ctx.get("causa_plantada"),
                "chars_contexto": len(ctx["texto"]), "gabarito": caso.get("gabarito"), "teto_tokens": teto,
                **{k: r.get(k) for k in _CHAVES_DA_INFERENCIA},
                **{k: ambiente.get(k) for k in _CHAVES_DO_AMBIENTE}}
    if tuple(registro) != CHAVES_OFICIAIS:
        raise ValueError(f"registro fora do formato oficial: {list(registro)}")
    return registro


# ------------------------------------------------------------------ a probabilidade do rótulo

def _causas_normalizadas() -> list[str]:
    return sorted(avaliar._PERMITIDAS)


def alternativas_por_causa(tokens: list[dict], trecho: dict, causas: list[str]) -> dict[str, float]:
    """Para cada causa do conjunto diferente da respondida, a maior massa de uma alternativa devolvida que leva a ela
    (a mesma árvore de prefixos de analisar_confianca.alternativas_divergentes, guardada causa a causa). Uma
    alternativa que é prefixo de duas causas conta para as duas; a massa é a do que já foi escrito vezes a da
    alternativa, um limite inferior, porque só as alternativas devolvidas entram."""
    respondida = trecho["texto"]
    escrito, acumulada = "", 1.0
    por_causa: dict[str, float] = {}
    for k in range(trecho["ini"], trecho["fim"]):
        t = tokens[k]
        primeiro = escrito == ""
        for alt in t.get("top_logprobs") or []:
            if alt["token"] == t["token"]:
                continue
            parte, fecha = conf._parte_do_rotulo(alt["token"], primeiro)
            candidato = avaliar._normalizar(escrito + parte)
            if not candidato or (not parte and not fecha):
                continue
            compativeis = [c for c in causas if (c == candidato if fecha else c.startswith(candidato))]
            if not compativeis or respondida in compativeis:
                continue
            m = acumulada * math.exp(alt["logprob"])
            for c in compativeis:
                por_causa[c] = max(por_causa.get(c, 0.0), m)
        parte, _ = conf._parte_do_rotulo(t["token"], primeiro)
        escrito += parte
        acumulada *= math.exp(t["logprob"])
    return por_causa


def _entropia_normalizada(top: list[dict]) -> float | None:
    """A entropia das alternativas devolvidas numa posição (probabilidades renormalizadas), dividida pelo máximo
    log(n): 0 é certeza, 1 é indiferença entre as n alternativas; None com menos de duas."""
    ps = [math.exp(a["logprob"]) for a in top]
    if len(ps) < 2:
        return None
    soma = sum(ps)
    qs = [p / soma for p in ps if p > 0]
    return round(-sum(q * math.log(q) for q in qs) / math.log(len(ps)), 6)


def confianca_do_rotulo(tokens: list[dict], causas: list[str] | None = None) -> dict | None:
    """A leitura da especificação (seções 6.3 e 14): a probabilidade do primeiro token do rótulo depois de CAUSA_RAIZ:
    (achado por analisar_confianca.trecho_do_rotulo, em bytes), a conjunta dos tokens do rótulo (a medida da corrida
    12), a massa das alternativas que levam a outra causa, as alternativas causa a causa (escore = massa), a segunda
    causa, a margem para ela e a entropia normalizada das alternativas na posição do rótulo. None sem a linha."""
    causas = causas or _causas_normalizadas()
    trecho = conf.trecho_do_rotulo(tokens)
    if trecho is None:
        return None
    primeiro = tokens[trecho["ini"]]
    p_rotulo = math.exp(primeiro["logprob"])
    outras = alternativas_por_causa(tokens, trecho, causas)
    divergentes = conf.alternativas_divergentes(tokens, trecho, causas)
    alternativas = [{"opcao": trecho["texto"], "escore": p_rotulo}]
    alternativas += [{"opcao": c, "escore": m} for c, m in sorted(outras.items(), key=lambda x: (-x[1], x[0]))]
    segunda = alternativas[1] if len(alternativas) > 1 else None
    top = primeiro.get("top_logprobs") or []
    return {"rotulo": trecho["texto"], "trecho": trecho, "logprob_rotulo": primeiro["logprob"], "p_rotulo": p_rotulo,
            "p_conjunta": conf.probabilidade_conjunta(tokens, trecho), "tokens_do_rotulo": trecho["fim"] - trecho["ini"],
            "massa_divergente": divergentes["massa_divergente"], "margem": p_rotulo - (segunda["escore"] if segunda else 0.0),
            "entropia_normalizada": _entropia_normalizada(top), "alternativas_top": len(top),
            "alternativas": alternativas, "segunda": segunda}


def probabilidade_do_rotulo_original(tokens: list[dict], trecho: dict | None, rotulo_original: str) -> tuple[float | None, bool]:
    """Depois de uma intervenção: a probabilidade do rótulo ORIGINAL na resposta nova. Se o rótulo novo é o mesmo, é a
    do primeiro token dele; senão, é a da alternativa devolvida na posição do rótulo que começa o rótulo original.
    Quando ele não está entre as alternativas devolvidas, o Ollama não pontua uma continuação dada e fica só um limite
    inferior (a menor alternativa devolvida), marcado com True (especificação, risco 6). Sem rótulo novo: (None, True)."""
    if trecho is None:
        return None, True
    alvo = avaliar._normalizar(rotulo_original)
    primeiro = tokens[trecho["ini"]]
    p_primeiro = math.exp(primeiro["logprob"])
    if trecho["texto"] == alvo:
        return p_primeiro, False
    # o rótulo novo pode dividir o primeiro token com o original (" campo" em campo_ausente e campo_renomeado, como na
    # corrida 12): na leitura pelo primeiro token, a probabilidade do original é a desse token, sem limite inferior
    parte, fecha = conf._parte_do_rotulo(primeiro["token"], True)
    candidato = avaliar._normalizar(parte)
    if candidato and ((alvo == candidato) if fecha else alvo.startswith(candidato)):
        return p_primeiro, False
    menor = None
    for alt in primeiro.get("top_logprobs") or []:
        p = math.exp(alt["logprob"])
        menor = p if menor is None else min(menor, p)
        if alt["token"] == primeiro["token"]:
            continue
        parte, fecha = conf._parte_do_rotulo(alt["token"], True)
        candidato = avaliar._normalizar(parte)
        if candidato and ((alvo == candidato) if fecha else alvo.startswith(candidato)):
            return p, False
    return menor, True


# ------------------------------------------------------------------ limiares e selo (ficha 31)

def calcular_limiares(linhas: list[dict], parcela: float = PARCELA_BAIXA, medida: str = MEDIDA_DO_SELO, k: int | None = None,
                      origem: str | None = None) -> dict:
    """Os limiares do selo pela curva risco-cobertura (regra R7, ficha 31 a): baixo = a parcela de menor probabilidade
    (`baixo_ate` é a maior probabilidade dentro dela), alto = acima da mediana dos acertos (`alto_a_partir_de`), médio
    entre os dois. `linhas` traz `p` (a medida) e `acerto`; linha sem probabilidade fica fora da curva e é contada."""
    validas = [l for l in linhas if isinstance(l.get("p"), (int, float))]
    notas = [float(l["p"]) for l in validas]
    acertos = [bool(l["acerto"]) for l in validas]
    n = len(validas)
    revisao = conf.revisao(notas, acertos, parcela) if n else {"revisados": 0, "erros_pegos": 0, "erros": 0, "acertos_revisados": 0, "risco_no_que_sobra": None}
    ordenadas = sorted(notas)
    quantos = int(round(parcela * n))
    certos = [p for p, a in zip(notas, acertos) if a]
    errados = [p for p, a in zip(notas, acertos) if not a]
    return {"medida": medida, "leitura": LEITURA_DA_PROBABILIDADE, "parcela_baixa": parcela,
            "baixo_ate": ordenadas[quantos - 1] if quantos >= 1 else None,
            "alto_a_partir_de": statistics.median(certos) if certos else None,
            "n": n, "sem_rotulo": len(linhas) - n, "k": k, "origem": origem,
            "erros": revisao["erros"], "revisados": revisao["revisados"], "erros_pegos": revisao["erros_pegos"],
            "acertos_revisados": revisao["acertos_revisados"], "risco_no_que_sobra": revisao["risco_no_que_sobra"],
            "mediana_certos": statistics.median(certos) if certos else None, "mediana_errados": statistics.median(errados) if errados else None,
            "regra": "ficha 31 (a): baixo = a parcela de menor probabilidade (gatilho de intervenção e de revisão humana); "
                     "alto = acima da mediana dos acertos; médio = entre os dois"}


def gravar_limiares(limiares: dict, caminho: Path | None = None) -> Path:
    caminho = caminho or caminho_dos_limiares()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps({**limiares, "gravado_em": agora()}, ensure_ascii=False, indent=2), encoding="utf-8")
    return caminho


def carregar_limiares(caminho: Path | None = None) -> dict | None:
    caminho = caminho or caminho_dos_limiares()
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def selo(p: float | None, limiares: dict | None) -> str | None:
    """alto, medio ou baixo pelos limiares; None sem limiares (antes da corrida 16) ou sem probabilidade lida."""
    if limiares is None or p is None:
        return None
    if limiares.get("baixo_ate") is not None and p <= limiares["baixo_ate"]:
        return "baixo"
    if limiares.get("alto_a_partir_de") is not None and p >= limiares["alto_a_partir_de"]:
        return "alto"
    return "medio"


# ------------------------------------------------------------------ gatilhos, divergência e falha

def gatilhos(confianca: dict | None, verificacoes: list[dict], limiares: dict | None, caso_id: str | None = None, amostra=()) -> dict:
    """Os gatilhos de intervenção da especificação (6.1), com a ficha 26 (a probabilidade manda): probabilidade do
    rótulo no selo baixo (ou rótulo não lido), só com limiares; FONTE divergente (verbete citado fora do contexto ou
    nenhum verbete entregue trata da causa); o caso pertencer à amostra fixa."""
    p = confianca.get("p_rotulo") if confianca else None
    por_probabilidade = bool(limiares) and (p is None or (limiares.get("baixo_ate") is not None and p <= limiares["baixo_ate"]))
    fonte = any(v.get("regra") in REGRAS_DA_FONTE_DIVERGENTE and v.get("resultado") == "nao_confere" for v in verificacoes)
    # o caso ao vivo se chama "<id>@tela"; a amostra fixa guarda os ids dos casos
    na_amostra = caso_id is not None and str(caso_id).split("@")[0] in set(amostra)
    return {"probabilidade": por_probabilidade, "fonte_divergente": fonte, "amostra": na_amostra,
            "algum": por_probabilidade or fonte or na_amostra}


def divergencia_e_falha(verificacoes: list[dict], intervencoes=()) -> tuple[dict, str | None]:
    """A divergência obrigatória do nó (especificação, 4.2): o que o modelo declarou difere do que o código mediu
    quando uma conferência da lista FALHA_POR_REGRA não confere ou quando uma intervenção mudou o rótulo. A falha é a
    da primeira regra da lista que não confere (só conferências; a intervenção marca divergência, não falha)."""
    nao_conferem = {v.get("regra"): v for v in verificacoes if v.get("resultado") == "nao_confere" and v.get("regra") in FALHA_POR_REGRA}
    detalhes, falha = [], None
    for regra, tipo in FALHA_POR_REGRA.items():
        v = nao_conferem.get(regra)
        if v is None:
            continue
        falha = falha or tipo
        ev = v.get("evidencia") if isinstance(v.get("evidencia"), dict) else {}
        ausentes = ", ".join(ev.get("ausentes") or []) or "pedidas"
        detalhes.append(DETALHE_DA_REGRA[regra].format(alvo=v.get("alvo"), ausentes=ausentes))
    for i in intervencoes:
        if i.get("mudou_rotulo"):
            nome = {"remocao": f"a remoção do verbete {i.get('verbete')}", "troca": f"a troca do verbete {i.get('verbete')} por um errado",
                    "sem_documentacao": "a inferência sem documentação", "repeticao_da_base": "a repetição da inferência de base"}.get(
                        i.get("tipo"), f"a intervenção {i.get('tipo')}")
            detalhes.append(f"{nome} mudou a resposta de {i.get('rotulo_antes')} para {i.get('rotulo_depois')}")
    if not detalhes:
        return {"ha": False, "entre": [], "detalhe": None}, falha
    return {"ha": True, "entre": ["modelo", "verificacao"], "detalhe": "; ".join(detalhes)}, falha


# ------------------------------------------------------------------ intervenções (especificação, 6.1 e 6.2)

def verbete_errado(indice: rec.Indice, caso: dict, causa_respondida: str | None, excluir=()) -> dict | None:
    """O verbete de erro mais parecido com o caso cuja causa é OUTRA que não a respondida e que não estava no contexto:
    o distrator da intervenção de troca, escolhido sem gabarito (recuperacao._errados_plausiveis precisa dele)."""
    alvo = avaliar._normalizar(causa_respondida or "")
    for _, v in rec.pontuar(indice, caso):
        m = v["meta"]
        if m.get("tipo") != "erro" or v["id"] in excluir:
            continue
        relacionadas = {avaliar._normalizar(c) for c in m.get("causas_relacionadas", [])}
        if avaliar._normalizar(m.get("causa_raiz") or "") == alvo or alvo in relacionadas:
            continue
        return v
    return None


def contexto_com_intervencao(verbetes: list[dict], ctx: dict, tipo: str, verbete_id: str | None = None, errado: dict | None = None) -> str:
    """O texto da documentação de cada intervenção: remoção (o verbete vira o marcador neutro), troca (o verbete vira
    o errado), sem documentação (vazio, como a condição A0) e repetição da base (o mesmo texto)."""
    if tipo == "sem_documentacao":
        return ""
    if tipo == "repeticao_da_base":
        return ctx["texto"]
    por_id = {v["id"]: v for v in verbetes}
    blocos = []
    for i in ctx["verbetes_ids"]:
        if i == verbete_id:
            blocos.append(MARCADOR_NEUTRO if tipo == "remocao" else bib.render(errado))
        else:
            blocos.append(bib.render(por_id[i]))
    return bib.CABECALHO + "\n\n" + "\n\n".join(blocos)


# ------------------------------------------------------------------ o diagnóstico inteiro, na trilha

def _sustentada_por(causa: str | None, ctx: dict, por_id: dict) -> list[str]:
    """Os verbetes entregues que tratam da causa (a regra de trilha.verificar para rotulo_sustentado_por_verbete)."""
    if not causa:
        return []
    saida = []
    for i in ctx["verbetes_ids"]:
        m = por_id[i]["meta"] if i in por_id else {}
        if avaliar._normalizar(m.get("causa_raiz") or "") == causa or causa in {avaliar._normalizar(c) for c in m.get("causas_relacionadas", [])}:
            saida.append(i)
    return saida


def diagnosticar(trilha: tr.Trilha, tid: str, caso: dict, verbetes: list[dict], indice: rec.Indice, *, k: int, modelo: str, comum: dict,
                 limiares: dict | None = None, intervencoes: str = "desligadas", amostra=(), top: int = TOP_LOGPROBS,
                 teto: int = TETO_TOKENS, evidencia=(), ts: str | None = None, causas: list[str] | None = None, extras=()) -> dict:
    """Diagnostica um caso (ao vivo ou lido do fixture, sempre sem gabarito) e emite tudo na trilha v2: candidatos,
    prompt, inferencia, declaracao (uma por linha e por verbete citado), verificacao (as oito sem gabarito mais as duas
    da Fase 4), as intervenções (cada uma com a própria inferencia e um evento intervencao ligados à inferência de
    base) e, por último, o nó de decisão `diagnostico`. `evidencia` são os eventos que quem chama já emitiu (poda,
    interceptação) e que o nó deve apontar. Devolve o registro oficial, a linha lateral, o nó e os resumos."""
    if intervencoes not in MODOS_DE_INTERVENCAO:
        raise ValueError(f"modo de intervenção desconhecido: {intervencoes!r} (use um de {MODOS_DE_INTERVENCAO})")
    ts = ts or agora()
    causas = causas or _causas_normalizadas()
    por_id = {v["id"]: v for v in verbetes}
    t0 = time.monotonic()
    # ! Alteração de IA - Revisar: (03/11/2026, P5) `extras` (verbetes recuperados pelo id do caso) entram no contexto depois
    # dos k da busca e ficam registrados no evento `candidatos` (`por_id`).
    # ! Motivo: ficha 32 e o ciclo de correção (plano, seção 3.7, item 4): as notas do próprio caso chegam ao modelo sem
    # depender da busca por palavras, e a trilha diz quais verbetes vieram por esse caminho.
    ctx, prompt = montar_prompt(verbetes, indice, caso, k, extras)
    sinais, itens = tr.candidatos(indice, caso, k)
    s_cand = trilha.evento("candidatos", tid, {"k": k, "sinais": sinais, "itens": itens, "hash_indice": hash_indice(indice), "por_id": ctx.get("por_id") or []},
                           "ao_vivo", ts=ts)
    sha_prompt = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]
    s_prompt = trilha.evento("prompt", tid, {"etapa": "diagnostico", "sha": trilha.blob(prompt, "prompt"), "prompt_sha256": sha_prompt,
                                             "chars": len(prompt), "hash_prompt_fixo": hash_prompt_fixo(verbetes, ctx, caso, prompt),
                                             "verbetes_ids": ctx["verbetes_ids"]}, "ao_vivo", pai=s_cand, ts=ts)
    r, captura = inferir(modelo, prompt, teto, caso["id"], top)
    ambiente = executar_bateria.ambiente_residente()
    registro = registro_oficial(modelo, caso, verbetes, ctx, prompt, r, {**comum, "k": k, "teto_tokens": teto}, ambiente)
    lateral = sc.linha_lateral(registro, captura, top)
    tokens = captura["resposta"].get("logprobs") or []
    s_inf = trilha.evento("inferencia", tid, {"etapa": "diagnostico", "resposta": trilha.blob(registro["resposta"], "resposta"),
                                              "segundos": r["segundos"], "tokens_entrada": r["tokens_entrada"], "tokens_saida": r["tokens_saida"],
                                              "prefill_ms": r["prefill_ms"], "geracao_ms": r["geracao_ms"],
                                              "prompt_eval_cached_count": captura["resposta"].get("prompt_eval_cached_count"),
                                              "done_reason": captura["resposta"].get("done_reason"), "top_logprobs": top},
                          "ao_vivo", pai=s_prompt, ts=ts)
    decl = tr.localizar_declaracoes(registro["resposta"])
    for chave, _ in tr._CAMPOS:
        item = decl["campos"][chave]
        lido = decl["lido"]["fonte_ids"] if chave == "fonte" else decl["lido"][chave]
        dados = {"campo": chave, "ausente": True, "valor": None, "lido": lido} if item is None else {"campo": chave, "lido": lido, **item}
        trilha.evento("declaracao", tid, dados, "ao_vivo", pai=s_inf, ts=ts)
    seq_citadas: dict[str, int] = {}
    for f in decl["fontes"]:
        s = trilha.evento("declaracao", tid, {"campo": "fonte_citada", **f}, "ao_vivo", pai=s_inf, ts=ts)
        seq_citadas.setdefault(f["valor"], s)
    verificacoes = tr.verificar(registro, caso, verbetes, decl, com_gabarito=False)
    verificacoes += tr.conferencias_fase4(decl, {i: bib.render(v) for i, v in por_id.items()})
    for v in verificacoes:
        trilha.evento("verificacao", tid, v, "ao_vivo", pai=s_inf, ts=ts)
    confianca = confianca_do_rotulo(tokens, causas)
    rotulo = confianca["rotulo"] if confianca else None
    p = confianca["p_rotulo"] if confianca else None
    o_selo = selo(p, limiares)
    g = gatilhos(confianca, verificacoes, limiares, caso["id"], amostra)

    rodadas: list[dict] = []
    puladas = None
    if intervencoes == "por_gatilho" and g["algum"] and rotulo is None:
        # sem a linha CAUSA_RAIZ não há rótulo de base para medir mudança: as intervenções não rodam e o nó diz por quê
        puladas = "sem rótulo de base: a resposta não tem a linha CAUSA_RAIZ"
    if intervencoes == "por_gatilho" and g["algum"] and rotulo is not None:
        citadas_no_contexto = [f["valor"] for f in decl["fontes"] if f["valor"] in ctx["verbetes_ids"]]
        alvo = citadas_no_contexto[0] if citadas_no_contexto else (ctx["verbetes_ids"][0] if ctx["verbetes_ids"] else None)
        origem_do_alvo = "citado" if citadas_no_contexto else "primeiro_entregue"
        errado = verbete_errado(indice, caso, rotulo, excluir=ctx["verbetes_ids"])
        for tipo in INTERVENCOES:
            com_verbete = tipo in ("remocao", "troca")
            if com_verbete and (alvo is None or (tipo == "troca" and errado is None)):
                continue
            texto = contexto_com_intervencao(verbetes, ctx, tipo, alvo, errado)
            prompt_i = estrategias.linear_com_biblioteca(caso, texto)
            r_i, cap_i = inferir(modelo, prompt_i, teto, caso["id"], top, etapa=f"intervenção {tipo}")
            tokens_i = cap_i["resposta"].get("logprobs") or []
            conf_i = confianca_do_rotulo(tokens_i, causas)
            p_depois, limite = probabilidade_do_rotulo_original(tokens_i, conf_i["trecho"] if conf_i else None, rotulo) if rotulo else (None, True)
            rotulo_depois = conf_i["rotulo"] if conf_i else None
            s_i = trilha.evento("inferencia", tid, {"etapa": f"intervencao:{tipo}", "resposta": trilha.blob(r_i["resposta"], "resposta"),
                                                    "prompt": trilha.blob(prompt_i, "prompt"), "segundos": r_i["segundos"],
                                                    "tokens_entrada": r_i["tokens_entrada"], "tokens_saida": r_i["tokens_saida"],
                                                    "prompt_eval_cached_count": cap_i["resposta"].get("prompt_eval_cached_count"), "top_logprobs": top},
                                "ao_vivo", pai=s_inf, ts=ts)
            dados = {"tipo": tipo, "verbete": alvo if com_verbete else None, "alvo": origem_do_alvo if com_verbete else None,
                     "verbete_errado": errado["id"] if tipo == "troca" else None, "rotulo_antes": rotulo, "rotulo_depois": rotulo_depois,
                     "p_antes": p, "p_depois": p_depois, "mudou_rotulo": rotulo_depois != rotulo, "limite_inferior": limite,
                     "p_rotulo_novo": conf_i["p_rotulo"] if conf_i else None, "segundos": r_i["segundos"], "seq_inferencia": s_i}
            trilha.evento("intervencao", tid, dados, "ao_vivo", pai=s_inf, ts=ts)
            rodadas.append(dados)

    divergencia, falha = divergencia_e_falha(verificacoes, rodadas)
    alternativas = [{**a, "sustentada_por": _sustentada_por(a["opcao"], ctx, por_id)} for a in (confianca["alternativas"] if confianca else [])]
    ev = list(evidencia) + [{"seq": s_cand, "papel": "verbete_entregue", "id": i} for i in ctx["verbetes_ids"]]
    ev += [{"seq": s_inf, "papel": "resposta"}] + [{"seq": s, "papel": "verbete_citado", "id": i} for i, s in seq_citadas.items()]
    conf_no = {"logprob_rotulo": confianca["logprob_rotulo"] if confianca else None, "p_rotulo": p,
               "p_conjunta": confianca["p_conjunta"] if confianca else None, "massa_divergente": confianca["massa_divergente"] if confianca else None,
               "margem": confianca["margem"] if confianca else None, "entropia_normalizada": confianca["entropia_normalizada"] if confianca else None,
               "alternativas_top": confianca["alternativas_top"] if confianca else 0, "selo": o_selo, "leitura": LEITURA_DA_PROBABILIDADE,
               "limiares": {"baixo_ate": limiares.get("baixo_ate"), "alto_a_partir_de": limiares.get("alto_a_partir_de")} if limiares else None}
    usados = list(ctx["verbetes_ids"]) + [i for i in seq_citadas if i not in ctx["verbetes_ids"]]
    campo_lido = decl["lido"]["campo"]
    # "CAMPO: nenhum" é a resposta prevista pelo prompt quando não há campo: o nó guarda None (a regra é a de
    # trilha.verificar para campo_existe_no_caso), senão o molde escreveria "no campo nenhum"
    campo_no = None if not campo_lido or "nenhum" in avaliar._normalizar(campo_lido) else campo_lido
    no = tr.no_de_decisao("diagnostico", escolha=rotulo, alternativas=alternativas, evidencia=ev,
                          resultado="rotulo_emitido" if rotulo else "sem_rotulo", divergencia=divergencia, confianca=conf_no,
                          prov={"used": usados, "wasDerivedFrom": [], "wasGeneratedBy": s_inf}, falha=falha,
                          extras={"campo": campo_no, "gatilhos": g, "k": k, "modo_de_intervencao": intervencoes, "intervencoes_puladas": puladas,
                                  "intervencoes": [{kk: vv for kk, vv in i.items() if kk in ("tipo", "verbete", "rotulo_depois", "p_depois",
                                                                                            "mudou_rotulo", "limite_inferior")} for i in rodadas]})
    no["justificativa"] = grr.justificativa_por_molde(no, eventos=trilha.eventos, verificacoes=verificacoes, intervencoes=rodadas)
    no["contraste"] = grr.contraste_por_molde(no)
    s_no = trilha.decisao(tid, no, pai=s_inf, ts=ts)
    return {"registro": registro, "lateral": lateral, "no": no, "seq_inferencia": s_inf, "seq_decisao": s_no, "confianca": confianca,
            "gatilhos": g, "intervencoes": rodadas, "verificacoes": verificacoes, "decl": decl, "ctx": ctx, "prompt_sha256": sha_prompt,
            "chars_prompt": len(prompt), "segundos_total": round(time.monotonic() - t0, 2)}


# ------------------------------------------------------------------ sondagem dos logprobs (começo de toda noite medida)

def sondagem_logprobs(modelo: str, caso: dict, verbetes: list[dict], indice: rec.Indice, k: int = 3, top: int = TOP_LOGPROBS,
                      teto: int = TETO_TOKENS, versao_ollama: str | None = None, digest: str | None = None) -> dict:
    """As três chamadas de sondar_logprobs.py (temperatura oficial com logprobs; temperatura 1,0 e 8 tokens, só para
    conferir a ferramenta; temperatura oficial sem logprobs), com a L1 curada e o prompt congelado, no mesmo formato
    da amostra da Pré-Fase 4: o que o Ollama instalado devolve antes de a noite medida começar (regra R6 e 6.3)."""
    ctx, prompt = montar_prompt(verbetes, indice, caso, k)
    capturas: list = []
    with sl.com_logprobs(top, capturas):
        ra = oll.gerar(modelo, prompt, teto)
    with sl.com_logprobs(top, capturas, temperatura=sl.TEMPERATURA_DE_CONFERENCIA, num_predict=sl.TOKENS_DA_CONFERENCIA):
        rb = oll.gerar(modelo, prompt, teto)
    rc = oll.gerar(modelo, prompt, teto)
    lp_a = capturas[0]["resposta"].get("logprobs") or []
    lp_b = capturas[1]["resposta"].get("logprobs") or []
    temperatura = (sl.comparar_temperatura(lp_a[0], lp_b[0], oll.TEMPERATURA, sl.TEMPERATURA_DE_CONFERENCIA)
                   if lp_a and lp_b else {"veredito": "indeterminado", "razao": None, "tokens_comuns": 0})
    c = confianca_do_rotulo(lp_a) if lp_a else None
    return {"metadados": {"gerado_em": agora(), "modelo": modelo, "digest": digest, "versao_ollama": versao_ollama, "caso": caso["id"],
                          "biblioteca": ROTULO_CURADA, "biblioteca_versao": evo.hash_biblioteca(PASTA_CURADA), "verbetes_ids": ctx["verbetes_ids"],
                          "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12], "prompt_chars": len(prompt),
                          "teto_tokens": teto, "top_pedido": top, "k": k},
            "conferencias": {"a": sl.resumo_da_resposta(capturas[0]["resposta"]), "b": sl.resumo_da_resposta(capturas[1]["resposta"]),
                             "temperatura": temperatura, "resposta_igual_sem_logprobs": ra["resposta"] == rc["resposta"],
                             "rotulo_lido": c["rotulo"] if c else None, "p_rotulo": c["p_rotulo"] if c else None,
                             "alternativas_na_posicao_do_rotulo": c["alternativas_top"] if c else 0},
            "chamadas": {"a": {**capturas[0], "medicao": {kk: vv for kk, vv in ra.items() if kk != "resposta"}},
                         "b": {**capturas[1], "medicao": {kk: vv for kk, vv in rb.items() if kk != "resposta"}},
                         "c": {"medicao": {kk: vv for kk, vv in rc.items() if kk != "resposta"}, "resposta": rc["resposta"]}}}


def sondagem_aceita(sondagem: dict) -> tuple[bool, list[str]]:
    """A noite pode seguir? Precisa de probabilidade por token, bytes de cada token e texto remontado igual à resposta;
    a probabilidade de depois da temperatura e a resposta diferente sem logprobs viram avisos, não paradas."""
    c = sondagem["conferencias"]
    a = c["a"]
    problemas, avisos = [], []
    if not a.get("tokens_com_logprob"):
        problemas.append("o Ollama não devolveu `logprobs`")
    if not a.get("tem_bytes"):
        problemas.append("os tokens vieram sem `bytes` (um acento partido não se remonta)")
    if not a.get("texto_bate"):
        problemas.append("os tokens não remontam a resposta")
    if a.get("top_por_posicao_max", 0) < 2:
        problemas.append("menos de duas alternativas por posição")
    if c["temperatura"].get("veredito") != "antes":
        avisos.append(f"probabilidade com veredito de temperatura {c['temperatura'].get('veredito')!r} (esperado 'antes')")
    if c.get("resposta_igual_sem_logprobs") is False:
        avisos.append("a resposta com logprobs difere da resposta sem logprobs no mesmo prompt")
    return not problemas, problemas + avisos
