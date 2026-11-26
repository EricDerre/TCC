#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (25/11/2026, decisão 158) que confere o .docx e o PDF do TCC antes da entrega e acusa qualquer marcação de IA: a tag `! Alteração de IA - Revisar` e as linhas `! Motivo:` (que vivem em comentários do Markdown), comentário do Word, texto oculto, alteração controlada, propriedades do arquivo (autor, último a salvar, programa, empresa) que citem ferramenta ou fornecedor de IA, texto alternativo e nome de imagem, blocos de texto dos PNG embutidos, variáveis do documento, customXml, e no PDF os metadados (Info e XMP), anotações, arquivos embutidos, camadas ocultas, texto invisível e a tag no texto das páginas. Sai com 0 se tudo estiver limpo e com 1 se achar qualquer marcação.
# ! Motivo: a decisão 158 do Eric manda entregar o TCC em PDF e em Word "sem nenhuma marcação de IA (inclusive as ocultas)". O texto visível é revisado a olho, mas as marcas ocultas (um comentário esquecido, o autor "python-docx" ou "Claude" nas propriedades, texto com `w:vanish`) não aparecem na leitura; só uma conferência por script as encontra. O corpo visível pode citar Claude Code, Ollama e Qwen (a seção 5.8 declara o uso do agente de apoio): isso não é falha, por isso os termos de IA só são procurados onde não há texto de leitura (propriedades, customXml, docVars, nomes e descrições de imagem, blocos dos PNG, metadados do PDF).
"""Confere se o .docx e o PDF do TCC estão sem marcação de IA.

Uso:
    python ferramentas/conferir_entrega_tcc.py arquivo.docx arquivo.pdf [--json saida.json]
Sai com 0 (tudo limpo) ou 1 (achou alguma marcação). Imprime uma linha por conferência (OK, AVISO ou FALHA) e, sempre, as
propriedades do arquivo (autor, último a salvar, programa) para uma pessoa ler. Com o PyMuPDF instalado a conferência do PDF é
completa; sem ele, o script avisa e confere só metadados e busca bruta, dizendo o que não conferiu.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path

TERMOS_DE_IA = re.compile(r"claude|anthropic|chatgpt|openai|copilot|gemini|deepseek|gpt-", re.IGNORECASE)
CADEIAS_DA_TAG = ("de IA - Revisar", "! Motivo:")
TIPOS_DE_ANOTACAO = ("Text", "FreeText", "Highlight", "Underline", "StrikeOut", "Squiggly", "Stamp", "Caret", "Ink", "Popup",
                     "FileAttachment", "Line", "Square", "Circle", "Polygon", "PolyLine", "Sound", "Movie", "Redact")

Resultado = tuple[str, str, str]   # (nome da conferência, "OK" | "AVISO" | "FALHA", onde achou / observação)


def _ok(nome: str, achados: list[str], aviso: bool = False) -> Resultado:
    if not achados:
        return (nome, "OK", "")
    return (nome, "AVISO" if aviso else "FALHA", "; ".join(achados[:8]) + (f" (+{len(achados) - 8})" if len(achados) > 8 else ""))


def _texto(dados: bytes) -> str:
    return dados.decode("utf-8", errors="replace")


def _partes_xml(z: zipfile.ZipFile) -> list[str]:
    return [n for n in z.namelist() if n.lower().endswith((".xml", ".rels", ".txt", ".vml"))]


def _valor(xml: str, tag: str) -> str:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", xml, re.DOTALL)
    return html.unescape(m.group(1)).strip() if m else ""


# ------------------------------------------------------------------------------------------------------------- .docx
def _png_blocos_de_texto(dados: bytes) -> list[str]:
    """Texto dos blocos tEXt, zTXt e iTXt de um PNG (devolve vazio se não for PNG)."""
    if dados[:8] != b"\x89PNG\r\n\x1a\n":
        return []
    saida, i = [], 8
    while i + 8 <= len(dados):
        tamanho, tipo = struct.unpack(">I4s", dados[i:i + 8])
        corpo = dados[i + 8:i + 8 + tamanho]
        i += 12 + tamanho
        try:
            if tipo == b"tEXt":
                saida.append(corpo.decode("latin-1").replace("\x00", ": "))
            elif tipo == b"zTXt":
                chave, resto = corpo.split(b"\x00", 1)
                saida.append(chave.decode("latin-1") + ": " + zlib.decompress(resto[1:]).decode("latin-1"))
            elif tipo == b"iTXt":
                chave, resto = corpo.split(b"\x00", 1)
                comprimido, metodo = resto[0], resto[1]
                _lingua, _traduzida, texto = resto[2:].split(b"\x00", 2)
                if comprimido:
                    texto = zlib.decompress(texto)
                saida.append(chave.decode("latin-1") + ": " + texto.decode("utf-8", errors="replace"))
        except (ValueError, zlib.error):
            saida.append("(bloco de texto ilegível)")
        if tipo == b"IEND":
            break
    return saida


def conferir_docx(caminho: Path) -> tuple[list[Resultado], dict[str, str]]:
    resultados: list[Resultado] = []
    info: dict[str, str] = {}
    with zipfile.ZipFile(caminho) as z:
        nomes = z.namelist()
        xmls = {n: _texto(z.read(n)) for n in _partes_xml(z)}
        binarios = {n: z.read(n) for n in nomes if n.lower().startswith(("word/media/", "word/embeddings/"))}
        partes_word = {n: t for n, t in xmls.items() if n.startswith("word/") and n.endswith(".xml")}

        # propriedades para leitura humana
        core, app, custom = xmls.get("docProps/core.xml", ""), xmls.get("docProps/app.xml", ""), xmls.get("docProps/custom.xml", "")
        info["Autor (dc:creator)"] = _valor(core, "dc:creator")
        info["Último a salvar (cp:lastModifiedBy)"] = _valor(core, "cp:lastModifiedBy")
        info["Título (dc:title)"] = _valor(core, "dc:title")
        info["Programa (Application)"] = _valor(app, "Application")
        info["Empresa (Company)"] = _valor(app, "Company")
        info["Gerente (Manager)"] = _valor(app, "Manager")

        # 1. a tag e os comentários do Markdown em qualquer parte de texto
        achados = []
        for nome, xml in xmls.items():
            visivel = html.unescape(xml)
            for cadeia in CADEIAS_DA_TAG:
                if cadeia in visivel:
                    achados.append(f"{nome}: «{cadeia}»")
            if nome.startswith("word/") and nome.endswith(".xml"):
                texto_dos_runs = html.unescape("".join(re.findall(r"<w:(?:t|instrText|delText)[^>]*>([^<]*)</w:(?:t|instrText|delText)>", xml)))
                if "<!--" in texto_dos_runs:
                    achados.append(f"{nome}: «<!--» no texto")
            elif "&lt;!--" in xml:
                achados.append(f"{nome}: «<!--» escapado")
        resultados.append(_ok("Tag de IA e comentários do Markdown no texto", achados))

        # 2. comentários do Word
        achados = [n for n in nomes if re.fullmatch(r"word/(comments\w*|people)\.xml", n)]
        for nome, xml in partes_word.items():
            if re.search(r"<w:(commentRangeStart|commentRangeEnd|commentReference)\b", xml):
                achados.append(f"{nome}: referência a comentário")
        resultados.append(_ok("Comentários do Word", achados))

        # 3. texto oculto (w:webHidden é normal no sumário e não conta; w:vanish com val 0/false/off está desligado)
        achados = []
        for nome, xml in partes_word.items():
            for m in re.finditer(r"<w:(vanish|specVanish)\b([^>]*)>", xml):
                if not re.search(r'w:val="(0|false|off)"', m.group(2)):
                    achados.append(f"{nome}: w:{m.group(1)}")
                    break
        resultados.append(_ok("Texto oculto (w:vanish, w:specVanish)", achados))

        # 4. alterações controladas
        achados = []
        for nome, xml in partes_word.items():
            achou = sorted(set(re.findall(r"<w:(ins|del|moveFrom|moveTo|rPrChange|pPrChange|sectPrChange|tblPrChange)[ >/]", xml)))
            if achou:
                achados.append(f"{nome}: " + ", ".join("w:" + a for a in achou))
        resultados.append(_ok("Alterações controladas", achados))

        # 5. propriedades, docVars, customXml, imagens e PNG
        achados = []
        for nome in ("docProps/core.xml", "docProps/app.xml", "docProps/custom.xml"):
            for m in TERMOS_DE_IA.finditer(xmls.get(nome, "")):
                achados.append(f"{nome}: «{m.group(0)}»")
            if any(c in html.unescape(xmls.get(nome, "")) for c in CADEIAS_DA_TAG):
                achados.append(f"{nome}: tag")
        resultados.append(_ok("Propriedades do arquivo (core, app, custom)", achados))

        achados = []
        for nome, xml in xmls.items():
            for m in re.finditer(r"<w:docVar\b[^>]*>", xml):
                if TERMOS_DE_IA.search(m.group(0)):
                    achados.append(f"{nome}: {m.group(0)[:80]}")
        resultados.append(_ok("Variáveis do documento (docVars)", achados))

        achados = []
        for nome in nomes:
            if nome.startswith("customXml/") and TERMOS_DE_IA.search(_texto(z.read(nome))):
                achados.append(nome)
        resultados.append(_ok("customXml", achados))

        achados = []
        for nome, xml in partes_word.items():
            for m in re.finditer(r"<(?:wp:docPr|pic:cNvPr)\b[^>]*>", xml):
                if TERMOS_DE_IA.search(html.unescape(m.group(0))):
                    achados.append(f"{nome}: {m.group(0)[:100]}")
        for nome in nomes:
            if nome.startswith("word/media/") and TERMOS_DE_IA.search(nome):
                achados.append(f"nome do arquivo {nome}")
        resultados.append(_ok("Imagens: nome e texto alternativo", achados))

        achados = []
        for nome, dados in binarios.items():
            if nome.lower().endswith(".png"):
                for bloco in _png_blocos_de_texto(dados):
                    if TERMOS_DE_IA.search(bloco) or any(c in bloco for c in CADEIAS_DA_TAG):
                        achados.append(f"{nome}: {bloco[:60]}")
            elif TERMOS_DE_IA.search(_texto(dados)):
                achados.append(f"{nome}: texto de IA nos bytes")
        resultados.append(_ok("PNG e outras imagens: blocos de texto", achados))

        # relações externas que citem IA
        achados = []
        for nome, xml in xmls.items():
            if nome.endswith(".rels"):
                for m in re.finditer(r"<Relationship\b[^>]*TargetMode=\"External\"[^>]*>", xml):
                    if TERMOS_DE_IA.search(m.group(0)):
                        achados.append(f"{nome}: {m.group(0)[:100]}")
        resultados.append(_ok("Ligações externas", achados))

        # 6. modelo anexado com caminho de usuário: só avisa
        achados = []
        settings = xmls.get("word/settings.xml", "")
        if "<w:attachedTemplate" in settings:
            rels = xmls.get("word/_rels/settings.xml.rels", "")
            for alvo in re.findall(r'Target="([^"]*)"', rels):
                if re.search(r"(?i)[\\/]users[\\/]|%USERPROFILE%|C:\\Users", html.unescape(alvo)):
                    achados.append(f"attachedTemplate aponta para {alvo}")
        resultados.append(_ok("Template anexado com caminho de usuário (attachedTemplate)", achados, aviso=True))
    return resultados, info


# --------------------------------------------------------------------------------------------------------------- PDF
def _importar_pymupdf():
    try:
        import pymupdf  # type: ignore
        return pymupdf
    except ImportError:
        try:
            import fitz  # type: ignore
            return fitz
        except ImportError:
            return None


def _decodificar_literal(bruto: bytes) -> str:
    if bruto.startswith(b"\xfe\xff"):
        return bruto[2:].decode("utf-16-be", errors="replace")
    return bruto.decode("latin-1", errors="replace")


def _metadados_brutos(dados: bytes) -> dict[str, str]:
    saida: dict[str, str] = {}
    for m in re.finditer(rb"/(Author|Creator|Producer|Title|Subject|Keywords)\s*(?:\(((?:\\.|[^\\)])*)\)|<([0-9A-Fa-f\s]+)>)", dados):
        chave = m.group(1).decode()
        if m.group(2) is not None:
            valor = _decodificar_literal(m.group(2))
        else:
            valor = _decodificar_literal(bytes.fromhex(re.sub(rb"\s", b"", m.group(3)).decode()))
        saida.setdefault(chave, valor)
    return saida


def _conferir_cadeias_e_metadados(meta: dict[str, str], xmp: str) -> Resultado:
    achados = []
    for chave, valor in meta.items():
        if valor and TERMOS_DE_IA.search(valor):
            achados.append(f"{chave}: «{valor[:60]}»")
    for m in TERMOS_DE_IA.finditer(xmp):
        achados.append(f"XMP: «{m.group(0)}»")
    return _ok("Metadados do PDF (Info e XMP)", achados)


def conferir_pdf(caminho: Path, usar_fitz: bool = True) -> tuple[list[Resultado], dict[str, str]]:
    resultados: list[Resultado] = []
    info: dict[str, str] = {}
    mu = _importar_pymupdf() if usar_fitz else None
    if mu is None:
        dados = caminho.read_bytes()
        meta = _metadados_brutos(dados)
        for k, v in meta.items():
            info[f"PDF {k}"] = v
        xmp = ""
        m = re.search(rb"<x:xmpmeta.*?</x:xmpmeta>", dados, re.DOTALL)
        if m:
            xmp = m.group(0).decode("utf-8", errors="replace")
        resultados.append(_conferir_cadeias_e_metadados(meta, xmp))
        achados = [t.decode() for t in re.findall(rb"/Subtype\s*/(" + "|".join(TIPOS_DE_ANOTACAO).encode() + rb")\b", dados)]
        resultados.append(_ok("Anotações e comentários", [f"/Subtype /{a}" for a in sorted(set(achados))]))
        resultados.append(_ok("Arquivos embutidos", ["/EmbeddedFile"] if b"/EmbeddedFile" in dados else []))
        resultados.append(_ok("Camadas opcionais (OCG)", ["/OCProperties presente (sem PyMuPDF não dá para ver se há camada oculta)"]
                              if b"/OCProperties" in dados else [], aviso=True))
        achados = []
        for cadeia in CADEIAS_DA_TAG:
            if cadeia.encode() in dados:
                achados.append(f"«{cadeia}» nos bytes do PDF")
        resultados.append(_ok("Tag de IA no PDF (busca bruta)", achados))
        resultados.append(("PyMuPDF não instalado", "AVISO",
                           "não conferido: texto das páginas (fluxos comprimidos), texto invisível, anotações dentro de fluxos "
                           "comprimidos, camadas ocultas e metadados em objetos comprimidos"))
        return resultados, info

    doc = mu.open(str(caminho))
    try:
        meta = {k: str(v or "") for k, v in doc.metadata.items() if k in ("author", "creator", "producer", "title", "subject", "keywords")}
        for k, v in meta.items():
            info[f"PDF {k}"] = v
        resultados.append(_conferir_cadeias_e_metadados(meta, doc.get_xml_metadata() or ""))
        achados, tags, invisiveis = [], [], []
        for n, pagina in enumerate(doc, 1):
            for anot in pagina.annots() or []:
                achados.append(f"página {n}: {anot.type[1]}")
            texto = pagina.get_text()
            for cadeia in CADEIAS_DA_TAG:
                if cadeia in texto:
                    tags.append(f"página {n}: «{cadeia}»")
            try:
                for span in pagina.get_texttrace():
                    if span.get("type") == 3 or span.get("opacity", 1) == 0:
                        if "".join(chr(ch[0]) for ch in span.get("chars", [])).strip():
                            invisiveis.append(f"página {n}")
                            break
            except Exception:   # noqa: BLE001 - versão sem get_texttrace
                pass
        resultados.append(_ok("Anotações e comentários", achados))
        resultados.append(_ok("Arquivos embutidos", [str(nome) for nome in (doc.embfile_names() if doc.embfile_count() else [])]))
        try:
            ocultas = [str(v.get("name")) for v in doc.get_ocgs().values() if not v.get("on", True)]
        except Exception:   # noqa: BLE001
            ocultas = []
        resultados.append(_ok("Camadas opcionais (OCG) ocultas", ocultas))
        resultados.append(_ok("Texto invisível", invisiveis))
        resultados.append(_ok("Tag de IA no texto das páginas", tags))
        info["PDF páginas"] = str(len(doc))
    finally:
        doc.close()
    return resultados, info


# ---------------------------------------------------------------------------------------------------- linha de comando
def imprimir(titulo: str, resultados: list[Resultado], info: dict[str, str]) -> None:
    print(f"== {titulo}")
    for nome, estado, onde in resultados:
        print(f"{estado:<5} {nome}" + (f": {onde}" if onde else ""))
    for chave, valor in info.items():
        print(f"      {chave}: {valor or '(vazio)'}")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", type=Path)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--json", type=Path, default=None, help="grava o resultado em JSON")
    args = ap.parse_args(argv)
    res_docx, info_docx = conferir_docx(args.docx)
    res_pdf, info_pdf = conferir_pdf(args.pdf)
    imprimir(f"Word: {args.docx.name}", res_docx, info_docx)
    imprimir(f"PDF: {args.pdf.name}", res_pdf, info_pdf)
    falhas = [r for r in res_docx + res_pdf if r[1] == "FALHA"]
    avisos = [r for r in res_docx + res_pdf if r[1] == "AVISO"]
    print(f"\nResultado: {'LIMPO' if not falhas else 'ACHOU MARCAÇÃO'} ({len(falhas)} falha(s), {len(avisos)} aviso(s))")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({
            "limpo": not falhas,
            "docx": {"arquivo": str(args.docx), "conferencias": [list(r) for r in res_docx], "propriedades": info_docx},
            "pdf": {"arquivo": str(args.pdf), "conferencias": [list(r) for r in res_pdf], "propriedades": info_pdf},
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
