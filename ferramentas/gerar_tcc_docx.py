#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (03/11/2026) que gera o documento do TCC em Word (.docx) a partir do Markdown
# `Documentacao/TCC - ABNT 14724 - V1.md`, usando como molde o `Template_TCC_ABNT.docx` que o orientador deixou na pasta
# `TCC/` do repositório da disciplina (cópia em `Documentacao/memorial/4-projeto-de-pesquisa-abnt/`). O script abre o
# molde como zip, mantém estilos, fontes, cabeçalho com o número da página e configurações, e troca só o corpo
# (`word/document.xml`): capa e folha de rosto com os sete autores, resumo e abstract em parágrafo único, listas, sumário
# como campo do Word, seções numeradas com o recuo e a entrelinha do molde, alíneas, citações longas, tabelas com título
# e fonte, referências com entrelinha simples, glossário e apêndices. As marcações de IA (comentários HTML) ficam só no
# Markdown. Saída: `Documentacao/TCC_v<versão>_<AAAAMMDD>.docx` (nome que o orientador pediu) e, com `--copiar-para`, a
# mesma cópia na pasta `TCC/` do clone.
# ! Motivo: o Eric pediu (03/11/2026, ficha 25 opção b) um documento provisório do TCC já no molde do orientador e na
# NBR 14724, para o grupo ver o que melhorar antes da entrega. Escrever direto no Word perderia a rastreabilidade que o
# projeto tem no Markdown (tags de IA, números copiados dos relatórios com a origem em comentário, revisão por script);
# gerar o .docx do Markdown deixa o texto versionado e regenerável a cada versão. A máquina não tem pandoc nem
# LibreOffice, e o pacote `docx` do npm não carrega no Node 14 instalado; mexer no XML do molde com a biblioteca padrão
# do Python é o que funciona aqui e ainda preserva exatamente a formatação que o orientador definiu. Dois pontos em que
# o molde e a norma divergem foram resolvidos pela norma (NBR 14724): papel A4 em vez de Carta, e títulos sem número
# (resumo, listas, sumário, referências, glossário, apêndices) centralizados; o restante segue o molde.
"""Gera o .docx do TCC a partir do Markdown, no molde do orientador.

Uso (na raiz do repositório):
    python ferramentas/gerar_tcc_docx.py                       # Documentacao/TCC - ABNT 14724 - V1.md -> Documentacao/TCC_v1_<data>.docx
    python ferramentas/gerar_tcc_docx.py --copiar-para ../squad-24-projeto/TCC   # e copia para a pasta TCC/ do clone
Opções: --entrada, --molde, --saida (caminho do .docx), --copiar-para (pasta), --folhas N (número fixo no "N f." da ficha
catalográfica; sem ele, a ficha leva um campo do Word, NUMPAGES menos 2, que o Word atualiza ao abrir ou ao exportar o PDF).

Gramática do Markdown de entrada (o que o script entende):
    <!-- ... -->                    comentário: nunca vai para o Word (é onde ficam as tags de IA e a origem dos números)
    ## Dados                        bloco com linhas `- **Chave:** valor` (Universidade, Curso, Autores (um por linha, com `|`),
                                    Título, Subtítulo, Natureza, Orientador, Local, Ano, Versão, Data; opcionais: Grau, CDD, CDU,
                                    Ficha elaborada por, Banca (itens separados por `|`, cada um "Nome com titulação - Instituição"))
    # RESUMO / # ABSTRACT           parágrafo único; a última linha "Palavras-chave: ..." / "Keywords: ..." fica fora do parágrafo
    # AGRADECIMENTOS, # DEDICATÓRIA parágrafos comuns (opcionais)
    # LISTA DE ABREVIATURAS E SIGLAS  linhas `- **SIGLA** significado`
    # LISTA DE TABELAS, # SUMÁRIO   gerados pelo script (campos do Word, com o texto já preenchido)
    # 1 TÍTULO / ## 1.1 Título / ### 1.1.1 Título   seções numeradas (primária em caixa-alta, secundária em negrito, terciária em itálico)
    # REFERÊNCIAS                   um parágrafo por referência (entrelinha simples, alinhadas à esquerda)
    # GLOSSÁRIO                     linhas `**Termo:** definição`
    # APÊNDICE A - Título           seções sem número, com o mesmo corpo das seções textuais
    parágrafo                       texto com **negrito** e *itálico*
    - item                          alíneas a), b), c) (o script completa `;` e `.` se faltarem)
    > texto                         citação longa (recuo de 4 cm, corpo 10, entrelinha simples)
    Tabela: Título                  seguida da tabela em barras `| a | b |` e, opcionalmente, de `Fonte: ...`
    ![Legenda](caminho.png)         figura (PNG ou JPEG) com "Figura N" acima e `Fonte: ...` logo abaixo, se houver
"""
from __future__ import annotations

import argparse
import re
import shutil
import struct
import sys
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "Documentacao" / "TCC - ABNT 14724 - V1.md"
MOLDE = RAIZ / "Documentacao" / "memorial" / "4-projeto-de-pesquisa-abnt" / "Template_TCC_ABNT.docx"
FONTE = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
LARGURA_TEXTO = 9071  # A4 (11906) menos as margens de 3 cm (1701) e 2 cm (1134), em twips
PAGINA = '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1701" w:right="1134" w:bottom="1134" w:left="1701" w:header="720" w:footer="720" w:gutter="0"/>'
PRE_TEXTUAIS = {"DEDICATÓRIA", "AGRADECIMENTOS", "RESUMO", "ABSTRACT", "LISTA DE FIGURAS", "LISTA DE TABELAS",
                "LISTA DE ABREVIATURAS E SIGLAS", "SUMÁRIO"}
