# ! Alteração de IA - Revisar
"""
Estado central de fault injection (viabiliza a metodologia de
Fuzzing/Mutação Dinâmica da documentação do TCC). Inicializado por env var
FAULT_MODE no boot (runs determinísticos), sobrescrevível via
POST /api/admin/fault-mode em runtime.

Uso nas rotas (produtos.py/pedidos.py): monte um dict puro a partir do ORM,
chame apply_fault(dict, entity=...) por último, e retorne via
JSONResponse(content=...) explícito — isso faz o FastAPI pular a validação
de response_model, que senão filtraria/desfaria silenciosamente qualquer
campo alterado pela injeção antes de sair pela rede (response_model continua
declarado nas rotas só pra gerar a doc OpenAPI do contrato "normal").
malformed_json não passa por aqui — é tratado direto na rota, retornando uma
string quebrada via Response(), já que não existe como "dict alterado".
"""
import random
import time
from typing import Any, Optional

from .config import settings

MODES = {
    "normal",
    "error_500",
    "latency",
    "type_drift",
    "field_missing",
    "field_renamed",
    "malformed_json",
}


class FaultState:
    def __init__(
        self,
        mode: str = "normal",
        target_field: Optional[str] = None,
        probability: float = 1.0,
    ):
        self.mode = mode if mode in MODES else "normal"
        self.target_field = target_field
        self.probability = probability


state = FaultState(mode=settings.fault_mode)


class ErrorFault(Exception):
    """Levantada quando o modo error_500 deve disparar — o router converte
    isso num HTTPException 500."""


def _should_apply() -> bool:
    return random.random() < state.probability


def apply_fault(data: dict[str, Any], entity: str) -> dict[str, Any]:
    """Aplica o modo de falha ativo a um dict de resposta já pronto. Chame
    por último, logo antes de devolver a resposta. entity é só um rótulo
    (não usado pra filtrar por enquanto) — mantido pra facilitar modos
    futuros que dependam do tipo de entidade."""
    if state.mode in ("normal", "malformed_json") or not _should_apply():
        return data

    if state.mode == "latency":
        time.sleep(2)
        return data

    if state.mode == "error_500":
        raise ErrorFault(f"fault injection: error_500 em {entity}")

    field = state.target_field
    if field and field in data:
        if state.mode == "type_drift":
            data = {**data, field: str(data[field])}
        elif state.mode == "field_missing":
            data = {k: v for k, v in data.items() if k != field}
        elif state.mode == "field_renamed":
            data = {**data}
            data[f"{field}_v2"] = data.pop(field)

    return data
