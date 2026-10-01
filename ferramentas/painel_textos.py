#!/usr/bin/env python3
# ! Alteração de IA - Revisar: leitura de pendencias.md e roadmap.md para o painel do projeto (28/09/2026):
# transforma as fichas de pendência ("### N. Título" seguido de campos "- **Campo:** valor", com subitens
# "  - (a) …" nas Opções) e as duas tabelas do roadmap (§1 estado por fase, §2 corridas) em estruturas que
# gerar_dashboard.py desenha como cartões, e converte o restante dos dois documentos em HTML (títulos,
# tabelas, listas, parágrafos; links relativos viram só o texto, porque o painel é publicado fora do
# repositório e o link não abriria).
# ! Motivo: o Eric pediu um relatório visual por pergunta das pendências e um relatório do roadmap, tudo
# numa única página; os dois .md continuam sendo a fonte (ninguém digita nada duas vezes), e o formato de
# ficha é o que permite montar um cartão por pergunta sem adivinhar onde cada campo começa. As palavras
# fixas de estado ("aberta"/"fechada em …" nas fichas; "Concluída"/"Em andamento"/"Não iniciada" nas fases;
# "feita"/"rodando"/"pendente"/"opcional"/"aguarda" nas corridas) são o que dá a cor de cada cartão.
"""Leitura das fichas de pendencias.md e das tabelas de roadmap.md para o painel do projeto.

Formato da ficha (em pendencias.md):

    ### 12. Título curto
    - **Estado:** aberta            (ou: fechada em 28/09/2026)
    - **Quem decide:** Eric
    - **Aberta em:** 23/09/2026
    - **O que é:** …
    - **Por que importa:** …
    - **Opções:**
      - (a) …
      - (b) …
    - **Recomendação:** …
    - **Decisão:** em aberto        (ou o que foi decidido)

Testes: python ferramentas/testar_painel_textos.py
"""
from __future__ import annotations

import html
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

RE_COMENTARIO = re.compile(r"<!--.*?-->", re.S)
RE_CAMPO = re.compile(r"^- \*\*([^*:]+):\*\*\s*(.*)$")
RE_SUBITEM = re.compile(r"^\s{2,}- (.*)$")
RE_FICHA = re.compile(r"^(\d+)\. (.+)$")
RE_DATA = re.compile(r"\d{2}/\d{2}/\d{4}")
RE_TITULO = re.compile(r"^(#{1,4}) (.+)$")

CAMPOS_CABECALHO = ("Estado", "Quem decide", "Aberta em")
CAMPOS_CORPO = ("O que é", "Por que importa", "Opções", "Recomendação", "Decisão")


# ------------------------------------------------------------------ estruturas

@dataclass
class Ficha:
    bloco: str
    indice_bloco: int
    numero: int
    titulo: str
    campos: dict[str, str] = field(default_factory=dict)
    listas: dict[str, list[str]] = field(default_factory=dict)

    @property
    def estado(self) -> str:
        return self.campos.get("Estado", "").strip()

    @property
    def aberta(self) -> bool:
        return self.estado.lower().startswith("aberta")

    @property
    def fechada_em(self) -> str | None:
        m = RE_DATA.search(self.estado)
        return m.group(0) if (m and not self.aberta) else None

    @property
    def quem(self) -> str:
        return self.campos.get("Quem decide", "").strip() or "—"

    @property
    def depende_do_eric(self) -> bool:
        return self.aberta and "eric" in self.quem.lower()

    @property
    def decisao_em_aberto(self) -> bool:
        d = self.campos.get("Decisão", "").strip().lower()
        return (not d) or d.startswith("em aberto")

    @property
    def id_html(self) -> str:
        return f"p{self.indice_bloco}-{self.numero}"


@dataclass
class Bloco:
    titulo: str
    intro: str
    fichas: list[Ficha]
    resto: str


@dataclass
class Fase:
    nome: str
    o_que_e: str
    estado: str
    classe: str


@dataclass
class Corrida:
    numero: str
    nome: str
    comando: str
    tempo: str
    prerequisito: str
    fecha: str
    estado: str
    classe: str
    saida: str | None


