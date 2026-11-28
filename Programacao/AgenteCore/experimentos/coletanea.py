#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (27/11/2026): a coletânea de erros sorteados para a banca (cartão #99 do Kanban do
# orientador; plano aprovado em claude-memoria/plano-aprovado-coletanea-da-banca.md, decisões 193 a 197). São 64 cartas: os 58 erros
# já provados em corrida (42 de contrato da API, reproduzidos na tela nas corridas 17 e 28b, e 16 quebras de localizador do front,
# curadas na corrida 19) e 6 cartas sem erro, uma por página. A pilha é a ordem do SHA-256 de "<número>|<carta>", com o número dito
# pela banca; cada rodada tira as próximas cartas, e o sorteio é gravado em `sorteio.json` e em `resultados_alvo/hub/sorteios.jsonl`
# antes de o primeiro erro ser ligado.
# ! Motivo: o botão do hub rodava sempre os mesmos dez cenários da medida, na mesma ordem, e a banca podia dizer que as rodadas eram
# casos fixos preparados de antemão. As cartas usam só modos de injeção que já existem; o gabarito de cada uma sai do modo (a causa é a
# de `cenarios_fase4.MODO_POR_CAUSA`) e é conferido em código contra o próprio `CobaiaAPI/app/fault_injection.py` e contra a prova
# gravada, para nenhuma carta ter gabarito digitado errado. O SHA-256 no lugar do `random` deixa qualquer pessoa refazer a lista.
"""Coletânea de erros sorteados para a banca: as 64 cartas, a conferência, a pilha pelo número da banca e o registro do sorteio.

Uso:
  python coletanea.py --listar                                   # as 64 cartas, por grupo
  python coletanea.py --conferir                                 # a conferência do gabarito e da prova de cada carta
  python coletanea.py --sortear --numero 4821 --quantas 5 --posicao 0   # refaz um sorteio gravado
"""
from __future__ import annotations

import argparse
import ast
import copy
import datetime as dt
import functools
import hashlib
import json
import re
import sys
from pathlib import Path

import cenarios_fase4 as cen
import taxonomia

EXP = Path(__file__).resolve().parent
API = EXP.parent.parent / "CobaiaAPI" / "app"
PROVAS = EXP / "resultados_alvo"            # as provas são os registros versionados, qualquer que seja o RESULTADOS_DIR da corrida
TIPOS = ("contrato", "localizador", "sem_erro")
PAGINAS_DO_CONTRATO = ("api-catalogo", "api-detalhe")
QUANTAS_PERMITIDAS = (3, 5, 10)
ORIGENS_DO_NUMERO = ("digitado", "relógio")
ARQUIVO_DO_SORTEIO = "sorteio.json"         # na pasta da corrida
ARQUIVO_DOS_SORTEIOS = "sorteios.jsonl"     # em <resultados>/hub/, só acréscimo
_NUMERO = re.compile(r"^\d{1,18}$")
_NOME_DA_CLASSE = {1: "léxica", 2: "sintática", 3: "semântica", 4: "tradução", 5: "runtime", 6: "efeito"}
GRUPOS = [{"classe": k, "nome": _NOME_DA_CLASSE[k], "pergunta": taxonomia.CLASSES[k]["pergunta"]} for k in sorted(_NOME_DA_CLASSE)] + [
    {"classe": None, "nome": "sem erro", "pergunta": "A página roda sem nenhum erro ligado?"}]

