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

import json
import re

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


# ! Alteração de IA - Revisar: (05/11/2026, ficha 42, decisão 90) a árvore que vai ao prompt deixa de ser a árvore podada
# inteira: fica o título e o que a tela tem de diferente da corrida de referência em modo normal da mesma página. Sai a linha
# igual à da referência podada; sai a linha cujo nome só a árvore completa da referência tem (o rodapé, que a tela de erro sobe
# para o nível que a poda guarda, e os cartões além dos três primeiros); fica a linha com o mesmo nome e outro atributo (o id
# renomeado de uma quebra de localizador); saem o aviso "(mais N cartões omitidos pela poda)", que não é da página, e as linhas
# repetidas. Sem referência, saem os cartões e as repetidas. A árvore podada inteira continua na trilha, no evento de poda.
# ! Motivo: o plano aprovado (seção 3.3) limita o prompt na tela ao maior da calibração mais 10% (1409 tokens), e os 37 prompts
# da corrida 18b passaram disso, o maior com 2034; a árvore era o maior bloco do caso, cerca de 1700 caracteres, quase todos
# iguais à referência, e 83,1% do tempo do diagnóstico (mediana da corrida 21b) é o modelo lendo o prompt. O corte não acrescenta
# frase nenhuma: o molde perde texto, que era a condição da decisão 90 ao rever a 82.
VERSAO_DO_CASO = 3  # 1: pacote P2 (corrida 18); 2: ficha 37 (corrida 18b); 3: decisão 90 (corridas 18c e 21c)
_AVISO_DA_PODA = re.compile(r'^\s*text "\(mais \d+ cartões omitidos pela poda\)"\s*$')
_NOME_DA_LINHA = re.compile(r'^\s*\S+ "(.*?)"(?: |$)')


def _nome_da_linha(linha: str) -> str | None:
    """O nome entre aspas de uma linha da árvore podada, com o espaço limpo como a poda limpa; None em linha sem nome (`main`)."""
    m = _NOME_DA_LINHA.match(linha)
    return " ".join(m.group(1).split()) if m else None


def _sem_cartoes(linhas: list[str]) -> list[str]:
    """Tira cada `group` da árvore podada e o que está dentro dele (mais recuado)."""
    fica, recuo = [], None
    for linha in linhas:
        atual = len(linha) - len(linha.lstrip())
        if recuo is not None and atual > recuo:
            continue
        recuo = None
        if linha.strip() == "group":
            recuo = atual
            continue
        fica.append(linha)
    return fica


def arvore_do_prompt(arvore: str, referencia: str | None = None, nomes_da_referencia=()) -> str:
    """A árvore podada encurtada para o prompt: o título e o que difere da `referencia` (a árvore podada da corrida em modo
    normal); `nomes_da_referencia` são os nomes de todos os nós dela, antes da poda. Sem referência, sem os cartões. Nos dois
    casos, sem o aviso da poda e sem linha repetida."""
    linhas = (arvore or "").strip("\n").splitlines()
    if not linhas:
        return ""
    titulo, corpo = linhas[0], linhas[1:]
    if referencia:
        linhas_ref = referencia.splitlines()
        iguais = {linha.strip() for linha in linhas_ref}
        nomes_podados = {_nome_da_linha(linha) for linha in linhas_ref}
        nomes = set(nomes_da_referencia or ())

        def difere(linha: str) -> bool:
            if linha.strip() in iguais:
                return False
            nome = _nome_da_linha(linha)
            return nome is None or nome in nomes_podados or nome not in nomes

        corpo = [linha for linha in corpo if difere(linha)]
    else:
        corpo = _sem_cartoes(corpo)
    fica, vistas = [titulo], set()
    for linha in corpo:
        chave = linha.strip()
        if _AVISO_DA_PODA.match(linha) or chave in vistas:
            continue
        vistas.add(chave)
        fica.append(linha)
    return "\n".join(fica)