# ------------------------------------------------------------------ utilidades de texto

def sem_comentarios(md: str) -> str:
    return RE_COMENTARIO.sub("", md)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.replace("*", "").strip().lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def secoes(md: str, nivel: int = 2) -> list[tuple[str, str]]:
    """Divide o texto em (título, corpo) pelos títulos de nível `nivel`; o que vem antes do primeiro
    título entra com título ''."""
    marca = "#" * nivel + " "
    out: list[tuple[str, str]] = []
    titulo, corpo = "", []
    for linha in md.split("\n"):
        if linha.startswith(marca):
            out.append((titulo, "\n".join(corpo)))
            titulo, corpo = linha[len(marca):].strip(), []
        else:
            corpo.append(linha)
    out.append((titulo, "\n".join(corpo)))
    return out


def celulas(linha: str) -> list[str]:
    """Divide uma linha de tabela Markdown pelas barras, ignorando barras dentro de `código`."""
    s = linha.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    out, atual, em_codigo = [], [], False
    for ch in s:
        if ch == "`":
            em_codigo = not em_codigo
        if ch == "|" and not em_codigo:
            out.append("".join(atual).strip())
            atual = []
        else:
            atual.append(ch)
    out.append("".join(atual).strip())
    return out


def primeira_tabela(md: str) -> tuple[list[str], list[list[str]], str]:
    """Cabeçalho, linhas do corpo e o texto que sobra (antes e depois) da primeira tabela do trecho."""
    linhas = md.split("\n")
    ini = next((i for i, l in enumerate(linhas) if l.startswith("|")), None)
    if ini is None:
        return [], [], md
    fim = ini
    while fim < len(linhas) and linhas[fim].startswith("|"):
        fim += 1
    tab = linhas[ini:fim]
    cab = celulas(tab[0])
    corpo = [celulas(l) for l in tab[2:] if not re.match(r"^\|\s*-", l)]
    return cab, corpo, "\n".join(linhas[:ini] + linhas[fim:])


# ------------------------------------------------------------------ pendências

def ler_pendencias(caminho: Path) -> list[Bloco]:
    md = sem_comentarios(caminho.read_text(encoding="utf-8"))
    blocos = []
    for titulo, corpo in secoes(md):
        if not titulo:
            continue
        blocos.append(_bloco(titulo, len(blocos), corpo))
    return blocos


def _bloco(titulo: str, indice: int, corpo: str) -> Bloco:
    partes = secoes(corpo, nivel=3)
    intro = partes[0][1]
    fichas, resto = [], []
    for sub, body in partes[1:]:
        m = RE_FICHA.match(sub)
        if m and "- **Estado:**" in body:
            fichas.append(_ficha(titulo, indice, int(m.group(1)), m.group(2).strip(), body))
        else:
            resto.append(f"### {sub}\n{body}")
    return Bloco(titulo=titulo, intro=intro.strip("\n"), fichas=fichas, resto="\n".join(resto).strip("\n"))


def _ficha(bloco: str, indice: int, numero: int, titulo: str, body: str) -> Ficha:
    campos: dict[str, str] = {}
    listas: dict[str, list[str]] = {}
    atual = None
    for linha in body.split("\n"):
        m = RE_CAMPO.match(linha)
        if m:
            atual = m.group(1).strip()
            campos[atual] = m.group(2).strip()
            continue
        s = RE_SUBITEM.match(linha)
        if s and atual:
            listas.setdefault(atual, []).append(s.group(1).strip())
            continue
        if linha.strip() and atual and not linha.startswith("- "):
            campos[atual] = (campos[atual] + " " + linha.strip()).strip()
    return Ficha(bloco, indice, numero, titulo, campos, listas)


# ------------------------------------------------------------------ roadmap

def classe_fase(estado: str) -> str:
    e = _norm(estado)
    if e.startswith("concluida"):
        return "concluida"
    if e.startswith("em andamento"):
        return "andamento"
    if e.startswith("nao iniciada"):
        return "nao_iniciada"
    return "outro"


