#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): monta o caso ao vivo no formato dos casos
# gravados (plano aprovado, seção 3.4): `entrada` com requisicao, status, contrato, corpo (o trecho em disputa que a
# poda deixou), sintoma, e, quando houver, arvore, seletor_quebrado e observacao; o contrato esperado vem do
# `openapi.json` da CobaiaAPI convertido para a forma textual dos fixtures (`id: inteiro | nome: texto | ...`); o
# sintoma sai de um molde em código a partir de três fontes (a conferência do roteiro que falhou, o diff do corpo
# contra o contrato e o diff da árvore podada contra a corrida de referência em modo `normal`), curto, determinístico
# e sem o nome do modo de falha nem da causa. Nada aqui chama modelo nem navegador.
# ! Motivo: o prompt do diagnóstico é congelado (ficha 34) e lê o caso por `estrategias._dados_do_caso`, que só
# conhece as chaves dos casos gravados; a Fase 4 precisa que o mesmo caso, lido do fixture e lido da tela, chegue ao
# modelo na mesma forma (regra R2 do plano), e o sintoma escrito por código é o que impede o nome do modo ou da causa
# de vazar para o prompt e virar dica.
"""Caso ao vivo da Fase 4 (pacote P2): contrato do openapi, sintoma por molde e montagem no formato gravado."""
from __future__ import annotations

CHAVES_DA_ENTRADA = ("requisicao", "status", "contrato", "corpo", "sintoma", "observacao", "arvore", "seletor_quebrado")
OBRIGATORIAS = ("requisicao", "status", "contrato", "corpo", "sintoma")
_TIPOS_OPENAPI = {"integer": "inteiro", "string": "texto", "number": "numero", "boolean": "booleano", "null": "nulo",
                  "array": "lista", "object": "objeto"}


# ------------------------------------------------------------------ contrato

def _tipo(prop: dict) -> str:
    if "enum" in prop:
        return "texto (" + " ou ".join(f"'{v}'" for v in prop["enum"]) + ")"
    if "anyOf" in prop:
        return "|".join(_tipo(p) for p in prop["anyOf"])
    if prop.get("format") == "date":
        return "data ISO (AAAA-MM-DD)"
    return _TIPOS_OPENAPI.get(prop.get("type"), str(prop.get("type")))


# ! Alteração de IA - Revisar: o `preco` de `ProdutoOut` é `Decimal` no Pydantic e sai no OpenAPI gerado como
# `{"type": "string"}`, mas a rota devolve número no fio (`float(valor_produto)`, `produtos.py`) e os casos gravados
# dizem `preco: numero`; o ajuste faz o contrato lido do OpenAPI bater com o dos fixtures.
# ! Motivo: sem o ajuste, todo caso ao vivo diria que o preço esperado é texto e a poda apontaria diferença onde não
# há; é um fato do OpenAPI da CobaiaAPI conferido em 26/10/2026 (fixture `fixtures_fase4/openapi.json`).
AJUSTES_PRODUTO = {"preco": "numero"}
TAG_OPENAPI = {
    "x-alteracao-de-ia": "! Alteração de IA - Revisar: cópia do openapi.json gerado pela CobaiaAPI em runtime (GET /openapi.json), "
                         "gravada uma vez em fixtures_fase4/ pela Fase 4 (pacote P2) com as chaves na ordem em que a API as declara.",
    "x-motivo": "! Motivo: o contrato esperado do caso ao vivo é lido deste arquivo (contrato_do_openapi) e precisa ser o mesmo "
                "em toda corrida; a API não versiona o openapi.json, só o gera ao subir. JSON não aceita comentário, e o "
                "OpenAPI permite chaves `x-`.",
}


def anotar_openapi(openapi: dict) -> dict:
    """O openapi.json com as duas chaves `x-` da tag de IA (o formato OpenAPI aceita extensões assim)."""
    return {**openapi, **TAG_OPENAPI}


def contrato_do_openapi(openapi: dict, esquema: str = "ProdutoOut", ajustes: dict | None = None) -> str:
    """O esquema do `openapi.json` (FastAPI) na forma textual dos casos gravados: `campo: tipo | campo: tipo|nulo | ...`,
    na ordem em que o esquema declara os campos; `ajustes` troca o tipo de um campo (ver AJUSTES_PRODUTO)."""
    props = openapi["components"]["schemas"][esquema]["properties"]
    ajustes = ajustes or {}
    return " | ".join(f"{nome}: {ajustes.get(nome, _tipo(p))}" for nome, p in props.items())


# ------------------------------------------------------------------ diff da árvore e sintoma por molde

