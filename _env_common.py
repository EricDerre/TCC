# ! Alteração de IA - Revisar
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) a docstring abaixo ganhou o parágrafo final, sobre o
# caminho do Linux.
# ! Motivo: ela dizia que no Linux o serviço do MariaDB tinha como plano B o servidor iniciado como processo direto e que esse
# caminho não tinha sido testado; as células de 18 e 19/11/2026 testaram, e `ensure_mariadb_running` deixou de ter esse plano B
# no Linux. É o primeiro texto que quem abre o arquivo lê.
"""
Helpers compartilhados por install.py e run.py.

Achado empírico importante (testado nesta máquina Windows, sem privilégios de
administrador): `winget install MariaDB.Server` instala os binários e já
inicializa o data dir (root sem senha, igual ao que connect.php espera), mas
NÃO registra nem inicia um Windows Service — o instalador de serviço do MSI
exige elevação que a sessão não tinha. Por isso, no Windows, o MariaDB é
sempre gerenciado como um subprocesso comum (igual ao `php -S` e ao
`uvicorn`), nunca via `Get-Service`/`net start`. Em Linux/macOS, os pacotes
via apt/brew normalmente registram e sobem um serviço (systemd/brew services)
sozinhos — esse caminho não foi testado ao vivo nesta sessão (só a máquina
Windows atual estava disponível), então mantém o fallback de systemctl/brew
services, mas com o mesmo "iniciar como processo direto" como plano B caso o
serviço não suba.

Desde 19/11/2026 (pacote I3 do instalador único) o caminho do Linux está testado em células do WSL (Ubuntu 22.04, 24.04
e 26.04, Debian 12 e 13, Fedora 45): lá o serviço sobe pelo systemd ou pelo `service` (`subir_servico_no_linux`), e o
plano B do processo direto não existe mais, porque o `mariadbd` não consegue escrever na pasta de dados do pacote como
usuário comum. No macOS, ainda sem teste, vale o que está escrito acima.
"""
import glob
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Console do Windows às vezes usa uma codepage legada (ex.: cp1252/cp850) que
# não imprime corretamente acentos em português — força UTF-8 na saída para
# os logs ficarem legíveis em qualquer terminal.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

if getattr(sys, "frozen", False):
    # Rodando como .exe compilado (PyInstaller onefile): __file__ apontaria
    # pra a pasta TEMPORÁRIA de extração (sys._MEIPASS), não pra onde o .exe
    # realmente está — confirmado ao vivo (o instalador procurava os SQL/PHP
    # dentro de %TEMP%\_MEIxxxxx\Programacao\... e não achava nada).
    # sys.executable, nesse caso, é o caminho real do .exe.
    REPO_ROOT = Path(sys.executable).resolve().parent
else:
    REPO_ROOT = Path(__file__).resolve().parent
COBAIA_FRONT = REPO_ROOT / "Programacao" / "CobaiaFront"
COBAIA_API = REPO_ROOT / "Programacao" / "CobaiaAPI"
AGENTE_CORE = REPO_ROOT / "Programacao" / "AgenteCore"
DB_NAME = "ti93phpdb01"
# ! Alteração de IA - Revisar: (07/11/2026, ficha 55) a pasta de dados do MariaDB portátil passa a ficar dentro do projeto, em
# `.mariadb/data` (fora do git), e não mais em `%LOCALAPPDATA%\MariaDB\data`; os binários continuam em `%LOCALAPPDATA%\MariaDB`.
# ! Motivo: o aplicativo Claude é um pacote MSIX: o que um processo dele grava em AppData\Local vai para a pasta privada do pacote,
# e o que ele lê é a mistura das duas camadas (a privada por cima da real). O servidor subido de dentro do app lia o dicionário do
# InnoDB (ibdata1, redo, undo) da cópia privada e as tabelas (.frm/.ibd) da cópia real, respondia `ERROR 1932 (42S02): Table
# 'ti93phpdb01.tbprodutos' doesn't exist in engine` em todas as tabelas e, numa partida em 07/11/2026, apagou os .ibd da cópia
# real. A pasta do projeto não é virtualizada: a janela do Eric e o app enxergam a mesma pasta de dados.
DATADIR_DO_PROJETO = REPO_ROOT / ".mariadb" / "data"
MY_INI_DO_PROJETO = DATADIR_DO_PROJETO / "my.ini"
OS_NAME = platform.system()  # "Windows" | "Linux" | "Darwin"
IS_FROZEN = getattr(sys, "frozen", False)