# ! Alteração de IA - Revisar: (05/11/2026, ficha 42, decisão 90) os campos ausentes do mesmo item viram uma frase só.
# ! Motivo: no erro 500 o SINTOMA repetia "O campo X não veio na resposta." para cada um dos sete campos do contrato, quase 200
# caracteres que o CORPO e a linha do contrato já mostram; é o mesmo fato, em menos texto.
def _frase_dos_ausentes(campos: list, item) -> str:
    onde = f"no item {item} da resposta" if item else "na resposta"
    if len(campos) == 1:
        return f"O campo {campos[0]} não veio {onde}."
    return f"Os campos {', '.join(str(c) for c in campos[:-1])} e {campos[-1]} não vieram {onde}."


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
    # ! Alteração de IA - Revisar: (05/11/2026, ficha 41, decisão 89) a frase diz em qual item está a diferença, quando ela só aparece a partir do segundo.
    # ! Motivo: a poda passou a olhar todos os itens da lista; sem o item, "o campo resumo não veio na resposta" afirmaria que ele falta em todos, e o sintoma mentiria sobre o caso.
    ausentes: dict = {}
    for d in diff_corpo.get("diferencas") or []:
        if d.get("tipo") == "ausente":
            ausentes.setdefault(d.get("item") or None, []).append(d.get("campo"))
    for d in diff_corpo.get("diferencas") or []:
        campo, tipo = d.get("campo"), d.get("tipo")
        no_item = f" no item {d['item']}" if d.get("item") else ""
        if tipo == "ausente":
            grupo = ausentes.pop(d.get("item") or None, None)
            if grupo:
                frases.append(_frase_dos_ausentes(grupo, d.get("item") or None))
        elif tipo == "renomeado":
            frases.append(f"O campo {d.get('esperado')} veio como {d.get('recebido')}{no_item}.")
        elif tipo == "tipo_diferente":
            frases.append(f"O campo {campo} veio como {d.get('recebido')} em vez de {d.get('esperado')}{no_item}.")
        elif tipo == "fora_do_dominio":
            frases.append(f"O campo {campo} veio com um valor fora do esperado ({d.get('recebido')}){no_item}.")
        elif tipo == "formato_divergente":
            frases.append(f"O campo {campo} veio em outro formato ({d.get('recebido')}){no_item}.")
        elif tipo == "nulo_inesperado":
            frases.append(f"O campo {campo} veio nulo{no_item}.")
        elif tipo == "inesperado":
            frases.append(f"A resposta trouxe o campo {campo}{no_item}, que o contrato não prevê.")
        elif tipo == "forma_diferente":
            frases.append(f"A resposta veio como {d.get('recebido')} em vez de {d.get('esperado')}.")
    return frases


# ------------------------------------------------------------------ diff do corpo contra a referência em modo normal

# ! Alteração de IA - Revisar: (01/11/2026, ficha 37 opção a) o caso ao vivo passa a comparar o corpo HTTP com o corpo da
# corrida de referência em modo normal do mesmo cenário: itens a menos ou a mais (pelo `id`), itens repetidos, valores
# diferentes item a item e o tempo da chamada contra o orçamento; `frases_da_referencia` escreve isso no SINTOMA,
# `corpo_do_caso` troca o CORPO quando a poda não achou diferença de campo contra o contrato, e
# `linhas_diff_da_referencia` dá os sinais em código para o evento de poda e o nó de decisão.
# ! Motivo: na corrida 18 (roadmap §2.10) 22 casos foram ao modelo com o primeiro produto normal da lista no CORPO,
# porque a poda só olhava o contrato; 11 viraram colecao_no_lugar_de_objeto e, nas falhas de lista e de latência, o
# sintoma dizia "Nenhuma diferença medida contra a referência". O harness já media tudo isso na regra R1.
LIMITE_DE_VALORES = 60
# ! Alteração de IA - Revisar: (05/11/2026, decisão 90) um exemplo só no CORPO, em vez de dois.
# ! Motivo: o segundo exemplo somava cerca de 200 caracteres e deixava `semt-20` e `semt-21` acima do limite do prompt na conferência sem modelo; a contagem de itens diferentes continua no CORPO.
LIMITE_DE_EXEMPLOS = 1


def _valor(v) -> str:
    return json.dumps(v, ensure_ascii=False)[:80]


def _compacto(valor, limite: int = 400) -> str:
    texto = json.dumps(valor, ensure_ascii=False)
    return texto if len(texto) <= limite else texto[:limite - 3] + "..."


def _forma(dado) -> str:
    return "lista" if isinstance(dado, list) else "objeto" if isinstance(dado, dict) else "outro"


def _nome_do_item(item) -> str:
    if isinstance(item, dict) and item.get("nome") not in (None, ""):
        return f' ("{item["nome"]}")'
    return ""


