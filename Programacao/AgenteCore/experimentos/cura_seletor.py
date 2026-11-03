#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (01/11/2026, Fase 4, pacote P4): a cura de seletor do plano aprovado (seção
# 3.6), sem modelo. Entrada: o passo do roteiro que falhou (ação, localizador original), o alvo registrado na corrida de
# referência (papel e nome pela árvore de acessibilidade; tag, atributos, caminho a partir do ancestral com id mais
# próximo, pai e posição entre os irmãos pelo DOM) e a árvore podada atual (`poda.podar_arvore`). Geração em código, na
# ordem fixa: (1) papel e nome iguais; (2) papel igual e nome parecido (texto normalizado, similaridade de
# `difflib.SequenceMatcher` acima de LIMIAR_NOME, fixado aqui e registrado em `condicoes_fase4.json`); (3) texto contido
# (`text=`); (4) `data-id` igual; (5) caminho a partir do ancestral com id; (6) posição entre os irmãos do mesmo papel.
# Verificação em código, na ordem: resolve para exatamente um elemento; visível e habilitado; mesmo papel do alvo; nome
# parecido; o efeito esperado do passo acontece na reexecução (o roteiro inteiro passa com o candidato no lugar do
# localizador). Só o primeiro candidato que passa as quatro verificações estáticas é reexecutado, e a cura "aplicada" é
# a que levou o roteiro ao fim; todos os candidatos ficam no evento `cura` da trilha com o resultado de cada verificação,
# e os nós `cura` e `reexecucao` fecham a decisão (divergência contra o segundo candidato; regra R3: "mesmo elemento"
# contra "outro elemento" pela impressão do DOM, que nenhum modo de quebra muda). O Playwright nunca é importado aqui:
# as funções que o usam recebem a página pronta, e as puras rodam nos testes sem navegador.
# ! Motivo: o projeto ABNT (§2.1) e a decisão 79 fixam que o agente não altera a aplicação: a cura é de localizador,
# aplicada só na reexecução de verificação e apresentada como sugestão; sem a ordem fixa e a verificação em código, a
# taxa de cura da corrida 19 não seria auditável nem reproduzível (plano, P4, "onde a geração em código falha").
"""Cura de seletor da Fase 4 (pacote P4): candidatos em ordem fixa, verificação em código e a escolha do primeiro que passa."""
from __future__ import annotations

import difflib
import json
import re
import unicodedata

import navegador
import trilha as tr

LIMIAR_NOME = 0.6
ESTRATEGIAS = ("papel_e_nome", "papel_e_nome_parecido", "texto_contido", "data_id", "caminho_do_ancestral_com_id", "posicao_entre_irmaos")
DESCRICAO_DA_ESTRATEGIA = {
    "papel_e_nome": "papel e nome iguais aos do alvo (na mesma ocorrência)",
    "papel_e_nome_parecido": "papel igual e nome parecido, pelo texto normalizado acima do limiar",
    "texto_contido": "qualquer elemento cujo texto contém o texto do alvo",
    "data_id": "elemento com o mesmo data-id do alvo",
    "caminho_do_ancestral_com_id": "o caminho do alvo a partir do ancestral com id mais próximo (ou do body)",
    "posicao_entre_irmaos": "o elemento do mesmo papel na mesma posição dentro do pai do alvo",
}
VERIFICACOES = ("resolve_um_elemento", "visivel_e_habilitado", "mesmo_papel", "nome_parecido", "efeito_na_reexecucao")
DESCRICAO_DA_VERIFICACAO = {
    "resolve_um_elemento": "resolve para exatamente um elemento",
    "visivel_e_habilitado": "o elemento está visível e habilitado",
    "mesmo_papel": "o papel na árvore de acessibilidade é o do alvo",
    "nome_parecido": "o nome acessível é parecido com o do alvo (acima do limiar)",
    "efeito_na_reexecucao": "o roteiro inteiro passa na reexecução com o candidato no lugar do localizador",
}
FALHAS = ("candidato_invalido", "candidato_ambiguo", "reexecucao_falhou")      # trilha.TAXONOMIA_DE_FALHAS["cura"]
# o que nenhum modo de quebra muda: decide "mesmo elemento" contra "outro elemento" (regra R3)
CAMPOS_DA_IMPRESSAO = ("tag", "type", "name", "form_action", "data_nome", "href")