_mariadbd_proc: subprocess.Popen | None = None


def log(msg: str) -> None:
    print(f"[cobaia] {msg}", flush=True)


def run(cmd, **kwargs) -> subprocess.CompletedProcess:
    log("$ " + " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, **kwargs)


def which_any(*names: str) -> str | None:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def find_by_glob(*patterns: str) -> str | None:
    """Procura um executável em locais de instalação conhecidos, sem depender
    do PATH ter sido atualizado no processo atual (comum logo após um
    `winget install` na mesma sessão de shell — confirmado nesta máquina)."""
    for pattern in patterns:
        matches = sorted(glob.glob(pattern), reverse=True)  # versão mais alta primeiro
        if matches:
            return matches[0]
    return None


# --------------------------------------------------------------------------
# PHP
# --------------------------------------------------------------------------

def find_php() -> str | None:
    found = which_any("php")
    if found:
        return found
    if OS_NAME == "Windows":
        # Confirmado nesta máquina: winget extrai o zip do PHP em
        # WinGet\Packages do usuário atual — não em C:\tools nem Program Files.
        return find_by_glob(
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\PHP.PHP*\php.exe"),
            r"C:\tools\php*\php.exe",
            r"C:\Program Files\PHP\*\php.exe",
            r"C:\PHP*\php.exe",
        )
    return None


def php_extension_dir(php_path: str) -> Path:
    return Path(php_path).parent / "ext"


def php_extension_flags(php_path: str, so: str | None = None) -> list[str]:
    """Confirmado nesta máquina: o build Windows do PHP tem um extension_dir
    default hardcoded (C:\\php\\ext) que não bate com o caminho real de
    instalação — sem forçar extension_dir explicitamente, as extensões abaixo
    falham a carregar silenciosamente. mbstring é usada por mb_strimwidth()
    em produtos_geral/busca/destaque/por_tipo/produto_detalhes.php — sem ela,
    essas páginas dão Fatal Error (confirmado testando ao vivo).
    output_buffering: cliente/index.php ecoa HTML antes de reserva_cli.php
    incluir admin/acesso_com.php (que só então chama session_start()) — sem
    output_buffering, isso vira "headers already sent" e a sessão do login
    não é retomada, truncando a página logo após a saudação (confirmado
    testando ao vivo). Um php.ini "de verdade" (XAMPP etc.) normalmente já
    vem com output_buffering ligado por padrão, o que mascara esse bug
    pré-existente do código — aqui ligamos explicitamente pra reproduzir esse
    mesmo comportamento sem precisar de um php.ini."""
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) no Linux a função devolve só o
    # `output_buffering`; `so=` troca o sistema só nos testes. No Windows e no macOS a lista é a de sempre.
    # ! Motivo: célula L-U2404 de 18/11/2026 (suspeita HL4): com `-d extension_dir=/usr/bin/ext -d extension=mysqli ...` o
    # `php -S` do Ubuntu subia com `mysqli: NAO carregada` e o site respondia `HTTP 500`, `Class "mysqli" not found in
    # .../conn/connect.php:13`; a pasta `ext` ao lado do executável só existe no PHP do Windows. No Linux o pacote da
    # distribuição já carrega mysqli, pdo_mysql e mbstring pelos arquivos de `conf.d`. Provado nas células de 19/11/2026
    # (Ubuntu 22.04, 24.04 e 26.04, Debian 12 e 13, Fedora 45), quando a regra morava em `instalador/servicos.py`, um
    # módulo provisório que trocava esta função só na memória porque este arquivo não podia mudar antes da corrida 28b.
    if (so or OS_NAME) == "Linux":
        return ["-d", "output_buffering=4096"]
    ext_dir = php_extension_dir(php_path)
    return [
        "-d", f"extension_dir={ext_dir}",
        "-d", "extension=mysqli",
        "-d", "extension=pdo_mysql",
        "-d", "extension=mbstring",
        "-d", "output_buffering=4096",
    ]


# --------------------------------------------------------------------------
# Python "de verdade" (só usado a partir de um .exe compilado)
# --------------------------------------------------------------------------

