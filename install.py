#!/usr/bin/env python3
# ! Alteração de IA - Revisar
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) a docstring do módulo ganha o uso (`python install.py [--conferir] [--reproduzir]`) e diz que no Linux os pacotes, o serviço do banco, o Chromium e o Ollama entram por `instalador/ferramentas.py`.
# ! Motivo: até o pacote I2 o Linux tinha um ponto de entrada provisório (`instalador/nucleo.py`) e a docstring descrevia só o instalador do Windows; com os passos do Linux dentro deste arquivo, quem abre o módulo precisa saber para onde o Linux vai.
"""
Instalador único "hit and run" do ambiente cobaia (CobaiaFront + CobaiaAPI).

Cuida de: PHP 8.2 (com mysqli/pdo_mysql), MariaDB Server, schema+seed do
banco `ti93phpdb01`, e o venv Python + dependências da CobaiaAPI.

Idempotente: seguro rodar mais de uma vez na mesma máquina.

Uso: python install.py [--conferir] [--reproduzir]. No Linux (apt e dnf) os pacotes do
sistema, o serviço e o root do MariaDB, o Chromium do Playwright e o Ollama entram pelas
funções de instalador/ferramentas.py, chamadas por instalar_no_linux.

Chamado por install.ps1 (Windows) ou install.sh (Linux/macOS), que só
garantem que existe um Python 3 disponível antes de chegar aqui.
"""
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) entram `argparse`, `time`, `datetime` e `REPO_ROOT` nos imports.
# ! Motivo: `main` passa a ler argumentos (`--conferir`, `--ate`, `--reproduzir`), `cronometrar` mede o tempo de cada passo com `time` e `gravar_passos` grava a data com `datetime` e a pasta `.ferramentas/instalacao` a partir de `REPO_ROOT`.
import argparse
import ctypes
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