# O que cada modo de injeção da CobaiaAPI faz, em palavras (lido de `fault_injection.py`), para o cartão do hub.
_O_QUE_O_MODO_FAZ = {
    "error_500": "a API responde erro 500 (erro interno do servidor)",
    "latency": "a API demora 2 s a mais em cada produto",
    "type_drift": "o campo `{campo}` chega com outro tipo (texto vira número, número vira texto)",
    "field_missing": "o campo `{campo}` some da resposta",
    "field_renamed": "o campo `{campo}` chega com outro nome (`{campo}_v2`)",
    "malformed_json": "o corpo da resposta chega cortado no meio",
    "escala_ou_unidade_errada": "o campo `{campo}` chega multiplicado por 100 (centavos no lugar de reais)",
    "formato_de_data_divergente": "a data `{campo}` chega como DD/MM/AAAA",
    "chave_de_juncao_errada": "o campo `{campo}` de cada produto chega com o valor do produto seguinte",
    "contagem_inconsistente": "a lista chega com um produto a menos",
    "nulo_inesperado": "o campo `{campo}` chega nulo",
    "valor_fora_do_dominio": "o campo `{campo}` chega com um valor que não existe (negativo, \"talvez\" ou marcado como inválido)",
    "corpo_vazio": "a resposta chega vazia",
    "corpo_nao_e_json": "a resposta chega como uma página HTML de erro, e não em JSON",
    "codificacao_incorreta": "os acentos do campo `{campo}` chegam estragados (\"Ã£\" no lugar de \"ã\")",
    "limite_de_requisicoes": "a API responde 429 (limite de requisições excedido)",
    "recurso_inexistente": "a API responde 404 (produto não encontrado) para um produto que existe",
    "registro_duplicado": "a lista chega com o primeiro produto repetido",
    "estrutura_aninhada_divergente": "o campo `{campo}` chega dentro de outro objeto, com valor e moeda",
    "colecao_no_lugar_de_objeto": "o detalhe de um produto chega como uma lista, e não como um objeto",
}
_PAGINA_EM_PALAVRAS = {"api-catalogo": "catálogo de produtos pela API", "api-detalhe": "detalhe do produto no modal"}


def _contrato(pagina: str, modo: str, campo: str | None, classe: int, nivel: int, produto_id: int | None, prova: tuple) -> dict:
    return {"id": f"contrato/{pagina}/{modo}" + (f"/{campo}" if campo else ""), "tipo": "contrato", "cenario": pagina, "modo": modo,
            "campo": campo, "causa": {m: c for c, m in cen.MODO_POR_CAUSA.items()}[modo], "classe": classe, "nivel": nivel, "forma": None,
            "produto_id": produto_id, "requisicao": f"GET /api/produtos/{produto_id}" if pagina == "api-detalhe" else "GET /api/produtos",
            "prova": list(prova)}


def _localizador(roteiro: str, modo: str) -> dict:
    return {"id": f"localizador/{roteiro}/{modo}", "tipo": "localizador", "cenario": roteiro, "modo": modo, "campo": None,
            "causa": "localizador_quebrado", "classe": 6, "nivel": 2, "forma": "harness", "produto_id": None, "requisicao": None,
            "prova": ["fase4_cura", f"{roteiro}/{modo}/harness"]}


def _sem_erro(pagina: str, prova: tuple) -> dict:
    return {"id": f"sem-erro/{pagina}", "tipo": "sem_erro", "cenario": pagina, "modo": "normal", "campo": None, "causa": None, "classe": None,
            "nivel": None, "forma": None, "produto_id": 1 if pagina == "api-detalhe" else None,
            "requisicao": "GET /api/produtos/1" if pagina == "api-detalhe" else ("GET /api/produtos" if pagina == "api-catalogo" else None),
            "prova": list(prova)}