def classe_corrida(estado: str) -> str:
    e = _norm(estado)
    for k in ("feita", "rodando", "pendente", "opcional", "aguarda"):
        if e.startswith(k):
            return k
    return "outro"


def ler_roadmap(caminho: Path) -> dict:
    md = sem_comentarios(caminho.read_text(encoding="utf-8"))
    m = re.search(r"^# .*?(\d{2}/\d{2}/\d{4})", md, re.M)
    out: dict = {"data": m.group(1) if m else "", "fases": [], "posicao": "", "corridas": [],
                 "fora_da_maquina": "", "secoes": []}
    for titulo, corpo in secoes(md):
        if not titulo:
            continue
        if titulo.startswith("1. "):
            _, linhas, resto = primeira_tabela(corpo)
            out["fases"] = [Fase(nome=r[0], o_que_e=r[1], estado=r[2], classe=classe_fase(r[2]))
                            for r in linhas if len(r) >= 3]
            out["posicao"] = resto.strip()
        elif titulo.startswith("2. "):  # "2. …" é a tabela de corridas; "2.1 …" e seguintes são texto livre
            cab, linhas, resto = primeira_tabela(corpo)
            idx = {_norm(c): i for i, c in enumerate(cab)}

            def col(r: list[str], prefixo: str) -> str:
                for k, i in idx.items():
                    if k.startswith(prefixo) and i < len(r):
                        return r[i]
                return ""

            for r in linhas:
                mcmd = re.search(r"`([^`]+)`", col(r, "comando"))
                comando = mcmd.group(1) if mcmd else ""
                msai = re.search(r"--?[Ss]aida\s+(\S+)", comando)
                estado = col(r, "estado")
                out["corridas"].append(Corrida(numero=col(r, "#"), nome=col(r, "corrida"), comando=comando,
                                               tempo=col(r, "inferencias"), prerequisito=col(r, "pre-requisito"),
                                               fecha=col(r, "o que fecha"), estado=estado,
                                               classe=classe_corrida(estado),
                                               saida=msai.group(1) if msai else None))
            out["fora_da_maquina"] = resto.strip()
        else:
            out["secoes"].append((titulo, corpo.strip("\n")))
    return out


# ------------------------------------------------------------------ markdown -> html

