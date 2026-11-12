#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (08/11/2026, Pós-Fase 4, pacote Q3): a ÁRVORE DE DECISÃO de um caso, lida da trilha v2 pelo mesmo
# leitor do relatório v3 (`gerar_relatorio_raciocinio._contexto_v3`, para a trilha não ser lida de dois jeitos) e emitida em Markdown (para o
# analista) e em JSON (para o hub do pacote Q6): um nó por decisão do agente, na ordem em que aconteceram. Decisão 1, o que o modelo lê (o que a
# poda tirou e manteve, e por qual regra em código); Decisão 2, que verbetes entram (os entregues, os que ficaram de fora com a pontuação e o sinal
# que decidiu); Decisão 3, a causa (a escolhida contra a segunda e as demais, a confiança em palavras com a taxa de acerto da faixa na corrida de
# calibração, a evidência citada e a divergência entre o declarado e o conferido); Decisão 4, a cura, quando houver (o candidato aplicado, os
# descartados e o motivo). Cada afirmação leva um rótulo de origem: observado (o código mediu), conferido (o código checou o que o modelo disse),
# declarado (o modelo escreveu, sem garantia) e desconhecido (faltou dado; nunca vira percentual). O que o modelo escreveu fica num bloco à parte,
# rotulado "texto do modelo". `gerar_da_pasta` grava `arvores/` (um .md e um .json por trilha, mais o índice) na pasta de uma corrida, sem tocar
# em nada que já existe nela, e mede cada Markdown com os filtros do pacote Q2 (`filtros_de_texto.py`); `--check` acusa diferença contra o regerado.
# ! Motivo: o plano aprovado da Pós-Fase 4 (seção 3.4) pede a árvore porque o relatório v3 diz o veredito e a evidência, mas não mostra as
# alternativas que o agente tinha em cada passo nem por que ficou com uma delas; e pede os rótulos de origem porque o raciocínio em texto de um
# modelo não é garantia do que ele fez (Turpin et al., 2023; Lanham et al., 2023): a árvore só afirma como "observado" o que o código mediu, e
# a faixa de confiança só ganha um percentual quando a leitura da calibração existe e usa os mesmos cortes desta corrida. Nada aqui chama
# modelo nem muda o prompt, a biblioteca, a busca ou a poda: tudo sai das trilhas gravadas.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python arvore_de_decisao.py --saida fase4_tela_v4 [--check]
  RESULTADOS_DIR=resultados_alvo python arvore_de_decisao.py --saida fase4_tela_v4 --trilha fase4_tela_v4/qwen2.5_7b/lex-1@tela
  python arvore_de_decisao.py --pasta <pasta de uma corrida> [--check] [--calibracao nenhuma]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
from collections import Counter
from pathlib import Path

import biblioteca_leitura as bl
import caminhos
import filtros_de_texto as ft
import gerar_relatorio_raciocinio as grr
import trilha as tr

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    with contextlib.suppress(OSError, ValueError, AttributeError):
        sys.stdout.reconfigure(encoding="utf-8")

VERSAO = 1
PASTA_ARVORES = "arvores"
ROTULOS = ("observado", "conferido", "declarado", "desconhecido")
SIGNIFICADO_DO_ROTULO = {"observado": "o código mediu", "conferido": "o código checou o que o modelo disse",
                         "declarado": "o modelo escreveu, sem garantia", "desconhecido": "faltou dado; nunca vira percentual"}
TEXTO_DO_MODELO = "texto do modelo"
DECISOES = (("leitura", "o que o modelo lê"), ("verbetes", "que verbetes entram"), ("causa", "a causa"), ("cura", "a cura"))
TITULO_DA_DECISAO = dict(DECISOES)
CONFIANCA_EM_PALAVRAS = {"alto": "alta", "medio": "média", "baixo": "baixa"}
ARQ_CALIBRACAO = caminhos.RESULTADOS / "fase4" / "calibracao.json"
ARQ_LIMIARES = caminhos.RESULTADOS / "fase4" / "limiares.json"
# O que cada regra da poda em código faz (poda.podar_arvore e poda.diff_contrato; caso_ao_vivo.diff_referencia), em palavras: singular e plural.
REGRA_DA_PODA_EM_PALAVRAS = {
    "cartoes_omitidos": ("cartão igual omitido (ficam os primeiros e os que contêm o alvo)", "cartões iguais omitidos (ficam os primeiros e os que contêm o alvo)"),
    "imagens_removidas": ("imagem removida", "imagens removidas"),
    "decoracao_removida": ("elemento de decoração removido (separador, moldura ou figura)", "elementos de decoração removidos (separadores, molduras e figuras)"),
    "listas_achatadas": ("lista ou grupo achatado (fica só o conteúdo)", "listas e grupos achatados (fica só o conteúdo)"),
    "textos_sem_letra_removidos": ("texto sem letra nem número removido", "textos sem letra nem número removidos"),
    "interativos_sem_nome_removidos": ("botão ou campo sem nome acessível removido", "botões e campos sem nome acessível removidos"),
    "headings_removidos": ("título abaixo do nível 4 removido fora dos cartões", "títulos abaixo do nível 4 removidos fora dos cartões"),
}
REGRA_DO_CORPO_EM_PALAVRAS = {"diff_contra_contrato": "o contrato esperado pela interface",
                              "diff_contra_referencia": "a resposta da mesma rota em modo normal (a referência)"}
O_QUE_A_PODA_MANTEM = ("os elementos tocados pelo roteiro, os controles com nome acessível, os textos com letra, os títulos até o nível 4 e os marcos "
                       "da página, na forma textual dos casos escritos")
# O significado de cada tipo da taxonomia de falhas da trilha (trilha.TAXONOMIA_DE_FALHAS), para a árvore dizer o código com o significado junto.
FALHA_EM_PALAVRAS = {
    "interceptacao_incompleta": "a interceptação da página não capturou tudo o que a chamada à API trouxe",
    "poda_removeu_evidencia": "a poda em código tirou do texto a evidência de que o diagnóstico precisava",
    "busca_sem_verbete_relevante": "a busca não entregou nenhum verbete que tratasse do caso",
    "prompt_diferente_do_fixo": "o texto entregue ao modelo saiu do molde fixo da corrida",
    "formato_das_quatro_linhas": "a resposta não veio com as quatro linhas pedidas (CAUSA_RAIZ, CAMPO, IMPACTO e FONTE)",
    "rotulo_errado": "a causa respondida não é a do caso",
    "rotulo_fora_da_taxonomia": "a causa respondida está fora das 23 causas permitidas",
    "campo_errado": "o campo apontado não aparece no caso",
    "citacao_fora_do_contexto": "a FONTE cita um verbete que não estava entre os entregues",
    "citacao_inexistente": "a FONTE cita um verbete que não existe na biblioteca",
    "causa_sem_verbete_que_a_trate": "a causa respondida não é tratada por nenhum dos verbetes entregues",
    "candidato_invalido": "o candidato de localizador não passou as verificações em código",
    "candidato_ambiguo": "o candidato de localizador resolve mais de um elemento",
    "reexecucao_falhou": "a reexecução com o localizador novo não levou o roteiro ao fim",
    "acrescimo_recusado_pela_validacao": "o acréscimo proposto à biblioteca foi recusado pelo validador em código",
    "texto_de_origem_proibida": "o texto proposto vem de uma origem que a biblioteca não aceita",
    "incidente": "um incidente do programa que roda os casos interrompeu o passo",
}
GATILHO_EM_PALAVRAS = {"probabilidade": "probabilidade baixa", "fonte_divergente": "FONTE divergente", "amostra": "amostra fixa"}
# As três conferências da FONTE em palavras: por resultado, no singular (um verbete citado) e no plural (vários), para a árvore dizer tudo numa frase só.
REGRA_DA_FONTE_EM_PALAVRAS = {
    "fonte_existe_na_biblioteca": {"confere": ("existe na biblioteca", "existem na biblioteca"), "nao_confere": ("não existe na biblioteca", "não existem na biblioteca")},
    "fonte_estava_no_contexto": {"confere": ("estava entre os entregues ao modelo", "estavam entre os entregues ao modelo"),
                                 "nao_confere": ("não estava entre os entregues ao modelo", "nenhum estava entre os entregues ao modelo")},
    "fonte_contem_termo_da_causa": {"confere": ("traz o termo da causa no texto", "trazem o termo da causa no texto"),
                                    "nao_confere": ("não traz o termo da causa no texto", "nenhum traz o termo da causa no texto")},
}
RESULTADO_EM_PALAVRAS = {"confere": "confere", "nao_confere": "não confere", "nao_se_aplica": "não se aplica",
                         "nao_verificavel": "não dá para conferir por código", "informativo": "só informa", "nao_tentado": "não tentado"}