# As 42 cartas de contrato: as 41 combinações de página, modo e campo que reproduziram na tela na corrida 17 (o primeiro caso de
# cada uma, em ordem de id, é a prova), geradas por script a partir de `reproducao.jsonl` em 27/11/2026, mais o `field_renamed` em
# `preco`, que só rodou na corrida 28b (5 de 5 com Task Success). Nos modos de um campo em que o caso gravado não dizia o campo, vale o
# campo padrão do modo na API (`CAMPO_PADRAO`): é o que a API altera.
_CARTAS: list[dict] = [
    _contrato("api-catalogo", "codificacao_incorreta", "nome", 1, 3, None, ("fase4_reproducao", "lex-11")),
    _contrato("api-catalogo", "codificacao_incorreta", "resumo", 1, 2, None, ("fase4_reproducao", "lex-18")),
    _contrato("api-catalogo", "corpo_nao_e_json", None, 1, 1, None, ("fase4_reproducao_ineditos", "lex-22")),
    _contrato("api-catalogo", "malformed_json", None, 1, 1, None, ("fase4_reproducao", "lex-1")),
    _contrato("api-detalhe", "codificacao_incorreta", "nome", 1, 3, 11, ("fase4_reproducao_ineditos", "lex-26")),
    _contrato("api-detalhe", "codificacao_incorreta", "resumo", 1, 2, 14, ("fase4_reproducao_ineditos", "lex-24")),
    _contrato("api-detalhe", "corpo_vazio", None, 1, 1, 1, ("fase4_reproducao", "lex-7")),
    _contrato("api-detalhe", "malformed_json", None, 1, 1, 1, ("fase4_reproducao", "lex-16")),
    _contrato("api-catalogo", "estrutura_aninhada_divergente", "preco", 2, 2, None, ("fase4_reproducao", "sin-11")),
    _contrato("api-catalogo", "estrutura_aninhada_divergente", "tipo", 2, 3, None, ("fase4_reproducao", "sin-21")),
    _contrato("api-catalogo", "field_missing", "id", 2, 3, None, ("fase4_reproducao", "sin-20")),
    _contrato("api-catalogo", "field_missing", "nome", 2, 1, None, ("fase4_reproducao_ineditos", "sin-22")),
    _contrato("api-catalogo", "field_missing", "preco", 2, 3, None, ("fase4_reproducao_ineditos", "sin-26")),
    _contrato("api-catalogo", "field_missing", "resumo", 2, 3, None, ("fase4_reproducao", "sin-5")),
    _contrato("api-catalogo", "field_renamed", "imagem", 2, 3, None, ("fase4_reproducao", "sin-14")),
    _contrato("api-catalogo", "field_renamed", "preco", 2, 2, None, ("fase5_agente_b", "contrato-field_renamed")),
    _contrato("api-detalhe", "colecao_no_lugar_de_objeto", None, 2, 1, 1, ("fase4_reproducao", "sin-4")),
    _contrato("api-detalhe", "field_missing", "destaque", 2, 1, 1, ("fase4_reproducao", "sin-16")),
    _contrato("api-detalhe", "field_renamed", "resumo", 2, 1, 10, ("fase4_reproducao_ineditos", "sin-23")),
    _contrato("api-catalogo", "nulo_inesperado", "id", 3, 1, None, ("fase4_reproducao", "semt-17")),
    _contrato("api-catalogo", "nulo_inesperado", "preco", 3, 1, None, ("fase4_reproducao", "semt-8")),
    _contrato("api-catalogo", "nulo_inesperado", "tipo", 3, 3, None, ("fase4_reproducao", "semt-14")),
    _contrato("api-catalogo", "type_drift", "destaque", 3, 2, None, ("fase4_reproducao_ineditos", "semt-24")),
    _contrato("api-catalogo", "type_drift", "preco", 3, 2, None, ("fase4_reproducao", "semt-1")),
    _contrato("api-catalogo", "type_drift", "tipo", 3, 1, None, ("fase4_reproducao", "semt-16")),
    _contrato("api-catalogo", "valor_fora_do_dominio", "destaque", 3, 1, None, ("fase4_reproducao", "semt-9")),
    _contrato("api-catalogo", "valor_fora_do_dominio", "id", 3, 3, None, ("fase4_reproducao_ineditos", "semt-27")),
    _contrato("api-catalogo", "valor_fora_do_dominio", "nome", 3, 3, None, ("fase4_reproducao", "semt-21")),
    _contrato("api-catalogo", "valor_fora_do_dominio", "preco", 3, 3, None, ("fase4_reproducao", "semt-20")),
    _contrato("api-detalhe", "nulo_inesperado", "resumo", 3, 3, 12, ("fase4_reproducao_ineditos", "semt-26")),
    _contrato("api-catalogo", "chave_de_juncao_errada", "id", 4, 3, None, ("fase4_reproducao_ineditos", "tra-26")),
    _contrato("api-catalogo", "chave_de_juncao_errada", "tipo", 4, 1, None, ("fase4_reproducao", "tra-17")),
    _contrato("api-catalogo", "contagem_inconsistente", None, 4, 2, None, ("fase4_reproducao", "tra-11")),
    _contrato("api-catalogo", "escala_ou_unidade_errada", "preco", 4, 2, None, ("fase4_reproducao", "tra-1")),
    _contrato("api-detalhe", "escala_ou_unidade_errada", "preco", 4, 3, 2, ("fase4_reproducao_ineditos", "tra-27")),
    _contrato("api-catalogo", "error_500", None, 5, 1, None, ("fase4_reproducao", "run-1")),
    _contrato("api-catalogo", "latency", None, 5, 1, None, ("fase4_reproducao", "run-2")),
    _contrato("api-catalogo", "limite_de_requisicoes", None, 5, 1, None, ("fase4_reproducao_ineditos", "run-22")),
    _contrato("api-catalogo", "registro_duplicado", None, 5, 3, None, ("fase4_reproducao", "run-21")),
    _contrato("api-detalhe", "latency", None, 5, 2, 1, ("fase4_reproducao", "run-19")),
    _contrato("api-detalhe", "recurso_inexistente", None, 5, 1, 5, ("fase4_reproducao_ineditos", "run-23")),
    _contrato("api-catalogo", "field_missing", "imagem", 6, 2, None, ("fase4_reproducao", "efe-3")),
]
# As 16 quebras de localizador do catálogo (`cenarios_fase4.QUEBRAS`), na forma do harness, todas curadas na corrida 19.
_CARTAS += [_localizador(q["cenario"], q["modo"]) for q in cen.QUEBRAS]
# As 6 cartas sem erro: a prova é a linha da referência (a página rodada em modo normal antes dos casos) no log versionado. No front,
# é a referência da célula cujo localizador é o seletor original do roteiro, ou seja, o roteiro sem nenhuma troca.
_CARTAS += [
    _sem_erro("api-catalogo", ("fase4_reproducao", "referência api-catalogo: passou")),
    _sem_erro("api-detalhe", ("fase4_reproducao", "referência api-detalhe produto 1: passou")),
    _sem_erro("front-busca", ("fase4_cura", "referência front-busca (id_renomeado, localizador #buscar): passou")),
    _sem_erro("front-admin-login", ("fase4_cura", "referência front-admin-login (id_renomeado, localizador #login_usuario): passou")),
    _sem_erro("front-admin-produtos", ("fase4_cura", "referência front-admin-produtos (classe_trocada, localizador button.delete[data-id='1']): passou")),
    _sem_erro("front-cliente-reserva", ("fase4_cura", "referência front-cliente-reserva (id_renomeado, localizador #enviar): passou")),
]


