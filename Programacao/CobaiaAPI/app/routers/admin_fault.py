# ! Alteração de IA - Revisar
from typing import Optional

from fastapi import APIRouter, Header, HTTPException

from ..config import settings
from ..fault_injection import MODES, state
from ..schemas import FaultModeIn, FaultModeOut

router = APIRouter(prefix="/api/admin", tags=["admin"], include_in_schema=False)


def _check_token(x_admin_token: Optional[str]) -> None:
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=403, detail="token inválido (header X-Admin-Token)")


@router.get("/fault-mode", response_model=FaultModeOut)
def get_fault_mode():
    return FaultModeOut(
        mode=state.mode, target_field=state.target_field, probability=state.probability
    )


@router.post("/fault-mode", response_model=FaultModeOut)
def set_fault_mode(body: FaultModeIn, x_admin_token: Optional[str] = Header(default=None)):
    _check_token(x_admin_token)
    if body.mode not in MODES:
        raise HTTPException(status_code=400, detail=f"modo inválido, use um de: {sorted(MODES)}")
    state.mode = body.mode
    state.target_field = body.target_field
    state.probability = body.probability
    return FaultModeOut(
        mode=state.mode, target_field=state.target_field, probability=state.probability
    )
