#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): a poda em código do plano aprovado
# (seção 3.3). Duas funções puras: `podar_arvore` reduz a árvore de acessibilidade capturada pelo Playwright ao que
# o roteiro toca e ao entorno (papéis interativos, textos, estados, marcos da página), com contagens antes e depois e
# as regras aplicadas, na mesma forma textual de `banco_casos.ARVORE_CARTOES` (papel, nome entre aspas, indentação de
# dois espaços, `level=N`, `class=` e `data-id=` quando o DOM os fornece); `diff_contrato` compara o corpo HTTP com o
# contrato textual dos casos (`id: inteiro | nome: texto | ...`) e devolve só o diff (campo ausente, renomeado, tipo
# diferente, valor fora do domínio, formato divergente, nulo inesperado, inesperado, forma diferente, corpo vazio,
# não JSON ou truncado) e o trecho em disputa. `tokens_estimados` e `cabe` usam `biblioteca.CHARS_POR_TOKEN`.
# ! Motivo: o prompt do diagnóstico é congelado (ficha 34) e cabe em `num_ctx` 8192; a árvore inteira de
# `produtos_api.php` tem 193 nós e 14 cartões iguais, e o corpo HTTP inteiro no prompt repetiria a diretriz que a
# Fase 2 já mediu como pior (diff pré-calculado contra JSON cru). A poda é controle de latência também: o prefill em
# CPU cresce mais que linearmente com o prompt (decisão 55). Tudo aqui roda sem navegador e sem modelo.
"""Poda em código da Fase 4: árvore de acessibilidade e corpo HTTP contra o contrato (pacote P2)."""
from __future__ import annotations

import json
import re

import biblioteca as bib

INTERATIVOS = frozenset({"button", "link", "textbox", "searchbox", "checkbox", "combobox", "radio", "menuitem", "tab", "option",
                         "switch", "slider", "spinbutton", "listbox", "menuitemcheckbox", "menuitemradio"})
MARCOS = frozenset({"navigation", "main", "dialog", "alertdialog", "form", "search", "banner", "contentinfo", "region", "complementary"})
DECORACAO = frozenset({"img", "iframe", "separator", "presentation", "none", "figure", "graphics-document"})
CONTEINERES = frozenset({"list", "listitem", "group", "article", "table", "row", "cell", "rowgroup", "columnheader", "rowheader", "generic"})
TEXTOS = frozenset({"text", "paragraph", "strong", "emphasis", "code", "blockquote", "caption", "term", "definition"})
MEMBROS_DE_CARTAO = frozenset({"paragraph", "text", "strong", "emphasis", "img", "button", "link"})
ESTADOS = ("disabled", "expanded", "selected", "checked", "pressed", "active", "readonly", "required", "invalid")
ATRIBUTOS_DO_DOM = ("id", "name", "class", "data-id", "data-testid", "href")
NIVEL_MAXIMO_FORA_DO_CARTAO = 4
NIVEL_DO_CARTAO = "3"


# ------------------------------------------------------------------ árvore de acessibilidade

def _tem_letra(texto: str | None) -> bool:
    return bool(texto) and any(ch.isalnum() for ch in texto)


def _limpo(texto: str | None) -> str:
    return " ".join((texto or "").split())


def _arvore(nos: list[dict]) -> list[dict]:
    """A lista achatada do snapshot (papel, nome, profundidade, atributos) vira uma árvore com `filhos` e `indice`."""
    raizes: list[dict] = []
    pilha: list[dict] = []
    for i, n in enumerate(nos):
        no = {"papel": n["papel"], "nome": _limpo(n.get("nome")), "atributos": dict(n.get("atributos") or {}),
              "profundidade": n["profundidade"], "indice": i, "filhos": []}
        while pilha and pilha[-1]["profundidade"] >= no["profundidade"]:
            pilha.pop()
        (pilha[-1]["filhos"] if pilha else raizes).append(no)
        pilha.append(no)
    return raizes


def _descendentes(no: dict):
    for f in no["filhos"]:
        yield f
        yield from _descendentes(f)