VERIFICACOES_DA_CURA = ("um elemento só", "visível e habilitado", "mesmo papel", "nome parecido", "efeito na reexecução")


# ------------------------------------------------------------------ as afirmações e os rótulos de origem

def afirmacao(texto: str, origem: str, eventos=()) -> dict:
    """Uma afirmação da árvore com o rótulo de origem; `eventos` são os números (seq) dos eventos da trilha de onde ela saiu.
    Uma afirmação desconhecida nunca leva percentual: faltou dado, e dado que falta não vira número."""
    if origem not in ROTULOS:
        raise ValueError(f"rótulo de origem {origem!r} fora de {ROTULOS}")
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("afirmação sem texto")
    if origem == "desconhecido" and "%" in texto:
        raise ValueError(f"afirmação desconhecida com percentual: {texto!r}")
    return {"texto": texto, "origem": origem, "eventos": [int(s) for s in eventos]}


def _p(v) -> str:
    """Probabilidade com três casas e vírgula (a leitura do primeiro token do rótulo, como o nó a guarda)."""
    return "não registrada" if v is None else grr._num(float(v), 3)


def _pontos(v) -> str:
    return "não registrada" if v is None else grr._num(float(v), 2)


def _n_coisas(n, singular: str, plural: str) -> str:
    try:
        n = int(n)
    except (TypeError, ValueError):
        return f"{n} {plural}"
    return f"{n} {singular if n == 1 else plural}"


def _lista_em_frase(itens: list[str]) -> str:
    itens = [str(i) for i in itens]
    if not itens:
        return "nenhum"
    return " e ".join(itens) if len(itens) < 3 else ", ".join(itens[:-1]) + " e " + itens[-1]


def _cod(valor) -> str:
    return grr._cod(valor)


def _tamanho(d) -> str:
    return grr._tamanho_em_palavras(d)


def _escolha_de(c: dict) -> str | None:
    return c["escolha"]


# ------------------------------------------------------------------ a confiança em palavras

def carregar_calibracao(caminho: Path | None = None) -> dict | None:
    """A leitura da corrida de calibração (`avaliar_fase4.py --calibracao`), de onde sai a taxa de acerto de cada faixa; None se não existir."""
    caminho = Path(caminho) if caminho else ARQ_CALIBRACAO
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else None


def carregar_limiares(caminho: Path | None = None) -> dict | None:
    """Os cortes do selo gravados pela calibração (`limiares.json`); None se não existir."""
    caminho = Path(caminho) if caminho else ARQ_LIMIARES
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else None


def _mesmos_cortes(a: dict | None, b: dict | None) -> bool:
    if not a or not b:
        return False
    for chave in ("baixo_ate", "alto_a_partir_de"):
        try:
            if abs(float(a[chave]) - float(b[chave])) > 1e-9:
                return False
        except (KeyError, TypeError, ValueError):
            return False
    return True


def historico_da_faixa(selo: str | None, calibracao: dict | None, cortes: dict | None) -> dict | None:
    """Quantos casos da corrida de calibração caíram na faixa `selo` e quantos tinham a causa certa (campo `por_selo` da leitura), só quando os
    cortes da calibração são os mesmos desta corrida; sem isso, None (a taxa fica desconhecida, nunca inventada)."""
    if not calibracao or selo is None or not _mesmos_cortes(cortes, calibracao.get("limiares")):
        return None
    for faixa in calibracao.get("por_selo") or []:
        if faixa.get("selo") == selo and faixa.get("casos"):
            casos, certos = int(faixa["casos"]), int(faixa.get("certos", 0))
            return {"casos": casos, "certos": certos, "acerto_pct": round(100 * certos / casos, 1)}
    return None


def confianca_em_palavras(confianca: dict | None, calibracao: dict | None = None, limiares: dict | None = None) -> dict:
    """A confiança do nó de diagnóstico em palavras: alta, média ou baixa pelo selo, a probabilidade lida e os cortes da faixa (observado), e a
    taxa de acerto histórica dessa faixa na corrida de calibração (observado quando a leitura existe com os mesmos cortes; desconhecido, sem
    percentual, quando não). Sem probabilidade lida, tudo fica desconhecido."""
    conf = confianca or {}
    p, selo = conf.get("p_rotulo"), conf.get("selo")
    cortes = conf.get("limiares") or limiares or {}
    palavra = CONFIANCA_EM_PALAVRAS.get(selo)
    saida = {"selo": selo, "palavra": palavra, "p_rotulo": p,
             "cortes": {k: cortes.get(k) for k in ("baixo_ate", "alto_a_partir_de")}, "historico": None, "afirmacoes": []}
    if selo is None or p is None or palavra is None:
        saida["afirmacoes"].append(afirmacao("A probabilidade da causa respondida não foi lida nesta resposta: a confiança fica desconhecida, sem faixa e sem taxa de acerto.",
                                             "desconhecido"))
        return saida
    baixo, alto = cortes.get("baixo_ate"), cortes.get("alto_a_partir_de")
    if baixo is not None and alto is not None:
        faixa = {"alto": f"começa em {_p(alto)}", "medio": f"vai de {_p(baixo)} a {_p(alto)}", "baixo": f"vai até {_p(baixo)}"}[selo]
        saida["afirmacoes"].append(afirmacao(f"Confiança {palavra}: a probabilidade lida na causa respondida foi {_p(p)}, e a faixa {palavra} {faixa} "
                                             "(cortes fixados na calibração).", "observado"))
    else:
        saida["afirmacoes"].append(afirmacao(f"Confiança {palavra}: a probabilidade lida na causa respondida foi {_p(p)}; os cortes das faixas não ficaram registrados na trilha.",
                                             "observado"))
    hist = historico_da_faixa(selo, calibracao, cortes)
    saida["historico"] = hist
    if hist:
        corrida = (calibracao or {}).get("metadados", {}).get("corrida") or "calibração"
        saida["afirmacoes"].append(afirmacao(f"Na corrida de calibração (`{corrida}`), dos {hist['casos']} casos que caíram na faixa {palavra}, o agente acertou a causa em "
                                             f"{hist['certos']} de {hist['casos']}: {grr._num(hist['acerto_pct'], 1)}%.", "observado"))
    else:
        saida["afirmacoes"].append(afirmacao(f"A taxa de acerto histórica da faixa {palavra} é desconhecida: a leitura da calibração não está disponível, "
                                             "ou os cortes desta corrida não são os dela.", "desconhecido"))
    return saida


# ------------------------------------------------------------------ as quatro decisões

def _no_decisao(numero: int, chave: str, escolha, afirmacoes: list[dict], alternativas: list[dict], eventos=(), **extras) -> dict:
    no = {"numero": numero, "chave": chave, "titulo": TITULO_DA_DECISAO[chave], "escolha": escolha, "alternativas": alternativas,
          "afirmacoes": afirmacoes, "eventos": sorted({int(s) for s in eventos})}
    no.update(extras)
    return no


