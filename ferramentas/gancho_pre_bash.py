# ! Alteração de IA - Revisar: hook PreToolUse novo (21/09/2026), em Python, que reescreve comandos Bash sabidamente
# verbosos (`testar_fase3*.py`, `avaliar_fase3*.py`, `rodar_*.ps1`, `git diff`) acrescentando o filtro
# `ferramentas/resumir_saida.py`; qualquer outro comando passa intacto.
# ! Motivo: é o exemplo da documentação oficial de custos do Claude Code ("PreToolUse que filtra saída de teste"),
# adaptado para Windows sem `jq`/bash: o hook lê o JSON do stdin, e só devolve `updatedInput` quando o comando
# casa com a lista; nunca altera arquivo do repositório e nunca nega comando.
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# só EXECUÇÕES (python … testar_fase3*.py / avaliar_fase3*.py, powershell … rodar_*.ps1, git diff): um grep ou sed
# que só cite esses nomes não pode ser resumido — em 21/09/2026 o padrão antigo escondeu as linhas de um grep
VERBOSOS = re.compile(r"(python(\.exe)?\s+[^|;&]*?(testar_fase3\w*|avaliar_fase3\w*)\.py|"
                      r"powershell[^|;&]*?rodar_\w+\.ps1|\bgit diff\b)")
FILTRO = "resumir_saida.py"


def main() -> int:
    try:
        entrada = json.load(sys.stdin)
    except Exception:
        return 0
    if entrada.get("tool_name") != "Bash":
        return 0
    comando = (entrada.get("tool_input") or {}).get("command") or ""
    if not VERBOSOS.search(comando) or FILTRO in comando or "run_in_background" in comando:
        return 0
    raiz = Path(__file__).resolve().parent
    filtro = (raiz / FILTRO).as_posix()
    novo = f"{{ {comando} ; }} 2>&1 | python \"{filtro}\" --cabeca 5 --cauda 40"
    saida = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "saida longa filtrada por ferramentas/resumir_saida.py (economia de tokens)",
            "updatedInput": {**(entrada.get("tool_input") or {}), "command": novo},
        }
    }
    # ensure_ascii=True: o Claude Code lê o stdout do hook na codepage do console (cp1252 nesta máquina) e um
    # acento no JSON viraria caractere inválido; o texto do motivo fica em ASCII puro.
    print(json.dumps(saida, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