def _indices_de(nos: list[dict], referencias) -> set[int]:
    """Os índices (na lista achatada) dos nós que `alvo`/`tocados` descrevem por papel, nome e ocorrência (a partir de 1)."""
    saida: set[int] = set()
    for ref in referencias:
        if not ref:
            continue
        ocorrencia = int(ref.get("ocorrencia") or 1)
        vistos = 0
        for i, n in enumerate(nos):
            if n["papel"] == ref.get("papel") and _limpo(n.get("nome")) == _limpo(ref.get("nome")):
                vistos += 1
                if vistos == ocorrencia:
                    saida.add(i)
                    break
    return saida


def _atribuir_interativos(nos: list[dict], interativos) -> dict[int, dict]:
    """Casa, na ordem do documento, cada elemento do DOM (papel, nome e atributos como class e data-id) com o nó da
    árvore de mesmo papel e nome ainda não casado; devolve {índice do nó: atributos}."""
    saida: dict[int, dict] = {}
    proximo: dict[tuple, int] = {}
    for item in interativos or []:
        chave = (item.get("papel"), _limpo(item.get("nome")))
        inicio = proximo.get(chave, 0)
        for i in range(inicio, len(nos)):
            if nos[i]["papel"] == chave[0] and _limpo(nos[i].get("nome")) == chave[1]:
                saida[i] = {k: item[k] for k in ATRIBUTOS_DO_DOM if item.get(k)}
                proximo[chave] = i + 1
                break
    return saida


def _linha_interativa(no: dict, dom: dict[int, dict]) -> str:
    partes = [f'{no["papel"]} "{no["nome"]}"']
    for estado in ESTADOS:
        valor = no["atributos"].get(estado)
        if valor not in (None, "", "false", False):
            partes.append(estado if valor in ("true", True) else f"{estado}={valor}")
    for chave, valor in dom.get(no["indice"], {}).items():
        partes.append(f'{chave}="{valor}"')
    return " ".join(partes)


def _linha_heading(no: dict) -> str:
    nivel = no["atributos"].get("level")
    return f'heading "{no["nome"]}"' + (f" level={nivel}" if nivel else "")