def _medidos() -> set[tuple]:
    """As combinações de página, modo e campo dos dez cenários da medida da Fase 5 (corrida 28b)."""
    return {(c["cenario"], c["modo"], c.get("campo")) for c in cen.CENARIOS_DO_ENSAIO}


for _c in _CARTAS:
    _c["medido_na_fase_5"] = _c["tipo"] != "sem_erro" and (_c["cenario"], _c["modo"], _c["campo"]) in _medidos()


def cartas() -> list[dict]:
    """As 64 cartas (cópia: quem chama pode mexer sem mudar a coletânea)."""
    return copy.deepcopy(_CARTAS)


def carta(id_: str) -> dict:
    for c in _CARTAS:
        if c["id"] == id_:
            return copy.deepcopy(c)
    raise KeyError(f"carta desconhecida: {id_!r}")


def descricao(carta_: dict) -> str:
    """O que a carta liga, em palavras, com a página."""
    if carta_["tipo"] == "contrato":
        o_que = _O_QUE_O_MODO_FAZ[carta_["modo"]].format(campo=carta_.get("campo") or "")
        return f"{o_que}, na página do {_PAGINA_EM_PALAVRAS[carta_['cenario']]}"
    titulo = _PAGINA_EM_PALAVRAS.get(carta_["cenario"]) or cen.cenario(carta_["cenario"])["titulo"]
    if carta_["tipo"] == "localizador":
        return f"{cen.DESCRICAO_DO_MODO[carta_['modo']]}, no roteiro \"{titulo}\""
    return f"nenhum erro ligado: a página do {titulo} roda como sempre" if carta_["cenario"] in _PAGINA_EM_PALAVRAS else \
        f"nenhum erro ligado: o roteiro \"{titulo}\" roda como sempre"