def diff_arvore(referencia: str, atual: str) -> dict:
    """Linhas da árvore podada de referência (corrida em modo normal) que faltam na atual, e as que sobram; a
    contagem respeita repetições."""
    def contagem(texto: str) -> dict[str, int]:
        saida: dict[str, int] = {}
        for linha in texto.splitlines():
            chave = linha.strip()
            if chave:
                saida[chave] = saida.get(chave, 0) + 1
        return saida

    ref, atu = contagem(referencia), contagem(atual)
    faltam = [l for l in ref for _ in range(max(0, ref[l] - atu.get(l, 0)))]
    sobram = [l for l in atu for _ in range(max(0, atu[l] - ref.get(l, 0)))]
    return {"a_menos": len(faltam), "a_mais": len(sobram), "faltam": faltam, "sobram": sobram}


def _frases_do_corpo(diff_corpo: dict) -> list[str]:
    frases = []
    corpo = diff_corpo.get("corpo")
    trecho = (diff_corpo.get("trecho") or "").strip()
    if corpo == "vazio":
        return ["A resposta veio vazia."]
    if corpo == "nao_json":
        return [f"A resposta não é JSON (começa por {trecho[:40]!r})."]
    if corpo == "truncado":
        return [f"A resposta veio cortada (termina em {trecho[-40:]!r})."]
    for d in diff_corpo.get("diferencas") or []:
        campo, tipo = d.get("campo"), d.get("tipo")
        if tipo == "ausente":
            frases.append(f"O campo {campo} não veio na resposta.")
        elif tipo == "renomeado":
            frases.append(f"O campo {d.get('esperado')} veio como {d.get('recebido')}.")
        elif tipo == "tipo_diferente":
            frases.append(f"O campo {campo} veio como {d.get('recebido')} em vez de {d.get('esperado')}.")
        elif tipo == "fora_do_dominio":
            frases.append(f"O campo {campo} veio com um valor fora do esperado ({d.get('recebido')}).")
        elif tipo == "formato_divergente":
            frases.append(f"O campo {campo} veio em outro formato ({d.get('recebido')}).")
        elif tipo == "nulo_inesperado":
            frases.append(f"O campo {campo} veio nulo.")
        elif tipo == "inesperado":
            frases.append(f"A resposta trouxe o campo {campo}, que o contrato não prevê.")
        elif tipo == "forma_diferente":
            frases.append(f"A resposta veio como {d.get('recebido')} em vez de {d.get('esperado')}.")
    return frases


def sintoma_por_molde(conferencia: dict | None, diff_corpo: dict | None, diff_arvore_: dict | None, status: int | None = None) -> str:
    """O sintoma observado, escrito por código: o que a conferência do roteiro esperava e viu, o que o corpo tem de
    diferente do contrato e o que a tela tem de diferente da referência. Nunca cita o modo de falha nem a causa."""
    frases = []
    if status is not None and status != 200:
        frases.append(f"A requisição respondeu HTTP {status}.")
    if conferencia:
        frases.append(f"A conferência '{conferencia.get('nome')}' falhou: esperava {conferencia.get('esperado')}; viu {conferencia.get('observado')}.")
    if diff_corpo:
        frases += _frases_do_corpo(diff_corpo)
    if diff_arvore_:
        if diff_arvore_.get("a_menos"):
            frases.append(f"A tela mostra {diff_arvore_['a_menos']} linha(s) a menos que a referência; faltam: "
                          + "; ".join(diff_arvore_["faltam"][:3]) + ".")
        if diff_arvore_.get("a_mais"):
            frases.append(f"A tela mostra {diff_arvore_['a_mais']} linha(s) a mais que a referência; sobram: "
                          + "; ".join(diff_arvore_["sobram"][:3]) + ".")
    if not frases:
        frases.append("Nenhuma diferença medida contra a referência.")
    return " ".join(frases)


# ------------------------------------------------------------------ o caso no formato gravado

def montar_caso(id_caso: str, requisicao: str, status: int | None, contrato: str, corpo: str, sintoma: str,
                arvore: str | None = None, seletor_quebrado: str | None = None, observacao: str | None = None) -> dict:
    """O caso ao vivo com exatamente as chaves que os casos gravados usam (sem gabarito), pronto para
    `estrategias._dados_do_caso` e para a busca na biblioteca."""
    if not requisicao or not str(requisicao).strip():
        raise ValueError("caso ao vivo sem requisicao")
    if not sintoma or not str(sintoma).strip():
        raise ValueError("caso ao vivo sem sintoma: o molde precisa produzir uma frase")
    entrada = {"requisicao": requisicao, "status": status, "contrato": contrato, "corpo": corpo, "sintoma": sintoma}
    for chave, valor in (("arvore", arvore), ("seletor_quebrado", seletor_quebrado), ("observacao", observacao)):
        if valor:
            entrada[chave] = valor
    assert set(entrada) <= set(CHAVES_DA_ENTRADA)
    return {"id": id_caso, "origem": "ao_vivo", "entrada": entrada}