from _env_common import (
    AGENTE_CORE,
    COBAIA_API,
    COBAIA_FRONT,
    DATADIR_DO_PROJETO,
    IS_FROZEN,
    OS_NAME,
    REPO_ROOT,
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
    elif OS_NAME == "Darwin":
        run(["brew", "install", "php"])
    else:
        # ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) saiu daqui o ramo do Linux (`sudo apt-get
        # install -y php php-mysql`), e a mensagem deste `else` diz onde o PHP entra fora do Windows e do macOS.
        # ! Motivo: células de 18 e 19/11/2026. No Ubuntu esse comando trazia o Apache (`apache2`, um servidor web na porta 80
        # que o projeto não usa, suspeita HL13) e não trazia o `php-mbstring` (`Call to undefined function
        # mb_strimwidth()`, HL11); no Fedora ele dava `sudo: apt-get: command not found` e o instalador parava em "Feche e
        # reabra o terminal" (HL3). No Linux os pacotes entram por `instalar_no_linux`, mais abaixo.
        log(f"Este passo só instala o PHP no Windows e no macOS; em {OS_NAME} ele vem dos pacotes do sistema "
            "(instalar_no_linux) ou é instalado à mão, na versão 8.x com mysqli, pdo_mysql e mbstring.")
        sys.exit(1)

    php = find_php()
    if not php:
        log("PHP foi instalado mas não foi encontrado automaticamente. "
            "Feche e reabra o terminal (PATH pode precisar de refresh) e rode o instalador de novo.")
        sys.exit(1)
    log(f"PHP instalado: {php}")
    return php


# ! Alteração de IA - Revisar: (26/10/2026) MariaDB portátil para máquina Windows sem administrador: a série que o
# instalador baixa e a API oficial de downloads que publica o arquivo e o SHA-256 de cada versão.
# ! Motivo: o MSI do winget (`MariaDB.Server`) exige elevação; na máquina-alvo i5, corporativa, o instalador parava
# nele e as cobaias nunca tinham subido. O zip oficial roda como processo comum, que é o caminho (3) que
# `_env_common.ensure_mariadb_running` já usa no Windows, e `_env_common` procura o portátil em `%LOCALAPPDATA%\MariaDB`.
MARIADB_SERIE = "11.8"
MARIADB_API = "https://downloads.mariadb.org/rest-api/mariadb/"


def _versao_tupla(versao: str) -> tuple[int, ...]:
    partes = []
    for pedaco in versao.split("."):
        digitos = "".join(ch for ch in pedaco if ch.isdigit())
        partes.append(int(digitos) if digitos else 0)
    return tuple(partes)


def escolher_zip_mariadb(resposta: dict, sufixo: str = "-winx64.zip") -> dict:
    """! Alteração de IA - Revisar: escolhe, na resposta da API de downloads do MariaDB
    (`.../rest-api/mariadb/<série>/`), a versão mais nova que tenha o zip do Windows 64 bits e
    devolve versão, nome do arquivo, URL e SHA-256 publicados.
    ! Motivo: a lista de cada versão traz o MSI, o zip de símbolos de depuração e o zip do servidor;
    o instalador precisa do zip do servidor e do hash que o site publica, para conferir o download
    antes de extrair. As chaves da resposta não vêm em ordem garantida, por isso a versão é comparada
    número a número."""
    releases = resposta.get("releases") or {}
    for chave in sorted(releases, key=_versao_tupla, reverse=True):
        release = releases[chave] or {}
        versao = release.get("release_id") or chave
        for arquivo in release.get("files") or []:
            nome = arquivo.get("file_name") or ""
            if nome.endswith(sufixo) and "debugsymbols" not in nome:
                return {"versao": versao, "nome": nome, "url": arquivo.get("file_download_url", ""),
                        "sha256": (arquivo.get("checksum") or {}).get("sha256sum", "")}
    raise ValueError(f"nenhum arquivo *{sufixo} (winx64.zip) na resposta da API do MariaDB")


def caminhos_mariadb_portatil(versao: str, base: Path | None = None, dados: Path | None = None) -> dict:
    """! Alteração de IA - Revisar: os caminhos do MariaDB portátil: zip baixado, pasta extraída
    (`mariadb-<versão>-winx64`), `bin`, `mariadb-install-db.exe`, pasta de dados e `my.ini`.
    ! Motivo: `_env_common.find_mysql_cli`, `find_mariadbd_server`, `find_mariadb_admin` e
    `find_mariadb_datadir_config` procuram exatamente nesses lugares (`%LOCALAPPDATA%\\MariaDB\\...`);
    montar os caminhos num lugar só evita que o instalador grave numa pasta que o run.py não acha.
    ! Alteração de IA - Revisar: (07/11/2026, ficha 55) a pasta de dados passa a ser `DATADIR_DO_PROJETO` (`.mariadb/data`
    dentro do projeto, fora do git); `dados=` troca o lugar só nos testes. Os binários continuam em `%LOCALAPPDATA%\\MariaDB`.
    ! Motivo: ver a tag de DATADIR_DO_PROJETO em _env_common.py: dentro do app Claude (pacote MSIX) a pasta de dados em
    AppData\\Local virava duas, e o servidor misturava as duas camadas."""
    if base is None:
        base = Path(os.path.expandvars(r"%LOCALAPPDATA%")) / "MariaDB"
    pasta = base / f"mariadb-{versao}-winx64"
    dados = dados or DATADIR_DO_PROJETO
    return {"base": base, "download": base / "download", "zip": base / "download" / f"mariadb-{versao}-winx64.zip",
            "pasta": pasta, "bin": pasta / "bin", "install_db": pasta / "bin" / "mariadb-install-db.exe",
            "dados": dados, "my_ini": dados / "my.ini"}


def eh_administrador() -> bool:
    """! Alteração de IA - Revisar: diz se o processo roda com direitos de administrador no Windows.
    ! Motivo: é o que decide entre o MSI do winget (precisa de elevação) e o zip portátil; em outro
    sistema devolve False e nada muda lá."""
    if OS_NAME != "Windows":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def usar_mariadb_portatil(so: str = OS_NAME, admin: bool | None = None, ambiente=None) -> bool:
    """! Alteração de IA - Revisar: no Windows sem administrador o MariaDB vem do zip portátil;
    `COBAIA_MARIADB_PORTATIL=1` força o portátil mesmo com administrador e `=0` força o MSI.
    ! Motivo: quem tem administrador continua com o MSI do winget (caminho testado nas máquinas dos
    integrantes); quem não tem, como na máquina-alvo i5, não pode nem tentar o MSI. A variável existe
    para o instalador rodar sem terminal (install.ps1, Cobaia.exe) e para testes."""
    if ambiente is None:
        ambiente = os.environ
    if so != "Windows":
        return False
    forcado = ambiente.get("COBAIA_MARIADB_PORTATIL")
    if forcado == "1":
        return True
    if forcado == "0":
        return False
    if admin is None:
        admin = eh_administrador()
    return not admin


def conferir_sha256(caminho: Path, esperado: str) -> bool:
    """! Alteração de IA - Revisar: SHA-256 do arquivo comparado com o hash publicado (maiúsculas ou minúsculas).
    ! Motivo: o zip vem da internet para uma máquina corporativa; sem a conferência, um download truncado
    ou trocado seria extraído e executado."""
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest() == esperado.strip().lower()


def extrair_zip_seguro(zip_path: Path, destino: Path) -> None:
    """! Alteração de IA - Revisar: extrai o zip só depois de conferir que nenhum caminho dele sai da pasta de destino.
    ! Motivo: `ZipFile.extractall` grava onde o nome do arquivo mandar; um zip com `..\\` no nome escreveria fora de
    `%LOCALAPPDATA%\\MariaDB`."""
    destino = destino.resolve()
    with zipfile.ZipFile(zip_path) as z:
        for nome in z.namelist():
            alvo = (destino / nome).resolve()
            if alvo != destino and destino not in alvo.parents:
                raise ValueError(f"o zip tem um caminho fora da pasta de destino: {nome}")
        destino.mkdir(parents=True, exist_ok=True)
        z.extractall(destino)


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) função nova `tamanho_legivel`, usada pela linha de progresso de
# `baixar_arquivo`.
# ! Motivo: célula L-F45 de 19/11/2026: ao baixar o script do Ollama (alguns kB) o instalador mostrava `0 MB de 0 MB`,
# porque a linha só sabia contar em MB inteiros. Arquivo de 1 MB para cima continua aparecendo como antes (`1 MB de 97 MB`).
def tamanho_legivel(nbytes: int) -> str:
    """`21 kB` abaixo de 1 MB; daí para cima, MB inteiros (`25 MB`)."""
    if nbytes < (1 << 20):
        return f"{max(1, round(nbytes / 1024))} kB"
    return f"{nbytes >> 20} MB"