_LINHA_PODADA = re.compile(r'^(?P<papel>[a-z][\w-]*)(?: "(?P<nome>(?:[^"\\]|\\.)*)")?(?P<resto>.*)$')
_ATRIBUTO = re.compile(r'([\w-]+)="([^"]*)"')


# ------------------------------------------------------------------ texto

def normalizar(texto) -> str:
    """Minúsculas, sem acento e com os espaços colapsados: é o texto que as comparações de nome usam."""
    base = unicodedata.normalize("NFKD", str(texto or ""))
    sem_acento = "".join(ch for ch in base if not unicodedata.combining(ch))
    return " ".join(sem_acento.lower().split())


def similaridade(a, b) -> float:
    """Razão de `difflib.SequenceMatcher` entre os dois textos normalizados (1,0 iguais; 0,0 sem nada em comum), tomada
    nas duas ordens e ficando a maior: a conta do SequenceMatcher não é simétrica ("Ver detalhes" contra "Saiba Mais..."
    dá 0,24 numa ordem e 0,08 na outra, medido em 01/11/2026), e o limiar precisa valer igual dos dois lados."""
    na, nb = normalizar(a), normalizar(b)
    if not na and not nb:
        return 1.0
    if not na or not nb:
        return 0.0
    return max(difflib.SequenceMatcher(None, na, nb).ratio(), difflib.SequenceMatcher(None, nb, na).ratio())


def _aspas(texto: str) -> str:
    """O valor do atributo `name` no seletor `role=`: entre aspas duplas, ou simples quando o nome tem aspas duplas."""
    if '"' in texto:
        return "'" + texto.replace("'", "\\'") + "'"
    return '"' + texto + '"'


# ------------------------------------------------------------------ a árvore podada

def nos_da_arvore_podada(arvore) -> list[dict]:
    """As linhas da árvore podada (texto de `poda.podar_arvore` ou a lista de linhas) como nós: papel, nome, atributos
    (`class="..."`, `data-id="..."`, `level=3`, `disabled`) e a linha original."""
    linhas = arvore.splitlines() if isinstance(arvore, str) else list(arvore)
    nos = []
    for bruta in linhas:
        linha = bruta.strip()
        if not linha:
            continue
        m = _LINHA_PODADA.match(linha)
        if not m:
            continue
        atributos = dict(_ATRIBUTO.findall(m.group("resto") or ""))
        for parte in _ATRIBUTO.sub("", m.group("resto") or "").split():
            chave, _, valor = parte.partition("=")
            atributos[chave] = valor if valor else "true"
        nos.append({"papel": m.group("papel"), "nome": (m.group("nome") or "").replace('\\"', '"'), "atributos": atributos, "linha": bruta})
    return nos


# ------------------------------------------------------------------ candidatos, na ordem fixa

def _cand(estrategia: str, cadeia: list[str], nth: int | None, motivo: str, nome_encontrado: str | None = None,
          similaridade_: float | None = None) -> dict:
    c = {"estrategia": estrategia, "gerado": True, "motivo": motivo, "cadeia": list(cadeia), "nth": nth, "seletor": None,
         "nome_encontrado": nome_encontrado, "similaridade": similaridade_}
    c["seletor"] = seletor_de(c)
    return c


def _nao(estrategia: str, motivo: str, similaridade_: float | None = None) -> dict:
    return {"estrategia": estrategia, "gerado": False, "motivo": motivo, "cadeia": [], "nth": None, "seletor": None,
            "nome_encontrado": None, "similaridade": similaridade_}


def _nth(quantos_na_arvore: int, ocorrencia: int) -> int | None:
    """Sem `nth` quando a árvore mostra um só e o alvo era o primeiro; senão a ocorrência da referência (a partir de 0)."""
    return None if quantos_na_arvore <= 1 and ocorrencia <= 1 else max(0, ocorrencia - 1)


def seletor_de(candidato: dict) -> str | None:
    """O seletor do Playwright, legível: as partes da cadeia unidas por ` >> ` e o `nth=` no fim."""
    if not candidato.get("cadeia"):
        return None
    texto = " >> ".join(candidato["cadeia"])
    return texto + (f" >> nth={candidato['nth']}" if candidato.get("nth") is not None else "")


