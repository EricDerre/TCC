#!/usr/bin/env bash
# ! Alteração de IA - Revisar: bootstrap fino (Linux/macOS) que localiza o Python e
# chama run.py, sem nenhuma lógica de subida de serviço aqui.
# ! Motivo: mesmo papel do run.ps1 no Windows - a orquestração dos três processos
# (MariaDB, php -S e uvicorn) e o encerramento conjunto ficam só no run.py, para não
# duplicar a parte mais frágil do projeto em duas linguagens de shell.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I2 do instalador único) prefere o Python que o install.sh trouxe para
# .ferramentas/python e chama `python -m instalador.servicos`, que sobe os mesmos três processos do run.py.
# ! Motivo: célula L-U2404 de 18/11/2026, suspeita HL4 confirmada: o run.py passa ao `php -S` a pasta de extensões do
# Windows e, no Linux, o site respondia `Class "mysqli" not found`. O run.py não pode mudar antes de a corrida 28b ser
# lida; `instalador/servicos.py` troca as opções só na memória e chama o `run.main()`.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) o lançador volta a chamar o `run.py` (a última linha passa de `python -m instalador.servicos` para `python run.py`).
# ! Motivo: as opções do PHP por sistema (no Linux só o `output_buffering`) e a subida do banco sem systemd entraram no `_env_common.py`, que o `run.py` chama; o módulo provisório `instalador/servicos.py` deixou de existir.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PY="$(ls "$SCRIPT_DIR"/.ferramentas/python/*/bin/python3 2>/dev/null | head -n 1 || true)"
if [ -z "$PY" ]; then
    if command -v python3 &>/dev/null; then
        PY=python3
    elif command -v python &>/dev/null; then
        PY=python
    else
        echo "[run.sh] Python não encontrado. Rode ./install.sh primeiro."
        exit 1
    fi
fi

cd "$SCRIPT_DIR"
exec "$PY" "$SCRIPT_DIR/run.py"
