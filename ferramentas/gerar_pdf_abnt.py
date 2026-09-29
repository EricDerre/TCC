#!/usr/bin/env python3
# ! Alteração de IA - Revisar: gera o PDF do projeto de pesquisa (versão beta) a partir do Markdown
# (29/09/2026; ficha 11g e item 11 da revisão do ABNT, pré-aprovados pelo Eric como "pré-release"):
# tira as marcações de IA (comentários HTML) de uma CÓPIA em memória, converte o Markdown do Google
# Docs (títulos em negrito, tabelas, listas em citação, quebras com dois espaços) em HTML com folha
# de estilo no padrão ABNT (A4, margens 3/2 cm, Times 12, entrelinha 1,5, títulos em caixa-alta) e
# imprime em PDF pelo Microsoft Edge em modo sem janela (msedge --headless --print-to-pdf). O .md
# continua com as marcações.
# ! Motivo: a pendência antiga dizia "regerar o PDF e retirar as 20 marcações antes da entrega"; o
# Eric pediu a versão beta agora, mantendo as marcações no fonte. A máquina não tem pandoc, wkhtmltopdf
# nem Playwright no Python do sistema — o Edge está em toda máquina Windows 11 e imprime HTML em PDF
# sem instalar nada.
"""Uso: python ferramentas/gerar_pdf_abnt.py [--entrada "Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V3.md"]
                                          [--saida "Documentacao/Projeto de Pesquisa - ABNT 15287_2025 - V4-beta.pdf"]"""
from __future__ import annotations

import argparse
import html
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "Documentacao" / "Projeto de Pesquisa - ABNT 15287_2025 - V3.md"
SAIDA = RAIZ / "Documentacao" / "Projeto de Pesquisa - ABNT 15287_2025 - V4-beta.pdf"
EDGE = [Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")]

CSS = """
@page { size: A4; margin: 3cm 2cm 2cm 3cm; }
body { font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 1.5; color: #000; text-align: justify; }
h1 { font-size: 12pt; font-weight: bold; text-transform: uppercase; margin: 0 0 12pt; page-break-before: always; }
h2 { font-size: 12pt; font-weight: bold; margin: 18pt 0 6pt; }
p { margin: 0 0 6pt; text-indent: 1.25cm; }
p.sem-recuo, .capa p, .refs p, .glossario p, blockquote p { text-indent: 0; }
.capa { text-align: center; }
.capa p { margin: 0; }
.capa .titulo { font-weight: bold; margin-top: 60pt; margin-bottom: 60pt; }
.capa .autores { margin-top: 48pt; margin-bottom: 48pt; }
.capa .local { margin-top: 72pt; }
.natureza { margin-left: 8cm; text-align: justify; font-size: 11pt; line-height: 1.2; margin-top: 24pt; margin-bottom: 48pt; }
.quebra { page-break-after: always; }
blockquote { margin: 6pt 0 6pt 1.25cm; }
ul { margin: 0 0 6pt 1.25cm; padding: 0; }
li { margin: 0 0 3pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 12pt; font-size: 11pt; line-height: 1.2; }
th, td { border: 1px solid #000; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { font-weight: bold; }
.refs p { text-align: left; line-height: 1.0; margin: 0 0 12pt; }
.glossario p { margin: 0 0 6pt; }
.sumario p { margin: 0; }
"""


def inline(s: str) -> str:
    s = s.replace("\\-", "-").replace("\\[", "[").replace("\\]", "]").replace("\\.", ".").replace("\\*", "*")
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def sem_marcacoes(md: str) -> str:
    return re.sub(r"<!--.*?-->", "", md, flags=re.S)


def _tabela(linhas: list[str]) -> str:
    def cel(l: str) -> list[str]:
        s = l.strip()
        return [c.strip() for c in s[1:-1].split("|")] if s.startswith("|") and s.endswith("|") else [c.strip() for c in s.split("|")]
    cab = cel(linhas[0])
    corpo = [cel(l) for l in linhas[2:]]
    if len(cab) == 2 and not cab[0] and not corpo:
        return f'<div class="natureza">{inline(cab[1])}</div>'
    th = "".join(f"<th>{inline(c)}</th>" for c in cab)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in corpo)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"