class _Podador:
    def __init__(self, nos: list[dict], alvo: dict | None, tocados, interativos, max_cartoes: int) -> None:
        self.nos = nos
        self.marcados = _indices_de(nos, [alvo, *tocados])
        self.dom = _atribuir_interativos(nos, interativos)
        self.max_cartoes = max_cartoes
        self.regras = {"cartoes_omitidos": 0, "imagens_removidas": 0, "decoracao_removida": 0, "listas_achatadas": 0,
                       "textos_sem_letra_removidos": 0, "interativos_sem_nome_removidos": 0, "headings_removidos": 0}

    def _descartar(self, no: dict) -> None:
        if no["papel"] == "img":
            self.regras["imagens_removidas"] += 1
        elif no["papel"] in DECORACAO:
            self.regras["decoracao_removida"] += 1
        for f in _descendentes(no):
            if f["papel"] == "img":
                self.regras["imagens_removidas"] += 1
            elif f["papel"] in DECORACAO:
                self.regras["decoracao_removida"] += 1

    def _folhas(self, no: dict, recuo: str, dentro_de_cartao: bool) -> list[str]:
        """Um nó que não é marco nem cartão: interativos com nome, textos com letra e headings até o nível 4; o resto
        some, contado. Contêineres (list, listitem, group) são achatados: só o conteúdo deles aparece."""
        papel = no["papel"]
        if papel in DECORACAO:
            self._descartar(no)
            return []
        if papel in INTERATIVOS:
            if not _tem_letra(no["nome"]):
                self.regras["interativos_sem_nome_removidos"] += 1
                for f in no["filhos"]:
                    self._descartar(f) if f["papel"] in DECORACAO else None
                return []
            for f in no["filhos"]:
                if f["papel"] in DECORACAO:
                    self._descartar(f)
            return [recuo + _linha_interativa(no, self.dom)]
        if papel == "heading":
            nivel = int(no["atributos"].get("level") or 0)
            if not dentro_de_cartao and nivel > NIVEL_MAXIMO_FORA_DO_CARTAO:
                self.regras["headings_removidos"] += 1
                return []
            return [recuo + _linha_heading(no)]
        if papel in TEXTOS:
            linhas = []
            if no["nome"]:
                if _tem_letra(no["nome"]):
                    linhas.append(recuo + f'text "{no["nome"]}"')
                else:
                    self.regras["textos_sem_letra_removidos"] += 1
            for f in no["filhos"]:
                linhas += self._folhas(f, recuo, dentro_de_cartao)
            return linhas
        if papel in CONTEINERES or papel in MARCOS:
            if papel in CONTEINERES:
                self.regras["listas_achatadas"] += 1
            linhas = []
            for f in no["filhos"]:
                linhas += self._folhas(f, recuo, dentro_de_cartao)
            return linhas
        linhas = []
        for f in no["filhos"]:
            linhas += self._folhas(f, recuo, dentro_de_cartao)
        return linhas

    def _marco(self, no: dict, recuo: str) -> list[str]:
        linhas = [recuo + no["papel"]]
        for f in no["filhos"]:
            linhas += self._folhas(f, recuo + "  ", False)
        return linhas

    def _contem_marcado(self, cartao: dict) -> bool:
        nos = [cartao["heading"], *cartao["membros"]]
        for n in nos:
            if n["indice"] in self.marcados or any(f["indice"] in self.marcados for f in _descendentes(n)):
                return True
        return False

    def _cartao(self, cartao: dict, recuo: str) -> list[str]:
        linhas = [recuo + "group", recuo + "  " + _linha_heading(cartao["heading"])]
        for m in cartao["membros"]:
            linhas += self._folhas(m, recuo + "  ", True)
        return linhas

    def _main(self, no: dict, recuo: str) -> list[str]:
        """Dentro de `main`, os cartões (segmentos que começam em heading de nível 3) ficam limitados aos primeiros
        `max_cartoes` mais os que contêm o alvo ou um nó tocado; o resto vira uma linha com a contagem."""
        blocos: list[tuple] = []
        cartao = None
        for f in no["filhos"]:
            if f["papel"] == "heading" and str(f["atributos"].get("level")) == NIVEL_DO_CARTAO:
                cartao = {"heading": f, "membros": []}
                blocos.append(("cartao", cartao))
            elif cartao is not None and f["papel"] in MEMBROS_DE_CARTAO:
                cartao["membros"].append(f)
            else:
                cartao = None
                blocos.append(("no", f))
        cartoes = [b for t, b in blocos if t == "cartao"]
        mantidos = {id(c) for k, c in enumerate(cartoes) if k < self.max_cartoes or self._contem_marcado(c)}
        linhas = [recuo + "main"]
        omitidos = 0
        ultimo_cartao = None
        for t, b in blocos:
            if t == "no":
                linhas += self._folhas(b, recuo + "  ", False)
            elif id(b) in mantidos:
                linhas += self._cartao(b, recuo + "  ")
                ultimo_cartao = len(linhas)
            else:
                omitidos += 1
                self._descartar(b["heading"])
                for m in b["membros"]:
                    self._descartar(m)
        if omitidos:
            aviso = recuo + f'  text "(mais {omitidos} cartões omitidos pela poda)"'
            linhas.insert(ultimo_cartao if ultimo_cartao is not None else len(linhas), aviso)
            self.regras["cartoes_omitidos"] = omitidos
        return linhas

    def podar(self, titulo: str) -> list[str]:
        linhas = [f'document "{titulo}"']
        for raiz in _arvore(self.nos):
            if raiz["papel"] == "main":
                linhas += self._main(raiz, "  ")
            elif raiz["papel"] in MARCOS:
                linhas += self._marco(raiz, "  ")
            else:
                linhas += self._folhas(raiz, "  ", False)
        return linhas