def find_or_install_real_python() -> str:
    """Retorna um python.exe de instalação normal, nunca o interpretador
    embutido no .exe compilado. Necessário só pra CRIAR o venv da
    CobaiaAPI — confirmado ao vivo que `venv.EnvBuilder` roda de dentro de
    um binário frozen do PyInstaller falha (o interpretador embutido não
    tem o layout de uma instalação Python normal: faltam
    venvlauncher.exe/venvwlauncher.exe no caminho relativo esperado).
    No fluxo normal (`python install.py`), isso nunca é chamado —
    sys.executable já É um Python de verdade nesse caso."""
    for cmd in ("python", "python3", "py"):
        found = which_any(cmd)
        if found:
            return found

    log("Python (instalação normal) não encontrado — instalando "
        "(necessário só pra criar o venv da CobaiaAPI)...")
    if OS_NAME == "Windows":
        run([
            "winget", "install", "--id", "Python.Python.3.14", "-e",
            "--accept-package-agreements", "--accept-source-agreements",
        ])
        found = find_by_glob(
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python\Python3*\python.exe"),
            r"C:\Program Files\Python3*\python.exe",
            r"C:\Python3*\python.exe",
        )
    elif OS_NAME == "Linux":
        run(["sudo", "apt-get", "update"])
        run(["sudo", "apt-get", "install", "-y", "python3", "python3-venv", "python3-pip"])
        found = which_any("python3")
    elif OS_NAME == "Darwin":
        run(["brew", "install", "python3"])
        found = which_any("python3")
    else:
        found = None

    if not found:
        log("Não foi possível localizar/instalar um Python de verdade. "
            "Instale manualmente (python.org) e rode o instalador de novo.")
        sys.exit(1)
    return found


# --------------------------------------------------------------------------
# Ollama (runtime do LLM local usado pelo AgenteCore)
# --------------------------------------------------------------------------

def find_ollama() -> str | None:
    """! Alteração de IA - Revisar: localiza o executável do Ollama.
    ! Motivo: mesma situação já confirmada com PHP e MariaDB — logo após um
    `winget install` o PATH do processo atual ainda não foi atualizado, então
    depender só do PATH faria o instalador achar que não instalou nada. Os
    caminhos de instalação do Windows não foram verificados ao vivo (o Ollama
    ainda não foi instalado nesta máquina), por isso há mais de um padrão."""
    found = which_any("ollama")
    if found:
        return found
    if OS_NAME == "Windows":
        return find_by_glob(
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Ollama.Ollama*\ollama.exe"),
            r"C:\Program Files\Ollama\ollama.exe",
        )
    return None


def playwright_chromium_instalado() -> bool:
    """! Alteração de IA - Revisar: verifica se o Chromium do Playwright já foi baixado,
    olhando o diretório de cache do próprio Playwright.
    ! Motivo: evita gastar rede e tempo repetindo um download de centenas de MB a cada
    execução do instalador. O `playwright install` já é idempotente por conta própria,
    mas checar antes evita até o custo de subir o processo."""
    if OS_NAME == "Windows":
        base = os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright")
    elif OS_NAME == "Darwin":
        base = os.path.expanduser("~/Library/Caches/ms-playwright")
    else:
        base = os.path.expanduser("~/.cache/ms-playwright")
    return bool(glob.glob(os.path.join(base, "chromium-*")))


def modelo_llm_ja_baixado(ollama: str, modelo: str) -> bool:
    """! Alteração de IA - Revisar: consulta `ollama list` para saber se o modelo já
    está na máquina antes de mandar baixar.
    ! Motivo: o modelo é o download mais pesado do projeto (de 1 GB a quase 5 GB
    conforme o porte). Sem essa checagem, cada execução do instalador dispararia um
    `ollama pull` — que até reaproveita camadas já baixadas, mas ainda assim faz
    tráfego de rede e não deixa claro no log que nada precisava ser baixado."""
    resultado = subprocess.run([ollama, "list"], capture_output=True, text=True)
    if resultado.returncode != 0:
        return False
    # ! Alteração de IA - Revisar: compara com o nome exato da primeira coluna de cada linha,
    # em vez de procurar a string em qualquer lugar da saída.
    # ! Motivo: `modelo in stdout` casava por substring — "qwen2.5:7b" era dado como baixado
    # se só "qwen2.5:7b-instruct-q8_0" existisse na máquina, e o `ollama pull` do modelo
    # certo nunca acontecia. Um nome sem tag ("qwen2.5-coder") aparece na lista como
    # "qwen2.5-coder:latest", por isso a normalização.
    alvo = modelo if ":" in modelo else f"{modelo}:latest"
    for linha in resultado.stdout.splitlines()[1:]:  # a primeira linha é o cabeçalho
        partes = linha.split()
        if partes and partes[0] == alvo:
            return True
    return False


