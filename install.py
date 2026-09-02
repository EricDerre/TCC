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
import os
import subprocess
import sys

from _env_common import (
    AGENTE_CORE,
    COBAIA_API,
    COBAIA_FRONT,
    IS_FROZEN,
    OS_NAME,
    ensure_mariadb_running,
    ensure_root_no_password,
    find_mysql_cli,
    find_ollama,
    find_or_install_real_python,
    find_php,
    log,
    modelo_llm_ja_baixado,
    playwright_chromium_instalado,
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
        # Cria via subprocesso de um Python "de verdade" (nunca via
        # venv.EnvBuilder in-process nem com o interpretador embutido no
        # .exe compilado) — confirmado ao vivo que o interpretador congelado
        # do PyInstaller não consegue criar venvs (falta o layout normal de
        # instalação). No fluxo por script, sys.executable já é real; só
        # busca/instala um Python separado quando rodando como .exe.
        base_python = find_or_install_real_python() if IS_FROZEN else sys.executable
        run([base_python, "-m", "venv", str(venv_dir)])
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


def ensure_ollama() -> str | None:
    """! Alteração de IA - Revisar: instala o Ollama (runtime do LLM local) se ainda
    não existir, e devolve o caminho do executável.
    ! Motivo: a inferência do agente roda inteiramente na máquina do usuário — sem
    isso instalado, o AgenteCore não tem como produzir diagnóstico. Segue o mesmo
    padrão dos demais componentes (gerenciador de pacotes nativo por sistema
    operacional, e busca em caminho conhecido porque o PATH não atualiza na sessão
    atual logo após a instalação)."""
    ollama = find_ollama()
    if ollama:
        log(f"Ollama já instalado: {ollama}")
        return ollama

    log("Ollama não encontrado — instalando...")
    if OS_NAME == "Windows":
        run([
            "winget", "install", "--id", "Ollama.Ollama", "-e",
            "--accept-package-agreements", "--accept-source-agreements",
        ])
    elif OS_NAME == "Linux":
        log("No Linux o Ollama é instalado pelo script oficial:")
        log("  curl -fsSL https://ollama.com/install.sh | sh")
        log("Rode o comando acima e execute o instalador de novo.")
        return None
    elif OS_NAME == "Darwin":
        run(["brew", "install", "--cask", "ollama"])

    ollama = find_ollama()
    if not ollama:
        log("Ollama foi instalado mas não foi localizado nesta sessão. "
            "Feche e reabra o terminal e rode o instalador de novo.")
    return ollama


def setup_agente_core() -> None:
    """! Alteração de IA - Revisar: prepara o ambiente do AgenteCore — venv,
    dependências, navegador do Playwright, Ollama e download do modelo.
    ! Motivo: são as dependências mais pesadas do projeto (o navegador e o modelo
    somam alguns GB), então só são baixadas quando o AgenteCore de fato existe. Isso
    mantém a instalação do ambiente cobaia leve para quem só quer rodar o site, e
    passa a valer automaticamente assim que o agente for implementado."""
    req = AGENTE_CORE / "requirements.txt"
    if not req.exists():
        log("AgenteCore ainda não implementado — pulando Ollama, modelo e Playwright.")
        return

    venv_dir = AGENTE_CORE / ".venv"
    if not venv_dir.exists():
        log("Criando venv do AgenteCore...")
        base_python = find_or_install_real_python() if IS_FROZEN else sys.executable
        run([base_python, "-m", "venv", str(venv_dir)])
    else:
        log("venv do AgenteCore já existe.")

    bin_dir = "Scripts" if OS_NAME == "Windows" else "bin"
    pip = venv_dir / bin_dir / ("pip.exe" if OS_NAME == "Windows" else "pip")
    python_venv = venv_dir / bin_dir / ("python.exe" if OS_NAME == "Windows" else "python")
    run([str(pip), "install", "-r", str(req)])

    # Chromium do próprio Playwright (não o Chrome/Edge do sistema): a versão fica
    # travada pela versão do Playwright, o que é o que torna as medições de MTTR e
    # Task Success reproduzíveis entre as máquinas dos integrantes e ao longo do tempo.
    if playwright_chromium_instalado():
        log("Chromium do Playwright já baixado.")
    else:
        run([str(python_venv), "-m", "playwright", "install", "chromium"])

    ollama = ensure_ollama()
    if ollama:
        # Porte escolhido pela comparação medida em
        # Programacao/AgenteCore/experimentos/RESULTADO_FASE2.md: o 3b diagnostica
        # corretamente (quando recebe a divergência de contrato já calculada em código),
        # responde em ~7s só em CPU e ocupa ~2 GB, contra ~19s e ~4,8 GB do 7b. O 1.5b
        # foi descartado por gerar CSS inválido na cura de seletor e errar o diagnóstico.
        modelo = os.environ.get("COBAIA_MODELO_LLM", "qwen2.5-coder:3b")
        if modelo_llm_ja_baixado(ollama, modelo):
            log(f"Modelo {modelo} já baixado.")
        else:
            log(f"Baixando o modelo {modelo} (pode demorar na primeira vez)...")
            run([ollama, "pull", modelo])


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
    setup_agente_core()

    log("")
    log("Instalação concluída. Para rodar o site, use:")
    log("  Windows (clique duplo ou terminal):  run.cmd")
    log("  Linux/macOS:                          ./run.sh")


if __name__ == "__main__":
    main()