def _decisao_leitura(c: dict) -> dict:
    """Decisão 1: o que o modelo lê. O que a poda tirou e manteve, e por qual regra em código; num caso em texto, o caso escrito inteiro."""
    afs: list[dict] = []
    alternativas: list[dict] = []
    seqs: list[int] = []
    prompt_ev = next((e for e in c["por_tipo"].get("prompt", []) if e["dados"].get("etapa") == "diagnostico"), None)
    if c["eh_texto"]:
        chars = len(c["texto_caso"] or "")
        escolha = f"ler o caso escrito inteiro, como veio ({chars} caracteres)"
        afs.append(afirmacao(f"O caso entrou em texto, sem poda: o modelo leu a requisição, o status, o contrato, o corpo e o sintoma como estavam no caso escrito "
                             f"({chars} caracteres).", "observado", [c["seq"][0]["seq"]]))
        if prompt_ev:
            seqs.append(prompt_ev["seq"])
            afs.append(afirmacao(f"O texto entregue ao modelo, com os verbetes da decisão 2, tem {prompt_ev['dados'].get('chars')} caracteres.", "observado", [prompt_ev["seq"]]))
        return _no_decisao(1, "leitura", escolha, afs, alternativas, seqs)
    partes_da_escolha: list[str] = []
    diferencas: list[dict] = []
    if c["interceptacoes"]:
        chamadas = []
        for n, e in enumerate(c["interceptacoes"]):
            d = e["dados"]
            seqs.append(e["seq"])
            status = grr._status_em_palavras(d.get("status")) if n == 0 else f"status {d.get('status')}"
            chamadas.append(f"`{d.get('metodo')} {d.get('caminho')}` ({status}" + (f", {d['corpo_chars']} caracteres de corpo" if d.get("corpo_chars") is not None else "") + ")")
        afs.append(afirmacao(("A página chamou " if len(chamadas) == 1 else f"A página fez {len(chamadas)} chamadas à API: ") + _lista_em_frase(chamadas) + ".",
                             "observado", [e["seq"] for e in c["interceptacoes"]]))
    for e in c["podas"]:
        d = e["dados"]
        seqs.append(e["seq"])
        alvo, antes, depois = d.get("alvo"), d.get("antes") or {}, d.get("depois") or {}
        regras = d.get("regras") or {}
        if alvo == "arvore":
            partes_da_escolha.append(f"a árvore de acessibilidade podada ({_tamanho(depois)})")
            alternativas += [{"opcao": "a árvore de acessibilidade inteira", "detalhe": _tamanho(antes), "escolhida": False},
                             {"opcao": "a árvore podada", "detalhe": _tamanho(depois), "escolhida": True}]
            afs.append(afirmacao(f"A poda da árvore de acessibilidade da tela levou {_tamanho(antes)} a {_tamanho(depois)}.", "observado", [e["seq"]]))
            tiradas = [_n_coisas(n, *REGRA_DA_PODA_EM_PALAVRAS[r]) for r, n in regras.items() if r in REGRA_DA_PODA_EM_PALAVRAS and n]
            if tiradas:
                afs.append(afirmacao(f"O que saiu, pelas regras em código: {_lista_em_frase(tiradas)}.", "observado", [e["seq"]]))
            else:
                afs.append(afirmacao("Nenhuma regra da poda tirou nó algum desta árvore.", "observado", [e["seq"]]))
            afs.append(afirmacao(f"O que ficou: {O_QUE_A_PODA_MANTEM}.", "observado", [e["seq"]]))
            for x in d.get("diff") or []:
                afs.append(afirmacao(f"A tela comparada com a referência (a mesma página sem falha injetada): esperado {_cod(x.get('esperado'))}, "
                                     f"recebido {_cod(x.get('recebido'))}.", "observado", [e["seq"]]))
                diferencas.append({"alvo": "tela", "onde": "árvore de acessibilidade, contra a referência", "esperado": x.get("esperado"), "recebido": x.get("recebido"), "tipo": x.get("tipo")})
        else:
            nomes = [REGRA_DO_CORPO_EM_PALAVRAS[r] for r in (regras if isinstance(regras, list) else list(regras)) if r in REGRA_DO_CORPO_EM_PALAVRAS]
            contra = _lista_em_frase(nomes) if nomes else "o contrato esperado pela interface"
            partes_da_escolha.append(f"a diferença do corpo da resposta ({_tamanho(depois)})")
            alternativas += [{"opcao": "o corpo da resposta inteiro", "detalhe": _tamanho(antes), "escolhida": False},
                             {"opcao": "a diferença do corpo contra " + contra, "detalhe": _tamanho(depois), "escolhida": True}]
            afs.append(afirmacao(f"A poda do corpo da resposta levou {_tamanho(antes)} a {_tamanho(depois)}: só a diferença contra {contra} vai ao modelo.",
                                 "observado", [e["seq"]]))
            linhas = d.get("diff") or []
            for x in linhas:
                onde = (f"campo {x['campo']}" if x.get("campo") else "corpo inteiro") + (f" (item {x['item']})" if x.get("item") else "")
                diferencas.append({"alvo": "corpo", "onde": onde, "esperado": x.get("esperado"), "recebido": x.get("recebido") if x.get("recebido") is not None else "ausente",
                                   "tipo": x.get("tipo")})
            if linhas:
                afs.append(afirmacao(f"A comparação do corpo achou {_n_coisas(len(linhas), 'diferença', 'diferenças')}" + (f", a primeira no campo `{grr._cel(linhas[0]['campo'])}`" if linhas[0].get("campo") else ", no corpo inteiro")
                                     + " (a tabela das diferenças está abaixo).", "observado", [e["seq"]]))
            else:
                afs.append(afirmacao("A comparação do corpo não achou diferença de campo contra o contrato.", "observado", [e["seq"]]))
    if not c["podas"]:
        afs.append(afirmacao("A trilha não registra poda neste caso: o modelo leu o que a busca e o caso trouxeram, sem corte em código.", "observado"))
    if prompt_ev:
        seqs.append(prompt_ev["seq"])
        afs.append(afirmacao(f"O texto entregue ao modelo, com os verbetes da decisão 2, tem {prompt_ev['dados'].get('chars')} caracteres.", "observado", [prompt_ev["seq"]]))
    escolha = ("mandar ao modelo " + _lista_em_frase(partes_da_escolha) + ", não a página inteira") if partes_da_escolha else "o que a trilha registrou da leitura"
    return _no_decisao(1, "leitura", escolha, afs, alternativas, seqs, diferencas=diferencas)


def _reforcos(item: dict) -> list[tuple[str, float]]:
    saida = []
    for chave, nome in (("reforco_endpoint", "rota"), ("reforco_entidade", "entidade"), ("reforco_status", "status")):
        v = item.get(chave) or 0.0
        if v:
            saida.append((nome, float(v)))
    return saida


def _composicao(item: dict) -> str:
    base = f"{_pontos(item.get('bm25'))} pelas palavras do caso"
    ref = _reforcos(item)
    if not ref:
        return base + ", sem reforço"
    return base + ", mais " + _lista_em_frase([f"{grr._num(v, 1)} por {nome}" for nome, v in ref])


def _frase_dos_reforcos(dentro: list[dict]) -> str:
    """Uma frase só para os três reforços em código e quem os ganhou, um reforço por vez (a conta de cada entregue fica na tabela, para não repetir
    os números)."""
    por_reforco: dict[str, list[str]] = {}
    sem_reforco = []
    for i in dentro:
        nomes = [n for n, _ in _reforcos(i)]
        if not nomes:
            sem_reforco.append(f"`{i['id']}`")
        for n in nomes:
            por_reforco.setdefault(n, []).append(f"`{i['id']}`")
    regra = "os reforços em código (2,0 quando o verbete declara a rota da requisição, 1,0 quando trata da mesma entidade e 1,0 quando cita o status)"
    if not por_reforco:
        return f"A pontuação é só a da busca por palavras no texto do caso: nenhum dos entregues ganhou {regra}."
    artigo = {"rota": "o da rota", "entidade": "o da entidade", "status": "o do status"}
    partes = []
    for k, nome in enumerate(("rota", "entidade", "status")):
        if nome in por_reforco:
            partes.append((f"o reforço da {nome} entrou em " if not partes else f"{artigo[nome]}, em ") + _lista_em_frase(por_reforco[nome]))
    if sem_reforco:
        partes.append(_lista_em_frase(sem_reforco) + (" pontuou" if len(sem_reforco) == 1 else " pontuaram") + " só pelas palavras")
    return f"A pontuação soma a busca por palavras no texto do caso e {regra}: " + "; ".join(partes) + "."