def diff_referencia(corpo_ref: str | None, corpo_atual: str | None, tempo_ref_ms: float | None, tempo_ms: float | None,
                    orcamento_ms: float = 1000, chave: str = "id") -> dict | None:
    """O corpo atual contra o da referência em modo normal. Listas de objetos são casadas pela `chave` (o `id`):
    `faltam` e `sobram` (ids), `duplicados` (id e vezes), `valores` (id, campo, referencia, recebido, item a item, até
    LIMITE_DE_VALORES) e `exemplos` (os primeiros itens que diferem, compactos); objetos são comparados campo a campo.
    `lento` é o tempo da chamada acima do orçamento (o mesmo da regra R1). Sem referência ou sem JSON de um lado, None."""
    if corpo_ref is None or corpo_atual is None:
        return None
    try:
        ref, atual = json.loads(corpo_ref), json.loads(corpo_atual)
    except (ValueError, TypeError):
        return None
    saida: dict = {"forma": _forma(atual), "forma_ref": _forma(ref), "itens": len(atual) if isinstance(atual, list) else 1 if isinstance(atual, dict) else None,
                   "itens_ref": len(ref) if isinstance(ref, list) else 1 if isinstance(ref, dict) else None,
                   "faltam": [], "sobram": [], "duplicados": [], "valores": [], "valores_a_mais": 0, "exemplos": [], "nomes": {},
                   "tempo_ms": tempo_ms, "tempo_ref_ms": tempo_ref_ms,
                   "lento": tempo_ms is not None and orcamento_ms is not None and tempo_ms > orcamento_ms, "igual": False}
    valores: list[dict] = []
    exemplos: list = []

    def comparar(item_ref: dict, item_atual: dict, ident) -> bool:
        diferente = False
        for campo, v_ref in item_ref.items():
            if campo in item_atual and item_atual[campo] != v_ref:
                valores.append({"id": ident, "campo": campo, "referencia": _valor(v_ref), "recebido": _valor(item_atual[campo])})
                diferente = True
        return diferente

    if isinstance(ref, list) and isinstance(atual, list):
        com_chave = all(isinstance(x, dict) and x.get(chave) is not None for x in ref + atual) and ref and atual
        if com_chave:
            ref_por_id: dict = {}
            for x in ref:
                ref_por_id.setdefault(x[chave], x)
            vezes: dict = {}
            atu_por_id: dict = {}
            for x in atual:
                vezes[x[chave]] = vezes.get(x[chave], 0) + 1
                atu_por_id.setdefault(x[chave], x)
            saida["faltam"] = [i for i in ref_por_id if i not in atu_por_id]
            saida["sobram"] = [i for i in atu_por_id if i not in ref_por_id]
            saida["duplicados"] = [{"id": i, "vezes": n} for i, n in vezes.items() if n > 1]
            saida["nomes"] = {str(i): x.get("nome") for i, x in list(ref_por_id.items()) + list(atu_por_id.items()) if isinstance(x, dict)}
            for i, x in atu_por_id.items():
                if i in ref_por_id and (comparar(ref_por_id[i], x, i) or vezes[i] > 1) and len(exemplos) < LIMITE_DE_EXEMPLOS:
                    exemplos.append(_compacto(x) + (f" (aparece {vezes[i]} vezes)" if vezes[i] > 1 else ""))
        else:
            for pos, (a, b) in enumerate(zip(ref, atual)):
                if isinstance(a, dict) and isinstance(b, dict):
                    if comparar(a, b, pos + 1) and len(exemplos) < LIMITE_DE_EXEMPLOS:
                        exemplos.append(_compacto(b))
                elif a != b:
                    valores.append({"id": pos + 1, "campo": None, "referencia": _valor(a), "recebido": _valor(b)})
    elif isinstance(ref, dict) and isinstance(atual, dict):
        comparar(ref, atual, None)
    saida["valores"], saida["valores_a_mais"] = valores[:LIMITE_DE_VALORES], max(0, len(valores) - LIMITE_DE_VALORES)
    saida["exemplos"] = exemplos
    saida["igual"] = (saida["forma"] == saida["forma_ref"] and saida["itens"] == saida["itens_ref"]
                      and not (saida["faltam"] or saida["sobram"] or saida["duplicados"] or valores))
    return saida


def _por_campo(valores: list[dict]) -> list[tuple[str, list[dict]]]:
    grupos: dict = {}
    for v in valores:
        grupos.setdefault(v["campo"], []).append(v)
    return list(grupos.items())