# --------------------------------------------------------------------------
# MariaDB
# --------------------------------------------------------------------------

def find_mysql_cli() -> str | None:
    found = which_any("mariadb", "mysql")
    if found:
        return found
    if OS_NAME == "Windows":
        # ! Alteração de IA - Revisar: (26/10/2026, Fase 4, P0) também procura o MariaDB portátil (zip oficial
        # extraído em %LOCALAPPDATA%\MariaDB\mariadb-<versão>-winx64\), aqui e nas três funções abaixo.
        # ! Motivo: na máquina corporativa não há administrador para o MSI do winget (MariaDB.Server) e o
        # servidor roda como processo comum a partir do zip, que é o mesmo caminho (3) de ensure_mariadb_running;
        # sem o glob, run.py e install.py diziam "MariaDB não encontrado" com o servidor presente.
        return find_by_glob(
            r"C:\Program Files\MariaDB*\bin\mariadb.exe",
            r"C:\Program Files\MariaDB*\bin\mysql.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\MariaDB\mariadb-*-winx64\bin\mariadb.exe"),
        )
    return None


def find_mariadbd_server() -> str | None:
    """Binário do servidor em si (não o cliente CLI)."""
    found = which_any("mariadbd", "mysqld")
    if found:
        return found
    if OS_NAME == "Windows":
        return find_by_glob(
            r"C:\Program Files\MariaDB*\bin\mariadbd.exe",
            r"C:\Program Files\MariaDB*\bin\mysqld.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\MariaDB\mariadb-*-winx64\bin\mariadbd.exe"),
        )
    return None


def find_mariadb_admin() -> str | None:
    """! Alteração de IA - Revisar: localiza o utilitário de administração do servidor
    (mariadb-admin/mysqladmin), usado só para desligar o banco de forma limpa.
    ! Motivo: ver stop_managed_mariadbd(). Mesma busca por caminho conhecido que os
    demais binários, porque o PATH pode não incluir a pasta bin do MariaDB no Windows
    (confirmado nesta máquina que mariadb-admin.exe existe ao lado do mariadbd.exe)."""
    found = which_any("mariadb-admin", "mysqladmin")
    if found:
        return found
    if OS_NAME == "Windows":
        return find_by_glob(
            r"C:\Program Files\MariaDB*\bin\mariadb-admin.exe",
            r"C:\Program Files\MariaDB*\bin\mysqladmin.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\MariaDB\mariadb-*-winx64\bin\mariadb-admin.exe"),
        )
    return None


def find_mariadb_datadir_config(raiz: Path | None = None) -> str | None:
    # ! Alteração de IA - Revisar: (07/11/2026, ficha 55) o my.ini de `.mariadb/data` na raiz do repositório vem antes dos caminhos
    # antigos; `raiz=` troca a raiz só nos testes.
    # ! Motivo: ver DATADIR_DO_PROJETO. Sem a preferência, a janela do Eric continuaria subindo o servidor com a pasta de AppData e
    # o app com a mistura das duas camadas; com ela, os dois sobem o mesmo servidor sobre a mesma pasta.
    my_ini = (raiz or REPO_ROOT) / ".mariadb" / "data" / "my.ini"
    if my_ini.exists():
        return str(my_ini)
    if OS_NAME == "Windows":
        # ! Alteração de IA - Revisar: (26/10/2026) o my.ini do MariaDB portátil fica na pasta de dados criada por
        # `mariadb-install-db.exe --datadir=%LOCALAPPDATA%\MariaDB\data` (ver a tag em find_mysql_cli).
        # ! Motivo: sem o --defaults-file apontando para esse my.ini, o mariadbd portátil subiria sem saber a pasta
        # de dados e a porta.
        return find_by_glob(
            r"C:\Program Files\MariaDB*\data\my.ini",
            os.path.expandvars(r"%LOCALAPPDATA%\MariaDB\data\my.ini"),
        )
    return None


