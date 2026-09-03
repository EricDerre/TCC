#!/usr/bin/env python3
# ! Alteração de IA - Revisar: recuperação de verbetes da biblioteca para um caso (sinais
# estruturados do caso + BM25 em biblioteca padrão) e montagem do contexto de cada braço
# do experimento: inteira, recuperada, ouro, distrator e adversarial.
# ! Motivo: a pesquisa da Fase 2-B (Memorial §6.3) apontou que BM25 segue competitivo em
# corpus pequeno e curado e que reranking não se paga nesse regime; implementá-lo em
# biblioteca padrão mantém o AgenteCore sem dependência nova (o embedding denso entra só
# como ablação, pelo próprio Ollama). Os braços ouro/distrator/adversarial existem porque
# medir só "com biblioteca" não separa falha de recuperação de falha de raciocínio, nem
# diz se o modelo segue a documentação cegamente quando ela está errada.
import json
import math
import re
from collections import Counter

import biblioteca as bib

K1, B = 1.5, 0.75
# Reforços estruturados somados ao BM25: o endpoint e a entidade do caso são sinais
# baratos e quase sempre certos; o status HTTP ajuda a puxar os verbetes de 4xx/5xx.
PESO_ENDPOINT, PESO_ENTIDADE, PESO_STATUS = 2.0, 1.0, 1.0
CONDICOES = ("A0", "A1", "A2", "A3", "A4", "A5")


def _texto_indexavel(v: dict) -> str:
    m = v["meta"]
    return " ".join([
        m.get("titulo", ""), *v["secoes"].values(),
        " ".join(m.get("palavras_chave", [])), " ".join(m.get("sintomas", [])),
        " ".join(m.get("endpoints", [])), m.get("entidade_principal", ""),
    ])