def converter(md: str) -> str:
    linhas = sem_marcacoes(md).split("\n")
    saida: list[str] = []
    i = 0
    capa = True
    secao = ""
    par: list[str] = []
    n_2026 = 0

    def fecha_par() -> None:
        nonlocal par
        if par:
            texto = "<br>".join(inline(p) for p in par)
            classe = ""
            if capa:
                if any("**" in p for p in par) and "TCC" not in texto:
                    classe = ' class="titulo"' if "DESENVOLVIMENTO" in texto else ""
                if par[0].isupper() and len(par) > 1:
                    classe = ' class="autores"'
            saida.append(f"<p{classe}>{texto}</p>")
            par = []

    while i < len(linhas):
        l = linhas[i]
        s = l.rstrip()
        if not s.strip():
            fecha_par()
            i += 1
            continue
        m = re.match(r"^(#{1,2}) \*\*(.+?)\*\*\s*$", s) or re.match(r"^(#{1,2}) (.+)$", s)
        if m:
            fecha_par()
            if capa:
                saida.append("</div>")
                capa = False
            nivel = len(m.group(1))
            titulo = m.group(2).strip()
            if nivel == 1:
                secao = titulo.lower()
                if "refer" in secao:
                    saida.append('</div><div class="refs">' if False else "")
            saida.append(f"<h{nivel}>{inline(titulo)}</h{nivel}>")
            i += 1
            continue
        if s.lstrip().startswith("|"):
            fecha_par()
            tab = []
            while i < len(linhas) and linhas[i].lstrip().startswith("|"):
                tab.append(linhas[i])
                i += 1
            saida.append(_tabela(tab))
            continue
        if s.startswith("> "):
            fecha_par()
            itens, textos = [], []
            while i < len(linhas) and linhas[i].startswith(">"):
                t = linhas[i][1:].strip()
                if t.startswith("* "):
                    itens.append(f"<li>{inline(t[2:])}</li>")
                elif t:
                    textos.append(inline(t))
                i += 1
            saida.append("<blockquote>" + ("".join(f"<p>{t}</p>" for t in textos)) + (f"<ul>{''.join(itens)}</ul>" if itens else "") + "</blockquote>")
            continue
        if s.startswith("* ") or s.startswith("- "):
            fecha_par()
            itens = []
            while i < len(linhas) and (linhas[i].startswith("* ") or linhas[i].startswith("- ")):
                itens.append(f"<li>{inline(linhas[i][2:])}</li>")
                i += 1
            saida.append(f"<ul>{''.join(itens)}</ul>")
            continue
        # linha de texto: termina com dois espaços = quebra dentro do parágrafo
        par.append(s.strip())
        if capa and s.strip() in ("2026",):
            n_2026 += 1
            fecha_par()
            saida.append('<div class="quebra"></div>')
        elif not l.endswith("  "):
            fecha_par()
        i += 1
    fecha_par()
    corpo = "\n".join(saida)
    # classes de seção: referências (sem recuo, entrelinha simples) e glossário
    corpo = re.sub(r"(<h1>REFER[^<]*</h1>)", r'\1<div class="refs">', corpo, count=1)
    corpo = re.sub(r"(<h1>GLOSS[^<]*</h1>)", r'</div>\1<div class="glossario">', corpo, count=1)
    corpo = re.sub(r"(<h1>SUM[^<]*</h1>)", r'\1<div class="sumario">', corpo, count=1)
    corpo = re.sub(r"(<h1>1 INTRO[^<]*</h1>)", r'</div>\1', corpo, count=1)
    corpo += "</div>"
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Projeto de Pesquisa</title><style>{CSS}</style></head><body><div class="capa">{corpo}</body></html>'


def edge() -> Path:
    for p in EDGE:
        if p.exists():
            return p
    raise SystemExit("Microsoft Edge não encontrado (msedge.exe)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrada", default=str(ENTRADA))
    ap.add_argument("--saida", default=str(SAIDA))
    ap.add_argument("--manter-html", action="store_true", help="deixa o HTML intermediário ao lado do PDF")
    args = ap.parse_args()
    entrada, saida = Path(args.entrada), Path(args.saida)
    md = entrada.read_text(encoding="utf-8")
    n_marc = len(re.findall(r"<!--", md))
    pagina = converter(md)
    html_tmp = saida.with_suffix(".html") if args.manter_html else Path(tempfile.gettempdir()) / (saida.stem + ".html")
    html_tmp.write_text(pagina, encoding="utf-8")
    if saida.exists():
        saida.unlink()
    cmd = [str(edge()), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run", "--disable-extensions",
           f"--print-to-pdf={saida}", html_tmp.resolve().as_uri()]
    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    for _ in range(40):
        if saida.exists() and saida.stat().st_size > 0:
            break
        time.sleep(0.5)
    if not saida.exists():
        raise SystemExit("o Edge não gravou o PDF")
    if not args.manter_html:
        try:
            os.remove(html_tmp)
        except OSError:
            pass
    print(f"PDF gravado: {saida} ({saida.stat().st_size:,} bytes; {n_marc} marcações de IA retiradas da cópia)")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