def _clausulas_de_lista(d: dict) -> list[str]:
    """As cláusulas de contagem: o que falta, o que sobra e o que se repete, com o nome do item quando há."""
    nomes = d.get("nomes") or {}
    partes = []
    if d["faltam"]:
        ids = ", ".join(f"{i}{_nome_do_item({'nome': nomes.get(str(i))})}" for i in d["faltam"])
        partes.append(("falta o id " if len(d["faltam"]) == 1 else "faltam os ids ") + ids)
    if d["sobram"]:
        ids = ", ".join(f"{i}{_nome_do_item({'nome': nomes.get(str(i))})}" for i in d["sobram"])
        partes.append(("sobra o id " if len(d["sobram"]) == 1 else "sobram os ids ") + ids)
    for dup in d["duplicados"]:
        partes.append(f"o id {dup['id']}{_nome_do_item({'nome': nomes.get(str(dup['id']))})} aparece {dup['vezes']} vezes")
    return partes


def _segundos(ms: float) -> str:
    return f"{ms / 1000:.1f}".replace(".", ",") + " s"


def frases_da_referencia(d: dict | None, ignorar_campos=()) -> list[str]:
    """As frases do SINTOMA sobre a referência em modo normal: contagem da lista, valores item a item, tempo da chamada.
    `ignorar_campos` são os campos que o diff contra o contrato já descreveu (não repetir o mesmo campo em duas frases)."""
    if not d:
        return []
    frases = []
    if d["forma"] == "lista" and d["forma_ref"] == "lista":
        clausulas = _clausulas_de_lista(d)
        if clausulas:
            frases.append(f"A lista veio com {d['itens']} itens; a referência em modo normal tem {d['itens_ref']}: " + "; ".join(clausulas) + ".")
    for campo, grupo in _por_campo(d["valores"]):
        if campo in ignorar_campos:
            continue
        ex = grupo[0]
        if d["forma"] == "lista":
            quantos = f"{len(grupo)} {'item' if len(grupo) == 1 else 'itens'}"
            frases.append(f"O campo {campo} veio diferente da referência em modo normal em {quantos}, por exemplo no id {ex['id']}: "
                          f"{ex['recebido']} em vez de {ex['referencia']}.")
        else:
            frases.append(f"O campo {campo} veio {ex['recebido']}; na referência em modo normal, {ex['referencia']}.")
    if d["lento"]:
        frases.append(f"A chamada levou {_segundos(d['tempo_ms'])}"
                      + (f"; na referência em modo normal, {d['tempo_ref_ms']:.0f} ms." if d.get("tempo_ref_ms") is not None else "."))
    return frases


def corpo_do_caso(diff_corpo: dict | None, diff_ref: dict | None) -> str:
    """O CORPO do caso ao vivo: o trecho em disputa da poda quando o corpo não é JSON ou tem diferença de campo contra o
    contrato (e sem referência); senão, a forma e a contagem da lista contra a referência em modo normal, o que falta,
    sobra ou se repete, os campos diferentes e um ou dois itens de exemplo (ou o primeiro item, quando nada difere)."""
    if not diff_corpo:
        return ""
    trecho = diff_corpo.get("trecho") or ""
    if diff_corpo.get("corpo") != "json" or diff_corpo.get("diferencas") or not diff_ref:
        return trecho
    d = diff_ref
    if d["forma"] == "lista" and d["forma_ref"] == "lista":
        if d["igual"]:
            return f"lista com {d['itens']} itens, igual à referência em modo normal; primeiro item: {trecho}"
        partes = [f"lista com {d['itens']} itens (referência em modo normal: {d['itens_ref']})"] + _clausulas_de_lista(d)
        partes += [f"{campo} diferente em {len(grupo)} {'item' if len(grupo) == 1 else 'itens'}" for campo, grupo in _por_campo(d["valores"])]
        texto = "; ".join(partes)
        return texto + ("; por exemplo: " + "; ".join(d["exemplos"]) if d["exemplos"] else f"; primeiro item: {trecho}")
    if d["forma"] == "objeto" and d["valores"]:
        return trecho + " (contra a referência em modo normal: " + ", ".join(f"{v['campo']} {v['recebido']} em vez de {v['referencia']}" for v in d["valores"]) + ")"
    return trecho