def gerar_candidatos(alvo: dict, arvore_podada, limiar: float = LIMIAR_NOME) -> list[dict]:
    """Os seis candidatos, na ordem fixa do plano (seção 3.6), gerados do alvo da referência e da árvore podada atual.
    Cada um diz se foi gerado e por quê (ou por que não); a lista tem sempre as seis estratégias, para o relatório."""
    # a linha `document "<título>"` é o título da página, não um elemento: fica fora das três estratégias por nome e texto
    nos = [n for n in nos_da_arvore_podada(arvore_podada) if n["papel"] != "document"]
    papel = alvo.get("papel") or ""
    nome = alvo.get("nome") or ""
    texto = alvo.get("texto") or ""
    ocorrencia = int(alvo.get("ocorrencia") or 1)
    atributos = alvo.get("atributos") or {}
    saida: list[dict] = []
    # (1) papel e nome iguais
    iguais = [n for n in nos if n["papel"] == papel and normalizar(n["nome"]) == normalizar(nome)] if nome else []
    if iguais:
        saida.append(_cand("papel_e_nome", [f"role={papel}[name={_aspas(nome)}]"], _nth(len(iguais), ocorrencia),
                           f'a árvore podada tem {len(iguais)} {papel} "{nome}"; o alvo era a ocorrência {ocorrencia}'))
    else:
        saida.append(_nao("papel_e_nome", f'a árvore podada não tem {papel} "{nome}"' if nome else "o alvo da referência não tem nome acessível"))
    # (2) papel igual e nome parecido
    mesmo_papel = [n for n in nos if n["papel"] == papel and n["nome"] and normalizar(n["nome"]) != normalizar(nome)]
    melhor = max(mesmo_papel, key=lambda n: similaridade(nome, n["nome"]), default=None) if nome else None
    sim = similaridade(nome, melhor["nome"]) if melhor else 0.0
    if melhor and sim >= limiar:
        repetidos = [n for n in mesmo_papel if normalizar(n["nome"]) == normalizar(melhor["nome"])]
        saida.append(_cand("papel_e_nome_parecido", [f"role={papel}[name={_aspas(melhor['nome'])}]"], _nth(len(repetidos), ocorrencia),
                           f'{papel} "{melhor["nome"]}" é parecido com "{nome}" (similaridade {sim:.2f}, limiar {limiar})', melhor["nome"], round(sim, 3)))
    else:
        saida.append(_nao("papel_e_nome_parecido", f'nenhum {papel} da árvore podada tem nome parecido com "{nome}" acima do limiar {limiar}'
                          + (f' (o mais próximo, "{melhor["nome"]}", fica em {sim:.2f})' if melhor else ""), round(sim, 3) if melhor else None))
    # (3) texto contido
    if texto.strip():
        contem = [n for n in nos if normalizar(texto) in normalizar(n["nome"])]
        if contem:
            saida.append(_cand("texto_contido", [f"text={texto}"], _nth(len(contem), ocorrencia),
                               f'{len(contem)} nó(s) da árvore podada contêm o texto "{texto}"'))
        else:
            saida.append(_nao("texto_contido", f'nenhum nó da árvore podada contém o texto "{texto}"'))
    else:
        saida.append(_nao("texto_contido", "o alvo da referência não tem texto visível"))
    # (4) data-id igual
    data_id = atributos.get("data-id")
    if data_id not in (None, ""):
        tag = alvo.get("tag") or "*"
        na_arvore = any(str(n["atributos"].get("data-id")) == str(data_id) for n in nos)
        saida.append(_cand("data_id", [f'{tag}[data-id="{data_id}"]'], None,
                           f'a árvore podada mostra um nó com data-id="{data_id}"' if na_arvore else f'a árvore podada não mostra data-id="{data_id}"; o candidato tenta o DOM'))
    else:
        saida.append(_nao("data_id", "o alvo da referência não tem data-id"))
    # (5) caminho a partir do ancestral com id mais próximo
    caminho = alvo.get("caminho")
    if caminho:
        ancestral = alvo.get("ancestral_com_id")
        saida.append(_cand("caminho_do_ancestral_com_id", [caminho], None,
                           f"caminho registrado na referência a partir de #{ancestral}" if ancestral else "sem ancestral com id na referência: o caminho parte do body"))
    else:
        saida.append(_nao("caminho_do_ancestral_com_id", "a referência não registrou o caminho do alvo"))
    # (6) posição entre os irmãos do mesmo papel
    pai, posicao = alvo.get("pai"), alvo.get("posicao_entre_irmaos")
    if pai and posicao:
        saida.append(_cand("posicao_entre_irmaos", [pai, f"role={papel}"], max(0, int(posicao) - 1),
                           f"o {posicao}º {papel} dentro de {pai}, como na referência"))
    else:
        saida.append(_nao("posicao_entre_irmaos", "a referência não registrou o pai ou a posição do alvo"))
    return saida


