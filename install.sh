#!/usr/bin/env bash
# ! Alteração de IA - Revisar: bootstrap fino (Linux/macOS) que só garante a existência
# de um Python 3 e então delega toda a instalação para install.py.
# ! Motivo: mesmo papel do install.ps1 no Windows — install.py concentra a lógica real,
# mas precisa de um Python que pode não existir na máquina. Manter aqui só essa checagem
# evita duplicar a instalação em três linguagens de shell diferentes.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "[install.sh] Python 3 não encontrado -- instalando..."
    if [ "$(uname)" = "Darwin" ]; then
        if ! command -v brew &>/dev/null; then
            echo "[install.sh] Homebrew não encontrado. Instale em https://brew.sh e rode ./install.sh de novo."
            exit 1
        fi
        brew install python3
    elif command -v apt-get &>/dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-venv python3-pip
    else
        echo "[install.sh] Gerenciador de pacotes não reconhecido. Instale Python 3 manualmente e rode ./install.sh de novo."
        exit 1
    fi
    PY=python3
fi

"$PY" "$SCRIPT_DIR/install.py"