# ------------------------------------------------------------------ a conferência

@functools.lru_cache(maxsize=None)
def _da_api() -> dict:
    """`CAMPO_PADRAO`, `MODOS_DE_LISTA` e `MODOS_DE_RESPOSTA` de `fault_injection.py` e os campos de `ProdutoOut` de `schemas.py`, lidos
    pelo `ast` (sem importar a API, que precisa do FastAPI, ausente da venv do AgenteCore)."""
    arvore = ast.parse((API / "fault_injection.py").read_text(encoding="utf-8"))
    lido = {n.targets[0].id: ast.literal_eval(n.value) for n in arvore.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id in ("CAMPO_PADRAO", "MODOS_DE_LISTA", "MODOS_DE_RESPOSTA")}
    esquemas = ast.parse((API / "schemas.py").read_text(encoding="utf-8"))
    produto = next(n for n in esquemas.body if isinstance(n, ast.ClassDef) and n.name == "ProdutoOut")
    lido["campos_do_produto"] = {n.target.id for n in produto.body if isinstance(n, ast.AnnAssign)}
    return lido


@functools.lru_cache(maxsize=None)
def _linhas(corrida: str, arquivo: str, raiz: str) -> tuple:
    caminho = Path(raiz) / corrida / arquivo
    if not caminho.exists():
        return ()
    if arquivo.endswith(".jsonl"):
        return tuple(json.loads(x) for x in caminho.read_text(encoding="utf-8").splitlines() if x.strip())
    return tuple(caminho.read_text(encoding="utf-8", errors="replace").splitlines())


def _conferir_prova(c: dict, raiz: Path) -> list[str]:
    corrida, chave = (list(c.get("prova") or []) + [None, None])[:2]
    if not corrida or not chave:
        return [f"{c['id']}: sem prova"]
    if c["tipo"] == "sem_erro":
        return [] if any(chave in linha for linha in _linhas(corrida, "fase4.log", str(raiz))) else [f"{c['id']}: a linha {chave!r} não está em {corrida}/fase4.log"]
    if c["tipo"] == "localizador":
        linhas = [r for r in _linhas(corrida, "cura.jsonl", str(raiz)) if str(r.get("id", "")).startswith(chave + "/")]
        if not linhas or not all(r.get("quebrou") and r.get("curado") for r in linhas):
            return [f"{c['id']}: {corrida}/cura.jsonl não tem a célula {chave} quebrada e curada"]
        return []
    padrao = _da_api()["CAMPO_PADRAO"].get(c["modo"])
    reproducao = _linhas(corrida, "reproducao.jsonl", str(raiz))
    if reproducao:
        r = next((x for x in reproducao if x.get("id") == chave), None)
        if r is None or not r.get("reproduz"):
            return [f"{c['id']}: o caso {chave} não reproduziu em {corrida}/reproducao.jsonl"]
        campo_ok = r.get("campo") == c["campo"] or (r.get("campo") is None and c["campo"] == padrao)
        if (r.get("cenario"), r.get("modo"), r.get("causa"), r.get("classe")) != (c["cenario"], c["modo"], c["causa"], c["classe"]) or not campo_ok:
            return [f"{c['id']}: a prova {corrida}/{chave} é de outra página, modo, campo, causa ou classe"]
        return []
    linhas = [x for x in _linhas(corrida, "cenarios.jsonl", str(raiz)) if x.get("cenario") == chave]
    if not linhas or not any(x.get("detectou") for x in linhas):
        return [f"{c['id']}: o cenário {chave} não está, ou não foi detectado, em {corrida}/cenarios.jsonl"]
    x = linhas[0]
    if (x.get("roteiro"), x.get("modo"), x.get("campo"), x.get("causa_esperada"), x.get("classe")) != (c["cenario"], c["modo"], c["campo"], c["causa"], c["classe"]):
        return [f"{c['id']}: a prova {corrida}/{chave} é de outra página, modo, campo, causa ou classe"]
    return []


