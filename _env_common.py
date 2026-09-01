# ! Alteração de IA - Revisar
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


def php_extension_flags(php_path: str) -> list[str]:
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


# --------------------------------------------------------------------------
# MariaDB
# --------------------------------------------------------------------------

def find_mysql_cli() -> str | None:
    found = which_any("mariadb", "mysql")
    if found:
        return found
    if OS_NAME == "Windows":
        return find_by_glob(
            r"C:\Program Files\MariaDB*\bin\mariadb.exe",
            r"C:\Program Files\MariaDB*\bin\mysql.exe",
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
        )
    return None


def find_mariadb_datadir_config() -> str | None:
    if OS_NAME == "Windows":
        return find_by_glob(r"C:\Program Files\MariaDB*\data\my.ini")
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


def ensure_mariadb_running(cli: str) -> bool:
    """Garante que existe um mariadbd/mysqld respondendo em localhost:3306.
    Tenta, em ordem: (1) já está rodando, (2) serviço do SO (systemd/brew
    services no Linux/macOS — não aplicável no Windows, ver módulo docstring),
    (3) inicia o binário do servidor diretamente como subprocesso (sempre o
    caminho usado no Windows, já que winget não registra serviço)."""
    global _mariadbd_proc

    if _can_connect(cli):
        return True

    if OS_NAME == "Linux":
        run(["sudo", "systemctl", "start", "mariadb"])
        if wait_for_mariadb(cli, timeout_s=30):
            return True
    elif OS_NAME == "Darwin":
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
    global _mariadbd_proc
    if _mariadbd_proc and _mariadbd_proc.poll() is None:
        _mariadbd_proc.terminate()