def _decisao_verbetes(c: dict) -> dict:
    """Decisão 2: que verbetes entram. Os entregues com a pontuação repartida, os que ficaram de fora e o sinal que decidiu na fronteira."""
    afs: list[dict] = []
    ev = next(iter(c["por_tipo"].get("candidatos") or []), None)
    entregues = list(c["entregues"])
    if ev is None:
        afs.append(afirmacao("A trilha não registra a busca na biblioteca para este caso.", "desconhecido"))
        return _no_decisao(2, "verbetes", _lista_em_frase([f"`{i}`" for i in entregues]) if entregues else "nenhum verbete", afs, [], (), entregues=entregues)
    d = ev["dados"]
    itens = sorted(d.get("itens") or [], key=lambda i: i.get("posicao", 0))
    k = d.get("k") or len(entregues)
    dentro = [i for i in itens if i.get("escolhido")]
    fora = [i for i in itens if not i.get("escolhido")]
    if not entregues:
        entregues = [i["id"] for i in dentro]
    escolha = f"entregar ao modelo os {len(entregues)} verbetes mais bem pontuados pela busca"
    afs.append(afirmacao(f"A busca pontuou {len(itens)} verbetes da biblioteca e entregou os {len(dentro)} primeiros: "
                         + _lista_em_frase([f"`{i['id']}` ({_pontos(i.get('pontuacao'))})" for i in dentro]) + ".", "observado", [ev["seq"]]))
    if dentro:
        afs.append(afirmacao(_frase_dos_reforcos(dentro), "observado", [ev["seq"]]))
    if fora:
        primeiros = fora[:5]
        afs.append(afirmacao(f"Ficaram de fora {len(fora)} verbetes; os mais perto de entrar: "
                             + _lista_em_frase([f"`{i['id']}` ({_pontos(i.get('pontuacao'))})" for i in primeiros]) + ".", "observado", [ev["seq"]]))
    sinais = d.get("sinais")
    if isinstance(sinais, dict):
        ref_normal = any(isinstance(e["dados"].get("regras"), list) and "diff_contra_referencia" in e["dados"]["regras"] for e in c["podas"])
        termos = sinais.get("termos")
        texto = ("Sinais da consulta, tirados do caso em código: rota " + (f"`{sinais['endpoint']}`" if sinais.get("endpoint") else "nenhuma")
                 + ", entidade " + (f"`{sinais['entidade']}`" if sinais.get("entidade") else "nenhuma")
                 + ", status " + (str(sinais["status"]) if sinais.get("status") is not None else "nenhum")
                 + (f" e {termos} termos de busca" if termos is not None else "")
                 + ", vindos do sintoma, da requisição, do corpo e da comparação do corpo com o contrato"
                 + (" e com a referência" if ref_normal else "") + ".")
        afs.append(afirmacao(texto, "observado", [ev["seq"]]))
    else:
        afs.append(afirmacao("A trilha não guardou os sinais da consulta (rota, entidade, status e termos): não dá para dizer qual sinal decidiu a busca.", "desconhecido", [ev["seq"]]))
    if dentro and fora:
        ultimo, primeiro = dentro[-1], fora[0]
        gap = float(ultimo.get("pontuacao") or 0) - float(primeiro.get("pontuacao") or 0)
        bm_in, bm_out = float(ultimo.get("bm25") or 0), float(primeiro.get("bm25") or 0)
        if bm_in > bm_out:
            texto = (f"Entre o último entregue, `{ultimo['id']}`, e o primeiro de fora, `{primeiro['id']}`, só o texto do caso já punha o primeiro à frente "
                     f"({_pontos(bm_in)} contra {_pontos(bm_out)})"
                     + (f", e os reforços em código levaram a diferença a {_pontos(gap)}" if _reforcos(ultimo) else f"; a diferença final foi {_pontos(gap)}") + ".")
        elif gap > 0:
            texto = (f"Entre o último entregue, `{ultimo['id']}`, e o primeiro de fora, `{primeiro['id']}`, só pelo texto do caso o segundo estaria à frente "
                     f"({_pontos(bm_out)} contra {_pontos(bm_in)}); os reforços em código viraram a ordem, com diferença final de {_pontos(gap)}.")
        else:
            texto = f"O último entregue, `{ultimo['id']}`, e o primeiro de fora, `{primeiro['id']}`, empataram na pontuação; a ordem alfabética do identificador decidiu."
        afs.append(afirmacao(texto, "observado", [ev["seq"]]))
    alternativas = [{"opcao": i["id"], "detalhe": f"posição {i.get('posicao')}, pontuação {_pontos(i.get('pontuacao'))}: {_composicao(i)}", "escolhida": bool(i.get("escolhido")),
                     "pontuacao": i.get("pontuacao"), "posicao": i.get("posicao")} for i in dentro + fora[:5]]
    return _no_decisao(2, "verbetes", escolha, afs, alternativas, [ev["seq"]], entregues=entregues, pontuados=len(itens), k=k,
                       sinais=sinais if isinstance(sinais, dict) else None)


def _verificacoes_por_regra(c: dict) -> dict[str, list[dict]]:
    saida: dict[str, list[dict]] = {}
    for v in c["sem_gabarito"]:
        saida.setdefault(v.get("regra"), []).append(v)
    return saida


def _frase_dos_citados(citados: list[str], por_regra: dict[str, list[dict]]) -> str | None:
    """As três conferências dos verbetes citados na FONTE numa frase só: quando todos têm o mesmo resultado numa regra, a regra sai no plural;
    quando divergem, sai verbete a verbete. Uma frase por verbete repetia as mesmas palavras e reprovava no filtro de repetição do pacote Q2."""
    if not citados:
        return None
    partes = []
    for regra, formas in REGRA_DA_FONTE_EM_PALAVRAS.items():
        res = {}
        for i in citados:
            v = next((x for x in por_regra.get(regra, []) if x.get("alvo") == i), None)
            if v is not None and v.get("resultado") in formas:
                res[i] = v["resultado"]
        if not res:
            continue
        valores = set(res.values())
        if len(valores) == 1:
            r = next(iter(valores))
            partes.append(f"{formas[r][0 if len(citados) == 1 else 1]} ({RESULTADO_EM_PALAVRAS[r]})")
        else:
            partes.append(f"{formas['confere'][0]}: " + "; ".join(f"`{i}` {RESULTADO_EM_PALAVRAS[r]}" for i, r in res.items()))
    if not partes:
        return None
    cabeca = f"Verbete citado `{citados[0]}`: " if len(citados) == 1 else f"Os {len(citados)} verbetes citados (" + _lista_em_frase([f"`{i}`" for i in citados]) + "): "
    return cabeca + ", ".join(partes) + "."


