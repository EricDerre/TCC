#!/usr/bin/env bash
# ! Alteração de IA - Revisar
# Bootstrap fino (Linux/macOS): garante que existe Python 3, depois delega tudo pra install.py.
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