# ------------------------------------------------------------------ verificação em código

def _v(resultado: str, detalhe: str, **extras) -> dict:
    return {"resultado": resultado, "detalhe": detalhe, **extras}


def verificar_candidato(resolucao: dict, alvo: dict, limiar: float = LIMIAR_NOME) -> dict:
    """As quatro verificações estáticas sobre o que o candidato resolveu na página (`resolucao`: contagem, visivel,
    habilitado, papel, nome), na ordem fixa, mais a quinta como "não tentada"; `passou_estaticas` e a falha da taxonomia
    (`candidato_ambiguo` quando resolve mais de um; `candidato_invalido` nos outros casos)."""
    n = int(resolucao.get("contagem") or 0)
    v: dict = {}
    if n == 1:
        v["resolve_um_elemento"] = _v("confere", "1 elemento")
        visivel, habilitado = bool(resolucao.get("visivel")), bool(resolucao.get("habilitado"))
        if visivel and habilitado:
            v["visivel_e_habilitado"] = _v("confere", "visível e habilitado")
        else:
            v["visivel_e_habilitado"] = _v("nao_confere", "; ".join(x for x, ok in (("não visível", not visivel), ("não habilitado", not habilitado)) if ok))
        papel = resolucao.get("papel")
        v["mesmo_papel"] = _v("confere" if papel == alvo.get("papel") else "nao_confere",
                              f"papel {papel!r}, esperado {alvo.get('papel')!r}" if papel != alvo.get("papel") else f"papel {papel!r}")
        sim = similaridade(alvo.get("nome") or "", resolucao.get("nome") or "")
        v["nome_parecido"] = _v("confere" if sim >= limiar else "nao_confere",
                                f'"{resolucao.get("nome") or ""}" contra "{alvo.get("nome") or ""}": similaridade {sim:.2f} (limiar {limiar})', similaridade=round(sim, 3))
    else:
        v["resolve_um_elemento"] = _v("nao_confere", "nenhum elemento" if n == 0 else f"{n} elementos")
        for chave in ("visivel_e_habilitado", "mesmo_papel", "nome_parecido"):
            v[chave] = _v("nao_se_aplica", "sem um elemento só para conferir")
    v["efeito_na_reexecucao"] = _v("nao_tentado", "só é medido quando o candidato passa as quatro verificações estáticas")
    passou = all(v[k]["resultado"] == "confere" for k in VERIFICACOES[:4])
    v["passou_estaticas"] = passou
    v["falha"] = None if passou else ("candidato_ambiguo" if n > 1 else "candidato_invalido")
    return v


def mesmo_elemento(impressao_a: dict | None, impressao_b: dict | None) -> bool | None:
    """A impressão do DOM (tag, type, name, action do formulário, data-nome, href) é a mesma? None sem uma das duas."""
    if not impressao_a or not impressao_b:
        return None
    return all((impressao_a.get(k) or None) == (impressao_b.get(k) or None) for k in CAMPOS_DA_IMPRESSAO)


# ------------------------------------------------------------------ a escolha: o primeiro que passa

def _n_passadas(c: dict) -> int:
    v = c.get("verificacoes") or {}
    n = sum(1 for k in VERIFICACOES[:4] if (v.get(k) or {}).get("resultado") == "confere")
    return n + (1 if (c.get("efeito") or {}).get("resultado") == "confere" else 0)