def _decisao_causa(c: dict, calibracao: dict | None, limiares: dict | None) -> dict:
    """Decisão 3: a causa. A escolhida contra a segunda e as demais alternativas, a confiança em palavras, a evidência citada (campo, trecho e
    verbete pela camada de leitura) e a divergência entre o que o modelo declarou e o que o código conferiu."""
    diag = c["diag"]
    afs: list[dict] = []
    seqs: list[int] = []
    if diag is None:
        afs.append(afirmacao("Nenhum nó de diagnóstico nesta trilha: o agente não chamou o modelo para dizer a causa.", "observado"))
        if c["cura"] is not None:
            afs.append(afirmacao("A cura de localizador roda sem modelo; a decisão dela está no bloco seguinte.", "observado"))
        return _no_decisao(3, "causa", None, afs, [], seqs, segunda=None, campo=None, confianca=confianca_em_palavras(None, calibracao, limiares),
                           divergencia=None, falha=None)
    ev_diag = next((e for e in c["nos"] if e["dados"] is diag), None)
    if ev_diag:
        seqs.append(ev_diag["seq"])
    escolha = c["escolha"]
    decl = c["decl"]
    por_regra = _verificacoes_por_regra(c)
    # o que o modelo declarou: a causa e o campo (a causa em palavras fica na linha da escolha, para não repetir)
    if escolha is not None:
        afs.append(afirmacao(f"A linha CAUSA_RAIZ da resposta diz `{grr._cel(escolha)}`.", "declarado"))
    else:
        afs.append(afirmacao("A resposta não trouxe a linha CAUSA_RAIZ: nenhuma causa respondida.", "declarado"))
    campo = c["campo"]
    if campo:
        afs.append(afirmacao(f"O modelo apontou o campo `{grr._cel(campo)}`.", "declarado"))
        for v in por_regra.get("campo_existe_no_caso", []):
            if v.get("resultado") in ("confere", "nao_confere"):
                afs.append(afirmacao(f"`{grr._cel(campo)}` aparece no caso (procurado no contrato, no corpo, na requisição, na árvore e no seletor): "
                                     f"{RESULTADO_EM_PALAVRAS[v['resultado']]}.", "conferido"))
    else:
        afs.append(afirmacao("O modelo não apontou campo (linha CAMPO: nenhum).", "declarado"))
    # a segunda causa e as demais alternativas, com a probabilidade lida
    alternativas_no = sorted(diag.get("alternativas") or [], key=lambda a: -(a.get("escore") if isinstance(a.get("escore"), (int, float)) else -1))
    segunda = grr._segunda(diag)
    p_escolha = grr._escore_da_escolha(diag)
    if segunda is not None:
        sust = segunda.get("sustentada_por")
        frase = (f"A segunda causa, `{grr._cel(segunda['opcao'])}` ({grr._causa_em_palavras(segunda['opcao'], c['leituras'])}), ficou com probabilidade "
                 f"{_p(segunda.get('escore'))} contra {_p(p_escolha)} da escolhida")
        if sust == []:
            frase += "; nenhum verbete entregue a sustenta"
        elif sust:
            frase += "; verbetes entregues que a sustentam: " + _lista_em_frase([f"`{s}`" for s in sust])
        afs.append(afirmacao(frase + ".", "observado", seqs))
    outras = [a for a in alternativas_no if a.get("opcao") not in (escolha, (segunda or {}).get("opcao"))]
    if len(outras) == 1:
        afs.append(afirmacao(f"A outra alternativa lida na resposta, `{grr._cel(outras[0]['opcao'])}`, tem probabilidade {_p(outras[0].get('escore'))}.", "observado", seqs))
    elif outras:
        soma = sum(float(a.get("escore") or 0) for a in outras)
        afs.append(afirmacao(f"As outras {len(outras)} alternativas lidas na resposta somam probabilidade {_p(soma)}; as maiores: "
                             + _lista_em_frase([f"`{grr._cel(a['opcao'])}` ({_p(a.get('escore'))})" for a in outras[:3]]) + ".", "observado", seqs))
    elif segunda is None and escolha is not None:
        afs.append(afirmacao("A trilha não registra alternativa à causa respondida.", "desconhecido", seqs))
    # a confiança em palavras
    confianca = confianca_em_palavras(diag.get("confianca"), calibracao, limiares)
    afs += confianca["afirmacoes"]
    g = diag.get("gatilhos") or {}
    if g:
        partes = [f"{GATILHO_EM_PALAVRAS[k]} {'disparou' if g.get(k) else 'não disparou'}" for k in ("probabilidade", "fonte_divergente", "amostra") if k in g]
        afs.append(afirmacao("Gatilhos de revisão humana: " + "; ".join(partes) + ".", "observado", seqs))
    intervencoes = c["intervencoes"]
    if intervencoes:
        for i in intervencoes:
            afs.append(afirmacao(f"Intervenção `{grr._cel(i.get('tipo'))}`" + (f" no verbete `{grr._cel(i['verbete'])}`" if i.get("verbete") else "")
                                 + f": rótulo {grr._cel(i.get('rotulo_antes'))} antes e {grr._cel(i.get('rotulo_depois'))} depois; {grr._efeito_da_intervencao(i)}.", "conferido"))
    else:
        afs.append(afirmacao(f"Nenhuma intervenção rodou neste caso (modo `{grr._cel(diag.get('modo_de_intervencao') or 'não registrado')}`).", "observado", seqs))
    # a evidência: o trecho medido em código
    por_seq = {e["seq"]: e for e in c["seq"]}
    _, sinal, onde = grr._campo_e_sinal(diag, por_seq)
    if sinal:
        afs.append(afirmacao(f"O sinal medido em código está presente {onde or 'na resposta HTTP'}: {_cod(sinal)}.", "observado",
                             [x["seq"] for x in diag.get("evidencia") or [] if x.get("papel") in ("sinal_em_codigo", "corpo_http", "arvore_podada")]))
    elif c["eh_texto"]:
        dados = c["dados_do_caso"]
        afs.append(afirmacao(f"Não houve diferença medida em código: o caso entrou em texto, e o modelo leu a requisição `{grr._cel(dados.get('requisicao') or 'não informada')}`, "
                             f"o {grr._status_em_palavras(dados.get('status'))} e o corpo como estavam no caso escrito.", "observado"))
    else:
        afs.append(afirmacao("A trilha não aponta um sinal medido em código para esta causa.", "desconhecido", seqs))
    # a evidência: os verbetes citados na FONTE, conferidos, e a leitura de cada um
    fonte = decl.get("fonte")
    citados: list[str] = []
    for d in c["citadas"]:
        if d.get("valor") and d["valor"] not in citados:
            citados.append(d["valor"])
    if fonte is None or fonte.get("ausente"):
        afs.append(afirmacao("A linha FONTE não veio na resposta: nenhum verbete citado.", "declarado"))
    elif citados:
        afs.append(afirmacao("A linha FONTE cita " + _lista_em_frase([f"`{i}`" for i in citados]) + ".", "declarado"))
    else:
        afs.append(afirmacao(f"A linha FONTE veio sem identificador de verbete: {_cod(fonte.get('valor'))}.", "declarado"))
    frase_citados = _frase_dos_citados(citados, por_regra)
    if frase_citados:
        afs.append(afirmacao(frase_citados, "conferido"))
    formato = next(iter(por_regra.get("fonte_formato_valido", [])), None)
    if formato is not None and formato.get("resultado") in ("confere", "nao_confere"):
        afs.append(afirmacao("A FONTE veio no formato pedido, só identificadores entre colchetes." if formato["resultado"] == "confere"
                             else "A FONTE não veio no formato pedido: há texto livre além dos identificadores entre colchetes.", "conferido"))
    sust = next(iter(por_regra.get("rotulo_sustentado_por_verbete_do_contexto", [])), None)
    if sust is not None and sust.get("resultado") in ("confere", "nao_confere"):
        ev_s = sust.get("evidencia") if isinstance(sust.get("evidencia"), dict) else {}
        quais = ev_s.get("verbetes") or []
        afs.append(afirmacao(("Há verbete entregue sobre essa causa: " + _lista_em_frase([f"`{q}`" for q in quais]) + ".") if sust["resultado"] == "confere" and quais
                             else ("Há verbete entregue sobre essa causa." if sust["resultado"] == "confere" else "Nenhum dos verbetes entregues é sobre essa causa."), "conferido"))
    para_ler = citados or ([escolha] if escolha and escolha in (c["leituras"] or {}) else [])
    if len(para_ler) == 1:
        afs.append(afirmacao(f"Leitura do verbete {grr._referencia_do_verbete(para_ler[0], c['leituras'])}.", "observado"))
    elif para_ler:
        afs.append(afirmacao("Camada de leitura de cada verbete citado: " + "; ".join(grr._referencia_do_verbete(i, c["leituras"]) for i in para_ler) + ".", "observado"))
    # a divergência e a falha
    div = diag.get("divergencia") or {}
    if div.get("ha"):
        afs.append(afirmacao("O declarado pelo modelo diverge do conferido pelo código" + (f" (entre {' e '.join(div['entre'])})" if div.get("entre") else "")
                             + (f": {grr._prosa(div['detalhe'])}." if div.get("detalhe") else "."), "conferido", seqs))
    else:
        afs.append(afirmacao("Nenhuma divergência entre o declarado pelo modelo e o conferido pelo código.", "conferido", seqs))
    falha = diag.get("falha")
    if falha:
        afs.append(afirmacao(f"Falha registrada no nó: `{falha}` ({FALHA_EM_PALAVRAS.get(falha, 'tipo fora da lista desta árvore')}; origem na taxonomia da trilha: "
                             f"{tr.origem_da_falha(falha) or 'não prevista'}).", "conferido", seqs))
    julgaveis = [v for v in c["sem_gabarito"] if v.get("resultado") in ("confere", "nao_confere")]
    conferem = sum(1 for v in julgaveis if v["resultado"] == "confere")
    afs.append(afirmacao(f"Conferências em código com veredito: {conferem} de {len(julgaveis)} conferem; a frase de impacto não tem como ser conferida por código.", "conferido", seqs))
    for no_bib in c["nos_bib"]:
        if no_bib.get("operacao") == "correcao":
            afs.append(afirmacao(f"Biblioteca (ciclo de correção): {'corrigido' if no_bib.get('escolha') == 'corrigido' else 'não corrigido'}.", "observado"))
        else:
            afs.append(afirmacao(f"Biblioteca: {len(no_bib.get('aplicadas') or [])} edição(ões) aplicada(s), {len(no_bib.get('para_revisao') or [])} para revisão humana, "
                                 f"{len(no_bib.get('recusadas') or [])} recusada(s).", "observado"))
    alternativas = [{"opcao": a.get("opcao"), "probabilidade": a.get("escore"), "escolhida": a.get("opcao") == escolha,
                     "detalhe": f"probabilidade {_p(a.get('escore'))}; verbetes entregues que a tratam: "
                                + (_lista_em_frase([f"`{s}`" for s in a.get("sustentada_por") or []]) if a.get("sustentada_por") else "nenhum")}
                    for a in alternativas_no]
    return _no_decisao(3, "causa", escolha, afs, alternativas, seqs, segunda=(segunda or {}).get("opcao"), campo=campo, confianca=confianca,
                       divergencia=div if div.get("ha") else None, falha=falha, causa_em_palavras=c["causa_em_palavras"], probabilidade=p_escolha,
                       gatilhos=g or None)


def _detalhe_do_candidato(cand: dict) -> str:
    if not cand.get("gerado"):
        return f"não gerado: {grr._prosa(cand.get('motivo') or 'sem motivo registrado')}"
    partes = ["gerado"]
    partes.append("passou as verificações estáticas" if cand.get("passou_estaticas") else "não passou as verificações estáticas")
    if cand.get("aplicado"):
        partes.append("aplicado: levou o roteiro ao fim na reexecução")
    elif cand.get("reexecutado"):
        partes.append(f"recusado na reexecução: {grr._prosa((cand.get('efeito') or {}).get('detalhe') or 'o roteiro não chegou ao fim')}")
    elif cand.get("passou_estaticas"):
        partes.append(f"não foi tentado: {grr._prosa((cand.get('efeito') or {}).get('detalhe') or 'um candidato anterior já tinha levado o roteiro ao fim')}")
    return "; ".join(partes)


