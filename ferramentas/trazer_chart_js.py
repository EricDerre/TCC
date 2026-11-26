#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/11/2026, ficha 116, decisão 178): traz para o repositório a biblioteca de gráficos que o painel do
# projeto usa, a Chart.js 4.4.1. Baixa um arquivo só, `chart.umd.js`, de `cdn.jsdelivr.net`, confere o que baixou contra o código de integridade
# que o próprio jsDelivr publica para esse arquivo do pacote do npm e, quando o cdnjs também publica o dele, contra esse segundo código; só então
# grava o arquivo em `ferramentas/terceiros/` e a ficha dele em `terceiros.json` (origem, versão, licença, tamanho, códigos de integridade e a
# decisão que autorizou). `--conferir` não usa a rede: refaz o código do arquivo em disco e compara com a ficha.
# ! Motivo: o painel pedia a biblioteca à internet toda vez que abria; sem conexão os gráficos não eram desenhados (antes da proteção de
# 26/11/2026, o painel inteiro parava). O Eric decidiu trazer a biblioteca para o repositório e autorizou o download deste arquivo, desta versão
# e desta origem, e só dele. O arquivo entra como veio, sem nenhuma alteração: é por isso que ele não leva a tag de IA dentro (a tag mudaria o
# arquivo e o código de integridade deixaria de bater) e fica coberto pela ficha em `terceiros.json`. Se o código publicado não bater com o que
# foi baixado, nada é gravado.
"""Traz a Chart.js 4.4.1 para ferramentas/terceiros/ (ficha 116). Uso, na raiz do repositório:
  python ferramentas/trazer_chart_js.py              # baixa, confere a integridade e grava o arquivo e a ficha dele
  python ferramentas/trazer_chart_js.py --conferir   # sem rede: confere o arquivo em disco contra a ficha
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "ferramentas" / "terceiros"
NOME = "chart.umd.js"
VERSAO = "4.4.1"
ORIGEM = f"https://cdn.jsdelivr.net/npm/chart.js@{VERSAO}/dist/{NOME}"
FICHA_NO_JSDELIVR = f"https://data.jsdelivr.com/v1/packages/npm/chart.js@{VERSAO}?structure=flat"
FICHA_NO_CDNJS = f"https://api.cdnjs.com/libraries/Chart.js/{VERSAO}?fields=sri"
LICENCA = "MIT"
TAMANHO_MAXIMO = 2_000_000
AGENTE = "trazer-chart-js/1 (python-urllib)"


def _pedir(url: str) -> bytes:
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pedido, timeout=60) as resposta:  # o endereço é uma das três constantes acima, sempre https
        dados = resposta.read(TAMANHO_MAXIMO + 1)
    if len(dados) > TAMANHO_MAXIMO:
        raise ValueError(f"{url}: passa de {TAMANHO_MAXIMO} bytes")
    return dados


def codigos(dados: bytes) -> dict:
    """Os códigos de integridade de um conteúdo: o SHA-256 em hexadecimal e em base64, e os SRI SHA-384 e SHA-512."""
    em_base64 = lambda nome: base64.b64encode(hashlib.new(nome, dados).digest()).decode("ascii")
    return {"sha256": hashlib.sha256(dados).hexdigest(), "sha256_base64": em_base64("sha256"), "sri_sha384": "sha384-" + em_base64("sha384"),
            "sri_sha512": "sha512-" + em_base64("sha512")}


def publicado_no_jsdelivr() -> dict:
    """O que o jsDelivr publica para `/dist/chart.umd.js` do pacote do npm: o SHA-256 em base64 e o tamanho."""
    ficha = json.loads(_pedir(FICHA_NO_JSDELIVR).decode("utf-8"))
    for arquivo in ficha.get("files") or []:
        if arquivo.get("name") == f"/dist/{NOME}":
            return {"sha256_base64": arquivo.get("hash"), "bytes": arquivo.get("size")}
    raise ValueError(f"o jsDelivr não lista /dist/{NOME} no pacote chart.js@{VERSAO}")


def publicado_no_cdnjs() -> str | None:
    """O SRI que o cdnjs publica para o mesmo arquivo, ou None quando ele não o lista ou não responde (é a segunda conferência, não a que decide)."""
    try:
        sri = json.loads(_pedir(FICHA_NO_CDNJS).decode("utf-8")).get("sri") or {}
    except (OSError, ValueError):
        return None
    return sri.get(NOME)


def trazer(pasta: Path = PASTA) -> dict:
    dados = _pedir(ORIGEM)
    meus = codigos(dados)
    inicio = dados[:400].decode("utf-8", errors="replace")
    if f"Chart.js v{VERSAO}" not in inicio or "MIT License" not in inicio:
        raise ValueError("o arquivo baixado não traz o aviso de versão e de licença da Chart.js 4.4.1 no começo")
    if b"<!--" in dados:
        raise ValueError("o arquivo baixado tem `<!--`, que não pode ir para dentro de um bloco de script do painel")
    jsdelivr = publicado_no_jsdelivr()
    if jsdelivr["sha256_base64"] != meus["sha256_base64"] or jsdelivr["bytes"] != len(dados):
        raise ValueError(f"o que foi baixado não bate com o que o jsDelivr publica: {meus['sha256_base64']} e {len(dados)} bytes aqui, "
                         f"{jsdelivr['sha256_base64']} e {jsdelivr['bytes']} bytes lá")
    cdnjs = publicado_no_cdnjs()
    if cdnjs is not None and cdnjs != meus["sri_sha512"]:
        raise ValueError(f"o que foi baixado não bate com o código que o cdnjs publica para {NOME}: {meus['sri_sha512']} aqui, {cdnjs} lá")
    ficha = {"biblioteca": "Chart.js", "versao": VERSAO, "licenca": LICENCA, "origem": ORIGEM, "bytes": len(dados), "baixado_em": dt.date.today().isoformat(),
             "sha256": meus["sha256"], "sri_sha384": meus["sri_sha384"], "sri_sha512": meus["sri_sha512"],
             "conferido_contra": {"jsdelivr": {"onde": FICHA_NO_JSDELIVR, "sha256_base64": jsdelivr["sha256_base64"], "bytes": jsdelivr["bytes"], "bate": True},
                                  "cdnjs": {"onde": FICHA_NO_CDNJS, "sri_sha512": cdnjs, "bate": True if cdnjs is not None else None}},
             "autorizado_por": "ficha 116 (decisão 178): só este arquivo, desta versão e desta origem",
             "usado_por": "ferramentas/gerar_dashboard.py, que o embute no HTML do painel",
             "aviso_de_licenca": inicio.split("*/")[0].strip() + " */"}
    registro = {"tag_ia": {"alteracao": "! Alteração de IA - Revisar: arquivo novo (26/11/2026, ficha 116, decisão 178), gravado por ferramentas/trazer_chart_js.py: a ficha de cada "
                                         "arquivo de terceiros guardado nesta pasta (origem, versão, licença, tamanho e códigos de integridade).",
                           "motivo": "! Motivo: o arquivo de terceiros entra no repositório como foi baixado, sem a tag de IA dentro, porque a tag mudaria o arquivo e o código de "
                                     "integridade deixaria de bater; esta ficha é o que diz de onde ele veio, quem autorizou e como conferir. O gerador do painel só embute o arquivo "
                                     "cujo SHA-256 bate com o daqui."},
                "arquivos": {NOME: ficha}}
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / NOME).write_bytes(dados)
    (pasta / "terceiros.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return ficha


def conferir(pasta: Path = PASTA) -> bool:
    """Sem rede: o arquivo em disco bate com o SHA-256 e o tamanho da ficha?"""
    try:
        ficha = json.loads((pasta / "terceiros.json").read_text(encoding="utf-8"))["arquivos"][NOME]
        dados = (pasta / NOME).read_bytes()
    except (OSError, ValueError, KeyError):
        return False
    return hashlib.sha256(dados).hexdigest() == ficha.get("sha256") and len(dados) == ficha.get("bytes")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--conferir", action="store_true", help="sem rede: confere o arquivo em disco contra a ficha em terceiros.json")
    args = ap.parse_args(argv)
    if args.conferir:
        ok = conferir()
        print(f"--conferir: {NOME} {'bate com' if ok else 'NÃO bate com'} a ficha em {PASTA / 'terceiros.json'}")
        return 0 if ok else 1
    ficha = trazer()
    print(f"gravado: {PASTA / NOME} ({ficha['bytes']} bytes, SHA-256 {ficha['sha256']}); conferido contra o jsDelivr"
          + (" e contra o cdnjs" if ficha["conferido_contra"]["cdnjs"]["bate"] else "; o cdnjs não publicou código para este arquivo"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