def inline(s: str) -> str:
    """Negrito, itálico, código e links de um trecho de Markdown; links relativos viram só o texto."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r'<span class="ref">\1</span>', s)
    # ! Alteração de IA - Revisar: os trechos entre crases saem do texto antes do negrito e do itálico e voltam
    # depois, cada um no lugar de uma marca numerada (30/09/2026, noite).
    # ! Motivo: antes o texto era cortado nas crases e o negrito era procurado em cada pedaço; um negrito com
    # nome de modelo dentro (`**decisão 52: `qwen2.5:7b` com L1**`, tabela §1 do roadmap) ficava com metade dos
    # asteriscos em cada pedaço e saía no painel com os `**` à vista. O conteúdo das crases continua intocado
    # (um glob como `a/**/*.log` não vira negrito).
    codigos: list[str] = []

    def guardar(m: re.Match) -> str:
        codigos.append(m.group(1))
        return f"\x00{len(codigos) - 1}\x00"

    s = re.sub(r"`([^`]+)`", guardar, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?![*\w])", r"<em>\1</em>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codigos[int(m.group(1))]}</code>", s)


def tabela_html(linhas: list[str]) -> str:
    cab = celulas(linhas[0])
    corpo = [celulas(l) for l in linhas[2:] if not re.match(r"^\|\s*-", l)]
    th = "".join(f"<th>{inline(c)}</th>" for c in cab)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in corpo)
    return f'<div class="tabela"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def _lista(linhas: list[str], i: int) -> tuple[str, int]:
    itens: list[list] = []
    while i < len(linhas) and re.match(r"^\s*- ", linhas[i]):
        recuo = len(linhas[i]) - len(linhas[i].lstrip())
        texto = linhas[i].lstrip()[2:]
        if recuo == 0 or not itens:
            itens.append([texto, []])
        else:
            itens[-1][1].append(texto)
        i += 1
    saida = []
    for texto, subs in itens:
        sub = ("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in subs) + "</ul>") if subs else ""
        saida.append(f"<li>{inline(texto)}{sub}</li>")
    return "<ul>" + "".join(saida) + "</ul>", i


def md_doc_para_html(md: str) -> str:
    """Documento Markdown simples (títulos ##/###/####, tabelas, listas, listas numeradas, parágrafos)
    em HTML; o título de nível 1 é ignorado (a página tem o seu)."""
    linhas = sem_comentarios(md).split("\n")
    out: list[str] = []
    par: list[str] = []
    i = 0

    def fecha_par() -> None:
        if par:
            out.append(f"<p>{inline(' '.join(par))}</p>")
            par.clear()

    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            fecha_par()
            i += 1
            continue
        if l.startswith("|"):
            fecha_par()
            tab = []
            while i < len(linhas) and linhas[i].startswith("|"):
                tab.append(linhas[i])
                i += 1
            out.append(tabela_html(tab))
            continue
        m = RE_TITULO.match(l)
        if m:
            fecha_par()
            n = len(m.group(1))
            if n > 1:
                out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if re.match(r"^\s*- ", l):
            fecha_par()
            bloco, i = _lista(linhas, i)
            out.append(bloco)
            continue
        if re.match(r"^\d+\. ", l):
            fecha_par()
            itens = []
            while i < len(linhas) and re.match(r"^\d+\. ", linhas[i]):
                itens.append(f"<li>{inline(re.sub(r'^\d+\. ', '', linhas[i]))}</li>")
                i += 1
            out.append("<ol>" + "".join(itens) + "</ol>")
            continue
        par.append(l.strip())
        i += 1
    fecha_par()
    return "\n".join(out)


def html_ficha(f: Ficha) -> str:
    """Um cartão por ficha: número, título, chips de estado e de quem decide, e os campos na ordem fixa."""
    cls = "aberta" if f.aberta else "fechada"
    estado_txt = "Aberta" if f.aberta else (f"Fechada em {f.fechada_em}" if f.fechada_em else "Fechada")
    chips = [f'<span class="chip {cls}">{html.escape(estado_txt)}</span>',
             f'<span class="chip quem">decide: {inline(f.quem)}</span>']
    if f.campos.get("Aberta em"):
        chips.append(f'<span class="chip data">aberta em {inline(f.campos["Aberta em"])}</span>')
    partes: list[str] = []

    def campo_html(campo: str) -> None:
        txt = f.campos.get(campo, "")
        itens = f.listas.get(campo, [])
        if not txt and not itens:
            return
        corpo = f"<p>{inline(txt)}</p>" if txt else ""
        if itens:
            corpo += '<ul class="opcoes">' + "".join(f"<li>{inline(x)}</li>" for x in itens) + "</ul>"
        partes.append(f'<div class="fc"><h4>{html.escape(campo)}</h4>{corpo}</div>')

    for campo in ("O que é", "Por que importa", "Opções", "Recomendação"):
        campo_html(campo)
    dec = f.campos.get("Decisão", "").strip()
    cls_dec = "pendente" if f.decisao_em_aberto else "tomada"
    partes.append(f'<div class="fc decisao {cls_dec}"><h4>Decisão</h4><p>{inline(dec) if dec else "em aberto"}</p></div>')
    for campo, txt in f.campos.items():
        if campo in CAMPOS_CABECALHO or campo in CAMPOS_CORPO:
            continue
        if campo == "Texto original":
            partes.append(f"<details><summary>Texto original</summary><p>{inline(txt)}</p></details>")
        else:
            partes.append(f'<div class="fc"><h4>{html.escape(campo)}</h4><p>{inline(txt)}</p></div>')
    quem = "eric" if "eric" in f.quem.lower() else "outro"
    return (f'<article class="ficha {cls}" id="{f.id_html}" data-estado="{cls}" data-quem="{quem}">'
            f'<header><span class="num">{f.numero}</span><h3>{inline(f.titulo)}</h3>'
            f'<div class="chips">{"".join(chips)}</div></header>{"".join(partes)}</article>')