def _decisao_cura(c: dict) -> dict:
    """Decisão 4: a cura de localizador, toda em código: o candidato aplicado, os descartados com o motivo e a reexecução validada."""
    cura = c["cura"]
    no_cura, no_re = c["no_cura"], next((e["dados"] for e in reversed(c["nos"]) if e["dados"].get("decisao") == "reexecucao"), None)
    ev_cura = (c["por_tipo"].get("cura") or [None])[-1]
    seqs = [ev_cura["seq"]] if ev_cura else []
    seqs += [e["seq"] for e in c["nos"] if e["dados"].get("decisao") in ("cura", "reexecucao")]
    afs: list[dict] = []
    cands = cura.get("candidatos") or []
    gerados = [x for x in cands if x.get("gerado")]
    estaticos = [x for x in gerados if x.get("passou_estaticas")]
    ap = cura.get("aplicado") or {}
    afs.append(afirmacao(f"O passo {cura.get('passo')} do roteiro, localizador `{grr._cel(cura.get('localizador'))}`, falhou: o navegador não achou o elemento "
                         "(a mensagem dele está em citação abaixo).", "observado", seqs))
    afs.append(afirmacao(f"Dos {len(cands)} candidatos previstos, {len(gerados)} foram gerados da árvore podada e do alvo da referência, e {len(estaticos)} passaram nas "
                         f"quatro checagens em código (um elemento só, visível e habilitado, mesmo papel e nome parecido acima de {grr._num(cura.get('limiar_nome'), 1)}).",
                         "observado", seqs))
    if cura.get("curado") and ap:
        afs.append(afirmacao(f"Aplicado `{ap.get('estrategia')}` (`{grr._cel(ap.get('seletor'))}`): {grr.ESTRATEGIA_EM_PALAVRAS.get(ap.get('estrategia'), 'estratégia fora da lista desta árvore')}; "
                             f"passou as 5 verificações em código: {_lista_em_frase(list(VERIFICACOES_DA_CURA))}.", "observado", seqs))
        mesmo = cura.get("mesmo_elemento")
        afs.append(afirmacao("A reexecução foi validada: o roteiro chegou ao fim com o localizador novo"
                             + (", e é o mesmo elemento da referência." if mesmo else
                                (", mas resolve outro elemento, não o alvo da referência (regra R3)." if mesmo is False else "; a impressão do elemento não foi comparada com a da referência.")),
                             "observado", seqs))
    else:
        afs.append(afirmacao(f"Nenhum candidato levou o roteiro ao fim; falha registrada: `{grr._cel(cura.get('falha'))}` "
                             f"({FALHA_EM_PALAVRAS.get(cura.get('falha'), 'tipo fora da lista desta árvore')}); {cura.get('reexecucoes', 0)} reexecução(ões).", "observado", seqs))
    nao_tentados = [x for x in estaticos if not x.get("aplicado") and not x.get("reexecutado")]
    recusados = [x for x in gerados if x.get("reexecutado") and not x.get("aplicado")]
    nao_gerados = [x for x in cands if not x.get("gerado")]
    if nao_tentados:
        um = len(nao_tentados) == 1
        afs.append(afirmacao(("Outro candidato, " if um else f"Outros {len(nao_tentados)} candidatos, ") + _lista_em_frase([f"`{x['estrategia']}`" for x in nao_tentados])
                             + (", também passou" if um else ", também passaram") + " nas quatro checagens e não " + ("foi tentado" if um else "foram tentados")
                             + ", porque o primeiro já tinha fechado o roteiro.", "observado", seqs))
    if recusados:
        afs.append(afirmacao(_n_coisas(len(recusados), "Recusado na reexecução", "Recusados na reexecução") + ": "
                             + "; ".join(f"`{x['estrategia']}` ({grr._prosa((x.get('efeito') or {}).get('detalhe') or 'o roteiro não chegou ao fim')})" for x in recusados) + ".",
                             "observado", seqs))
    if nao_gerados:
        afs.append(afirmacao(("Não foi gerado: " if len(nao_gerados) == 1 else "Não foram gerados: ")
                             + "; ".join(f"`{x['estrategia']}` ({grr._prosa(x.get('motivo') or 'sem motivo registrado')})" for x in nao_gerados) + ".", "observado", seqs))
    if cura.get("mttr_s") is not None:
        afs.append(afirmacao(f"Da detecção à reexecução validada: {grr._num(float(cura['mttr_s']), 1)} s.", "observado", seqs))
    div = (no_cura or {}).get("divergencia") or {}
    if div.get("ha"):
        afs.append(afirmacao(f"Divergência registrada no nó da cura: {grr._prosa(div.get('detalhe'))}.", "observado", seqs))
    elif div.get("detalhe"):
        afs.append(afirmacao(f"Sem divergência no nó da cura: {grr._prosa(div['detalhe'])}.", "observado", seqs))
    div_re = (no_re or {}).get("divergencia") or {}
    if div_re.get("ha"):
        afs.append(afirmacao(f"Divergência registrada na reexecução: {grr._prosa(div_re.get('detalhe'))}.", "observado", seqs))
    alternativas = [{"opcao": x["estrategia"], "seletor": x.get("seletor"), "escolhida": bool(x.get("aplicado")), "detalhe": _detalhe_do_candidato(x),
                     "verificacoes_passadas": sum(1 for v in (x.get("verificacoes") or {}).values() if (v or {}).get("resultado") == "confere")} for x in cands]
    escolha = ap.get("estrategia") if cura.get("curado") and ap else "nenhuma"
    return _no_decisao(4, "cura", escolha, afs, alternativas, seqs, seletor=ap.get("seletor") if ap else None, curado=bool(cura.get("curado")),
                       mesmo_elemento=cura.get("mesmo_elemento"), erro=cura.get("erro"), mttr_s=cura.get("mttr_s"), passo=cura.get("passo"),
                       localizador=cura.get("localizador"), divergencia=div if div else None, falha=cura.get("falha"),
                       reexecucao=(no_re or {}).get("escolha"))


# ------------------------------------------------------------------ a árvore de um caso

def _texto_do_modelo(c: dict) -> dict:
    decl, blobs = c["decl"], c["blobs"]
    inf = next((e["dados"] for e in c["por_tipo"].get("inferencia", []) if e["dados"].get("etapa") == "diagnostico"), None)
    resposta = blobs.get(inf["resposta"]) if inf and inf.get("resposta") else None
    rac = next((e["dados"] for e in c["por_tipo"].get("declaracao", []) if e["dados"].get("campo") == "raciocinio"), None)

    def valor(chave: str):
        d = decl.get(chave)
        return None if d is None or d.get("ausente") else d.get("valor")

    return {"rotulo": TEXTO_DO_MODELO, "impacto": valor("impacto"), "fonte": valor("fonte"),
            "raciocinio": (rac.get("valor") or None) if rac and not rac.get("vazio") else None, "resposta": resposta}


def arvore_do_caso(eventos: list[dict], tid: str, pasta_blobs: Path | None = None, leituras: dict | None = None, calibracao: dict | None = None,
                   limiares: dict | None = None, relatorio_v3: str | None = None) -> dict:
    """A árvore de decisão de uma trilha: as decisões na ordem (leitura, verbetes, causa e, quando houver, cura), cada uma com a escolha, as
    alternativas e as afirmações rotuladas; o texto do modelo à parte; e o resumo com a contagem por rótulo."""
    c = grr._contexto_v3(eventos, tid, pasta_blobs, leituras)
    decisoes = [_decisao_leitura(c), _decisao_verbetes(c), _decisao_causa(c, calibracao, limiares)]
    if c["cura"] is not None:
        decisoes.append(_decisao_cura(c))
    rotulos = Counter(a["origem"] for d in decisoes for a in d["afirmacoes"])
    causa = decisoes[2]
    cab = c["cab"]
    resumo = {"decisoes": len(decisoes), "afirmacoes": sum(rotulos.values()), "rotulos": {r: rotulos.get(r, 0) for r in ROTULOS},
              "divergencia": any(bool((d.get("divergencia") or {}).get("ha")) for d in decisoes), "cura": c["cura"] is not None,
              "selo": causa["confianca"]["selo"], "confianca": causa["confianca"]["palavra"], "falha": causa.get("falha") or (decisoes[-1].get("falha") if c["cura"] else None),
              "escolha": c["escolha"], "causa_em_palavras": c["causa_em_palavras"], "campo": c["campo"],
              "nos": Counter(e["dados"].get("decisao") for e in c["nos"])}
    return {"versao": VERSAO, "gerado_por": "arvore_de_decisao.py", "trilha": tid, "nome": grr.nome_do_relatorio(tid), "caso": c["caso_id"],
            "corrida": cab.get("corrida"), "modo": cab.get("modo"), "modelo": cab.get("modelo"), "classe": c["classe"], "nivel": c["nivel"],
            "eventos": {"primeiro": c["seq"][0]["seq"], "ultimo": c["seq"][-1]["seq"], "hash": grr.hash_da_trilha(eventos, tid)},
            "relatorio_v3": relatorio_v3, "rotulos": dict(SIGNIFICADO_DO_ROTULO), "decisoes": decisoes, "texto_do_modelo": _texto_do_modelo(c), "resumo": resumo}


# ------------------------------------------------------------------ o Markdown para o analista