POS_TEXTUAIS_PREFIXOS = ("REFERÊNCIAS", "GLOSSÁRIO", "APÊNDICE", "ANEXO")
EMU_POR_TWIP = 635
# ! Alteração de IA - Revisar: (25/11/2026, decisão 158) constantes da ficha catalográfica e da folha de aprovação: caixa de 12,5 x 7,5 cm em twips e a altura útil da página A4 (16838 menos as margens de 1701 e 1134).
# ! Motivo: a ficha (NBR 14724) tem de ter o tamanho exato da caixa e ficar no pé da página; a altura útil serve para calcular o espaço em branco acima dela.
FICHA_LARGURA = 7087
FICHA_ALTURA = 4252
ALTURA_UTIL = 16838 - 1701 - 1134
PARTICULAS = {"de", "da", "do", "das", "dos", "e"}
SUFIXOS_DE_NOME = {"filho", "júnior", "junior", "neto", "sobrinho"}
TITULACOES = {"prof", "profa", "dr", "dra", "me", "ma", "ms", "msc", "mestre", "mestra", "doutor", "doutora", "esp"}
MARCA_FOLHAS = "{FOLHAS}"


class ErroDeEntrada(Exception):
    """Markdown fora da gramática: o chamador decide como avisar."""


# ----------------------------------------------------------------------------------------------------- texto e runs
def run(texto: str, *, b: bool = False, i: bool = False, sz: int = 24, color: str | None = None) -> str:
    props = FONTE + ("<w:b/>" if b else "") + ("<w:i/>" if i else "") + (f'<w:color w:val="{color}"/>' if color else "")
    props += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    partes = texto.split("\t")
    corpo = ""
    for n, parte in enumerate(partes):
        if n:
            corpo += "<w:tab/>"
        if parte:
            corpo += f'<w:t xml:space="preserve">{escape(parte)}</w:t>'
    return f"<w:r><w:rPr>{props}</w:rPr>{corpo}</w:r>"


_INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+`)")


def runs_inline(texto: str, *, sz: int = 24, b: bool = False, i: bool = False, color: str | None = None) -> str:
    """Converte **negrito**, *itálico* e `código` (vira texto simples) em runs; o resto sai como está."""
    saida = ""
    for pedaco in _INLINE.split(texto):
        if not pedaco:
            continue
        if pedaco.startswith("**") and pedaco.endswith("**"):
            saida += run(pedaco[2:-2], b=True, i=i, sz=sz, color=color)
        elif pedaco.startswith("*") and pedaco.endswith("*"):
            saida += run(pedaco[1:-1], b=b, i=True, sz=sz, color=color)
        elif pedaco.startswith("`") and pedaco.endswith("`"):
            saida += run(pedaco[1:-1], b=b, i=i, sz=sz, color=color)
        else:
            saida += run(pedaco, b=b, i=i, sz=sz, color=color)
    return saida


def par(runs: str, *, jc: str | None = "both", before: int = 0, after: int = 120, line: int = 360, first: int = 0,
        left: int = 0, hanging: int = 0, outline: int | None = None, quebra_antes: bool = False, keep_next: bool = False,
        sect: str = "") -> str:
    ppr = ""
    if quebra_antes:
        ppr += "<w:pageBreakBefore/>"
    if keep_next:
        ppr += "<w:keepNext/>"
    ppr += f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    ind = ""
    if left:
        ind += f' w:left="{left}"'
    if hanging:
        ind += f' w:hanging="{hanging}"'
    elif first:
        ind += f' w:firstLine="{first}"'
    if ind:
        ppr += f"<w:ind{ind}/>"
    if jc:
        ppr += f'<w:jc w:val="{jc}"/>'
    if outline is not None:
        ppr += f'<w:outlineLvl w:val="{outline}"/>'
    return f"<w:p><w:pPr>{ppr}{sect}</w:pPr>{runs}</w:p>"


def paragrafo_corpo(texto: str) -> str:
    return par(runs_inline(texto), first=709)


def titulo_sem_numero(texto: str, *, quebra: bool = True) -> str:
    """Títulos de elementos sem indicativo numérico: centralizados (NBR 14724), em negrito e caixa-alta, no sumário.
    Em apêndice e anexo, o hífen entre a letra e o título vira meia-risca (APÊNDICE A – Título), como na norma."""
    texto = re.sub(r"^((?:APÊNDICE|ANEXO) [A-Z]) - ", r"\1 – ", texto.upper())
    return par(run(texto, b=True), jc="center", before=0, after=360, quebra_antes=quebra, outline=0, keep_next=True)


def titulo_numerado(nivel: int, texto: str, *, quebra: bool) -> str:
    if nivel == 1:
        return par(run(texto.upper(), b=True), jc="left", before=0 if quebra else 360, after=240, quebra_antes=quebra,
                   outline=0, keep_next=True)
    if nivel == 2:
        return par(run(texto, b=True), jc="left", before=240, after=120, outline=1, keep_next=True)
    return par(run(texto, i=True), jc="left", before=240, after=120, outline=2, keep_next=True)


# --------------------------------------------------------------------------------------------------- campos do Word
def campo(instr: str, cache: str, *, ppr_extra: str = "") -> str:
    """Campo complexo com o resultado já escrito (o Word atualiza ao abrir, por w:updateFields)."""
    return (f"<w:p><w:pPr>{ppr_extra}</w:pPr>"
            f'<w:r>{_rpr()}<w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            f'<w:r>{_rpr()}<w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
            f'<w:r>{_rpr()}<w:fldChar w:fldCharType="separate"/></w:r>'
            f"{cache}"
            f'<w:r>{_rpr()}<w:fldChar w:fldCharType="end"/></w:r></w:p>')


def _rpr(sz: int = 24) -> str:
    return f'<w:rPr>{FONTE}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'


def campo_simples(instr: str, cache: str, sz: int = 24) -> str:
    return (f'<w:r>{_rpr(sz)}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{_rpr(sz)}<w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
            f'<w:r>{_rpr(sz)}<w:fldChar w:fldCharType="separate"/></w:r>'
            f"{run(cache, sz=sz)}"
            f'<w:r>{_rpr(sz)}<w:fldChar w:fldCharType="end"/></w:r>')


# -------------------------------------------------------------------------------------------------------- tabelas
def tabela(linhas: list[list[str]]) -> str:
    """Tabela no padrão das normas de apresentação tabular: traços horizontais no alto, abaixo do cabeçalho e no pé;
    sem traços verticais; corpo 10; entrelinha simples; largura total do texto."""
    colunas = max(len(l) for l in linhas)
    linhas = [l + [""] * (colunas - len(l)) for l in linhas]
    pesos = [max(len(l[c]) for l in linhas) or 1 for c in range(colunas)]
    pesos = [max(p, 6) for p in pesos]
    total = sum(pesos)
    larguras = [int(LARGURA_TEXTO * p / total) for p in pesos]
    larguras[-1] += LARGURA_TEXTO - sum(larguras)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in larguras)
    xml = (f'<w:tbl><w:tblPr><w:tblW w:w="{LARGURA_TEXTO}" w:type="dxa"/><w:jc w:val="center"/>'
           f'<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
           f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
           f'<w:left w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
           f'<w:tblCellMar><w:left w:w="57" w:type="dxa"/><w:right w:w="57" w:type="dxa"/></w:tblCellMar>'
           f'<w:tblLook w:val="04A0"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>')
    for n, linha in enumerate(linhas):
        cabecalho = n == 0
        trpr = "<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>" if cabecalho else "<w:trPr><w:cantSplit/></w:trPr>"
        celulas = ""
        for c, texto in enumerate(linha):
            borda = ('<w:tcBorders><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>'
                     if cabecalho else "")
            tcpr = f'<w:tcPr><w:tcW w:w="{larguras[c]}" w:type="dxa"/>{borda}<w:vAlign w:val="center"/></w:tcPr>'
            conteudo = par(runs_inline(texto.strip(), sz=20, b=cabecalho), jc="left", after=0, line=240)
            celulas += f"<w:tc>{tcpr}{conteudo}</w:tc>"
        xml += f"<w:tr>{trpr}{celulas}</w:tr>"
    return xml + "</w:tbl>"


def dividir_linha_tabela(linha: str) -> list[str]:
    linha = linha.strip()
    linha = linha.removeprefix("|")
    linha = linha.removesuffix("|")
    return [c.strip() for c in linha.split("|")]


def linha_e_separador(linha: str) -> bool:
    return bool(re.fullmatch(r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?", linha.strip()))


# --------------------------------------------------------------------------------------------------------- figuras
def dimensoes_imagem(dados: bytes) -> tuple[int, int]:
    if dados[:8] == b"\x89PNG\r\n\x1a\n":
        largura, altura = struct.unpack(">II", dados[16:24])
        return largura, altura
    if dados[:2] == b"\xff\xd8":  # JPEG: procura o marcador SOF
        i = 2
        while i < len(dados):
            if dados[i] != 0xFF:
                raise ErroDeEntrada("JPEG inválido")
            marcador = dados[i + 1]
            if marcador in (0xC0, 0xC1, 0xC2):
                altura, largura = struct.unpack(">HH", dados[i + 5:i + 9])
                return largura, altura
            tamanho = struct.unpack(">H", dados[i + 2:i + 4])[0]
            i += 2 + tamanho
    raise ErroDeEntrada("figura precisa ser PNG ou JPEG")


@dataclass
class Figura:
    numero: int
    rid: str
    nome: str
    dados: bytes
    tipo: str


def desenho(fig: Figura) -> str:
    largura_px, altura_px = dimensoes_imagem(fig.dados)
    largura_emu = min(LARGURA_TEXTO * EMU_POR_TWIP, int(largura_px * 9525))  # 96 dpi
    altura_emu = int(largura_emu * altura_px / largura_px)
    return (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{largura_emu}" cy="{altura_emu}"/><wp:docPr id="{fig.numero}" name="Figura {fig.numero}"/>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{fig.numero}" name="{escape(fig.nome)}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{fig.rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{largura_emu}" cy="{altura_emu}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            f"</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>")


# ---------------------------------------------------------------------------------------------------- o documento
@dataclass
class Secao:
    nivel: int  # 0 = sem número (pré ou pós-textual), 1 a 3 = numeradas
    titulo: str
    linhas: list[str] = field(default_factory=list)


@dataclass
class Documento:
    dados: dict[str, str]
    secoes: list[Secao]
    tabelas: list[str] = field(default_factory=list)   # títulos, na ordem, para a lista de tabelas
    figuras: list[Figura] = field(default_factory=list)
    sumario: list[tuple[int, str]] = field(default_factory=list)
    folhas: int | None = None   # número fixo do "N f." da ficha; None = campo do Word


def tirar_comentarios(texto: str) -> str:
    """Tira os comentários HTML e o espaço que sobra antes de pontuação quando o comentário ficava entre a frase e o ponto."""
    sem = re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)
    return re.sub(r"[ \t]+([.,;:)])", r"\1", sem)


def ler_markdown(caminho: Path) -> Documento:
    texto = tirar_comentarios(caminho.read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
    dados: dict[str, str] = {}
    secoes: list[Secao] = []
    atual: Secao | None = None
    em_dados = False
    for linha in texto.split("\n"):
        m = re.match(r"^(#{1,3})\s+(.*\S)\s*$", linha)
        if m:
            nivel, titulo = len(m.group(1)), m.group(2).strip()
            titulo = re.sub(r"^\*\*(.*)\*\*$", r"\1", titulo)
            if nivel == 2 and titulo.lower() == "dados":
                em_dados, atual = True, None
                continue
            em_dados = False
            if nivel == 1 and (titulo.upper() in PRE_TEXTUAIS or titulo.upper().startswith(POS_TEXTUAIS_PREFIXOS)):
                atual = Secao(0, titulo)
            else:
                if not re.match(r"^\d+(\.\d+)*\s", titulo):
                    raise ErroDeEntrada(f"título sem número nem reconhecido como elemento sem número: {titulo!r}")
                atual = Secao(nivel, titulo)
            secoes.append(atual)
            continue
        if em_dados:
            m2 = re.match(r"^-\s+\*\*(.+?):\*\*\s*(.*)$", linha)
            if m2:
                dados[m2.group(1).strip()] = m2.group(2).strip()
            continue
        if atual is not None:
            atual.linhas.append(linha)
        elif linha.strip():
            raise ErroDeEntrada(f"texto antes da primeira seção: {linha[:60]!r}")
    obrigatorios = ["Universidade", "Curso", "Autores", "Título", "Natureza", "Orientador", "Local", "Ano", "Versão", "Data"]
    faltam = [c for c in obrigatorios if not dados.get(c)]
    if faltam:
        raise ErroDeEntrada("faltam no bloco Dados: " + ", ".join(faltam))
    return Documento(dados, secoes)


def blocos(linhas: list[str]):
    """Agrupa as linhas de uma seção em blocos: ('p', texto), ('lista', itens), ('citacao', texto), ('tabela', titulo,
    linhas, fonte), ('figura', legenda, caminho, fonte)."""
    i, n = 0, len(linhas)
    while i < n:
        linha = linhas[i]
        if not linha.strip():
            i += 1
            continue
        if linha.startswith("- "):
            itens = []
            while i < n and linhas[i].startswith("- "):
                itens.append(linhas[i][2:].strip())
                i += 1
            yield ("lista", itens)
            continue
        if linha.startswith(">"):
            partes = []
            while i < n and linhas[i].startswith(">"):
                partes.append(linhas[i].lstrip("> ").strip())
                i += 1
            yield ("citacao", " ".join(p for p in partes if p))
            continue
        if linha.startswith("Tabela:"):
            titulo = linha[len("Tabela:"):].strip()
            i += 1
            while i < n and not linhas[i].strip():
                i += 1
            corpo = []
            while i < n and linhas[i].strip().startswith("|"):
                if not linha_e_separador(linhas[i]):
                    corpo.append(dividir_linha_tabela(linhas[i]))
                i += 1
            fonte = ""
            while i < n and not linhas[i].strip():
                i += 1
            if i < n and linhas[i].startswith("Fonte:"):
                fonte = linhas[i].strip()
                i += 1
            if not corpo:
                raise ErroDeEntrada(f"tabela sem linhas: {titulo!r}")
            yield ("tabela", titulo, corpo, fonte)
            continue
        m = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", linha)
        if m:
            i += 1
            fonte = ""
            while i < n and not linhas[i].strip():
                i += 1
            if i < n and linhas[i].startswith("Fonte:"):
                fonte = linhas[i].strip()
                i += 1
            yield ("figura", m.group(1).strip(), m.group(2).strip(), fonte)
            continue
        partes = []
        while i < n and linhas[i].strip() and not linhas[i].startswith(("- ", ">", "Tabela:", "![")):
            partes.append(linhas[i].rstrip())
            i += 1
        yield ("p", " ".join(p.strip() for p in partes))


def alineas(itens: list[str]) -> str:
    xml = ""
    for k, item in enumerate(itens):
        letra = chr(ord("a") + k) if k < 26 else f"{k + 1}"
        texto = item.rstrip()
        ultimo = k == len(itens) - 1
        if not texto.endswith((";", ".", ":", "!", "?")):
            texto += "." if ultimo else ";"
        xml += par(runs_inline(f"{letra}) {texto}"), left=1134, hanging=425, after=60)
    return xml


def corpo_da_secao(sec: Secao, doc: Documento, entrada: Path, *, referencias: bool = False, glossario: bool = False,
                   siglas: bool = False) -> str:
    xml = ""
    for bloco in blocos(sec.linhas):
        tipo = bloco[0]
        if tipo == "p":
            texto = bloco[1]
            if referencias:
                xml += par(runs_inline(texto), jc="left", after=240, line=240)
            elif glossario:
                xml += par(runs_inline(texto), after=120)
            elif siglas:
                xml += par(runs_inline(texto), jc="left", after=60, line=360)
            else:
                xml += paragrafo_corpo(texto)
        elif tipo == "lista":
            if siglas:
                for item in bloco[1]:
                    xml += par(runs_inline(item), jc="left", after=60, left=0)
            else:
                xml += alineas(bloco[1])
        elif tipo == "citacao":
            xml += par(runs_inline(bloco[1], sz=20), left=2268, after=240, line=240)
        elif tipo == "tabela":
            _, titulo, corpo, fonte = bloco
            doc.tabelas.append(titulo)
            numero = len(doc.tabelas)
            legenda = run("Tabela ", sz=24) + campo_simples("SEQ Tabela \\* ARABIC", str(numero)) + run(f" – {titulo}", sz=24)
            xml += par(legenda, jc="center", before=240, after=120, keep_next=True)
            xml += tabela(corpo)
            xml += par(runs_inline(fonte or "Fonte: elaborado pelos autores.", sz=20), jc="left", before=60, after=240, line=240)
        elif tipo == "figura":
            _, legenda, caminho, fonte = bloco
            arquivo = (entrada.parent / caminho).resolve()
            if not arquivo.is_file():
                raise ErroDeEntrada(f"figura não encontrada: {arquivo}")
            numero = len(doc.figuras) + 1
            tipo_img = "png" if arquivo.suffix.lower() == ".png" else "jpeg"
            fig = Figura(numero, f"rIdFig{numero}", arquivo.name, arquivo.read_bytes(), tipo_img)
            doc.figuras.append(fig)
            titulo = run("Figura ", sz=24) + campo_simples("SEQ Figura \\* ARABIC", str(numero)) + run(f" – {legenda}", sz=24)
            xml += par(titulo, jc="center", before=240, after=120, keep_next=True)
            xml += par(desenho(fig), jc="center", after=120, line=240, keep_next=True)
            xml += par(runs_inline(fonte or "Fonte: elaborado pelos autores.", sz=20), jc="left", before=60, after=240, line=240)
    return xml


# ! Alteração de IA - Revisar: (25/11/2026, decisão 158) bloco novo: ficha catalográfica e folha de aprovação, mais as funções
# de nome (inverter_nome, sem_titulacao, romano) que a ficha usa para montar a entrada pelo sobrenome e as entradas secundárias.
# ! Motivo: o TCC passa a ser entregue com folha de aprovação e ficha catalográfica (NBR 14724) na ordem capa, folha de rosto,
# ficha, aprovação, dedicatória, agradecimentos, resumo, abstract, listas, sumário. As regras de nome seguem o uso brasileiro:
# o último sobrenome vai para a frente, "de/da/do/das/dos/e" ficam no fim do prenome, e Filho/Júnior/Neto/Sobrinho acompanham
# o sobrenome ("Silva Filho, João da"). Tudo sai do bloco Dados, sem digitar a ficha à mão.
def inverter_nome(nome: str) -> str:
    """"Guilherme Penha dos Santos" -> "Santos, Guilherme Penha dos"; "João da Silva Filho" -> "Silva Filho, João da"."""
    partes = nome.split()
    if len(partes) < 2:
        return nome.strip()
    n_sobrenome = 2 if partes[-1].lower() in SUFIXOS_DE_NOME and len(partes) > 2 else 1
    return f"{' '.join(partes[-n_sobrenome:])}, {' '.join(partes[:-n_sobrenome])}"


def sem_titulacao(nome: str) -> str:
    """Tira "Prof.", "Me.", "Dr." etc. do começo do nome do orientador."""
    partes = nome.split()
    while partes and partes[0].rstrip(".").lower() in TITULACOES:
        partes.pop(0)
    return " ".join(partes)


def romano(n: int) -> str:
    saida = ""
    for valor, letra in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                         (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= valor:
            saida += letra
            n -= valor
    return saida


def lista_de_autores(d: dict[str, str]) -> list[str]:
    return [a.strip() for a in d["Autores"].split("|") if a.strip()]


def orientador_rotulo_e_nome(d: dict[str, str]) -> tuple[str, str]:
    """O campo Orientador do bloco Dados vem como "Orientador: Prof. Me. Fulano"; devolve ("Orientador", "Prof. Me. Fulano")."""
    m = re.match(r"^(Orientador|Orientadora)\s*:\s*(.*)$", d["Orientador"].strip())
    return (m.group(1), m.group(2).strip()) if m else ("Orientador", d["Orientador"].strip())


def palavras_chave(doc: Documento) -> list[str]:
    """Palavras-chave da linha "Palavras-chave: a; b; c." do RESUMO, na ordem em que aparecem."""
    for sec in doc.secoes:
        if sec.titulo.upper() == "RESUMO":
            for linha in sec.linhas:
                m = re.match(r"^\s*Palavras-chave:\s*(.*?)\.?\s*$", linha)
                if m:
                    return [p.strip() for p in m.group(1).split(";") if p.strip()]
    return []


def cdd_cdu(d: dict[str, str]) -> str:
    partes = [f"{k} {d[k]}" for k in ("CDD", "CDU") if d.get(k)]
    return " / ".join(partes)


def frase_da_ficha(d: dict[str, str]) -> str:
    quem = d.get("Ficha elaborada por")
    return f"Ficha catalográfica elaborada por {quem}." if quem else "Ficha catalográfica elaborada pelos autores."


def _maiuscula_inicial(texto: str) -> str:
    return texto[:1].upper() + texto[1:]


def linhas_da_ficha(d: dict[str, str], chaves: list[str], folhas: str) -> list[str]:
    """Texto da ficha, uma linha por parágrafo ("" separa os grupos); `folhas` entra em "N f. : il."."""
    autores = lista_de_autores(d)
    titulo = d["Título"].rstrip(": ")
    subtitulo = d.get("Subtítulo", "").strip()
    if subtitulo:
        inicial = subtitulo[:1].lower() + subtitulo[1:] if subtitulo[1:2].islower() else subtitulo
        titulo += f" : {inicial}"
    if len(autores) > 3:
        quem = f"{autores[0]} [et al.]"
    elif len(autores) > 1:
        quem = ", ".join(autores[:-1]) + " e " + autores[-1]
    else:
        quem = autores[0]
    rotulo, orientador = orientador_rotulo_e_nome(d)
    grau = d.get("Grau", "Graduação")
    assuntos = " ".join(f"{k}. {_maiuscula_inicial(p)}." for k, p in enumerate(chaves, 1))
    secundarias = [inverter_nome(a) + "." for a in autores[1:]]
    secundarias.append(inverter_nome(sem_titulacao(orientador)) + ", orient.")
    secundarias.append("Título.")
    romanas = " ".join(f"{romano(k)}. {t}" for k, t in enumerate(secundarias, 1))
    return [
        inverter_nome(autores[0]),
        f"{titulo} / {quem}. – {d['Local']}, {d['Ano']}.",
        f"{folhas} f. : il.",
        "",
        f"{rotulo}: {orientador}.",
        f"Trabalho de Conclusão de Curso ({grau}) – {d['Universidade']}, {d['Local']}, {d['Ano']}.",
        "",
        (assuntos + " " + romanas).strip(),
    ]


def campo_folhas(cache: str = "0") -> str:
    """{ = { NUMPAGES } - 2 }: total de páginas do arquivo menos a capa e a própria página da ficha."""
    r = _rpr(20)
    return (f'<w:r>{r}<w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            f'<w:r>{r}<w:instrText xml:space="preserve"> = </w:instrText></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{r}<w:instrText xml:space="preserve"> NUMPAGES </w:instrText></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'{run("0", sz=20)}'
            f'<w:r>{r}<w:fldChar w:fldCharType="end"/></w:r>'
            f'<w:r>{r}<w:instrText xml:space="preserve"> - 2 </w:instrText></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'{run(cache, sz=20)}'
            f'<w:r>{r}<w:fldChar w:fldCharType="end"/></w:r>')


def secao_do_word(numero_inicial: int | None = None) -> str:
    num = f'<w:pgNumType w:start="{numero_inicial}"/>' if numero_inicial is not None else ""
    return f'<w:sectPr>{PAGINA}{num}<w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr>'


def ficha_catalografica(d: dict[str, str], chaves: list[str], folhas: int | None) -> str:
    """Página da ficha: espaço em branco, caixa de 12,5 x 7,5 cm (tabela de uma célula, altura exata) e, abaixo dela, a frase
    de quem elaborou. O último parágrafo fecha a seção do Word da ficha (página que não entra na numeração impressa)."""
    texto = linhas_da_ficha(d, chaves, MARCA_FOLHAS)
    paragrafos = ""
    for k, linha in enumerate(texto):
        if not linha:
            paragrafos += par("", jc="left", after=0, line=240)
            continue
        recuo = {"left": 0} if k == 0 else {"left": 397}
        if MARCA_FOLHAS in linha:
            runs = campo_folhas() if folhas is None else run(str(folhas), sz=20)
            runs += run(linha.replace(MARCA_FOLHAS, ""), sz=20)
        else:
            runs = run(linha, sz=20)
        paragrafos += par(runs, jc="left", after=0, line=240, **recuo)
    codigos = cdd_cdu(d)
    if codigos:
        paragrafos += par(run(codigos, sz=20), jc="right", before=120, after=0, line=240)
    borda = "".join(f'<w:{lado} w:val="single" w:sz="6" w:space="0" w:color="000000"/>' for lado in ("top", "left", "bottom", "right"))
    caixa = (f'<w:tbl><w:tblPr><w:tblW w:w="{FICHA_LARGURA}" w:type="dxa"/><w:jc w:val="center"/>'
             f'<w:tblBorders>{borda}</w:tblBorders><w:tblLayout w:type="fixed"/>'
             f'<w:tblCellMar><w:top w:w="113" w:type="dxa"/><w:left w:w="170" w:type="dxa"/><w:bottom w:w="113" w:type="dxa"/>'
             f'<w:right w:w="170" w:type="dxa"/></w:tblCellMar><w:tblLook w:val="04A0"/></w:tblPr>'
             f'<w:tblGrid><w:gridCol w:w="{FICHA_LARGURA}"/></w:tblGrid>'
             f'<w:tr><w:trPr><w:cantSplit/><w:trHeight w:val="{FICHA_ALTURA}" w:hRule="exact"/></w:trPr>'
             f'<w:tc><w:tcPr><w:tcW w:w="{FICHA_LARGURA}" w:type="dxa"/><w:vAlign w:val="top"/></w:tcPr>{paragrafos}</w:tc></w:tr></w:tbl>')
    # espaço acima da caixa: altura útil menos a caixa, a linha da frase (corpo 10) e uma folga de 38 pontos (com folga de 8 pontos o Word jogou a frase para uma página só dela)
    espaco = ALTURA_UTIL - FICHA_ALTURA - 240 - 760
    xml = (f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="{espaco}" w:lineRule="exact"/></w:pPr></w:p>' + caixa)
    xml += par(run(frase_da_ficha(d), sz=20), jc="center", before=60, after=0, line=240, sect=secao_do_word())
    return xml


def folha_de_aprovacao(d: dict[str, str]) -> str:
    autores = lista_de_autores(d)
    titulo, subtitulo = d["Título"], d.get("Subtítulo", "")
    xml = ""
    for k, autor in enumerate(autores):
        xml += par(run(autor.upper(), b=True), jc="center", after=600 if k == len(autores) - 1 else 40)
    xml += par(run(titulo.upper() + (":" if subtitulo and not titulo.endswith(":") else ""), b=True, sz=28), jc="center", after=60)
    if subtitulo:
        xml += par(run(subtitulo, i=True, sz=26), jc="center", after=480)
    xml += par(run(d["Natureza"], sz=20), jc="both", left=4535, after=360, line=240)
    xml += par(run("Aprovado em: ____/____/________."), jc="center", after=360)
    xml += par(run("BANCA EXAMINADORA", b=True), jc="center", after=240, keep_next=True)
    rotulo, orientador = orientador_rotulo_e_nome(d)
    blocos_banca = [(orientador, f"({rotulo})", d["Universidade"])]
    if d.get("Banca"):
        for item in [i.strip() for i in d["Banca"].split("|") if i.strip()]:
            nome, _, instituicao = item.partition(" - ")
            blocos_banca.append((nome.strip(), "", instituicao.strip()))
    else:
        blocos_banca += [("Examinador(a)", "", ""), ("Examinador(a)", "", "")]
    for nome, papel, instituicao in blocos_banca:
        xml += par(run("_" * 50), jc="center", before=560, after=0, line=240, keep_next=True)
        xml += par(run(nome, sz=22), jc="center", after=0, line=240, keep_next=True)
        if papel:
            xml += par(run(papel, sz=22), jc="center", after=0, line=240, keep_next=True)
        if instituicao:
            xml += par(run(instituicao, sz=22), jc="center", after=0, line=240)
    return xml


def capa_e_folha_de_rosto(d: dict[str, str], sect_final: str = "") -> str:
    autores = [a.strip() for a in d["Autores"].split("|") if a.strip()]
    titulo, subtitulo = d["Título"], d.get("Subtítulo", "")
    xml = par(run(d["Universidade"].upper(), b=True), jc="center", after=120)
    xml += par(run(d["Curso"].upper(), b=True), jc="center", after=1200)
    for k, autor in enumerate(autores):
        xml += par(run(autor.upper(), b=True, sz=26), jc="center", after=1600 if k == len(autores) - 1 else 60)
    xml += par(run(titulo.upper() + (":" if subtitulo and not titulo.endswith(":") else ""), b=True, sz=32), jc="center", after=80)
    if subtitulo:
        xml += par(run(subtitulo, i=True, sz=28), jc="center", after=2000)
    xml += par(run(d["Local"]), jc="center", after=80)
    xml += par(run(d["Ano"]), jc="center", after=0)
    # folha de rosto
    for k, autor in enumerate(autores):
        xml += par(run(autor.upper(), b=True, sz=24), jc="center", after=1400 if k == len(autores) - 1 else 60,
                   quebra_antes=(k == 0))
    xml += par(run(titulo.upper() + (":" if subtitulo and not titulo.endswith(":") else ""), b=True, sz=32), jc="center", after=80)
    if subtitulo:
        xml += par(run(subtitulo, i=True, sz=28), jc="center", after=1000)
    xml += par(run(d["Natureza"], sz=20), jc="both", left=4535, after=240, line=240)
    xml += par(run(d["Orientador"], sz=20), jc="left", left=4535, after=1800, line=240)
    xml += par(run(d["Local"]), jc="center", after=80)
    # ! Alteração de IA - Revisar: o último parágrafo da folha de rosto (o ano) passa a fechar a primeira seção do Word (capa e folha de rosto), recebendo `sect_final`.
    # ! Motivo: a ficha catalográfica (verso da folha de rosto) precisa começar em seção própria para não entrar na numeração impressa.
    xml += par(run(d["Ano"]), jc="center", after=0, sect=sect_final)
    return xml


def resumo(sec: Secao) -> str:
    """Parágrafo único, sem recuo, entrelinha simples; a linha das palavras-chave fica separada."""
    linhas = [l.strip() for l in sec.linhas if l.strip()]
    chaves = [l for l in linhas if re.match(r"^(Palavras-chave|Keywords):", l)]
    corpo = " ".join(l for l in linhas if l not in chaves)
    xml = titulo_sem_numero(sec.titulo)
    xml += par(runs_inline(corpo), after=360, line=240)
    for chave in chaves:
        xml += par(runs_inline(chave), jc="left", after=0, line=240)
    return xml


def montar_corpo(doc: Documento, entrada: Path) -> str:
    d = doc.dados
    # ! Alteração de IA - Revisar: o começo do documento passa a ser 4 seções do Word: (1) capa e folha de rosto, numeração começando em 0 (capa = 0, folha de rosto = 1); (2) ficha catalográfica, sem número e sem reiniciar; (3) folha de aprovação até o sumário, recomeçando em 2; (4) texto, com o cabeçalho do número e a contagem seguindo.
    # ! Motivo: antes eram duas seções (capa a sumário, texto). A ficha é o verso da folha de rosto e não conta como folha; sem seção própria, a primeira página da Introdução sairia com número uma unidade maior do que o "N f." da ficha prevê.
    pre = capa_e_folha_de_rosto(d, sect_final=secao_do_word(0))
    pre += ficha_catalografica(d, palavras_chave(doc), doc.folhas)
    pre += folha_de_aprovacao(d)
    textuais = ""
    pos = ""
    pre_opcionais = {}
    listas_siglas = ""
    # primeiro passa pelas seções numeradas e pós-textuais, para saber o sumário e a lista de tabelas
    for sec in doc.secoes:
        t = sec.titulo.upper()
        if sec.nivel == 0 and t in PRE_TEXTUAIS:
            if t in ("RESUMO", "ABSTRACT"):
                pre_opcionais[t] = resumo(sec)
            elif t == "LISTA DE ABREVIATURAS E SIGLAS":
                listas_siglas = titulo_sem_numero(sec.titulo) + corpo_da_secao(sec, doc, entrada, siglas=True)
            elif t in ("DEDICATÓRIA", "AGRADECIMENTOS"):
                pre_opcionais[t] = titulo_sem_numero(sec.titulo) + corpo_da_secao(sec, doc, entrada)
            continue  # LISTA DE TABELAS e SUMÁRIO são gerados
        if sec.nivel == 0:
            doc.sumario.append((0, sec.titulo))
            pos += titulo_sem_numero(sec.titulo)
            pos += corpo_da_secao(sec, doc, entrada, referencias=t.startswith("REFERÊNCIAS"), glossario=t.startswith("GLOSSÁRIO"))
        else:
            doc.sumario.append((sec.nivel - 1, sec.titulo))
            textuais += titulo_numerado(sec.nivel, sec.titulo, quebra=(sec.nivel == 1))
            textuais += corpo_da_secao(sec, doc, entrada)
    for chave in ("DEDICATÓRIA", "AGRADECIMENTOS", "RESUMO", "ABSTRACT"):
        pre += pre_opcionais.get(chave, "")
    if doc.figuras:
        pre += titulo_sem_numero("Lista de figuras")
        pre += campo_em_paragrafos('TOC \\h \\z \\c "Figura"', [(0, f"Figura {f.numero}") for f in doc.figuras], negrito=False)
    if doc.tabelas:
        pre += titulo_sem_numero("Lista de tabelas")
        pre += campo_em_paragrafos('TOC \\h \\z \\c "Tabela"', [(0, f"Tabela {n} – {t}") for n, t in enumerate(doc.tabelas, 1)], negrito=False)
    pre += listas_siglas
    pre += titulo_sem_numero("Sumário")
    pre += campo_em_paragrafos('TOC \\o "1-3" \\h \\z \\u', doc.sumario, negrito=True)
    quebra_de_secao = par("", sect=secao_do_word(2), after=0, line=240)
    return pre + quebra_de_secao + textuais + pos


def campo_em_paragrafos(instr: str, itens: list[tuple[int, str]], *, negrito: bool) -> str:
    """Campo TOC cujo resultado em cache ocupa vários parágrafos: o begin fica no primeiro e o end no último."""
    if not itens:
        itens = [(0, "")]
    xml = ""
    for k, (nivel, texto) in enumerate(itens):
        comeco = (f'<w:r>{_rpr()}<w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
                  f'<w:r>{_rpr()}<w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
                  f'<w:r>{_rpr()}<w:fldChar w:fldCharType="separate"/></w:r>') if k == 0 else ""
        fim = f'<w:r>{_rpr()}<w:fldChar w:fldCharType="end"/></w:r>' if k == len(itens) - 1 else ""
        xml += par(comeco + run(texto, b=(nivel == 0 and negrito)) + fim, jc="left", after=0, line=360, left=nivel * 425)
    return xml


def propriedades_core(d: dict[str, str]) -> str:
    """docProps/core.xml novo: autores do bloco Dados, título e datas da geração; nada herdado do molde."""
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    autores = escape("; ".join(lista_de_autores(d)))
    titulo = d["Título"].rstrip(": ") + (f": {d['Subtítulo']}" if d.get("Subtítulo") else "")
    return ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{escape(titulo)}</dc:title><dc:creator>{autores}</dc:creator>"
            f"<cp:lastModifiedBy>{autores}</cp:lastModifiedBy><cp:revision>1</cp:revision>"
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{agora}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{agora}</dcterms:modified></cp:coreProperties>')


def propriedades_app(app: str) -> str:
    """docProps/app.xml do molde sem Template, Manager e Company (o Application deixa de dizer "Macintosh")."""
    app = re.sub(r"\s*<(Template|Manager|Company)(/>|>.*?</\1>)", "", app, flags=re.DOTALL)
    return app.replace("Microsoft Macintosh Word", "Microsoft Office Word")


def gerar(entrada: Path, molde: Path, saida: Path, folhas: int | None = None) -> Documento:
    # ! Alteração de IA - Revisar: (25/11/2026, decisão 158) `gerar` aceita `folhas` (número fixo do "N f." da ficha), troca `docProps/core.xml` e `docProps/app.xml` do molde por propriedades próprias e não copia mais a miniatura `docProps/thumbnail.jpeg` do molde.
    # ! Motivo: o arquivo saía com autor "python-docx", descrição "generated by python-docx", datas de 2013 e a miniatura da primeira página do molde; a entrega não pode carregar propriedade que não seja dos autores (nem rastro de ferramenta).
    doc = ler_markdown(entrada)
    doc.folhas = folhas
    corpo = montar_corpo(doc, entrada)
    with zipfile.ZipFile(molde) as z:
        nomes = z.namelist()
        documento = z.read("word/document.xml").decode("utf-8")
        settings = z.read("word/settings.xml").decode("utf-8")
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        tipos = z.read("[Content_Types].xml").decode("utf-8")
        outros = {n: z.read(n) for n in nomes if n not in ("word/document.xml", "word/settings.xml", "docProps/thumbnail.jpeg",
                                                             "word/_rels/document.xml.rels", "[Content_Types].xml")}
    outros["docProps/core.xml"] = propriedades_core(doc.dados).encode("utf-8")
    outros["docProps/app.xml"] = propriedades_app(outros["docProps/app.xml"].decode("utf-8")).encode("utf-8")
    outros["_rels/.rels"] = re.sub(r"<Relationship [^>]*thumbnail[^>]*/>", "", outros["_rels/.rels"].decode("utf-8")).encode("utf-8")
    m = re.search(r"<w:body>(.*)</w:body>", documento, re.DOTALL)
    if not m:
        raise ErroDeEntrada("molde sem <w:body>")
    sect_final = re.search(r"<w:sectPr[ >].*?</w:sectPr>", m.group(1), re.DOTALL).group(0)
    sect_final = re.sub(r'<w:pgSz [^>]*/><w:pgMar [^>]*/>', PAGINA, sect_final)
    sect_final = re.sub(r' w:rsid\w*="[^"]*"', "", sect_final)
    raiz = documento[:m.start(1)]
    if 'xmlns:wp=' not in raiz:
        raiz = raiz.replace("<w:document ", '<w:document xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" ', 1)
    novo = raiz + corpo + sect_final + "</w:body>" + documento[m.end():]
    # ! Alteração de IA - Revisar: tira `<w:savePreviewPicture/>` das configurações do molde.
    # ! Motivo: com essa opção o Word grava no arquivo uma miniatura da primeira página (`docProps/thumbnail.jpeg`) toda vez que salva; o arquivo entregue não precisa dela.
    settings = settings.replace("<w:savePreviewPicture/>", "")
    if "<w:updateFields" not in settings:
        settings = settings.replace("<w:defaultTabStop", '<w:updateFields w:val="true"/><w:defaultTabStop', 1)
    for fig in doc.figuras:
        rels = rels.replace("</Relationships>",
                            f'<Relationship Id="{fig.rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fig.nome}"/></Relationships>')
        outros[f"word/media/{fig.nome}"] = fig.dados
        ext = "png" if fig.tipo == "png" else "jpeg"
        if f'Extension="{ext}"' not in tipos:
            tipos = tipos.replace("</Types>", f'<Default Extension="{ext}" ContentType="image/{ext}"/></Types>')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", tipos)
        for nome, dados in outros.items():
            z.writestr(nome, dados)
        z.writestr("word/document.xml", novo.encode("utf-8"))
        z.writestr("word/settings.xml", settings.encode("utf-8"))
        z.writestr("word/_rels/document.xml.rels", rels.encode("utf-8"))
    return doc


def nome_de_saida(doc: Documento) -> str:
    data = datetime.strptime(doc.dados["Data"], "%d/%m/%Y")
    return f"TCC_v{doc.dados['Versão']}_{data:%Y%m%d}.docx"


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", type=Path, default=ENTRADA)
    ap.add_argument("--molde", type=Path, default=MOLDE)
    ap.add_argument("--saida", type=Path, default=None, help="caminho do .docx (padrão: Documentacao/TCC_v<versão>_<data>.docx)")
    ap.add_argument("--copiar-para", type=Path, default=None, help="pasta que recebe uma cópia (a TCC/ do clone do orientador)")
    ap.add_argument("--folhas", type=int, default=None, help="número fixo do \"N f.\" da ficha catalográfica (padrão: campo do Word)")
    args = ap.parse_args(argv)
    try:
        doc_prev = ler_markdown(args.entrada)
        saida = args.saida or (args.entrada.parent / nome_de_saida(doc_prev))
        doc = gerar(args.entrada, args.molde, saida, folhas=args.folhas)
    except ErroDeEntrada as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    numeradas = sum(1 for s in doc.secoes if s.nivel)
    palavras = sum(len(" ".join(s.linhas).split()) for s in doc.secoes)
    print(f"Gerado: {saida} ({numeradas} seções numeradas, {len(doc.tabelas)} tabelas, {len(doc.figuras)} figuras, "
          f"cerca de {palavras} palavras no Markdown)")
    if args.copiar_para:
        destino = args.copiar_para / saida.name
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(saida, destino)
        print(f"Cópia: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
