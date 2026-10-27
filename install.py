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
import ctypes
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

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


def caminhos_mariadb_portatil(versao: str, base: Path | None = None) -> dict:
    """! Alteração de IA - Revisar: os caminhos do MariaDB portátil: zip baixado, pasta extraída
    (`mariadb-<versão>-winx64`), `bin`, `mariadb-install-db.exe`, pasta de dados e `my.ini`.
    ! Motivo: `_env_common.find_mysql_cli`, `find_mariadbd_server`, `find_mariadb_admin` e
    `find_mariadb_datadir_config` procuram exatamente nesses lugares (`%LOCALAPPDATA%\\MariaDB\\...`);
    montar os caminhos num lugar só evita que o instalador grave numa pasta que o run.py não acha."""
    if base is None:
        base = Path(os.path.expandvars(r"%LOCALAPPDATA%")) / "MariaDB"
    pasta = base / f"mariadb-{versao}-winx64"
    dados = base / "data"
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
                log(f"  {lidos >> 20} MB" + (f" de {total >> 20} MB" if total else ""))
    return lidos


def instalar_mariadb_portatil(perguntar: bool = True) -> str | None:
    """! Alteração de IA - Revisar: instala o MariaDB sem administrador: consulta a API de downloads
    (série MARIADB_SERIE), pergunta antes de baixar (a menos de `COBAIA_MARIADB_PORTATIL=1`), baixa
    o zip oficial em `%LOCALAPPDATA%\\MariaDB\\download`, confere o SHA-256 publicado, extrai em
    `%LOCALAPPDATA%\\MariaDB` e cria a pasta de dados com `mariadb-install-db.exe --datadir ... --port=3306`
    (root sem senha). Devolve o cliente achado por `find_mysql_cli`, ou None com a causa no log.
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