def _frase_com_rotulo(a: dict) -> str:
    texto = a["texto"].rstrip().removesuffix(".")
    return f"- {texto} ({a['origem']})."


def _tabela_de_alternativas(d: dict) -> str:
    alts = d.get("alternativas") or []
    if not alts:
        return ""
    if d["chave"] == "causa":
        cab = ["Alternativa", "Probabilidade lida na causa", "Verbetes entregues que a tratam", "Escolhida"]
        linhas = [[_cod(a.get("opcao")), _p(a.get("probabilidade")), grr._cel(a["detalhe"].split("tratam: ", 1)[-1]), "sim" if a.get("escolhida") else ""] for a in alts]
    elif d["chave"] == "cura":
        cab = ["Candidato", "Seletor", "Verificações que passou", "O que aconteceu", "Aplicado"]
        linhas = [[_cod(a.get("opcao")), _cod(a.get("seletor")) if a.get("seletor") else "não gerado", str(a.get("verificacoes_passadas", 0)), grr._cel(a["detalhe"]),
                   "sim" if a.get("escolhida") else ""] for a in alts]
    else:
        cab = ["Alternativa", "Detalhe", "Escolhida"]
        linhas = [[_cod(a.get("opcao")) if d["chave"] == "verbetes" else grr._cel(a.get("opcao")), grr._cel(a.get("detalhe")), "sim" if a.get("escolhida") else ""] for a in alts]
    return grr._tabela(cab, linhas)


def render_markdown(arvore: dict) -> str:
    """O Markdown da árvore: a legenda dos rótulos, um bloco por decisão (escolha, afirmações rotuladas e a tabela das alternativas), o texto do
    modelo à parte e o rastro com o hash dos eventos."""
    r = arvore["resumo"]
    legenda = "; ".join(f"{rot} ({SIGNIFICADO_DO_ROTULO[rot]})" for rot in ROTULOS)
    partes = [
        ("<!-- ! Alteração de IA - Revisar: árvore de decisão DERIVADA (Pós-Fase 4, pacote Q3), gerada por arvore_de_decisao.arvore_do_caso a partir da trilha v2 do caso; "
         "não editar à mão."),
        ("     ! Motivo: um nó por decisão do agente, na ordem em que aconteceram, com a origem de cada afirmação; nada aqui chama modelo, e o hash no fim prova de que "
         "eventos ela saiu. -->"),
        f"# Árvore de decisão do caso `{arvore['caso']}`",
        "",
        (f"Caso `{arvore['caso']}` da corrida `{arvore['corrida']}`, trilha `{arvore['trilha']}`, modelo `{arvore['modelo']}`. Um bloco por decisão do agente, na ordem em que "
         f"aconteceram. Cada frase termina com a origem entre parênteses: {legenda}. As linhas escritas pelo modelo ficam no bloco \"Texto do modelo\", no fim."),
        "",
        (f"Resumo: {r['decisoes']} decisões e {r['afirmacoes']} afirmações ("
         + ", ".join(f"{n} {rot}" for rot, n in r["rotulos"].items() if n) + "); "
         + ("há divergência entre o declarado e o conferido" if r["divergencia"] else "nenhuma divergência entre o declarado e o conferido")
         + ("; houve cura de localizador" if r["cura"] else "") + (f"; confiança {r['confianca']}" if r.get("confianca") else "") + "."),
        "",
    ]
    for d in arvore["decisoes"]:
        partes += [f"## Decisão {d['numero']}: {d['titulo']}", ""]
        escolha = d.get("escolha")
        if d["chave"] == "causa":
            linha = ("Escolha: " + (f"`{grr._cel(escolha)}` ({d.get('causa_em_palavras')})" if escolha is not None else "nenhuma causa respondida")
                     + (f"; segunda: `{grr._cel(d['segunda'])}`" if d.get("segunda") else "")
                     + (f"; confiança {d['confianca']['palavra']}" if (d.get("confianca") or {}).get("palavra") else "") + ".")
        elif d["chave"] == "cura":
            linha = "Escolha: " + (f"`{grr._cel(escolha)}` (`{grr._cel(d.get('seletor'))}`)" if d.get("curado") else "nenhum candidato aplicado") + "."
        else:
            linha = f"Escolha: {escolha}." if escolha else "Escolha: nada registrado."
        partes += [linha, ""]
        partes += [_frase_com_rotulo(a) for a in d["afirmacoes"]]
        partes.append("")
        if d.get("diferencas"):
            partes += [grr._tabela(["Onde", "Esperado", "Recebido"], [[grr._cel(x["onde"]), grr._cel(x["esperado"]), grr._cel(x["recebido"])] for x in d["diferencas"]]), ""]
        if d["chave"] == "cura" and d.get("erro"):
            partes += ["Mensagem do navegador, como veio:", "", *grr._citacao(d["erro"]), ""]
        tabela = _tabela_de_alternativas(d)
        if tabela:
            partes += [tabela, ""]
    tm = arvore["texto_do_modelo"]
    partes += ["## Texto do modelo", "",
               f"As linhas escritas pelo modelo, como vieram e sem garantia ({TEXTO_DO_MODELO}):", ""]
    partes += grr._citacao("IMPACTO: " + tm["impacto"]) if tm.get("impacto") else ["> a linha IMPACTO não veio na resposta"]
    partes += grr._citacao("FONTE: " + tm["fonte"]) if tm.get("fonte") else ["> a linha FONTE não veio na resposta"]
    if tm.get("raciocinio"):
        partes += ["", "Texto escrito antes das quatro linhas:", "", grr._bloco(tm["raciocinio"])]
    if tm.get("resposta"):
        partes += ["", "Resposta inteira:", "", grr._bloco(tm["resposta"])]
    partes += ["", "## Rastro", "",
               (f"Gerado dos eventos {arvore['eventos']['primeiro']} a {arvore['eventos']['ultimo']} da trilha; hash dos eventos deste caso: `{arvore['eventos']['hash']}` "
                "(a impressão digital destes eventos: muda se um byte deles mudar).")
               + (f" Relatório de defeito do mesmo caso: `{arvore['relatorio_v3']}`." if arvore.get("relatorio_v3") else ""), ""]
    return "\n".join(partes)


# ------------------------------------------------------------------ uma pasta de corrida inteira

def _indice_md(pasta: Path, modo: str | None, arquivo_trilha: str, indice: dict) -> str:
    r = indice["resumo"]
    linhas = [[f"[`{a['nome']}`]({a['nome']}.md)", _cod(a["caso"]), _cod(a["escolha"]) if a.get("escolha") is not None else "nenhuma", a.get("confianca") or "desconhecida",
               "sim" if a["divergencia"] else "não", "sim" if a["cura"] else "não",
               "/".join(str(a["rotulos"].get(rot, 0)) for rot in ROTULOS),
               ("passa" if (a.get("filtros") or {}).get("aprovado") else ("não passa" if a.get("filtros") else "não medido"))] for a in indice["arvores"]]
    return "\n".join([
        "<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por arvore_de_decisao.gerar_da_pasta (Pós-Fase 4, pacote Q3); não editar à mão.",
        "     ! Motivo: uma árvore por caso é ilegível sem a lista que diga a causa, a confiança, a divergência e a cura de cada uma; os outros arquivos da corrida ficam como estavam. -->",
        f"# Árvores de decisão da corrida `{pasta.name}`", "",
        f"{r['trilhas']} árvores geradas da trilha `{arquivo_trilha}`" + (f" (modo `{modo}`)" if modo else "") + f": {r['com_divergencia']} com divergência entre o declarado e o "
        f"conferido, {r['com_cura']} com cura de localizador; {r['afirmacoes']} afirmações ("
        + ", ".join(f"{n} {rot}" for rot, n in r["rotulos"].items() if n) + "). A coluna das afirmações conta " + "/".join(ROTULOS) + ". "
        + (f"Filtros de texto do pacote Q2: {r['filtros']['aprovados']} de {r['filtros']['n']} árvores passam em tudo." if r.get("filtros") else ""), "",
        grr._tabela(["Árvore", "Caso", "Causa escolhida", "Confiança", "Divergência", "Cura", "Afirmações por origem", "Filtros de texto"], linhas), ""])


def _medir_filtros(md: str, limiares_texto: dict | None) -> dict | None:
    if not limiares_texto:
        return None
    medidas = ft.medir(md)
    av = ft.avaliar(medidas, limiares_texto)
    return {"aprovado": av["aprovado"], "alarme_flesch": av["alarme_flesch"], "termos_sem_expansao": av["termos_sem_expansao"], "palavras": medidas["palavras"],
            "reprovou_em": sorted(ch for ch, cr in av["criterios"].items() if cr["passa"] is False)}


