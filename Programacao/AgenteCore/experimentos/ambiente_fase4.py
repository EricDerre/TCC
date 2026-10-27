#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P0): grava em `resultados_alvo/fase4/ambiente.json`
# as versões do Python, do Playwright, do navegador e do Ollama (as quatro que o P0 do plano aprovado exige), mais o
# canal do navegador, a máquina e o que foi encontrado das cobaias (PHP, MariaDB, uvicorn da CobaiaAPI, Edge).
# `--check` compara o que está gravado com o que a máquina tem agora e falha se alguma versão mudou.
# ! Motivo: o Ollama se atualiza sozinho (decisões 44 e 47) e o Playwright fixa a build do Chromium; sem o registro,
# nenhuma trilha da Fase 4 saberia declarar em que versões foi gravada, e a ponte de versão (regra R6) não teria com
# o que comparar. O bloco `cobaias` entra porque em 26/10/2026 a conferência mostrou PHP e MariaDB ausentes nesta
# máquina (as cobaias nunca subiram aqui), e o arquivo é o lugar de registrar esse resultado.
"""Registro do ambiente da Fase 4 (pacote P0): versões e o que a máquina tem."""
import argparse
import datetime as dt
import glob
import importlib.metadata
import json
import os
import platform
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

EXP = Path(__file__).resolve().parent
RAIZ = EXP.parent.parent.parent
sys.path.insert(0, str(RAIZ))

import caminhos
import cliente_ollama as oll
import navegador

CHAVES_VERSAO = ("navegador", "ollama", "playwright", "python")
ARQUIVO = "ambiente.json"


def caminho_padrao() -> Path:
    return caminhos.RESULTADOS / "fase4" / ARQUIVO


def montar(python: str, playwright: str, navegador: str, ollama: str, canal: str, executavel: str,
           maquina: dict, cobaias: dict) -> dict:
    """Monta o registro; as quatro versões precisam vir preenchidas e o canal precisa ser um dos aceitos."""
    versoes = {"python": python, "playwright": playwright, "navegador": navegador, "ollama": ollama}
    for chave, valor in versoes.items():
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"versão de {chave} vazia")
    import navegador as _nav
    if canal not in _nav.CANAIS:
        raise ValueError(f"canal {canal!r} fora de {_nav.CANAIS}")
    return {"versoes": versoes,
            "navegador": {"canal": canal, "executavel": executavel, "modo": "headless"},
            "maquina": maquina, "cobaias": cobaias,
            "gravado_em": dt.datetime.now().isoformat(timespec="seconds")}


def _cobaias() -> dict:
    """O que o instalador das cobaias (`_env_common` na raiz do repositório) encontra nesta máquina."""
    import _env_common as env
    uvicorn = env.COBAIA_API / ".venv" / "Scripts" / "uvicorn.exe"
    edge = sorted(glob.glob(r"C:\Program Files (x86)\Microsoft\Edge\Application\[0-9]*"))
    return {"php": env.find_php(), "mariadbd": env.find_mariadbd_server(), "cliente_mariadb": env.find_mysql_cli(),
            "uvicorn_cobaia_api": str(uvicorn) if uvicorn.exists() else None,
            "edge": Path(edge[-1]).name if edge else None,
            "playwright_chromium_baixado": env.playwright_chromium_instalado()}


def _ollama() -> str:
    try:
        versao = oll._get("/api/version").get("version", "")
    except Exception as e:
        raise SystemExit(f"Ollama não respondeu em /api/version ({e}); suba o Ollama antes de gravar o ambiente")
    return str(versao)


def coletar(canal: str = "chromium") -> dict:
    """Lê as versões da máquina: abre o navegador uma vez para ler a versão dele."""
    with navegador.Navegador(canal=canal) as nav:
        v = nav.versao()
    maquina = {"nome": platform.node(), "so": platform.platform(), "processador": platform.processor(),
               "nucleos_logicos": os.cpu_count()}
    return montar(python=platform.python_version(), playwright=v["playwright"], navegador=v["navegador"],
                  ollama=_ollama(), canal=canal, executavel=v["executavel"], maquina=maquina, cobaias=_cobaias())


def gravar(caminho: Path, dados: dict) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--canal", choices=navegador.CANAIS, default="chromium")
    ap.add_argument("--saida", default=None, help=f"arquivo de saída (padrão: {caminho_padrao()})")
    ap.add_argument("--check", action="store_true", help="compara o gravado com a máquina atual, sem regravar")
    args = ap.parse_args()
    caminho = Path(args.saida) if args.saida else caminho_padrao()
    atual = coletar(canal=args.canal)
    if args.check:
        gravado = json.loads(caminho.read_text(encoding="utf-8"))
        diferencas = [c for c in ("versoes", "navegador", "cobaias") if gravado.get(c) != atual.get(c)]
        if diferencas:
            for c in diferencas:
                print(f"{c}: gravado {gravado.get(c)} / agora {atual.get(c)}")
            sys.exit(1)
        print(f"--check ok: {caminho}")
        return
    gravar(caminho, atual)
    print(f"gravado: {caminho}")
    print(json.dumps(atual["versoes"], ensure_ascii=False))
    print("cobaias:", json.dumps(atual["cobaias"], ensure_ascii=False))


if __name__ == "__main__":
    main()
