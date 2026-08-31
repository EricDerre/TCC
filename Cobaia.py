#!/usr/bin/env python3
# ! Alteração de IA - Revisar
"""
Launcher único: instalação (idempotente) + subir os serviços + abrir o
navegador. É o script-fonte compilado em Cobaia.exe via PyInstaller (ver
build_exe.ps1) — pensado pra ser o "hit and run" de fato: um duplo clique
faz tudo, do zero ou numa máquina que já tem tudo instalado.

As dependências Python da CobaiaAPI continuam indo pro venv em
Programacao/CobaiaAPI/.venv (install.py já faz isso, sem mudança aqui) —
mesmo quando este script roda compilado como .exe, o .exe só orquestra
subprocessos (winget/pip/php/uvicorn), nunca importa FastAPI/SQLAlchemy
diretamente, então não há conflito entre o Python embutido no .exe e o
Python do venv.

Uso: python Cobaia.py  (ou Cobaia.exe depois de compilado)
"""
import webbrowser

import install
import run
from _env_common import log


def main() -> None:
    install.main()

    print()
    log("Iniciando CobaiaFront + CobaiaAPI...")
    front_proc, api_proc = run.start_services()

    front_url = f"http://localhost:{run.FRONT_PORT}"
    api_docs_url = f"http://localhost:{run.API_PORT}/docs"
    log(f"CobaiaFront: {front_url}")
    log(f"CobaiaAPI:   {api_docs_url}")

    if run.wait_until_ready():
        webbrowser.open(front_url)
        webbrowser.open(api_docs_url)
    else:
        log("Os serviços demoraram a responder — abra manualmente as URLs acima.")

    log("Ctrl+C (ou feche esta janela) encerra tudo.")
    run.wait_and_cleanup(front_proc, api_proc)


if __name__ == "__main__":
    main()