def escolher(candidatos: list[dict], resolver, reexecutar, alvo: dict, limiar: float = LIMIAR_NOME) -> dict:
    """Verifica cada candidato gerado na página (`resolver(candidato)` devolve a resolução) e reexecuta, na ordem fixa, só
    os que passam as quatro verificações estáticas (`reexecutar(candidato)` devolve passou, detalhe, mesmo_elemento),
    parando no primeiro que leva o roteiro ao fim. Devolve a lista completa, o aplicado, o segundo candidato (o que
    disputou com o aplicado), as contagens e a falha da taxonomia quando não houve cura."""
    saida: list[dict] = []
    aplicado = None
    reexecucoes = 0
    mesmo = None
    for c in candidatos:
        item = {**c, "verificacoes": None, "passou_estaticas": False, "reexecutado": False,
                "efeito": _v("nao_tentado", "candidato não gerado" if not c.get("gerado") else "não passou as verificações estáticas"), "aplicado": False, "falha": None}
        if c.get("gerado"):
            v = verificar_candidato(resolver(c), alvo, limiar)
            item["verificacoes"] = {k: v[k] for k in VERIFICACOES}
            item["passou_estaticas"], item["falha"] = v["passou_estaticas"], v["falha"]
            if v["passou_estaticas"] and aplicado is None:
                r = reexecutar(c)
                reexecucoes += 1
                item["reexecutado"] = True
                item["efeito"] = _v("confere" if r.get("passou") else "nao_confere", str(r.get("detalhe") or ""), segundos=r.get("segundos"))
                item["verificacoes"]["efeito_na_reexecucao"] = {"resultado": item["efeito"]["resultado"], "detalhe": item["efeito"]["detalhe"]}
                if r.get("passou"):
                    item["aplicado"] = True
                    mesmo = r.get("mesmo_elemento")
                    item["impressao"] = r.get("impressao")
                    aplicado = item
                else:
                    item["falha"] = "reexecucao_falhou"
            elif v["passou_estaticas"]:
                item["efeito"] = _v("nao_tentado", "passou as verificações estáticas, mas um candidato anterior já tinha levado o roteiro ao fim")
        saida.append(item)
    if aplicado is None:
        falha = "reexecucao_falhou" if reexecucoes else ("candidato_ambiguo" if any(c.get("falha") == "candidato_ambiguo" for c in saida)
                                                        else ("candidato_invalido" if any(c.get("gerado") for c in saida) else "candidato_invalido"))
    else:
        falha = None
    return {"candidatos": saida, "aplicado": aplicado, "segundo": segundo_candidato(saida, aplicado), "curado": aplicado is not None,
            "mesmo_elemento": mesmo, "reexecucoes": reexecucoes, "falha": falha, "resultado": "cura_aplicada" if aplicado else "sem_cura"}


def segundo_candidato(candidatos: list[dict], aplicado: dict | None) -> dict | None:
    """O candidato que disputou com o aplicado: o último que passou as estáticas e foi recusado na reexecução antes dele,
    ou o primeiro depois dele que passou as estáticas sem ser tentado; sem cura, o último recusado na reexecução.
    None quando nenhum outro candidato passou as verificações estáticas."""
    outros = [c for c in candidatos if c.get("passou_estaticas") and c is not aplicado]
    if not outros:
        return None
    recusados = [c for c in outros if c.get("reexecutado")]
    if recusados:
        return recusados[-1]
    return outros[0]


def _rotulo(c: dict | None) -> str:
    return f"`{c['estrategia']}` ({c.get('seletor')})" if c else "nenhum"


def contraste_da_cura(resultado: dict) -> str:
    """Esta e não a segunda: por que o candidato aplicado, e não o segundo, é o que vale (molde em código)."""
    ap, seg = resultado.get("aplicado"), resultado.get("segundo")
    gerados = [c for c in resultado.get("candidatos") or [] if c.get("gerado")]
    if ap and seg:
        if seg.get("reexecutado"):
            motivo = f"foi recusado na reexecução: {(seg.get('efeito') or {}).get('detalhe') or 'o roteiro não chegou ao fim'}"
        else:
            motivo = "também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim"
        return f"{_rotulo(ap)} e não {_rotulo(seg)}: o segundo {motivo}."
    if ap:
        return f"{_rotulo(ap)} e não os outros {len(gerados) - 1} candidatos gerados: nenhum outro passou as quatro verificações estáticas."
    if seg:
        return f"Nenhum candidato levou o roteiro ao fim; o que chegou mais perto foi {_rotulo(seg)}, recusado na reexecução."
    return "Nenhum candidato passou as verificações estáticas: não houve o que reexecutar."


