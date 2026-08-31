#!/usr/bin/env python3
# ! Alteração de IA - Revisar
"""
Sobe CobaiaFront (servidor embutido do PHP), MariaDB (se ainda não estiver
rodando) e CobaiaAPI (uvicorn) juntos. Ctrl+C encerra tudo.

Não instala nada — isso é papel do install.py (rode install.ps1/install.sh
primeiro se ainda não rodou).

As funções start_services/wait_until_ready/wait_and_cleanup são reutilizadas
por Cobaia.py (launcher combinado instalação+run+abrir navegador, compilado
em .exe via PyInstaller — ver build_exe.ps1).
"""
import socket
import subprocess
import sys
import time

from _env_common import (
    COBAIA_API,
    COBAIA_FRONT,
    OS_NAME,
    ensure_mariadb_running,
    find_mysql_cli,
    find_php,
    log,
    php_extension_flags,
    stop_managed_mariadbd,
)

FRONT_PORT = 8080
API_PORT = 8000


def start_services() -> tuple[subprocess.Popen, subprocess.Popen]:
    """Garante PHP/MariaDB disponíveis e sobe CobaiaFront + CobaiaAPI. Encerra
    o processo (sys.exit) se algo obrigatório estiver faltando."""
    php = find_php()
    if not php:
        log("PHP não encontrado. Rode install.ps1 (Windows) ou install.sh (Linux/macOS) primeiro.")
        sys.exit(1)

    cli = find_mysql_cli()
    if not cli or not ensure_mariadb_running(cli):
        log("MariaDB não encontrado/não subiu. Rode install.ps1/install.sh primeiro.")
        sys.exit(1)

    venv_dir = COBAIA_API / ".venv"
    uvicorn = venv_dir / ("Scripts/uvicorn.exe" if OS_NAME == "Windows" else "bin/uvicorn")
    if not uvicorn.exists():
        log(f"{uvicorn} não encontrado. Rode install.ps1/install.sh primeiro "
            "(ou implemente a CobaiaAPI se ainda não existe).")
        sys.exit(1)

    front_proc = subprocess.Popen([
        php, "-S", f"localhost:{FRONT_PORT}", "-t", str(COBAIA_FRONT),
        *php_extension_flags(php),
    ])
    api_proc = subprocess.Popen(
        [str(uvicorn), "app.main:app", "--port", str(API_PORT)],
        cwd=str(COBAIA_API),
    )
    return front_proc, api_proc


def _port_responds(port: int) -> bool:
    try:
        with socket.create_connection(("localhost", port), timeout=1):
            return True
    except OSError:
        return False


def wait_until_ready(timeout_s: int = 30) -> bool:
    """Espera as portas do CobaiaFront e da CobaiaAPI aceitarem conexão."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if _port_responds(FRONT_PORT) and _port_responds(API_PORT):
            return True
        time.sleep(0.5)
    return False


def wait_and_cleanup(front_proc: subprocess.Popen, api_proc: subprocess.Popen) -> None:
    """Bloqueia até Ctrl+C (ou um dos processos cair sozinho), depois encerra
    tudo de forma limpa."""
    try:
        while True:
            time.sleep(1)
            if front_proc.poll() is not None or api_proc.poll() is not None:
                break
    except KeyboardInterrupt:
        pass
    finally:
        for proc in (front_proc, api_proc):
            if proc.poll() is None:
                proc.terminate()
        stop_managed_mariadbd()


def main() -> None:
    front_proc, api_proc = start_services()
    log(f"CobaiaFront: http://localhost:{FRONT_PORT}")
    log(f"CobaiaAPI:   http://localhost:{API_PORT}/docs")
    log("Ctrl+C encerra tudo.")
    wait_and_cleanup(front_proc, api_proc)


if __name__ == "__main__":
    main()
