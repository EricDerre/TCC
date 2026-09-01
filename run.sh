#!/usr/bin/env bash
# ! Alteração de IA - Revisar: bootstrap fino (Linux/macOS) que localiza o Python e
# chama run.py, sem nenhuma lógica de subida de serviço aqui.
# ! Motivo: mesmo papel do run.ps1 no Windows — a orquestração dos três processos
# (MariaDB, php -S e uvicorn) e o encerramento conjunto ficam só no run.py, para não
# duplicar a parte mais frágil do projeto em duas linguagens de shell.
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