def validar(cartas_: list[dict] | None = None, raiz: Path = PROVAS) -> list[str]:
    """Os erros da coletânea (vazio quando está certa): carta repetida, tipo, página, roteiro ou modo que não existem, gabarito que não
    bate com o modo, campo fora do contrato `ProdutoOut` ou em modo que não usa campo, produto ou requisição trocados, marca da medida
    trocada, e prova que não está nos registros versionados."""
    cartas_ = _CARTAS if cartas_ is None else cartas_
    api = _da_api()
    causa_do_modo = {m: c for c, m in cen.MODO_POR_CAUSA.items()}
    erros, vistos = [], set()
    sem_erro_por_pagina: dict = {}
    for c in cartas_:
        id_ = c.get("id")
        if id_ in vistos:
            erros.append(f"{id_}: carta repetida")
        vistos.add(id_)
        tipo = c.get("tipo")
        if tipo not in TIPOS:
            erros.append(f"{id_}: tipo {tipo!r} fora de {TIPOS}")
            continue
        if tipo == "contrato":
            modo = c.get("modo")
            if c.get("cenario") not in PAGINAS_DO_CONTRATO:
                erros.append(f"{id_}: página {c.get('cenario')!r} fora de {PAGINAS_DO_CONTRATO}")
            if modo not in causa_do_modo:
                erros.append(f"{id_}: modo {modo!r} não é um modo de injeção da API")
                continue
            if c.get("causa") != causa_do_modo[modo]:
                erros.append(f"{id_}: a causa {c.get('causa')!r} não é a do modo {modo} ({causa_do_modo[modo]})")
            if modo in cen.MODOS_COM_CAMPO:
                if c.get("campo") not in api["campos_do_produto"]:
                    erros.append(f"{id_}: o campo {c.get('campo')!r} não está no contrato ProdutoOut")
            elif c.get("campo") is not None:
                erros.append(f"{id_}: o modo {modo} troca a resposta ou a lista inteira e não tem campo")
            if modo in api["MODOS_DE_LISTA"] and c.get("cenario") != "api-catalogo":
                erros.append(f"{id_}: o modo {modo} mexe na lista e só aparece no catálogo")
            if c.get("classe") not in _NOME_DA_CLASSE or c.get("nivel") not in taxonomia.NIVEIS:
                erros.append(f"{id_}: classe ou nível fora da taxonomia")
        elif tipo == "localizador":
            if c.get("cenario") not in cen.ROTEIROS_DA_CURA or c.get("modo") not in cen.MODOS_DE_QUEBRA:
                erros.append(f"{id_}: roteiro ou modo de quebra fora do catálogo de quebras")
                continue
            if (c.get("causa"), c.get("classe"), c.get("forma"), c.get("campo")) != ("localizador_quebrado", 6, "harness", None):
                erros.append(f"{id_}: o gabarito da quebra de localizador é localizador_quebrado, classe 6, forma harness, sem campo")
        else:
            if c.get("cenario") not in PAGINAS_DO_CONTRATO + cen.ROTEIROS_DA_CURA:
                erros.append(f"{id_}: página {c.get('cenario')!r} desconhecida")
            if (c.get("modo"), c.get("causa"), c.get("classe"), c.get("campo")) != ("normal", None, None, None):
                erros.append(f"{id_}: a carta sem erro liga o modo normal e não tem causa, classe nem campo")
            sem_erro_por_pagina[c.get("cenario")] = sem_erro_por_pagina.get(c.get("cenario"), 0) + 1
        pagina = c.get("cenario")
        produto_ok = (isinstance(c.get("produto_id"), int) and c.get("requisicao") == f"GET /api/produtos/{c.get('produto_id')}" if pagina == "api-detalhe"
                      else c.get("produto_id") is None and c.get("requisicao") == ("GET /api/produtos" if pagina == "api-catalogo" else None))
        if not produto_ok:
            erros.append(f"{id_}: produto ou requisição não batem com a página {pagina}")
        medida = tipo != "sem_erro" and (pagina, c.get("modo"), c.get("campo")) in _medidos()
        if bool(c.get("medido_na_fase_5")) != medida:
            erros.append(f"{id_}: a marca de cenário da medida da Fase 5 está trocada")
        erros += _conferir_prova(c, raiz)
    if any(n != 1 for n in sem_erro_por_pagina.values()):
        erros.append("mais de uma carta sem erro na mesma página")
    return erros


