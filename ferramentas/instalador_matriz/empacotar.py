#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único): monta o pacote que entra em cada célula de teste,
# um zip e um tar.gz com o que quem baixa o repositório do GitHub recebe.
# ! Motivo: a máquina limpa não tem git, e o working tree tem alterações que o Eric ainda não commitou. Copiar a pasta direto
# levaria o `.git`, as venvs e o fim de linha do Windows (o `install.sh` está com CRLF no working tree e com LF no git), e a
# célula testaria um arquivo que ninguém recebe. O pacote reproduz o conteúdo, o fim de linha e o modo que o git entrega.
"""Uso: python ferramentas/instalador_matriz/empacotar.py [--saida <pasta>]
Grava cobaia-pacote.zip e cobaia-pacote.tar.gz na pasta (padrão: .ferramentas/pacote na raiz) e imprime o SHA-256 de cada um."""
import argparse
import gzip
import hashlib
import io
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
# Arquivos novos do instalador que ainda não passaram por `git add` e precisam entrar no pacote.
EXTRAS = ("instalador", "versoes.json", "ferramentas/instalador_matriz", ".gitattributes")
DATA_FIXA = (1980, 1, 1, 0, 0, 0)


def _git(raiz: Path, *argumentos: str) -> list[str]:
    # o -z vem logo depois do subcomando: depois de um `--` ele seria lido como nome de arquivo
    saida = subprocess.run(["git", "-C", str(raiz), "-c", "core.quotepath=off", argumentos[0], "-z", *argumentos[1:]],
                           check=True, capture_output=True).stdout
    return [pedaco.decode("utf-8") for pedaco in saida.split(b"\0") if pedaco]


def listar(raiz: Path) -> list[dict]:
    """Os arquivos rastreados que existem no working tree, mais os novos dentro de EXTRAS que o .gitignore não exclui."""
    itens = {}
    for linha in _git(raiz, "ls-files", "--stage"):
        meta, caminho = linha.split("\t", 1)
        itens[caminho] = {"caminho": caminho, "modo": int(meta.split()[0][-3:], 8), "eol_indice": "", "eol_trabalho": ""}
    for linha in _git(raiz, "ls-files", "--eol"):
        meta, caminho = linha.split("\t", 1)
        partes = meta.split()
        itens[caminho]["eol_indice"] = partes[0].removeprefix("i/")
        itens[caminho]["eol_trabalho"] = partes[1].removeprefix("w/")
    for caminho in _git(raiz, "ls-files", "--others", "--exclude-standard", "--", *EXTRAS):
        itens[caminho] = {"caminho": caminho, "modo": 0o644, "eol_indice": "novo", "eol_trabalho": ""}
    return [item for caminho, item in sorted(itens.items()) if (raiz / caminho).is_file()]


def conteudo(raiz: Path, item: dict) -> bytes:
    """Os bytes do arquivo como o git os gravaria: texto com CRLF no working tree e LF (ou nada ainda) no índice sai com LF."""
    bruto = (raiz / item["caminho"]).read_bytes()
    if item["eol_indice"] == "novo":
        texto = b"\0" not in bruto[:8000]          # a mesma pista que o git usa para dizer que é texto
    else:
        texto = item["eol_trabalho"] in ("crlf", "mixed") and item["eol_indice"] in ("lf", "none")
    return bruto.replace(b"\r\n", b"\n") if texto else bruto


def montar(raiz: Path, destino: Path, prefixo: str = "TCC-main") -> dict:
    """Grava <destino>.zip e <destino>.tar.gz, com data fixa e ordem fixa, e devolve a contagem e o SHA-256 de cada um."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    itens = listar(raiz)
    em_memoria_tar = io.BytesIO()
    with zipfile.ZipFile(str(destino) + ".zip", "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z, \
            tarfile.open(fileobj=em_memoria_tar, mode="w", format=tarfile.PAX_FORMAT) as t:
        for item in itens:
            dados = conteudo(raiz, item)
            nome = f"{prefixo}/{item['caminho']}"
            info = zipfile.ZipInfo(nome, date_time=DATA_FIXA)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3                                  # Unix: o unzip do Linux respeita o modo
            info.external_attr = (0o100000 | item["modo"]) << 16
            z.writestr(info, dados, compresslevel=6)
            membro = tarfile.TarInfo(nome)
            membro.size, membro.mode, membro.mtime = len(dados), item["modo"], 0
            membro.uid = membro.gid = 0
            membro.uname = membro.gname = ""
            t.addfile(membro, io.BytesIO(dados))
    with open(str(destino) + ".tar.gz", "wb") as saida, gzip.GzipFile(filename="", fileobj=saida, mode="wb", mtime=0) as g:
        g.write(em_memoria_tar.getvalue())
    return {"arquivos": len(itens),
            "zip_sha256": hashlib.sha256(Path(str(destino) + ".zip").read_bytes()).hexdigest(),
            "tar_sha256": hashlib.sha256(Path(str(destino) + ".tar.gz").read_bytes()).hexdigest()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saida", type=Path, default=RAIZ / ".ferramentas" / "pacote")
    args = ap.parse_args()
    resumo = montar(RAIZ, args.saida / "cobaia-pacote")
    print(f"{resumo['arquivos']} arquivos em {args.saida}")
    print(f"cobaia-pacote.zip     sha256 {resumo['zip_sha256']}")
    print(f"cobaia-pacote.tar.gz  sha256 {resumo['tar_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
