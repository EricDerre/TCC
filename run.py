#!/usr/bin/env python3
# ! Alteração de IA - Revisar
"""
Sobe CobaiaFront (servidor embutido do PHP), MariaDB (se ainda não estiver
rodando) e CobaiaAPI (uvicorn) juntos. Ctrl+C encerra tudo.

Não instala nada — isso é papel do install.py (rode install.ps1/install.sh
primeiro se ainda não rodou).
"""
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


def main() -> None:
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

    log(f"CobaiaFront: http://localhost:{FRONT_PORT}")
    log(f"CobaiaAPI:   http://localhost:{API_PORT}/docs")
    log("Ctrl+C encerra tudo.")

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


if __name__ == "__main__":
    main()