def _can_connect(cli: str) -> bool:
    result = subprocess.run([cli, "-u", "root", "-e", "SELECT 1;"], capture_output=True)
    return result.returncode == 0


def wait_for_mariadb(cli: str, timeout_s: int = 60) -> bool:
    log("Aguardando o MariaDB responder...")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if _can_connect(cli):
            log("MariaDB respondendo.")
            return True
        time.sleep(2)
    return False


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) funções novas `banco_no_ar`, `systemd_no_ar`,
# `prefixo_de_root`, `comando_de_subir_o_banco` e `subir_servico_no_linux`, trazidas de `instalador/ferramentas.py`.
# ! Motivo: células L-U2404 e L-U2404-SS de 18 e 19/11/2026. Suspeita HL12: `ensure_mariadb_running` usava "entrar como root
# sem senha" como teste de "o banco está no ar"; no Ubuntu o root só entra pelo unix_socket (`ERROR 1698 (28000): Access
# denied for user 'root'@'localhost'`), então o instalador esperava 30 s, subia um segundo `mariadbd` como usuário comum,
# esperava 45 s e parava em "Não foi possível subir o MariaDB" com o serviço no ar. Suspeita HL7: sem o systemd, `sudo
# systemctl enable --now mariadb` responde "System has not been booted with systemd as init system (PID 1). Can't operate.",
# e o servidor direto como usuário comum dá `Can't create/write to file './ddl_recovery.log' (Errcode: 13 "Permission
# denied")`; `sudo service mariadb start` sobe. Enquanto este arquivo não podia mudar (até a corrida 28b ser lida), as
# funções moravam em `instalador/ferramentas.py`, e quem chama `ensure_mariadb_running` direto (o `run.py`, o
# `restaurar_banco.py` e a prova, `instalador/conferir.py`) continuava sem ligar o banco num WSL sem systemd reiniciado.
def banco_no_ar(cli: str) -> bool:
    """O servidor responde? Entrar como root sem senha prova que sim. Quando a entrada é recusada, o `mariadb-admin ping`
    ainda sai com código 0 se o servidor está no ar (ele conta a recusa como resposta do servidor) e com 1 se não está."""
    if _can_connect(cli):
        return True
    admin = find_mariadb_admin()
    if not admin:
        return False
    return subprocess.run([admin, "ping"], capture_output=True, check=False).returncode == 0


def systemd_no_ar() -> bool:
    """O systemd é quem sobe os serviços nesta máquina? No WSL e em contêiner ele pode estar desligado."""
    return Path("/run/systemd/system").is_dir()


def prefixo_de_root(uid: int | None = None, tem_sudo: bool | None = None) -> list[str] | None:
    """O começo dos comandos que precisam de root: nada para quem já é root, `sudo` para os outros, None se não há sudo."""
    if uid is None:
        uid = os.geteuid() if hasattr(os, "geteuid") else 0
    if uid == 0:
        return []
    if tem_sudo is None:
        tem_sudo = bool(shutil.which("sudo"))
    return ["sudo"] if tem_sudo else None


def comando_de_subir_o_banco(com_systemd: bool, prefixo: list[str]) -> list[str]:
    """Com o systemd, o serviço é ligado e marcado para subir no boot; sem ele, só ligado pelo `service`."""
    if com_systemd:
        return [*prefixo, "systemctl", "enable", "--now", "mariadb"]
    return [*prefixo, "service", "mariadb", "start"]


def subir_servico_no_linux(cli: str, espera_s: int = 40) -> bool:
    """Liga o serviço do MariaDB no Linux, pelo systemd ou pelo `service`, e espera o servidor responder."""
    if banco_no_ar(cli):
        return True
    prefixo = prefixo_de_root()
    if prefixo is None:
        log("Ligar o serviço do MariaDB precisa do sudo, e esta máquina não tem. Instale o sudo e rode de novo, como "
            "usuário comum.")
        return False
    comando = comando_de_subir_o_banco(systemd_no_ar(), prefixo)
    log("O MariaDB não está no ar; ligando o serviço...")
    run(comando)
    limite = time.time() + espera_s
    while time.time() < limite:
        if banco_no_ar(cli):
            return True
        time.sleep(2)
    log(f"O MariaDB não respondeu depois de `{' '.join(comando)}`; a mensagem do comando está logo acima.")
    return False