# ------------------------------------------------------------------ os eventos da trilha v2

def evento_de_cura(resultado: dict, alvo: dict, localizador: str, passo: int, erro: str | None, deteccao: str | None, validacao: str | None,
                   mttr_s: float | None, limiar: float = LIMIAR_NOME) -> dict:
    """Os dados do evento `cura` da trilha: o passo e o localizador que falharam, o alvo da referência, o limiar, todos os
    candidatos com o resultado de cada verificação, o aplicado, a cura e o MTTR (da detecção à reexecução validada)."""
    ap = resultado.get("aplicado")
    return {"localizador": localizador, "passo": passo, "erro": erro, "alvo": alvo, "limiar_nome": limiar, "estrategias": list(ESTRATEGIAS),
            "verificacoes": list(VERIFICACOES), "candidatos": [dict(c) for c in resultado["candidatos"]],
            "aplicado": {"estrategia": ap["estrategia"], "seletor": ap.get("seletor")} if ap else None,
            "segundo": {"estrategia": resultado["segundo"]["estrategia"], "seletor": resultado["segundo"].get("seletor")} if resultado.get("segundo") else None,
            "curado": bool(resultado.get("curado")), "mesmo_elemento": resultado.get("mesmo_elemento"), "reexecucoes": resultado.get("reexecucoes", 0),
            "falha": resultado.get("falha"), "resultado": resultado.get("resultado"), "deteccao": deteccao, "validacao": validacao, "mttr_s": mttr_s}


def no_de_cura(resultado: dict, seq_cura: int, seq_poda: int | None = None, justificativa: str | None = None) -> dict:
    """O nó de decisão `cura`: cada candidato gerado é uma alternativa com o escore (verificações passadas, de 0 a 5), a
    escolha é a estratégia aplicada (ou "nenhuma"), a evidência aponta o evento `cura` e a poda da árvore, e a
    divergência é contra o segundo candidato."""
    gerados = [c for c in resultado["candidatos"] if c.get("gerado")]
    alternativas = [{"opcao": c["estrategia"], "escore": _n_passadas(c), "seletor": c.get("seletor"), "aplicado": bool(c.get("aplicado"))} for c in gerados]
    ap, seg = resultado.get("aplicado"), resultado.get("segundo")
    escolha = ap["estrategia"] if ap else "nenhuma"
    if not ap:
        alternativas.append({"opcao": "nenhuma", "escore": 0})
    if ap and seg:
        if seg.get("reexecutado"):
            detalhe = (f"o aplicado foi {_rotulo(ap)}; o segundo candidato, {_rotulo(seg)}, passou as verificações estáticas mas foi recusado na reexecução "
                       f"({(seg.get('efeito') or {}).get('detalhe')}): as verificações estáticas não bastaram para decidir")
        else:
            detalhe = (f"o aplicado foi {_rotulo(ap)}; o segundo candidato, {_rotulo(seg)}, também passou as verificações estáticas e não foi tentado: "
                       "a ordem fixa decidiu, não a verificação")
        divergencia = {"ha": True, "entre": ["programa", "verificacao"], "detalhe": detalhe}
    elif ap:
        divergencia = {"ha": False, "entre": [], "detalhe": f"só {_rotulo(ap)} passou as verificações estáticas; não houve segundo candidato"}
    else:
        divergencia = {"ha": True, "entre": ["programa", "verificacao"],
                       "detalhe": "nenhum candidato levou o roteiro ao fim" + (f"; o segundo candidato, {_rotulo(seg)}, foi recusado na reexecução" if seg else
                                                                                "; nenhum passou as verificações estáticas")}
    evidencia = [{"seq": seq_cura, "papel": "candidato_de_seletor"}]
    if seq_poda:
        evidencia.append({"seq": seq_poda, "papel": "arvore_podada"})
    return tr.no_de_decisao("cura", escolha, alternativas, evidencia, resultado=resultado.get("resultado"), divergencia=divergencia,
                            contraste=contraste_da_cura(resultado), justificativa=justificativa, falha=resultado.get("falha"),
                            prov={"used": [c["estrategia"] for c in gerados], "wasDerivedFrom": [], "wasGeneratedBy": seq_cura})