def gerar_da_pasta(pasta: Path, leituras: dict | None = None, calibracao: dict | None = None, limiares: dict | None = None, limiares_texto: dict | None = None,
                   check: bool = False) -> dict:
    """Grava (ou, com check, confere) a árvore de cada trilha com nó de decisão da pasta de uma corrida, em `<pasta>/arvores/` (um .md e um .json por
    trilha, mais INDICE.md e INDICE.json), medindo cada Markdown com os filtros do pacote Q2. Nada fora de `arvores/` é tocado.
    Devolve {pasta, gravados: [nomes], diferentes: [nomes que não batem, só com check], indice}."""
    pasta = Path(pasta)
    condicoes = json.loads((pasta / "condicoes_fase4.json").read_text(encoding="utf-8")) if (pasta / "condicoes_fase4.json").exists() else {}
    modo = condicoes.get("modo")
    arquivo_trilha = pasta / f"trilha_{modo}.jsonl" if modo else next(iter(sorted(pasta.glob("trilha_*.jsonl"))), None)
    if arquivo_trilha is None or not arquivo_trilha.exists():
        raise FileNotFoundError(f"trilha da corrida não encontrada em {pasta}")
    eventos = tr.ler(arquivo_trilha)
    cab = next((e["dados"] for e in eventos if e["tipo"] == "corrida"), {})
    destino = pasta / PASTA_ARVORES
    arquivos: dict[str, str] = {}
    entradas = []
    nos_total: Counter = Counter()
    decisoes_total: Counter = Counter()
    rotulos_total: Counter = Counter()
    confiancas: Counter = Counter()
    termos_total: Counter = Counter()
    alarmes = 0
    for tid, seq in tr.por_trilha(eventos).items():
        if not any(e["tipo"] == "decisao" for e in seq):
            continue
        nome = grr.nome_do_relatorio(tid)
        v3 = f"../relatorios_v3/{nome}.md" if (pasta / "relatorios_v3" / f"{nome}.md").exists() else None
        arv = arvore_do_caso(eventos, tid, pasta_blobs=pasta / "blobs", leituras=leituras, calibracao=calibracao, limiares=limiares, relatorio_v3=v3)
        md = render_markdown(arv)
        filtros = _medir_filtros(md, limiares_texto)
        arquivos[f"{nome}.md"] = md
        arquivos[f"{nome}.json"] = json.dumps(arv, ensure_ascii=False, indent=1) + "\n"
        r = arv["resumo"]
        nos_total.update(r["nos"])
        decisoes_total.update(d["chave"] for d in arv["decisoes"])
        rotulos_total.update(r["rotulos"])
        confiancas[r["confianca"] or "desconhecida"] += 1
        if filtros:
            termos_total.update(filtros["termos_sem_expansao"])
            alarmes += bool(filtros["alarme_flesch"])
        entradas.append({"nome": nome, "trilha": tid, "caso": arv["caso"], "classe": arv["classe"], "nivel": arv["nivel"], "escolha": r["escolha"],
                         "causa_em_palavras": r["causa_em_palavras"], "campo": r["campo"], "confianca": r["confianca"], "selo": r["selo"], "divergencia": r["divergencia"],
                         "cura": r["cura"], "falha": r["falha"], "decisoes": r["decisoes"], "afirmacoes": r["afirmacoes"], "rotulos": r["rotulos"], "filtros": filtros,
                         "arquivos": {"md": f"{nome}.md", "json": f"{nome}.json"}, "relatorio_v3": v3, "hash_eventos": arv["eventos"]["hash"]})
    medidas = [e["filtros"] for e in entradas if e["filtros"]]
    indice = {"gerado_por": "arvore_de_decisao.py", "versao": VERSAO, "corrida": cab.get("corrida") or pasta.name, "modo": modo, "trilha": arquivo_trilha.name,
              "modelo": cab.get("modelo"), "hash_prompt_fixo": cab.get("hash_prompt_fixo"), "hash_biblioteca": cab.get("hash_biblioteca"),
              "calibracao": {"corrida": (calibracao or {}).get("metadados", {}).get("corrida"), "disponivel": bool(calibracao)},
              "limiares_texto": {"gerado_em": (limiares_texto or {}).get("metadados", {}).get("gerado_em")} if limiares_texto else None,
              "arvores": entradas,
              "resumo": {"trilhas": len(entradas), "decisoes_por_chave": {k: decisoes_total[k] for k, _ in DECISOES if decisoes_total[k]},
                         "nos_por_decisao": dict(sorted(nos_total.items())), "com_divergencia": sum(1 for e in entradas if e["divergencia"]),
                         "com_cura": sum(1 for e in entradas if e["cura"]), "afirmacoes": sum(rotulos_total.values()),
                         "rotulos": {r: rotulos_total.get(r, 0) for r in ROTULOS}, "por_confianca": dict(sorted(confiancas.items())),
                         "filtros": {"n": len(medidas), "aprovados": sum(1 for m in medidas if m["aprovado"])} if limiares_texto else None,
                         "filtros_detalhe": {"termos_sem_expansao": dict(sorted(termos_total.items())), "alarme_flesch": alarmes,
                                             "reprovaram": [e["nome"] for e in entradas if e["filtros"] and not e["filtros"]["aprovado"]]} if limiares_texto else None}}
    arquivos["INDICE.json"] = json.dumps(indice, ensure_ascii=False, indent=1) + "\n"
    arquivos["INDICE.md"] = _indice_md(pasta, modo, arquivo_trilha.name, indice)
    diferentes = []
    if check:
        diferentes = [n for n, t in arquivos.items() if not (destino / n).exists() or (destino / n).read_text(encoding="utf-8") != t]
    else:
        destino.mkdir(parents=True, exist_ok=True)
        for n, t in arquivos.items():
            (destino / n).write_text(t, encoding="utf-8", newline="\n")
    return {"pasta": destino, "gravados": list(arquivos), "diferentes": diferentes, "indice": indice}


# ------------------------------------------------------------------ linha de comando

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saida", help="a pasta da corrida em RESULTADOS_DIR (ex.: fase4_tela_v4)")
    ap.add_argument("--pasta", help="a pasta da corrida por caminho, no lugar de --saida")
    ap.add_argument("--check", action="store_true", help="regera e compara com o que está gravado em arvores/")
    ap.add_argument("--trilha", help="imprime o Markdown da árvore de uma trilha (id completo) em vez de gravar a pasta")
    ap.add_argument("--calibracao", help="arquivo da leitura da calibração (padrão: resultados_alvo/fase4/calibracao.json); 'nenhuma' desliga a taxa por faixa")
    ap.add_argument("--limiares", help="arquivo dos cortes do selo (padrão: resultados_alvo/fase4/limiares.json)")
    args = ap.parse_args(argv)
    if not args.saida and not args.pasta:
        ap.error("informe --saida <corrida> ou --pasta <pasta>")
    pasta = Path(args.pasta) if args.pasta else caminhos.fase3(args.saida)["raiz"]
    if argv is None:
        print(caminhos.descricao())
    leituras = bl.carregar(bl.PASTA_LEITURA) or None
    if leituras is None:
        print(f"aviso: camada de leitura ausente em {bl.PASTA_LEITURA}; os verbetes saem sem o arquivo de leitura")
    calibracao = None if (args.calibracao or "").lower() == "nenhuma" else carregar_calibracao(args.calibracao)
    limiares = carregar_limiares(args.limiares)
    limiares_texto = ft.carregar_limiares() if ft.ARQ_LIMIARES.exists() else None
    if args.trilha:
        condicoes = json.loads((pasta / "condicoes_fase4.json").read_text(encoding="utf-8")) if (pasta / "condicoes_fase4.json").exists() else {}
        arquivo = pasta / f"trilha_{condicoes.get('modo')}.jsonl" if condicoes.get("modo") else next(iter(sorted(pasta.glob("trilha_*.jsonl"))))
        print(render_markdown(arvore_do_caso(tr.ler(arquivo), args.trilha, pasta_blobs=pasta / "blobs", leituras=leituras, calibracao=calibracao, limiares=limiares)))
        return 0
    r = gerar_da_pasta(pasta, leituras=leituras, calibracao=calibracao, limiares=limiares, limiares_texto=limiares_texto, check=args.check)
    f = r["indice"]["resumo"].get("filtros")
    filtros = f"; filtros de texto: {f['aprovados']} de {f['n']} passam" if f else "; filtros de texto não medidos (limiares_texto.json ausente)"
    if args.check:
        if r["diferentes"]:
            print(f"--check: DIFERE ({len(r['diferentes'])} arquivo(s) fora de dia em {r['pasta']}: {r['diferentes'][:5]})")
            return 1
        print(f"--check: {len(r['gravados'])} arquivos de {r['pasta']} batem com a trilha{filtros}")
        return 0
    print(f"gravado: {len(r['gravados'])} arquivos em {r['pasta']} ({r['indice']['resumo']['trilhas']} árvores{filtros})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