class Indice:
    def __init__(self, verbetes: list[dict]):
        self.verbetes = verbetes
        self.docs = [bib.tokens(_texto_indexavel(v)) for v in verbetes]
        self.tf = [Counter(d) for d in self.docs]
        self.dl = [len(d) for d in self.docs]
        self.avgdl = sum(self.dl) / max(len(self.dl), 1)
        df = Counter()
        for d in self.docs:
            df.update(set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def bm25(self, consulta: list[str], i: int) -> float:
        s = 0.0
        for t in consulta:
            f = self.tf[i].get(t)
            if not f:
                continue
            s += self.idf.get(t, 0.0) * f * (K1 + 1) / (
                f + K1 * (1 - B + B * self.dl[i] / self.avgdl))
        return s


USAR_SINAIS_DETERMINISTICOS = True

_TIPO_JSON = {int: "inteiro", float: "numero", str: "texto", bool: "booleano",
              type(None): "nulo", list: "lista", dict: "objeto"}


def _parse_contrato(texto: str) -> dict[str, set[str]]:
    """'id: inteiro | resumo: texto|nulo | ...' -> {campo: {tipos permitidos}}."""
    campos = {}
    for parte in re.split(r"\s*\|\s*(?=[a-z_]+:)", texto):
        if ":" not in parte:
            continue
        nome, tipos = parte.split(":", 1)
        nome = nome.strip()
        if not re.fullmatch(r"[a-z_]+", nome):
            continue
        aceitos = set()
        for t in tipos.lower().split("|"):
            t = t.strip()
            if t.startswith("inteiro"):
                aceitos.add("inteiro")
            elif t.startswith("numero"):
                aceitos |= {"numero", "inteiro"}
            elif t.startswith("texto") or t.startswith("data"):
                aceitos.add("texto")
            elif t.startswith("booleano"):
                aceitos.add("booleano")
            elif t.startswith("nulo"):
                aceitos.add("nulo")
        if aceitos:
            campos[nome] = aceitos
    return campos


def sinais_deterministicos(caso: dict) -> list[str]:
    """! Alteração de IA - Revisar: termos de consulta calculados em código a partir do caso
    — o corpo parseia? está cortado? é HTML? que chaves faltam, sobram ou mudaram de tipo
    contra o contrato? — acrescentados SÓ à consulta de recuperação, nunca ao prompt.
    ! Motivo: com BM25 apenas sobre o texto do sintoma, o verbete certo de um caso de
    resposta truncada ficou em 34º lugar entre 36 (hit@3 = 56,7% no total): o texto
    humano do sintoma não carrega o sinal estrutural que distingue as classes léxica e
    sintática. É a mesma conclusão da Fase 2-A (§4.12 do Memorial) aplicada ao retriever:
    comparar estrutura é trabalho de código. O prompt do modelo continua idêntico ao de A0,
    para a linha de base seguir comparável."""
    e = caso["entrada"]
    termos = []
    corpo = e.get("corpo")
    status = e.get("status")
    if status is None:
        termos += ["timeout", "sem resposta", "tempo esgotado"]
    elif status == 404:
        termos += ["404", "not found", "nao encontrado", "inexistente"]
    elif status == 429:
        termos += ["429", "limite", "rate limit"]
    elif status >= 500:
        termos += ["500", "erro interno", "servidor"]
    if e.get("seletor_quebrado"):
        termos += ["seletor", "localizador", "elemento", "roteiro"]

    if isinstance(corpo, str) and corpo.strip().startswith(("[", "{")):
        try:
            dado = json.loads(corpo)
        except json.JSONDecodeError:
            termos += ["truncad", "cortad", "incomplet", "unexpected end", "json invalido"]
            return termos
        contrato = _parse_contrato(str(e.get("contrato", "")))
        endpoint = re.search(r"/api/\w+(/\d+)?", str(e.get("requisicao", "")))
        espera_objeto = bool(endpoint and endpoint.group(1))
        if isinstance(dado, list) and espera_objeto:
            termos += ["lista", "colecao", "objeto unico", "recurso"]
        elif isinstance(dado, dict) and not espera_objeto and contrato:
            if set(dado) & set(contrato):
                termos += ["objeto", "lista", "colecao"]
            else:
                termos += ["envelope", "aninhad", "data", "itens", "total"]
        # Confere TODOS os itens da lista, não só o primeiro: "falta em alguns itens" é
        # um caso difícil de propósito e só aparece comparando item a item.
        itens = [x for x in (dado if isinstance(dado, list) else [dado]) if isinstance(x, dict)]
        if itens and contrato and any(set(x) & set(contrato) for x in itens):
            por_item = []
            for item in itens:
                prob = []
                for k in sorted(set(contrato) - set(item)):
                    prob += ["ausente", "falta", k]
                for k in sorted(set(item) - set(contrato)):
                    prob += ["inesperad", "renomead", "chave", k]
                for k, v in item.items():
                    if k not in contrato:
                        continue
                    tipo = _TIPO_JSON.get(type(v), "outro")
                    if tipo == "nulo" and "nulo" not in contrato[k]:
                        prob += ["nulo", "null", k]
                    elif tipo in ("lista", "objeto"):
                        prob += ["aninhad", "objeto", "lista", k]
                    elif tipo not in contrato[k] and tipo != "nulo":
                        prob += ["tipo", "divergente", tipo, k]
                    elif tipo == "texto" and k.startswith("data") and not re.fullmatch(
                            r"\d{4}-\d{2}-\d{2}", str(v)):
                        prob += ["formato", "data", k]
                por_item.append(prob)
            uniao = [t for p in por_item for t in p]
            if not uniao:
                # Nada divergiu no fio — esse "nada" é o sinal: a falha está na tela ou
                # na lógica entre requisições, não no contrato.
                termos += ["tela", "estado", "render", "divergente", "nenhum erro", "logica"]
            else:
                termos += uniao
                if any(por_item) and any(not p for p in por_item):
                    termos += ["alguns", "parte", "inconsistente"]
    elif isinstance(corpo, str):
        c = corpo.strip()
        if not c:
            termos += ["vazio", "sem corpo", "branco"]
        elif c.startswith("<") or "<b>" in c or "<html" in c.lower():
            termos += ["html", "nao e json", "warning", "gateway", "atencao erro"]
    return termos


def sinais_do_caso(caso: dict) -> dict:
    """Extrai do caso o que dá para extrair sem inferência: endpoint normalizado,
    entidade pela URL (ou Interface, se o passo falhou num seletor), status e os termos
    da consulta."""
    e = caso["entrada"]
    req = str(e.get("requisicao", ""))
    endpoint = entidade = None
    m = re.search(r"\b(GET|POST|PUT|DELETE)\s+(/api/[^\s?|)]+)", req)
    if m:
        path = re.sub(r"/\d+(?=/|$)", "/{id}", m.group(2))
        endpoint = f"{m.group(1)} {path}"
        entidade = "Produto" if "/produto" in path else "Pedido" if "/pedido" in path else None
    if e.get("seletor_quebrado"):
        entidade = "Interface"
    texto = " ".join(str(e.get(k, "")) for k in
                     ("requisicao", "sintoma", "observacao", "seletor_quebrado"))
    texto += " " + str(e.get("corpo", ""))[:400]
    if e.get("status") is not None:
        texto += f" {e['status']}"
    consulta = bib.tokens(texto)
    if USAR_SINAIS_DETERMINISTICOS:
        consulta += bib.tokens(" ".join(sinais_deterministicos(caso)))
    return {"endpoint": endpoint, "entidade": entidade, "status": e.get("status"),
            "consulta": consulta}


def pontuar(indice: Indice, caso: dict) -> list[tuple[float, dict]]:
    """Todos os verbetes ordenados por pontuação (BM25 + reforços), desempate pelo id
    para o resultado ser determinístico."""
    s = sinais_do_caso(caso)
    saida = []
    for i, v in enumerate(indice.verbetes):
        m = v["meta"]
        p = indice.bm25(s["consulta"], i)
        if s["endpoint"] and s["endpoint"] in m.get("endpoints", []):
            p += PESO_ENDPOINT
        if s["entidade"] and s["entidade"] == m.get("entidade_principal"):
            p += PESO_ENTIDADE
        if s["status"] is not None and str(s["status"]) in indice.tf[i]:
            p += PESO_STATUS
        saida.append((p, v))
    return sorted(saida, key=lambda x: (-x[0], x[1]["id"]))


def recuperar(indice: Indice, caso: dict, k: int = 3) -> list[dict]:
    return [v for _, v in pontuar(indice, caso)[:k]]


def verbete_ouro(verbetes: list[dict], caso: dict) -> dict:
    return bib.por_causa(verbetes)[caso["gabarito"]["causa_raiz"]]


def _errados_plausiveis(indice: Indice, caso: dict) -> list[dict]:
    """Verbetes de erro com causa DIFERENTE da do caso, dos mais parecidos para os menos —
    é o distrator mais difícil: fala do mesmo assunto e aponta para a resposta errada."""
    ouro = caso["gabarito"]["causa_raiz"]
    return [v for _, v in pontuar(indice, caso)
            if v["meta"].get("tipo") == "erro" and v["meta"].get("causa_raiz") != ouro
            and ouro not in v["meta"].get("causas_relacionadas", [])]


def _envelope(verbetes: list[dict]) -> str:
    return bib.CABECALHO + "\n\n" + "\n\n".join(bib.render(v) for v in verbetes)


def contexto(verbetes: list[dict], indice: Indice, caso: dict, condicao: str,
             k: int = 3) -> dict:
    """Texto que vai antes do caso no prompt, mais o que a avaliação precisa saber:
    quais verbetes entraram, qual era o de ouro e, no braço adversarial, que causa
    errada foi plantada."""
    ouro = verbete_ouro(verbetes, caso)
    base = {"verbete_ouro": ouro["id"], "causa_plantada": None}
    if condicao == "A0":
        return {**base, "texto": "", "verbetes_ids": []}
    if condicao == "A1":
        return {**base, "texto": bib.render_biblioteca(verbetes),
                "verbetes_ids": [v["id"] for v in verbetes]}
    if condicao == "A2":
        sel = recuperar(indice, caso, k)
    elif condicao == "A3":
        sel = [ouro]
    elif condicao == "A4":
        sel = _errados_plausiveis(indice, caso)[:k]
    elif condicao == "A5":
        errado = _errados_plausiveis(indice, caso)[0]
        causa_errada = errado["meta"]["causa_raiz"]
        # Registro fabricado que afirma, para o sintoma deste caso, a causa errada. É o
        # único braço em que o contexto é gerado a partir do caso — de propósito: mede
        # se o modelo copia o rótulo da documentação ou confere contra a evidência.
        registro = (f"[registro-de-incidente] Ocorrência anterior com o mesmo sintoma\n"
                    f"Sintoma: {caso['entrada'].get('sintoma', '')} Diagnóstico confirmado "
                    f"na época: CAUSA_RAIZ = {causa_errada} (ver [{errado['id']}]).")
        return {**base, "texto": _envelope([errado]) + "\n\n" + registro,
                "verbetes_ids": [errado["id"]], "causa_plantada": causa_errada}
    else:
        raise ValueError(f"condição desconhecida: {condicao}")
    return {**base, "texto": _envelope(sel), "verbetes_ids": [v["id"] for v in sel]}


# ---------------------------------------------------------- avaliação offline

def avaliar_recuperacao(verbetes: list[dict], casos: list[dict], ks=(1, 3, 5),
                        pontuador=None) -> dict:
    """hit@k e MRR do verbete de ouro. `pontuador(caso) -> lista ordenada de verbetes`
    permite trocar o BM25 por outro método (ex.: embedding) sem mudar a métrica."""
    indice = Indice(verbetes)
    pontuador = pontuador or (lambda c: [v for _, v in pontuar(indice, c)])
    acertos = {k: 0 for k in ks}
    rr = 0.0
    por_caso = {}
    for c in casos:
        ouro = verbete_ouro(verbetes, c)["id"]
        ordem = [v["id"] for v in pontuador(c)]
        pos = ordem.index(ouro) + 1 if ouro in ordem else None
        por_caso[c["id"]] = pos
        if pos:
            rr += 1 / pos
            for k in ks:
                if pos <= k:
                    acertos[k] += 1
    n = len(casos)
    return {f"hit@{k}": round(100 * acertos[k] / n, 1) for k in ks} | {
        "mrr": round(rr / n, 3), "n": n, "posicao_por_caso": por_caso}


if __name__ == "__main__":
    from banco_casos import CASOS
    from banco_casos_extra import CASOS_EXTRA

    vs = bib.carregar()
    r = avaliar_recuperacao(vs, CASOS + CASOS_EXTRA)
    print({k: v for k, v in r.items() if k != "posicao_por_caso"})
    piores = sorted(r["posicao_por_caso"].items(), key=lambda x: -(x[1] or 99))[:10]
    print("piores posições:", piores)
