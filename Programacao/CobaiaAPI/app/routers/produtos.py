# ! Alteração de IA - Revisar: rotas de produto que montam um dict puro, aplicam a
# injeção de falha por último e devolvem JSONResponse explícito.
# ! Motivo: se a resposta saísse pelo response_model do FastAPI, o Pydantic
# revalidaria e desfaria a alteração antes de a resposta ir para a rede — o modo
# type_drift (preco de número para texto) nunca chegaria ao cliente, e é justamente
# esse o sinal de quebra de contrato que o agente precisa interceptar. O
# response_model segue declarado só para gerar a documentação do contrato normal.
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..fault_injection import ErrorFault, apply_fault, state
from ..models import Produto
from ..schemas import ProdutoOut

router = APIRouter(prefix="/api/produtos", tags=["produtos"])

_MALFORMED_BODY = '[{"id": 1, "nome": "resposta truncada de propos'


def _to_dict(p: Produto) -> dict:
    return {
        "id": p.id_produto,
        "nome": p.descri_produto,
        "resumo": p.resumo_produto,
        "tipo": p.tipo.rotulo_tipo,
        "preco": float(p.valor_produto) if p.valor_produto is not None else None,
        "imagem": p.imagem_produto,
        "destaque": p.destaque_produto == "Sim",
    }


@router.get("", response_model=list[ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    if state.mode == "malformed_json":
        return Response(content=_MALFORMED_BODY, media_type="application/json")
    produtos = db.query(Produto).all()
    try:
        data = [apply_fault(_to_dict(p), entity="produto") for p in produtos]
    except ErrorFault as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return JSONResponse(content=data)


@router.get("/{produto_id}", response_model=ProdutoOut)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    if state.mode == "malformed_json":
        return Response(content=_MALFORMED_BODY, media_type="application/json")
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    try:
        data = apply_fault(_to_dict(produto), entity="produto")
    except ErrorFault as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return JSONResponse(content=data)
