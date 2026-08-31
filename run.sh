#!/usr/bin/env bash
# ! Alteração de IA - Revisar
# Bootstrap fino (Linux/macOS) para run.py.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "[run.sh] Python não encontrado. Rode ./install.sh primeiro."
    exit 1
fi

"$PY" "$SCRIPT_DIR/run.py"