def linhas_diff_da_referencia(d: dict | None) -> list[dict]:
    """Uma linha de sinal em código por diferença contra a referência (campo, tipo, esperado, recebido), para o evento de
    poda do corpo e para a justificativa do nó de decisão."""
    if not d:
        return []
    linhas = []
    esperado_itens = f"{d['itens_ref']} itens (referência em modo normal)"
    if d["faltam"]:
        linhas.append({"campo": "itens", "tipo": "itens_a_menos", "esperado": esperado_itens, "recebido": _clausulas_de_lista({**d, "sobram": [], "duplicados": []})[0]})
    if d["sobram"]:
        linhas.append({"campo": "itens", "tipo": "itens_a_mais", "esperado": esperado_itens, "recebido": _clausulas_de_lista({**d, "faltam": [], "duplicados": []})[0]})
    if d["duplicados"]:
        linhas.append({"campo": "itens", "tipo": "itens_repetidos", "esperado": esperado_itens, "recebido": "; ".join(_clausulas_de_lista({**d, "faltam": [], "sobram": []}))})
    for campo, grupo in _por_campo(d["valores"]):
        ex = grupo[0]
        linhas.append({"campo": campo, "tipo": "valor_diferente_da_referencia", "esperado": f"{ex['referencia']} (referência em modo normal)",
                       "recebido": ex["recebido"] + (f" em {len(grupo)} itens" if d["forma"] == "lista" else "")})
    if d["lento"]:
        linhas.append({"campo": "tempo_ms", "tipo": "tempo_acima_do_orcamento",
                       "esperado": (f"{d['tempo_ref_ms']:.0f} ms (referência em modo normal)" if d.get("tempo_ref_ms") is not None else "dentro do orçamento"),
                       "recebido": f"{d['tempo_ms']:.0f} ms"})
    return linhas


def sintoma_por_molde(conferencia: dict | None, diff_corpo: dict | None, diff_arvore_: dict | None, status: int | None = None,
                      diff_ref: dict | None = None) -> str:
    """O sintoma observado, escrito por código: o que a conferência do roteiro esperava e viu, o que o corpo tem de
    diferente do contrato, o que mudou contra a referência em modo normal (lista, valores, tempo) e o que a tela tem de
    diferente da referência. Nunca cita o modo de falha nem a causa."""
    frases = []
    if status is not None and status != 200:
        frases.append(f"A requisição respondeu HTTP {status}.")
    if conferencia:
        frases.append(f"A conferência '{conferencia.get('nome')}' falhou: esperava {conferencia.get('esperado')}; viu {conferencia.get('observado')}.")
    if diff_corpo:
        frases += _frases_do_corpo(diff_corpo)
    frases += frases_da_referencia(diff_ref, {x.get("campo") for x in (diff_corpo or {}).get("diferencas") or [] if x.get("campo")})
    # ! Alteração de IA - Revisar: (05/11/2026, ficha 42, decisão 90) o SINTOMA guarda as contagens de linhas e perde as listas
    # `faltam` e `sobram`, que continuam no diff e na trilha.
    # ! Motivo: as três primeiras linhas da lista chegavam a repetir "- img; - img; - img", e o que a tela tem de novo agora está na
    # árvore do prompt; a medida sem modelo (`prompt_tela_blocos.json`) mostra que sem este corte 5 dos 37 prompts ficariam acima do limite.
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) as duas contagens viram uma frase só quando existem as duas.
    # ! Motivo: a conferência sem modelo mostrou "A tela mostra 6 linha(s) a menos que a referência. A tela mostra 6 linha(s) a mais que a
    # referência." em casos em que só o texto de um item mudou, e o maior prompt ficou a 1 token do limite de 1409.
    if diff_arvore_:
        a_menos, a_mais = diff_arvore_.get("a_menos"), diff_arvore_.get("a_mais")
        if a_menos and a_mais:
            frases.append(f"A tela mostra {a_menos} linha(s) a menos e {a_mais} a mais que a referência.")
        elif a_menos:
            frases.append(f"A tela mostra {a_menos} linha(s) a menos que a referência.")
        elif a_mais:
            frases.append(f"A tela mostra {a_mais} linha(s) a mais que a referência.")
    if not frases:
        frases.append("Nenhuma diferença medida contra a referência.")
    return " ".join(frases)


# ------------------------------------------------------------------ o caso no formato gravado

# ! Alteração de IA - Revisar: (05/11/2026, decisão 96) o tamanho do caso conta só o que vai ao modelo.
# ! Motivo: o caso ao vivo passou a guardar o corpo inteiro e a observação da poda fora de `entrada`; contados, o `caso_chars` da leitura diria que o caso cresceu quando ele encurtou.
def tamanho_do_caso(caso: dict) -> int:
    return len(json.dumps({k: v for k, v in caso.items() if k not in ("corpo_completo", "observacao_da_poda")}, ensure_ascii=False))


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