def podar_arvore(nos: list[dict], titulo: str = "", alvo: dict | None = None, tocados=(), interativos=None,
                 max_cartoes: int = 3) -> dict:
    """Reduz a árvore (lista de nós de `navegador.parse_aria`) ao que interessa ao diagnóstico, na forma textual dos
    casos gravados. `alvo` e `tocados` são {papel, nome, ocorrencia}; `interativos` traz, na ordem do documento, os
    atributos do DOM (class, data-id, id, name) dos elementos interativos. Devolve texto, linhas, contagens e regras."""
    podador = _Podador(nos, alvo, list(tocados), interativos, max_cartoes)
    linhas = podador.podar(titulo)
    return {"texto": "\n".join(linhas) + "\n", "linhas": linhas, "antes": len(nos), "depois": len(linhas),
            "regras": podador.regras, "marcados": sorted(podador.marcados)}


def tokens_estimados(texto: str) -> int:
    return round(len(texto) / bib.CHARS_POR_TOKEN)


def cabe(texto: str, max_tokens: int) -> bool:
    return tokens_estimados(texto) <= max_tokens


# ------------------------------------------------------------------ corpo HTTP contra o contrato

_DATA_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def campos_do_contrato(contrato: str) -> list[dict]:
    """`id: inteiro | nome: texto | resumo: texto|nulo | status: texto ('Em Analise' ou 'Cancelado') | data: data ISO (AAAA-MM-DD)`
    vira uma lista de {campo, tipos, dominio, texto}; tipos são inteiro, texto, numero, booleano, nulo, enum ou data."""
    campos = []
    for parte in contrato.split(" | "):
        nome, _, tipos = parte.partition(":")
        nome, tipos = nome.strip(), tipos.strip()
        if not nome:
            continue
        dominio = re.findall(r"'([^']+)'", tipos)
        if dominio:
            lista = ["enum"] + (["nulo"] if "nulo" in tipos.split("(")[0] else [])
        elif tipos.lower().startswith("data"):
            lista = ["data"] + (["nulo"] if "nulo" in tipos else [])
        else:
            lista = [t.strip() for t in tipos.split("|") if t.strip()]
        campos.append({"campo": nome, "tipos": lista, "dominio": dominio, "texto": tipos})
    return campos


def _tipo_observado(valor) -> str:
    if valor is None:
        return "nulo"
    if isinstance(valor, bool):
        return "booleano"
    if isinstance(valor, int):
        return "inteiro"
    if isinstance(valor, float):
        return "numero"
    if isinstance(valor, str):
        return "texto"
    if isinstance(valor, list):
        return "lista"
    if isinstance(valor, dict):
        return "objeto"
    return type(valor).__name__


def _compativel(valor, campo: dict) -> str | None:
    """None quando o valor cabe no contrato; senão o motivo: tipo, dominio ou formato."""
    tipos = [t for t in campo["tipos"] if t != "nulo"]
    observado = _tipo_observado(valor)
    for t in tipos:
        if t == "inteiro" and observado == "inteiro":
            return None
        if t == "numero" and observado in ("inteiro", "numero"):
            return None
        if t == "texto" and observado == "texto":
            return None
        if t == "booleano" and observado == "booleano":
            return None
        if t == "enum" and observado == "texto":
            return None if valor in campo["dominio"] else "dominio"
        if t == "data" and observado == "texto":
            return None if _DATA_ISO.match(valor) else "formato"
        if t in ("lista", "objeto") and observado == t:
            return None
    return "tipo"


def _parecido(a: str, b: str) -> bool:
    a, b = a.lower(), b.lower()
    if a in b or b in a:
        return True
    return _distancia(a, b) <= 3


def _distancia(a: str, b: str) -> int:
    anterior = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        atual = [i]
        for j, cb in enumerate(b, 1):
            atual.append(min(anterior[j] + 1, atual[j - 1] + 1, anterior[j - 1] + (ca != cb)))
        anterior = atual
    return anterior[-1]


def _compacto(valor, limite: int) -> str:
    texto = json.dumps(valor, ensure_ascii=False, separators=(", ", ": "))
    return texto if len(texto) <= limite else texto[:limite - 3] + "..."