def no_de_reexecucao(resultado: dict, seq_cura: int, seqs_verificacoes=()) -> dict:
    """O nó de decisão `reexecucao`: validada ou falhou; a evidência aponta o evento `cura` e as conferências do roteiro
    reexecutado; a divergência marca o caso em que outro elemento, não o alvo da referência, fez o roteiro passar (R3)."""
    curado = bool(resultado.get("curado"))
    mesmo = resultado.get("mesmo_elemento")
    ap = resultado.get("aplicado")
    if curado and mesmo is False:
        divergencia = {"ha": True, "entre": ["programa", "verificacao"],
                       "detalhe": f"o roteiro passou com outro elemento, não o alvo da referência (regra R3): {_rotulo(ap)} resolve um elemento com outra impressão do DOM"}
    elif curado:
        divergencia = {"ha": False, "entre": [], "detalhe": "o roteiro passou e o elemento é o mesmo da referência" if mesmo else "o roteiro passou; a impressão do elemento não foi comparada"}
    else:
        divergencia = {"ha": True, "entre": ["programa", "verificacao"],
                       "detalhe": "a reexecução não levou o roteiro ao fim" if resultado.get("reexecucoes") else "nenhum candidato chegou à reexecução"}
    evidencia = [{"seq": seq_cura, "papel": "candidato_de_seletor"}] + [{"seq": int(s), "papel": "sinal_em_codigo"} for s in seqs_verificacoes]
    resultado_ = "roteiro_concluido" if curado else ("roteiro_falhou" if resultado.get("reexecucoes") else "sem_candidato")
    falha = None if curado else ("reexecucao_falhou" if resultado.get("reexecucoes") else resultado.get("falha"))
    return tr.no_de_decisao("reexecucao", "validada" if curado else "falhou", [{"opcao": "validada"}, {"opcao": "falhou"}], evidencia,
                            resultado=resultado_, divergencia=divergencia, falha=falha,
                            prov={"used": [ap["estrategia"]] if ap else [], "wasDerivedFrom": [], "wasGeneratedBy": seq_cura},
                            extras={"mesmo_elemento": mesmo})


# ------------------------------------------------------------------ no navegador (a página do Playwright chega pronta)

JS_DESCREVER = r"""
(el) => {
  const atributos = {};
  for (const a of ['id', 'class', 'data-id', 'name', 'type', 'value', 'placeholder', 'aria-label', 'href', 'title', 'data-nome']) atributos[a] = el.getAttribute(a);
  const tag = el.tagName.toLowerCase();
  const nthOfType = (e) => { let i = 1; let s = e; while ((s = s.previousElementSibling)) { if (s.tagName === e.tagName) i++; } return i; };
  const passo = (e) => e.tagName.toLowerCase() + ':nth-of-type(' + nthOfType(e) + ')';
  // o papel pelo atributo role ou pela tag (o mesmo que o seletor role= do Playwright usa): a posição entre os irmãos conta
  // os irmãos anteriores do mesmo papel, porque o candidato (6) é "role=<papel> >> nth=<posição - 1>" dentro do pai
  const papelDe = (e) => {
    const r = e.getAttribute('role'); if (r) return r;
    const tg = e.tagName.toLowerCase();
    if (tg === 'a') return e.hasAttribute('href') ? 'link' : null;
    if (tg === 'button') return 'button';
    if (tg === 'select') return 'combobox';
    if (tg === 'textarea') return 'textbox';
    if (tg === 'input') { const ty = (e.getAttribute('type') || 'text').toLowerCase(); if (ty === 'search') return 'searchbox'; if (ty === 'checkbox') return 'checkbox';
      if (ty === 'radio') return 'radio'; if (['submit', 'button', 'reset', 'image'].includes(ty)) return 'button'; if (ty === 'hidden') return null; return 'textbox'; }
    return tg;
  };
  const posicaoPeloPapel = (e) => { const meu = papelDe(e); let i = 1; let s = e; while ((s = s.previousElementSibling)) { if (papelDe(s) === meu) i++; } return i; };
  const partes = []; let ancestral = null; let atual = el;
  while (atual && atual !== document.body) {
    partes.unshift(passo(atual));
    const pai = atual.parentElement;
    if (pai && pai !== document.body && pai.id) { ancestral = pai.id; break; }
    atual = pai;
  }
  const raiz = ancestral ? '#' + CSS.escape(ancestral) : 'body';
  const caminho = partes.length ? raiz + ' > ' + partes.join(' > ') : raiz;
  const pai = partes.length > 1 ? raiz + ' > ' + partes.slice(0, -1).join(' > ') : raiz;
  const form = el.closest('form');
  const texto = ((tag === 'input' ? (el.value || '') : (el.innerText || el.textContent || ''))).replace(/\s+/g, ' ').trim();
  return {tag, atributos, texto, caminho, ancestral_com_id: ancestral, pai, posicao_entre_irmaos: posicaoPeloPapel(el),
          impressao: {tag, type: atributos.type, name: atributos.name, form_action: form ? form.getAttribute('action') : null,
                      data_nome: atributos['data-nome'], href: atributos.href}};
}
"""


