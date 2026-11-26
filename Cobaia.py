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
import sys
import webbrowser

import install
import run
from _env_common import log


def main() -> None:
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) o `Cobaia.py` para quando `install.main()`
    # devolve um código diferente de zero.
    # ! Motivo: `install.main()` passou a devolver o código de saída. No Windows um passo obrigatório que falha continua
    # saindo por `sys.exit(1)`, como antes; mas rodando `python Cobaia.py` no Linux, uma instalação interrompida devolve 1,
    # e sem esta conferência o launcher subiria o site e a API numa instalação pela metade.
    codigo = install.main()
    if codigo:
        sys.exit(codigo)

    print()
    log("Iniciando CobaiaFront + CobaiaAPI...")
    front_proc, api_proc = run.start_services()

    front_url = f"http://localhost:{run.FRONT_PORT}"
    api_docs_url = f"http://localhost:{run.API_PORT}/docs"
    hub_url = f"http://127.0.0.1:{run.HUB_PORT}/"
    log(f"CobaiaFront: {front_url}")
    log(f"CobaiaAPI:   {api_docs_url}")

    # ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) o launcher passa a subir também o hub central e a abrir uma aba só,
    # nele; se o hub não for lançado ou a porta dele não responder, abre o site e a documentação da API, como antes, e avisa.
    # ! Motivo: o Eric pediu que o hub seja a central de tudo, aberta quando o `.exe` roda: é dele que se chega ao site e à API, se rodam
    # os testes e se veem as métricas. O hub sobe por `run.start_hub`, como processo à parte, e é encerrado junto com os outros.
    hub_proc = run.start_hub()
    if run.wait_until_ready():
        if hub_proc is not None and run.wait_for_port(run.HUB_PORT, timeout_s=30):
            log(f"Hub central: {hub_url}")
            webbrowser.open(hub_url)
        else:
            log("O hub central não respondeu; abrindo o site e a API, como antes.")
            webbrowser.open(front_url)
            webbrowser.open(api_docs_url)
    else:
        log("Os serviços demoraram a responder — abra manualmente as URLs acima.")

    log("Ctrl+C (ou feche esta janela) encerra tudo.")
    run.wait_and_cleanup(front_proc, api_proc, hub_proc)


if __name__ == "__main__":
    main()