def diff_contrato(contrato: str, corpo, forma_esperada: str | None = None, max_trecho: int = 400) -> dict:
    """Compara o corpo HTTP (texto ou já decodificado) com o contrato textual. Devolve `corpo` (json, vazio, nao_json,
    truncado), `forma` (lista, objeto, outro ou None), `itens`, `diferencas` (campo, tipo, esperado, recebido) e o
    `trecho` em disputa, curto, para o prompt; o corpo inteiro fica fora daqui (vai para o blob da trilha)."""
    saida: dict = {"corpo": None, "forma": None, "itens": None, "diferencas": [], "trecho": ""}
    texto = corpo if isinstance(corpo, str) else json.dumps(corpo, ensure_ascii=False)
    if not texto.strip():
        saida["corpo"] = "vazio"
        return saida
    try:
        dado = json.loads(texto)
    except ValueError:
        s = texto.strip()
        truncado = s[0] in "[{" and s[-1] not in "]}"
        saida["corpo"] = "truncado" if truncado else "nao_json"
        saida["trecho"] = ("..." + s[-(max_trecho // 2):]) if truncado else s[:max_trecho]
        return saida
    saida["corpo"] = "json"
    if isinstance(dado, list):
        saida["forma"], saida["itens"] = "lista", len(dado)
        amostra = dado[0] if dado and isinstance(dado[0], dict) else None
    elif isinstance(dado, dict):
        saida["forma"], saida["itens"] = "objeto", 1
        amostra = dado
    else:
        saida["forma"], amostra = "outro", None
    if forma_esperada and saida["forma"] != forma_esperada:
        saida["diferencas"].append({"campo": None, "tipo": "forma_diferente", "esperado": forma_esperada, "recebido": saida["forma"]})
    if amostra is None:
        saida["trecho"] = _compacto(dado, max_trecho)
        return saida
    campos = campos_do_contrato(contrato)
    esperados = {c["campo"] for c in campos}
    extras = [k for k in amostra if k not in esperados]
    usados: set[str] = set()
    em_disputa: list[str] = []
    for c in campos:
        nome = c["campo"]
        if nome not in amostra:
            parecido = next((k for k in extras if k not in usados and _parecido(nome, k)), None)
            if parecido:
                usados.add(parecido)
                saida["diferencas"].append({"campo": nome, "tipo": "renomeado", "esperado": nome, "recebido": parecido})
                em_disputa.append(parecido)
            else:
                saida["diferencas"].append({"campo": nome, "tipo": "ausente", "esperado": c["texto"], "recebido": None})
            continue
        valor = amostra[nome]
        if valor is None:
            if "nulo" not in c["tipos"]:
                saida["diferencas"].append({"campo": nome, "tipo": "nulo_inesperado", "esperado": c["texto"], "recebido": "nulo"})
                em_disputa.append(nome)
            continue
        motivo = _compativel(valor, c)
        if motivo == "tipo":
            saida["diferencas"].append({"campo": nome, "tipo": "tipo_diferente", "esperado": "/".join(t for t in c["tipos"] if t != "nulo"),
                                        "recebido": _tipo_observado(valor)})
            em_disputa.append(nome)
        elif motivo == "dominio":
            saida["diferencas"].append({"campo": nome, "tipo": "fora_do_dominio", "esperado": c["texto"], "recebido": _compacto(valor, 80)})
            em_disputa.append(nome)
        elif motivo == "formato":
            saida["diferencas"].append({"campo": nome, "tipo": "formato_divergente", "esperado": c["texto"], "recebido": _compacto(valor, 80)})
            em_disputa.append(nome)
    for k in extras:
        if k not in usados:
            saida["diferencas"].append({"campo": k, "tipo": "inesperado", "esperado": None, "recebido": _tipo_observado(amostra[k])})
            em_disputa.append(k)
    recorte = {k: amostra[k] for k in em_disputa if k in amostra}
    for d in saida["diferencas"]:
        if d["tipo"] == "ausente":
            recorte[d["campo"]] = "(ausente)"
    saida["trecho"] = _compacto(recorte if recorte else amostra, max_trecho)
    return saida
