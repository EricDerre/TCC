#!/usr/bin/env python3
# ! Alteração de IA - Revisar
"""
Instalador único "hit and run" do ambiente cobaia (CobaiaFront + CobaiaAPI).

Cuida de: PHP 8.2 (com mysqli/pdo_mysql), MariaDB Server, schema+seed do
banco `ti93phpdb01`, e o venv Python + dependências da CobaiaAPI.

Idempotente: seguro rodar mais de uma vez na mesma máquina.

Chamado por install.ps1 (Windows) ou install.sh (Linux/macOS), que só
garantem que existe um Python 3 disponível antes de chegar aqui.
"""
import subprocess
import sys
import venv

from _env_common import (
    COBAIA_API,
    COBAIA_FRONT,
    OS_NAME,
    ensure_mariadb_running,
    ensure_root_no_password,
    find_mysql_cli,
    find_php,
    log,
    run,
)


def ensure_php() -> str:
    php = find_php()
    if php:
        log(f"PHP já instalado: {php}")
        return php

    log("PHP não encontrado — instalando...")
    if OS_NAME == "Windows":
        run([
            "winget", "install", "--id", "PHP.PHP.8.2", "-e",
            "--accept-package-agreements", "--accept-source-agreements",
        ])
    elif OS_NAME == "Linux":
        run(["sudo", "apt-get", "update"])
        run(["sudo", "apt-get", "install", "-y", "php", "php-mysql"])
    elif OS_NAME == "Darwin":
        run(["brew", "install", "php"])
    else:
        log(f"SO não reconhecido ({OS_NAME}) — instale PHP 8.x com mysqli/pdo_mysql manualmente.")
        sys.exit(1)

    php = find_php()
    if not php:
        log("PHP foi instalado mas não foi encontrado automaticamente. "
            "Feche e reabra o terminal (PATH pode precisar de refresh) e rode o instalador de novo.")
        sys.exit(1)
    log(f"PHP instalado: {php}")
    return php


def ensure_mariadb_installed() -> str:
    cli = find_mysql_cli()
    if cli:
        log(f"Cliente MariaDB/MySQL já disponível: {cli}")
        return cli

    log("MariaDB não encontrado — instalando...")
    if OS_NAME == "Windows":
        run([
            "winget", "install", "--id", "MariaDB.Server", "-e",
            "--accept-package-agreements", "--accept-source-agreements",
        ])
    elif OS_NAME == "Linux":
        run(["sudo", "apt-get", "update"])
        run(["sudo", "apt-get", "install", "-y", "mariadb-server"])
        run(["sudo", "systemctl", "enable", "--now", "mariadb"])
    elif OS_NAME == "Darwin":
        run(["brew", "install", "mariadb"])
        run(["brew", "services", "start", "mariadb"])
    else:
        log(f"SO não reconhecido ({OS_NAME}) — instale MariaDB/MySQL Server manualmente.")
        sys.exit(1)

    cli = find_mysql_cli()
    if not cli:
        log("MariaDB foi instalado mas o cliente CLI não foi encontrado automaticamente. "
            "Feche e reabra o terminal e rode o instalador de novo.")
        sys.exit(1)
    return cli


def apply_sql_files(cli: str) -> None:
    files = [
        COBAIA_FRONT / "banco" / "bancoatualizado.sql",
        COBAIA_FRONT / "banco" / "schema_completo.sql",
        COBAIA_FRONT / "banco" / "seed.sql",
    ]
    for sql_file in files:
        if not sql_file.exists():
            log(f"Aviso: {sql_file} não encontrado, pulando.")
            continue
        log(f"Aplicando {sql_file.name}...")
        with open(sql_file, "rb") as f:
            result = subprocess.run([cli, "-u", "root"], stdin=f, capture_output=True)
        if result.returncode != 0:
            log(f"Erro ao aplicar {sql_file.name}:")
            log(result.stderr.decode(errors="replace"))
            sys.exit(1)
    log(f"Banco pronto (schema completo + seed).")


def setup_cobaia_api() -> None:
    venv_dir = COBAIA_API / ".venv"
    if not venv_dir.exists():
        log("Criando venv da CobaiaAPI...")
        venv.EnvBuilder(with_pip=True).create(str(venv_dir))
    else:
        log("venv da CobaiaAPI já existe.")

    pip = venv_dir / ("Scripts/pip.exe" if OS_NAME == "Windows" else "bin/pip")
    # requirements-dev.txt (inclui requirements.txt via -r) — é ambiente de
    # teste/cobaia, não produção, então pytest/ruff vêm de graça por padrão.
    req = COBAIA_API / "requirements-dev.txt"
    if not req.exists():
        log("requirements-dev.txt ainda não existe em CobaiaAPI — pulando instalação de dependências "
            "(rode o instalador de novo depois que a CobaiaAPI estiver implementada).")
        return
    run([str(pip), "install", "-r", str(req)])


def main() -> None:
    log(f"Sistema operacional detectado: {OS_NAME}")

    ensure_php()

    cli = ensure_mariadb_installed()
    if not ensure_mariadb_running(cli):
        log("Não foi possível subir o MariaDB. Verifique a instalação e rode o instalador de novo.")
        sys.exit(1)
    ensure_root_no_password(cli)
    apply_sql_files(cli)

    setup_cobaia_api()

    log("")
    log("Instalação concluída. Para rodar o site, use:")
    log("  Windows:      .\\run.ps1")
    log("  Linux/macOS:  ./run.sh")


if __name__ == "__main__":
    main()