def baixar_arquivo(url: str, destino: Path) -> int:
    """! Alteração de IA - Revisar: baixa a URL para o arquivo em blocos de 1 MB, com uma linha de progresso a cada 10 MB.
    ! Motivo: o zip do MariaDB tem cerca de 100 MB; sem progresso o instalador parece travado na rede corporativa."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    pedido = urllib.request.Request(url, headers={"User-Agent": "cobaia-install"})
    lidos = 0
    marco = -1
    with urllib.request.urlopen(pedido, timeout=120) as resposta, open(destino, "wb") as saida:
        total = int(resposta.headers.get("Content-Length") or 0)
        while True:
            bloco = resposta.read(1 << 20)
            if not bloco:
                break
            saida.write(bloco)
            lidos += len(bloco)
            if (lidos >> 20) // 10 != marco:
                marco = (lidos >> 20) // 10
                # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) a linha de progresso usa `tamanho_legivel` (kB para arquivo pequeno, MB para o resto).
                # ! Motivo: ver a tag de `tamanho_legivel`, acima (célula L-F45: `0 MB de 0 MB`).
                log(f"  {tamanho_legivel(lidos)}" + (f" de {tamanho_legivel(total)}" if total else ""))
    return lidos


def instalar_mariadb_portatil(perguntar: bool = True) -> str | None:
    """! Alteração de IA - Revisar: instala o MariaDB sem administrador: consulta a API de downloads
    (série MARIADB_SERIE), pergunta antes de baixar (a menos de `COBAIA_MARIADB_PORTATIL=1`), baixa
    o zip oficial em `%LOCALAPPDATA%\\MariaDB\\download`, confere o SHA-256 publicado, extrai em
    `%LOCALAPPDATA%\\MariaDB` e cria a pasta de dados com `mariadb-install-db.exe --datadir ... --port=3306`
    (root sem senha; desde 07/11/2026 a pasta de dados é `.mariadb/data` dentro do projeto, ficha 55).
    Devolve o cliente achado por `find_mysql_cli`, ou None com a causa no log.
    ! Motivo: em 26/10/2026 esse caminho foi feito à mão na máquina-alvo i5 (as cobaias nunca tinham
    subido lá); sem a função, quem clonasse o repositório numa máquina sem administrador pararia no MSI
    do winget. Cada passo é pulado quando já foi feito, então rodar de novo é seguro; bloqueio de rede
    ou de antivírus vira mensagem no log, nunca proteção desligada."""
    log(f"Instalando o MariaDB portátil (série {MARIADB_SERIE}) em %LOCALAPPDATA%\\MariaDB, sem administrador...")
    try:
        pedido = urllib.request.Request(f"{MARIADB_API}{MARIADB_SERIE}/", headers={"User-Agent": "cobaia-install"})
        with urllib.request.urlopen(pedido, timeout=60) as resposta:
            escolha = escolher_zip_mariadb(json.load(resposta))
    except Exception as e:
        log(f"Não deu para consultar a API de downloads do MariaDB ({e}). "
            "Baixe o zip winx64 em https://mariadb.org/download/ e extraia em %LOCALAPPDATA%\\MariaDB.")
        return None
    cam = caminhos_mariadb_portatil(escolha["versao"])
    if not cam["install_db"].exists():
        if perguntar and os.environ.get("COBAIA_MARIADB_PORTATIL") != "1":
            if not sys.stdin or not sys.stdin.isatty():
                log("Sem terminal para perguntar antes de baixar; rode com COBAIA_MARIADB_PORTATIL=1 para baixar sem perguntar.")
                return None
            pergunta = (f"Baixar {escolha['nome']} de downloads.mariadb.org (cerca de 100 MB) para {cam['download']} "
                        f"e extrair em {cam['base']}? [s/N] ")
            if input(pergunta).strip().lower() not in ("s", "sim", "y", "yes"):
                log("Download recusado. Instale o MariaDB manualmente ou rode o instalador de novo.")
                return None
        log(f"Baixando {escolha['url']} ...")
        baixar_arquivo(escolha["url"], cam["zip"])
        if not conferir_sha256(cam["zip"], escolha["sha256"]):
            cam["zip"].unlink(missing_ok=True)
            log("O SHA-256 do zip baixado não bate com o publicado pelo site do MariaDB; arquivo apagado. Tente de novo.")
            return None
        log(f"SHA-256 conferido ({escolha['sha256'][:12]}...). Extraindo em {cam['base']} ...")
        extrair_zip_seguro(cam["zip"], cam["base"])
    else:
        log(f"MariaDB portátil já extraído em {cam['pasta']}.")
    if not cam["my_ini"].exists():
        log(f"Criando a pasta de dados em {cam['dados']} (root sem senha, porta 3306)...")
        resultado = run([str(cam["install_db"]), f"--datadir={cam['dados']}", "--port=3306"])
        if resultado.returncode != 0:
            log("mariadb-install-db.exe falhou; veja a saída acima.")
            return None
    cli = find_mysql_cli()
    if not cli:
        log("MariaDB portátil extraído, mas o cliente não foi encontrado em %LOCALAPPDATA%\\MariaDB.")
    return cli


def ensure_mariadb_installed() -> str:
    cli = find_mysql_cli()
    if cli:
        log(f"Cliente MariaDB/MySQL já disponível: {cli}")
        return cli

    log("MariaDB não encontrado — instalando...")
    if OS_NAME == "Windows":
        # ! Alteração de IA - Revisar: (26/10/2026) sem administrador (ou com COBAIA_MARIADB_PORTATIL=1) o MariaDB
        # vem do zip portátil; o MSI do winget continua sendo o caminho com administrador e, se ele falhar, o
        # portátil é tentado em seguida.
        # ! Motivo: na máquina-alvo i5 (corporativa) o MSI do `MariaDB.Server` exige elevação e o instalador parava
        # aqui, com a mensagem "MariaDB foi instalado mas o cliente CLI não foi encontrado"; o zip oficial roda como
        # processo comum, que é o que ensure_mariadb_running já faz no Windows.
        if usar_mariadb_portatil():
            instalar_mariadb_portatil()
        else:
            resultado = run([
                "winget", "install", "--id", "MariaDB.Server", "-e",
                "--accept-package-agreements", "--accept-source-agreements",
            ])
            if resultado.returncode != 0:
                log("O winget não conseguiu instalar o MariaDB.Server; tentando o zip portátil...")
                instalar_mariadb_portatil()
    elif OS_NAME == "Darwin":
        run(["brew", "install", "mariadb"])
        run(["brew", "services", "start", "mariadb"])
    else:
        # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) saiu daqui o ramo do Linux (`apt-get install -y mariadb-server`
        # e `systemctl enable --now mariadb`).
        # ! Motivo: célula L-U2404-SS de 19/11/2026 (suspeita HL7): sem o systemd o `systemctl` responde "System has not been
        # booted with systemd as init system (PID 1). Can't operate."; e o `apt-get` sem `--no-remove` trocaria um
        # `mysql-server` já instalado pelo MariaDB sem perguntar. No Linux o pacote e o serviço entram por `instalar_no_linux`.
        log(f"Este passo só instala o MariaDB no Windows e no macOS; em {OS_NAME} ele vem dos pacotes do sistema "
            "(instalar_no_linux) ou é instalado à mão.")
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
    elif OS_NAME == "Darwin":
        run(["brew", "install", "--cask", "ollama"])
    else:
        # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) saiu daqui o ramo do Linux, que só imprimia o comando do script
        # oficial e devolvia None.
        # ! Motivo: célula L-U2404 de 18/11/2026 (suspeita HL5): a instalação terminava em "Instalação concluída" sem o
        # Ollama. No Linux quem instala o Ollama, na versão testada, é `instalador/ferramentas.py` (`preparar_ollama`).
        log(f"Este passo só instala o Ollama no Windows e no macOS; em {OS_NAME} ele entra por instalador/ferramentas.py.")
        return None

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
        # ! Alteração de IA - Revisar: o modelo padrão passa de qwen2.5-coder:3b para qwen2.5:7b
        # (decisão 52 do Memorial, 22/09/2026); a variável COBAIA_MODELO_LLM continua mandando.
        # ! Motivo: o 3b era o padrão provisório da comparação de porte da Fase 2
        # (RESULTADO_FASE2.md: ~7 s e ~2 GB contra ~19 s e ~4,8 GB do 7b) "até a decisão sair".
        # A decisão saiu da Fase 3 (13–15/09/2026): pela regra pré-registrada, qwen2.5:7b com a
        # biblioteca L1 fez 91,7% de acurácia balanceada nos 36 casos de avaliação, contra 71,2%
        # na melhor versão do 3b (resultados_alvo/fase3/decisao_modelo.md, seção 1). Custa mais
        # (mediana de 66,8 s por diagnóstico com a biblioteca original na máquina-alvo i5,
        # relatório da Fase 3 §9) e é o modelo que o agente das próximas fases usa.
        modelo = os.environ.get("COBAIA_MODELO_LLM", "qwen2.5:7b")
        if modelo_llm_ja_baixado(ollama, modelo):
            log(f"Modelo {modelo} já baixado.")
        else:
            log(f"Baixando o modelo {modelo} (pode demorar na primeira vez)...")
            run([ollama, "pull", modelo])


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) entram aqui `eh_root`, `caminho_para`,
# `instalar_no_linux`, `instalar_e_relatar_no_linux`, `relatar_versoes` e `_argumentos`, trazidos de `instalador/nucleo.py`, que deixa de existir; os passos do Windows e
# do macOS saem do `main` e viram `instalar_no_windows_ou_mac`, na mesma ordem; e o `main` passa a receber argumentos
# (`--conferir`, `--ate`, `--reproduzir`), a reconhecer a família do sistema e a devolver o código de saída.
# ! Motivo: célula L-U2404 de 18/11/2026 (suspeitas HL10 e HL12): este arquivo aplicava os `.sql` antes de o serviço e o root
# do MariaDB estarem prontos e parava em "Não foi possível subir o MariaDB" com o serviço no ar; no Fedora rodava `sudo
# apt-get` ("command not found", HL3). A ordem certa (pacotes, PHP, serviço, root com a pergunta, `.sql`, venvs, Chromium,
# Ollama) foi provada nas células de 19/11/2026 (Ubuntu 22.04, 24.04 e 26.04, Debian 12 e 13, Fedora 45) num ponto de
# entrada provisório, porque este arquivo não podia mudar antes de a corrida 28b ser lida; `python install.py` chamado
# direto ainda era o instalador antigo. Os módulos de `instalador/` são importados dentro das funções, e não no topo, para
# que `import install` no Windows (o `restaurar_banco.py` das corridas e o `Cobaia.exe`) carregue o mesmo que carregava.
USO = """Uso: python install.py [--conferir [--ate N1|N2|N3|N4]] [--reproduzir]
Sem argumento, instala. Com --conferir, roda a prova da instalação e grava .ferramentas/prova/registro.json.
--reproduzir exige, nas ferramentas que afetam as medidas, a versão exata do versoes.json."""

_PASSOS: list[dict] = []


def eh_root() -> bool:
    """O processo roda como root? (No Windows não existe `geteuid`.)"""
    return hasattr(os, "geteuid") and os.geteuid() == 0


def caminho_para(info: dict) -> str:
    """'apt' e 'dnf' (Debian, Ubuntu e derivados; Fedora) devolvem a própria família; 'nao_suportado' recebe a mensagem com a
    lista do que instalar à mão; Windows e macOS seguem pelos passos de `instalar_no_windows_ou_mac`."""
    if info["familia"] in ("apt", "dnf", "nao_suportado"):
        return info["familia"]
    return "como_estava"


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) funções novas `cronometrar` e `gravar_passos`: o instalador anota
# quanto cada passo levou e grava a lista em `.ferramentas/instalacao/passos.json`, que a prova copia para o `registro.json`.
# ! Motivo: a seção 3.3 do plano aprovado pede no registro o tempo de cada passo; até aqui só havia o tempo de cada nível da
# prova e o total da célula, porque este arquivo não podia mudar antes da corrida 28b (desvio 7 do anexo do plano). O
# arquivo fica dentro do projeto, em `.ferramentas/`, que está fora do git.
def cronometrar(nome: str, funcao, *argumentos):
    """Roda um passo do instalador e anota quanto ele levou, também quando o passo falha."""
    inicio = time.time()
    try:
        return funcao(*argumentos)
    finally:
        _PASSOS.append({"passo": nome, "segundos": round(time.time() - inicio, 1)})


def gravar_passos(resultado: str, pasta: Path | None = None) -> Path | None:
    """Grava os tempos dos passos e o resultado da instalação ('concluida' ou 'interrompida'). Não conseguir gravar vira
    aviso, nunca erro: a instalação não depende deste arquivo."""
    pasta = pasta or REPO_ROOT / ".ferramentas" / "instalacao"
    dados = {
        "tag_ia": {
            "alteracao": "! Alteração de IA - Revisar: arquivo gerado pelo install.py: quanto levou cada passo da última "
                         "instalação nesta pasta e como ela terminou.",
            "motivo": "! Motivo: o plano do instalador único (decisão 143, seção 3.3) pede o tempo de cada passo no registro "
                      "da prova; o instalador e a prova rodam em processos separados, e este arquivo leva um ao outro.",
        },
        "gravado_em": datetime.now().isoformat(timespec="seconds"),
        "resultado": resultado,
        "passos": list(_PASSOS),
    }
    try:
        pasta.mkdir(parents=True, exist_ok=True)
        caminho = pasta / "passos.json"
        caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    except OSError as e:
        log(f"Aviso: não foi possível gravar os tempos da instalação em {pasta}: {e}")
        return None
    return caminho


def instalar_no_linux(info: dict, ferr: dict) -> None:
    """Os passos do Linux, na ordem em que um depende do outro: o serviço e o root do banco vêm antes dos `.sql`. Valem para
    o `apt` e para o `dnf`. Um passo que não dá certo levanta `ferramentas.Falha`."""
    from instalador import ferramentas

    def venv_da_api() -> None:
        # Com a `.venv` presente e sem `pip` dentro (venv do Windows num clone usado pelo WSL, ou instalação que parou no
        # `ensurepip is not available`), o `setup_cobaia_api` rodaria `.venv/bin/pip` e morreria em `FileNotFoundError`.
        ferramentas.conferir_pasta_da_venv(COBAIA_API / ".venv")
        setup_cobaia_api()
        ferramentas.conferir_venv(COBAIA_API / ".venv", ("fastapi", "uvicorn", "pymysql"))

    cronometrar("pacotes do sistema", ferramentas.instalar_pacotes_do_sistema, info)
    cronometrar("PHP", ferramentas.conferir_php)
    cli = find_mysql_cli()
    if not cli:
        raise ferramentas.Falha("o cliente do MariaDB não foi encontrado depois da instalação dos pacotes")
    cronometrar("serviço do MariaDB", ferramentas.subir_banco, cli)
    cronometrar("root do MariaDB", ferramentas.garantir_root_sem_senha, cli)
    cronometrar("banco (os três .sql)", apply_sql_files, cli)
    cronometrar("venv da CobaiaAPI", venv_da_api)
    cronometrar("AgenteCore (venv, Chromium, Ollama e modelo)", ferramentas.preparar_agente, info, ferr)


def relatar_versoes(ferr: dict, reproduzir: bool) -> list[str]:
    """Imprime a versão encontrada de cada ferramenta contra o versoes.json e devolve as que impedem seguir."""
    from instalador import conferir, versoes
    julgadas = versoes.julgar(conferir._versoes_encontradas(), ferr, reproduzir=reproduzir)
    log("Versões encontradas:")
    for nome, dados in julgadas.items():
        log(f"  {nome}: {dados['encontrada'] or 'não lida'} ({dados['estado']}; testada {dados['testada']}; "
            f"aceita de {ferr[nome].get('aceita_de') or '?'} a {ferr[nome].get('aceita_ate') or 'a mais nova'})")
    return sorted(nome for nome, dados in julgadas.items() if dados["impede"])


def instalar_no_windows_ou_mac() -> None:
    """Os passos do Windows e do macOS, na ordem em que sempre rodaram. Um passo obrigatório que falha chama `sys.exit(1)`."""
    log(f"Sistema operacional detectado: {OS_NAME}")

    cronometrar("PHP", ensure_php)

    cli = cronometrar("MariaDB", ensure_mariadb_installed)
    if not cronometrar("serviço do MariaDB", ensure_mariadb_running, cli):
        log("Não foi possível subir o MariaDB. Verifique a instalação e rode o instalador de novo.")
        sys.exit(1)
    cronometrar("root do MariaDB", ensure_root_no_password, cli)
    cronometrar("banco (os três .sql)", apply_sql_files, cli)

    cronometrar("venv da CobaiaAPI", setup_cobaia_api)
    cronometrar("AgenteCore (venv, Chromium, Ollama e modelo)", setup_agente_core)

    log("")
    log("Instalação concluída. Para rodar o site, use:")
    log("  Windows (clique duplo ou terminal):  run.cmd")
    log("  Linux/macOS:                          ./run.sh")


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) função nova `codigo_de_saida`.
# ! Motivo: item estacionado da revisão do pacote I2: o ponto de entrada provisório devolvia 1 para qualquer `SystemExit`
# vindo de um passo, inclusive `sys.exit(0)` e `sys.exit()`, que são saída sem erro; uma instalação que terminasse assim
# sairia com código de erro.
def codigo_de_saida(e: SystemExit) -> int:
    """O código com que um `sys.exit` de dentro de um passo termina o instalador: `sys.exit()` e `sys.exit(0)` são saída sem
    erro (0); um número é ele mesmo; um texto (`sys.exit("mensagem")`) é erro (1)."""
    if e.code is None:
        return 0
    if isinstance(e.code, int):
        return e.code
    return 1


def instalar_e_relatar_no_linux(info: dict, reproduzir: bool) -> int:
    """Roda os passos do Linux, transforma a falha de um passo em mensagem e código de saída, e confere as versões no fim."""
    from instalador import ferramentas, versoes
    if info["suporte"] == "melhor_esforco":
        if info["familia"] == "dnf":
            log("Aviso: o Fedora entra como melhor esforço: o instalador garante o site e a API; o navegador do agente "
                "depende de bibliotecas que ele não instala aqui.")
        else:
            log("Aviso: esta distribuição não está entre as testadas (Ubuntu 22.04, 24.04 e 26.04; Debian 12 e 13); "
                "o instalador segue pelo apt, como melhor esforço.")
    ferr = versoes.carregar()
    try:
        instalar_no_linux(info, ferr)
    except ferramentas.Falha as e:
        log("")
        log(f"Instalação interrompida: {e}")
        return 1
    except SystemExit as e:
        # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) captura do `SystemExit` dos passos de Linux em `instalar_e_relatar_no_linux`.
        # ! Motivo: `apply_sql_files` e `setup_cobaia_api` chamam `sys.exit` quando falham; sem esta captura o instalador saía sem a
        # linha "Instalação interrompida".
        codigo = codigo_de_saida(e)
        if codigo == 0:
            log("Instalação encerrada por um passo do instalador, sem erro.")
            return 0
        log("")
        log("Instalação interrompida: um passo do instalador parou; a mensagem dele está logo acima.")
        return codigo
    impedidas = relatar_versoes(ferr, reproduzir)
    if impedidas:
        log(f"Instalação interrompida: a versão de {', '.join(impedidas)} impede seguir (veja a lista acima e o versoes.json).")
        return 1
    log("")
    log("Instalação concluída. Para rodar o site: ./run.sh")
    log("Para conferir a instalação: ./install.sh --conferir")
    return 0


def _argumentos(argv: list[str] | None) -> argparse.Namespace:
    """`argv=None` quer dizer "sem argumentos", e não "leia a linha de comando": o `Cobaia.py` chama `install.main()` e os
    argumentos do `Cobaia.exe` não são do instalador."""
    from instalador import registro
    ap = argparse.ArgumentParser(prog="install.py", description=USO, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--conferir", action="store_true", help="roda a prova da instalação em vez de instalar")
    ap.add_argument("--ate", choices=registro.NIVEIS, default="N4", help="último nível da prova (com --conferir)")
    ap.add_argument("--reproduzir", action="store_true", help="exige a versão exata nas ferramentas que afetam as medidas")
    return ap.parse_args([] if argv is None else argv)


def main(argv: list[str] | None = None) -> int:
    """Instala (sem argumento) ou roda a prova (`--conferir`). Devolve o código de saída; no Windows e no macOS um passo
    obrigatório que falha ainda sai por `sys.exit(1)`, como sempre saiu."""
    args = _argumentos(argv)
    from instalador import sistema
    if args.conferir:
        from instalador import conferir
        argumentos = ["--celula", "local", "--saida", str(REPO_ROOT / ".ferramentas" / "prova"), "--ate", args.ate]
        return conferir.main(argumentos + (["--reproduzir"] if args.reproduzir else []))
    info = sistema.detectar()
    log(f"Sistema: {info['nome']} (família {info['familia']}, {info['suporte']})")
    caminho = caminho_para(info)
    if caminho == "nao_suportado":
        # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o caso sem suporte imprime a lista do que instalar à mão e sai com 1.
        # ! Motivo: célula L-F45 (HL3) e decisão 141: fora do `apt` e do `dnf` o instalador antigo rodava `sudo apt-get` ("command not
        # found"); Arch e openSUSE recebem a lista do que instalar à mão, e o instalador sai com 1.
        from instalador import versoes
        for linha in sistema.mensagem_nao_suportado(info, versoes.carregar()).splitlines():
            log(linha)
        return 1
    if caminho == "como_estava" and info["suporte"] == "falta_homebrew":
        # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o macOS sem Homebrew avisa e sai com 1 antes de qualquer passo.
        # ! Motivo: sem o Homebrew o `brew install` morria em `FileNotFoundError`; o lançador antigo dava esta mensagem.
        log("Homebrew não encontrado. Instale em https://brew.sh e rode ./install.sh de novo.")
        return 1
    if caminho != "como_estava" and eh_root():
        log("Rode o instalador como usuário comum, sem `sudo` na frente: ele mesmo chama o sudo nos passos que precisam.")
        log("Como root, as venvs e o navegador ficariam na pasta do root, e a entrada do root do MariaDB passaria no "
            "teste pelo unix_socket sem ser trocada, com o site e a API quebrados para o usuário comum.")
        return 1
    _PASSOS.clear()
    resultado = "interrompida"
    try:
        if caminho == "como_estava":
            if args.reproduzir:
                # ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 4) com `--reproduzir` no Windows ou no
                # macOS, o instalador avisa que a conferência exata das versões só acontece na prova.
                # ! Motivo: o argumento era aceito em silêncio e a instalação terminava em "Instalação concluída" sem conferir
                # versão nenhuma, embora o texto de uso diga que o modo exige a versão exata; a regra de versões no caminho do
                # Windows entra no pacote I4.
                log("Aviso: no Windows e no macOS o --reproduzir ainda não confere as versões durante a instalação; para "
                    "conferir, rode a prova: python install.py --conferir --reproduzir")
            instalar_no_windows_ou_mac()
            codigo = 0
        else:
            codigo = instalar_e_relatar_no_linux(info, args.reproduzir)
        if codigo == 0:
            resultado = "concluida"
        return codigo
    finally:
        gravar_passos(resultado)


if __name__ == "__main__":
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) chamado direto, o arquivo importa a si mesmo pelo nome `install`
    # e roda o `main` desse módulo, com os argumentos da linha de comando.
    # ! Motivo: `instalador/ferramentas.py` faz `import install` (usa `baixar_arquivo`). Rodando como `python install.py`,
    # este arquivo é o módulo `__main__`, e o `import install` de lá carregaria uma segunda cópia dele, com outra lista de
    # passos (`_PASSOS`) e outras funções; assim só existe uma.
    import install
    sys.exit(install.main(sys.argv[1:]))
