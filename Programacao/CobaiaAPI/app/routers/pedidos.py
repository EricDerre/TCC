# ! Alteração de IA - Revisar: rotas de reserva que gravam na mesma tabela
# tbpedido_reserva e usam o mesmo status inicial 'Em Análise' que o site PHP usa.
# ! Motivo: espelhar exatamente as operações de cliente/registrar_reserva.php e
# cliente/cliente_cancelar.php (que gravam status 'Em Análise' e 'Cancelado') é o
# que faz uma reserva criada pela API aparecer na área do cliente do CobaiaFront —
# é a prova de que o banco é único e compartilhado entre os dois alvos.
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..fault_injection import ErrorFault, apply_fault
from ..models import PedidoReserva, Usuario
from ..schemas import PedidoCreate

router = APIRouter(prefix="/api/pedidos", tags=["pedidos"])


def _to_dict(p: PedidoReserva) -> dict:
    return {
        "id_pedido": p.id_pedido,
        "pessoas": p.pessoas,
        "data_pedido": p.data_pedido.isoformat(),
        "status": p.status,
        "nome": p.cliente.nome,
        "cpf": p.cliente.login_usuario,
    }


@router.get("")
def listar_pedidos(login: str, db: Session = Depends(get_db)):
    """Espelha vw_tbpedidos do CobaiaFront, filtrando por login_usuario (=cpf
    no domínio do CobaiaFront) em vez do id_usuario, pra bater com como
    cliente/index.php identifica o cliente logado."""
    cliente = db.query(Usuario).filter(Usuario.login_usuario == login).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="cliente não encontrado")
    pedidos = db.query(PedidoReserva).filter(PedidoReserva.id_clientes == cliente.id_usuario).all()
    try:
        data = [apply_fault(_to_dict(p), entity="pedido") for p in pedidos]
    except ErrorFault as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return JSONResponse(content=data)


@router.post("", status_code=201)
def criar_pedido(body: PedidoCreate, db: Session = Depends(get_db)):
    """Mesma operação que Programacao/CobaiaFront/cliente/registrar_reserva.php
    faz via SQL direto — mesma tabela, mesmo status inicial."""
    cliente = db.get(Usuario, body.id_clientes)
    if not cliente:
        raise HTTPException(status_code=404, detail="cliente não encontrado")
    pedido = PedidoReserva(
        id_clientes=body.id_clientes,
        pessoas=body.pessoas,
        data_pedido=body.data_pedido,
        status="Em Análise",
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    try:
        data = apply_fault(_to_dict(pedido), entity="pedido")
    except ErrorFault as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return JSONResponse(content=data, status_code=201)


@router.post("/{pedido_id}/cancelar")
def cancelar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """Mesma operação que cliente/cliente_cancelar.php faz via SQL direto."""
    pedido = db.get(PedidoReserva, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="pedido não encontrado")
    pedido.status = "Cancelado"
    db.commit()
    db.refresh(pedido)
    try:
        data = apply_fault(_to_dict(pedido), entity="pedido")
    except ErrorFault as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return JSONResponse(content=data)