def hash_da_coletanea(cartas_: list[dict] | None = None) -> str:
    """O SHA-256 do conteúdo das cartas: muda se qualquer carta mudar."""
    texto = json.dumps(_CARTAS if cartas_ is None else cartas_, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------ a pilha e o sorteio

def normalizar_numero(texto) -> str:
    """O número da banca: só algarismos, de 1 a 18; recusa o resto."""
    if not isinstance(texto, str) or not _NUMERO.match(texto.strip()):
        raise ValueError("o número da banca tem de ter só algarismos, de 1 a 18")
    return texto.strip()


def numero_do_relogio(agora: dt.datetime | None = None) -> str:
    """O número usado quando ninguém diz um: a hora do clique, AAAAMMDDhhmmss."""
    return (agora or dt.datetime.now()).strftime("%Y%m%d%H%M%S")


def ordem_da_pilha(numero: str, cartas_: list[dict] | None = None) -> list[str]:
    """A pilha do número: as cartas na ordem do SHA-256 de "<número>|<id da carta>"."""
    numero = normalizar_numero(numero)
    ids = [c["id"] for c in (_CARTAS if cartas_ is None else cartas_)]
    return sorted(ids, key=lambda i: hashlib.sha256(f"{numero}|{i}".encode("utf-8")).hexdigest())


def tirar(numero: str, posicao: int, quantas: int, cartas_: list[dict] | None = None) -> dict:
    """As próximas `quantas` cartas da pilha a partir de `posicao` (0 é o topo); recusa a pilha vazia."""
    pilha = ordem_da_pilha(numero, cartas_)
    if not isinstance(posicao, int) or posicao < 0 or not isinstance(quantas, int) or quantas < 1:
        raise ValueError("posição e quantidade inválidas")
    if posicao >= len(pilha):
        raise ValueError(f"a pilha do número {numero} acabou: diga um número novo")
    tiradas = pilha[posicao:posicao + quantas]
    proxima = posicao + len(tiradas)
    return {"cartas": tiradas, "posicao": posicao, "proxima": proxima, "total": len(pilha), "acabou": proxima >= len(pilha)}


def _ler_registro(registro: Path) -> list[dict]:
    try:
        linhas = Path(registro).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    saida = []
    for linha in linhas:
        try:
            saida.append(json.loads(linha))
        except ValueError:
            continue            # uma linha pela metade não apaga as outras
    return saida


def sorteios_do_numero(numero: str, registro: Path, codigo: str | None = None) -> list[dict]:
    """Os sorteios gravados com este número e esta coletânea, em ordem."""
    codigo = codigo or hash_da_coletanea()
    return [s for s in _ler_registro(registro) if s.get("numero") == numero and s.get("codigo_da_coletanea") == codigo]


def proxima_posicao(numero: str, registro: Path, codigo: str | None = None) -> int:
    """Onde a pilha deste número parou: o `proxima` do último sorteio gravado com o mesmo número e a mesma coletânea, ou 0."""
    feitos = sorteios_do_numero(normalizar_numero(numero), registro, codigo)
    return int(feitos[-1].get("proxima") or 0) if feitos else 0


def comando_que_refaz(numero: str, quantas: int, posicao: int) -> str:
    return f"python coletanea.py --sortear --numero {numero} --quantas {quantas} --posicao {posicao}"


def sortear(numero: str, quantas: int, registro: Path, corrida: str, origem: str, quando: str | None = None) -> dict:
    """O sorteio de uma rodada (não grava nada): as próximas cartas da pilha do número, com o que refaz a lista."""
    numero = normalizar_numero(numero)
    if quantas not in QUANTAS_PERMITIDAS:
        raise ValueError(f"quantas: esperava uma de {QUANTAS_PERMITIDAS}")
    if origem not in ORIGENS_DO_NUMERO:
        raise ValueError(f"origem do número: esperava uma de {ORIGENS_DO_NUMERO}")
    codigo = hash_da_coletanea()
    posicao = proxima_posicao(numero, registro, codigo)
    t = tirar(numero, posicao, quantas)
    return {"quando": quando or dt.datetime.now().isoformat(timespec="seconds"), "corrida": corrida, "numero": numero, "origem": origem,
            "codigo_da_coletanea": codigo, "posicao": posicao, "quantas": quantas, "cartas": t["cartas"], "proxima": t["proxima"],
            "total": t["total"], "acabou": t["acabou"], "comando": comando_que_refaz(numero, quantas, posicao)}


def gravar_sorteio(sorteio: dict, pasta_da_corrida: Path, registro: Path) -> Path:
    """Grava o sorteio na pasta da corrida e acrescenta a linha ao registro; devolve o `sorteio.json`."""
    pasta_da_corrida, registro = Path(pasta_da_corrida), Path(registro)
    pasta_da_corrida.mkdir(parents=True, exist_ok=True)
    arq = pasta_da_corrida / ARQUIVO_DO_SORTEIO
    arq.write_text(json.dumps(sorteio, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    registro.parent.mkdir(parents=True, exist_ok=True)
    with registro.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(sorteio, ensure_ascii=False) + "\n")
    return arq


# ------------------------------------------------------------------ linha de comando

def _listar() -> None:
    for g in GRUPOS:
        do_grupo = [c for c in _CARTAS if c["classe"] == g["classe"]]
        print(f"\n{g['nome']} ({len(do_grupo)}): {g['pergunta']}")
        for c in do_grupo:
            print(f"  {c['id']}{'  [um dos dez da medida da Fase 5]' if c['medido_na_fase_5'] else ''}: {descricao(c)}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Coletânea de erros sorteados para a banca (decisões 193 a 197).")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--conferir", action="store_true")
    ap.add_argument("--sortear", action="store_true")
    ap.add_argument("--numero")
    ap.add_argument("--quantas", type=int, default=5)
    ap.add_argument("--posicao", type=int, default=0)
    args = ap.parse_args(argv)
    if args.listar:
        _listar()
        return 0
    if args.conferir:
        erros = validar()
        for e in erros:
            print(f"!! {e}")
        print(f"{len(_CARTAS)} cartas, código {hash_da_coletanea()}: " + ("conferência limpa" if not erros else f"{len(erros)} erro(s)"))
        return 1 if erros else 0
    if args.sortear:
        try:
            t = tirar(normalizar_numero(args.numero or ""), args.posicao, args.quantas)
        except ValueError as e:
            print(f"!! {e}")
            return 2
        print(f"número {args.numero}, coletânea {hash_da_coletanea()}, posições {t['posicao'] + 1} a {t['proxima']} de {t['total']}")
        for i, id_ in enumerate(t["cartas"], t["posicao"] + 1):
            print(f"  {i}. {id_}: {descricao(carta(id_))}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