def ensure_mariadb_running(cli: str) -> bool:
    """Garante que existe um mariadbd/mysqld respondendo em localhost:3306.
    Tenta, em ordem: (1) já está rodando, (2) serviço do SO (systemd ou `service` no Linux, brew
    services no macOS; não aplicável no Windows, ver módulo docstring),
    (3) inicia o binário do servidor diretamente como subprocesso (sempre o
    caminho usado no Windows, já que winget não registra serviço; no Linux esse passo não existe mais)."""
    global _mariadbd_proc

    if _can_connect(cli):
        return True

    if OS_NAME == "Linux":
        # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) no Linux quem liga o banco é `subir_servico_no_linux`, e a
        # função volta daqui: sem `sudo systemctl start mariadb` fixo e sem o servidor direto como plano B.
        # ! Motivo: ver a tag de `banco_no_ar`, logo acima (HL12 e HL7): o teste antigo de "no ar" confundia acesso
        # recusado com banco desligado, o `systemctl` não opera sem o systemd, e o `mariadbd` direto como usuário comum
        # não consegue escrever na pasta de dados do pacote (`/var/lib/mysql`).
        return subir_servico_no_linux(cli)
    if OS_NAME == "Darwin":
        run(["brew", "services", "start", "mariadb"])
        if wait_for_mariadb(cli, timeout_s=30):
            return True

    # Fallback (sempre usado no Windows): sobe o servidor como processo comum.
    server_bin = find_mariadbd_server()
    if not server_bin:
        log("Binário do servidor MariaDB (mariadbd/mysqld) não encontrado.")
        return False

    log(f"Nenhum serviço de banco ativo — iniciando {server_bin} como processo...")
    cmd = [server_bin]
    ini = find_mariadb_datadir_config()
    if ini:
        cmd.append(f"--defaults-file={ini}")
    _mariadbd_proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return wait_for_mariadb(cli, timeout_s=45)


def ensure_root_no_password(cli: str) -> bool:
    """connect.php (intocado) espera root sem senha. Confirmado nesta máquina
    que o winget MariaDB.Server já deixa root sem senha por padrão — mas
    pacotes apt do Linux costumam usar auth_socket/unix_socket, então esse
    fallback continua necessário lá (não testado ao vivo)."""
    if _can_connect(cli):
        return True

    if OS_NAME == "Linux":
        log("root não acessível sem senha via TCP — tentando corrigir via socket local (sudo)...")
        fix_sql = (
            "ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD(''); "
            "FLUSH PRIVILEGES;"
        )
        fixed = subprocess.run(["sudo", cli, "-u", "root", "-e", fix_sql], capture_output=True)
        if fixed.returncode == 0 and _can_connect(cli):
            log("root ajustado para sem senha.")
            return True

    log("!! Não foi possível confirmar acesso a root sem senha no MariaDB.")
    log("!! Programacao/CobaiaFront/conn/connect.php (intocado) espera usuário 'root' sem senha.")
    log("!! Ajuste manualmente (ex.: `ALTER USER 'root'@'localhost' IDENTIFIED BY '';`) e rode o instalador de novo.")
    return False


def stop_managed_mariadbd() -> None:
    """! Alteração de IA - Revisar: pede o desligamento pelo protocolo do próprio servidor
    (mariadb-admin shutdown) e só recorre a terminate() se ele não encerrar em 15 s.
    ! Motivo: terminate() sozinho é TerminateProcess no Windows — o servidor morre sem
    gravar o que estava em memória, e na próxima subida o InnoDB entra em recuperação de
    falha (demora mais e enche o log de avisos). Como o run.py/Cobaia.exe sobe e derruba
    o banco a cada uso, isso acontecia em toda execução."""
    global _mariadbd_proc
    if not (_mariadbd_proc and _mariadbd_proc.poll() is None):
        return
    admin = find_mariadb_admin()
    if admin:
        subprocess.run([admin, "-u", "root", "shutdown"], capture_output=True, timeout=30)
        try:
            _mariadbd_proc.wait(timeout=15)
            return
        except subprocess.TimeoutExpired:
            log("MariaDB não encerrou pelo shutdown limpo — forçando.")
    _mariadbd_proc.terminate()