def _papel_e_nome(locator) -> tuple[str | None, str]:
    nos = navegador.parse_aria(locator.aria_snapshot())
    return (nos[0]["papel"], nos[0]["nome"]) if nos else (None, "")


def descrever_elemento(pagina, seletor: str) -> dict | None:
    """O alvo como a corrida de referência o registra: o que o seletor resolve agora na página (papel e nome pela árvore de
    acessibilidade; tag, atributos, texto, caminho, ancestral com id, pai, posição entre os irmãos e a impressão pelo DOM)
    e a ocorrência entre os elementos de mesmo papel e nome da página. None quando o seletor não resolve."""
    loc = pagina.locator(seletor)
    n = loc.count()
    if n == 0:
        return None
    el = loc.first
    dados = el.evaluate(JS_DESCREVER)
    papel, nome = _papel_e_nome(el)
    ocorrencia = 1
    if papel and nome:
        iguais = pagina.locator(f"role={papel}[name={_aspas(nome)}]")
        indice = iguais.evaluate_all("(els, alvo) => els.indexOf(alvo)", el.element_handle())
        ocorrencia = int(indice) + 1 if isinstance(indice, int) and indice >= 0 else 1
    return {"seletor": seletor, "contagem": n, "papel": papel, "nome": nome, "ocorrencia": ocorrencia, **dados}


def localizar(pagina, candidato: dict):
    """O Locator do candidato: a cadeia encadeada por `locator()` e o `nth` no fim."""
    loc = pagina.locator(candidato["cadeia"][0])
    for parte in candidato["cadeia"][1:]:
        loc = loc.locator(parte)
    if candidato.get("nth") is not None:
        loc = loc.nth(int(candidato["nth"]))
    return loc


def resolver_no_navegador(pagina, candidato: dict) -> dict:
    """O que o candidato resolve na página aberta: contagem e, com um elemento só, visível, habilitado, papel e nome."""
    try:
        loc = localizar(pagina, candidato)
        n = loc.count()
    except Exception as e:  # noqa: BLE001 - seletor que o Playwright não aceita conta como nenhum elemento, com o erro registrado
        return {"contagem": 0, "visivel": None, "habilitado": None, "papel": None, "nome": None, "erro": f"{type(e).__name__}: {str(e)[:200]}"}
    saida = {"contagem": n, "visivel": None, "habilitado": None, "papel": None, "nome": None}
    if n == 1:
        saida["visivel"], saida["habilitado"] = loc.is_visible(), loc.is_enabled()
        saida["papel"], saida["nome"] = _papel_e_nome(loc)
    return saida


def impressao_do_candidato(pagina, candidato: dict) -> dict | None:
    """A impressão do DOM do elemento que o candidato resolve (para a regra R3); None se não resolve um só."""
    try:
        loc = localizar(pagina, candidato)
        if loc.count() != 1:
            return None
        return loc.evaluate(JS_DESCREVER).get("impressao")
    except Exception:  # noqa: BLE001
        return None


def resumo_json(dado) -> str:
    return json.dumps(dado, ensure_ascii=False, sort_keys=True)
