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
from pathlib import Path

from _env_common import (
    AGENTE_CORE,
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


def comando_api(venv_dir: Path, so: str = OS_NAME) -> list[str]:
    """! Alteração de IA - Revisar: (26/10/2026) a CobaiaAPI sobe por `<venv>\\Scripts\\python.exe -m uvicorn`,
    não pelo lançador `uvicorn.exe` da venv.
    ! Motivo: na máquina-alvo i5 a venv da CobaiaAPI tinha sido criada em outra pasta de usuário
    (`C:\\Users\\EricDerre\\...`) e os lançadores `.exe` dela (uvicorn.exe, pip.exe) saíam com código 1 sem
    mensagem, porque carregam dentro deles o caminho antigo do python.exe; start_services só via a porta
    8000 nunca responder e não dizia por quê. O python.exe da venv lê o `pyvenv.cfg` e continua funcionando,
    e `-m uvicorn` chega ao mesmo servidor com os mesmos argumentos."""
    python_venv = venv_dir / ("Scripts/python.exe" if so == "Windows" else "bin/python")
    return [str(python_venv), "-m", "uvicorn", "app.main:app", "--port", str(API_PORT)]


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
    # ! Alteração de IA - Revisar: (26/10/2026) confere o python.exe da venv e sobe a API por comando_api().
    # ! Motivo: ver comando_api(); conferir o uvicorn.exe deixava passar uma venv cujo lançador não roda.
    comando = comando_api(venv_dir)
    if not Path(comando[0]).exists():
        log(f"{comando[0]} não encontrado. Rode install.ps1/install.sh primeiro "
            "(ou implemente a CobaiaAPI se ainda não existe).")
        sys.exit(1)

    front_proc = subprocess.Popen([
        php, "-S", f"localhost:{FRONT_PORT}", "-t", str(COBAIA_FRONT),
        *php_extension_flags(php),
    ])
    api_proc = subprocess.Popen(comando, cwd=str(COBAIA_API))
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


# ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) o hub central passa a subir junto com o site e a API: `HUB_PORT`,
# `comando_do_hub` (o Python da venv do AgenteCore rodando `Programacao/AgenteCore/experimentos/hub.py --sem-abrir --porta 8765 --pelo-exe`),
# `start_hub` (lança o processo, ou devolve None e avisa quando a venv ou o `hub.py` não existem) e `wait_for_port`; `wait_and_cleanup`
# passou a aceitar outros processos depois do site e da API e a encerrá-los junto; o `main` deste arquivo também sobe o hub e diz o endereço.
# ! Motivo: o Eric pediu que o hub seja a central de tudo, aberta quando o `.exe` roda, de onde se rodam os testes e se veem as métricas. O
# hub roda como processo à parte, com o Python da venv do AgenteCore (que o `install.py` cria e que tem o Playwright), porque o `.exe` só
# orquestra processos e não carrega o código do agente dentro dele. Se o hub cair sozinho, o site e a API continuam: só a queda de um dos
# dois encerra tudo, como antes. `--pelo-exe` diz ao hub que o site e a API já estão no ar e libera o botão de rodar os cenários.
HUB_PORT = 8765


def comando_do_hub(agente: Path = AGENTE_CORE, so: str = OS_NAME) -> list[str] | None:
    """O comando que sobe o hub, ou None quando a venv do AgenteCore ou o `hub.py` ainda não existem."""
    python_venv = agente / ".venv" / ("Scripts/python.exe" if so == "Windows" else "bin/python")
    script = agente / "experimentos" / "hub.py"
    if not python_venv.exists() or not script.exists():
        return None
    return [str(python_venv), str(script), "--sem-abrir", "--porta", str(HUB_PORT), "--pelo-exe"]


def start_hub(agente: Path = AGENTE_CORE) -> subprocess.Popen | None:
    """Sobe o hub central como processo à parte; None (com aviso) quando não há como."""
    comando = comando_do_hub(agente)
    if comando is None:
        log("Hub central não iniciado: a venv do AgenteCore ou o hub.py não foram encontrados (rode o instalador).")
        return None
    return subprocess.Popen(comando, cwd=str(agente / "experimentos"))


def wait_for_port(port: int, timeout_s: int = 30) -> bool:
    """Espera uma porta desta máquina aceitar conexão."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if _port_responds(port):
            return True
        time.sleep(0.5)
    return False


def wait_and_cleanup(front_proc: subprocess.Popen, api_proc: subprocess.Popen, *outros) -> None:
    """Bloqueia até Ctrl+C (ou o site ou a API cair sozinho), depois encerra
    tudo de forma limpa, inclusive os outros processos passados (o hub)."""
    try:
        while True:
            time.sleep(1)
            if front_proc.poll() is not None or api_proc.poll() is not None:
                break
    except KeyboardInterrupt:
        pass
    finally:
        for proc in (front_proc, api_proc, *outros):
            if proc is not None and proc.poll() is None:
                proc.terminate()
        stop_managed_mariadbd()


def main() -> None:
    front_proc, api_proc = start_services()
    log(f"CobaiaFront: http://localhost:{FRONT_PORT}")
    log(f"CobaiaAPI:   http://localhost:{API_PORT}/docs")
    hub_proc = start_hub()
    if hub_proc is not None:
        log(f"Hub central: http://127.0.0.1:{HUB_PORT}/")
    log("Ctrl+C encerra tudo.")
    wait_and_cleanup(front_proc, api_proc, hub_proc)


if __name__ == "__main__":
    main()
