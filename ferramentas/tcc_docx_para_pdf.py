#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (25/11/2026, decisão 158) que abre o .docx do TCC no Word (por COM, sem janela), atualiza todos os campos (sumário, lista de tabelas, lista de figuras, SEQ das legendas e o NUMPAGES do "N f." da ficha catalográfica), salva o .docx já com tudo paginado e exporta o PDF ao lado.
# ! Motivo: o `gerar_tcc_docx.py` escreve os campos com o texto de antes e deixa o Word atualizar ao abrir (aviso "atualizar campos?"); a entrega é em Word e em PDF, então o arquivo entregue já precisa abrir com o sumário e a ficha certos e sem esse aviso. O Word do Windows não roda dentro do aplicativo Claude (pacote MSIX), por isso o trabalho é feito numa pasta temporária dentro de Documentos (`_tcc_tmp_pdf`), apagada no fim, e o resultado é copiado para o destino. Ao salvar, o Word troca "último a salvar" pelo nome de usuário do Windows; o script devolve autor, último a salvar e título que o gerador gravou.
"""Converte o .docx do TCC em PDF pelo Word (COM) e deixa o .docx com os campos atualizados.

Uso:
    python ferramentas/tcc_docx_para_pdf.py entrada.docx [--saida-docx saida.docx] [--pdf saida.pdf]
Sem --saida-docx, o .docx é atualizado no próprio lugar; sem --pdf, o PDF fica ao lado com o mesmo nome.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

PASTA_TEMPORARIA = Path.home() / "Documents" / "_tcc_tmp_pdf"

# Só ASCII e "-": o Windows PowerShell 5.1 lê .ps1 sem BOM na codepage ANSI (regra do projeto); mesmo assim vai com BOM.
SCRIPT_PS1 = r"""
param([string]$Entrada, [string]$Pdf)
$ErrorActionPreference = 'Stop'
$word = $null
$doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($Entrada, $false, $false, $false)
    for ($i = 0; $i -lt 3; $i++) {
        $doc.Repaginate()
        [void]$doc.Fields.Update()
        foreach ($t in $doc.TablesOfContents) { $t.Update() }
        foreach ($t in $doc.TablesOfFigures) { $t.Update() }
        foreach ($s in $doc.Sections) {
            foreach ($h in $s.Headers) { [void]$h.Range.Fields.Update() }
        }
    }
    $doc.Repaginate()
    $paginas = $doc.ComputeStatistics(2)
    $doc.Save()
    $doc.ExportAsFixedFormat($Pdf, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    Write-Output ("PAGINAS=" + $paginas)
}
finally {
    if ($doc -ne $null) { try { $doc.Close(0) } catch { } }
    if ($word -ne $null) { try { $word.Quit() } catch { } }
}
"""


def _parte(z: zipfile.ZipFile, nome: str) -> str:
    return z.read(nome).decode("utf-8")


def _valor(xml: str, tag: str) -> str | None:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", xml, re.DOTALL)
    return m.group(1) if m else None


def devolver_propriedades(original: Path, salvo: Path) -> None:
    """Depois do Word salvar: volta autor, último a salvar e título do original e zera Company/Manager do app.xml."""
    with zipfile.ZipFile(original) as z:
        core_antes = _parte(z, "docProps/core.xml")
    with zipfile.ZipFile(salvo) as z:
        itens = {n: z.read(n) for n in z.namelist()}
    core = itens["docProps/core.xml"].decode("utf-8")
    for tag in ("dc:creator", "cp:lastModifiedBy", "dc:title"):
        valor = _valor(core_antes, tag)
        if valor is None:
            continue
        if re.search(rf"<{tag}>.*?</{tag}>|<{tag}/>", core, re.DOTALL):
            core = re.sub(rf"<{tag}>.*?</{tag}>|<{tag}/>", lambda _m: f"<{tag}>{valor}</{tag}>", core, count=1, flags=re.DOTALL)
        else:
            core = core.replace("</cp:coreProperties>", f"<{tag}>{valor}</{tag}></cp:coreProperties>")
    itens["docProps/core.xml"] = core.encode("utf-8")
    app = itens["docProps/app.xml"].decode("utf-8")
    app = re.sub(r"<(Company|Manager)>.*?</\1>", r"<\1/>", app, flags=re.DOTALL)
    # o Word recoloca <Template>Normal.dotm</Template> ao salvar; sai de novo para o app.xml não carregar o nome do modelo
    app = re.sub(r"<Template>.*?</Template>", "", app, flags=re.DOTALL)
    itens["docProps/app.xml"] = app.encode("utf-8")
    temp = salvo.with_suffix(".tmp")
    with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, dados in itens.items():
            z.writestr(nome, dados)
    temp.replace(salvo)


def converter(entrada: Path, saida_docx: Path, pdf: Path) -> int:
    """Devolve o número de páginas do arquivo. Levanta RuntimeError se o Word não responder."""
    PASTA_TEMPORARIA.mkdir(parents=True, exist_ok=True)
    try:
        copia = PASTA_TEMPORARIA / "tcc.docx"
        pdf_tmp = PASTA_TEMPORARIA / "tcc.pdf"
        script = PASTA_TEMPORARIA / "converter.ps1"
        shutil.copyfile(entrada, copia)
        script.write_bytes(b"\xef\xbb\xbf" + SCRIPT_PS1.encode("utf-8"))
        try:
            r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                                "-Entrada", str(copia), "-Pdf", str(pdf_tmp)],
                               capture_output=True, text=True, timeout=600)
        except subprocess.TimeoutExpired as erro:
            subprocess.run(["taskkill", "/F", "/IM", "WINWORD.EXE"], capture_output=True)
            raise RuntimeError("o Word não respondeu em 10 minutos") from erro
        paginas = re.search(r"PAGINAS=(\d+)", r.stdout)
        if r.returncode != 0 or not paginas or not pdf_tmp.is_file():
            raise RuntimeError(f"o Word (COM) falhou: {(r.stderr or r.stdout).strip()[:600]}")
        devolver_propriedades(entrada, copia)
        saida_docx.parent.mkdir(parents=True, exist_ok=True)
        pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(copia, saida_docx)
        shutil.copyfile(pdf_tmp, pdf)
        return int(paginas.group(1))
    finally:
        shutil.rmtree(PASTA_TEMPORARIA, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", type=Path)
    ap.add_argument("--saida-docx", type=Path, default=None)
    ap.add_argument("--pdf", type=Path, default=None)
    args = ap.parse_args(argv)
    entrada = args.entrada.resolve()
    saida_docx = (args.saida_docx or entrada).resolve()
    pdf = (args.pdf or entrada.with_suffix(".pdf")).resolve()
    try:
        paginas = converter(entrada, saida_docx, pdf)
    except RuntimeError as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    print(f"Word: {paginas} páginas; folhas da ficha (páginas menos a capa e a ficha): {paginas - 2}")
    print(f"Docx: {saida_docx}")
    print(f"PDF:  {pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
