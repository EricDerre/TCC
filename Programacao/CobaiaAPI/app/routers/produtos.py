# ! Alteração de IA - Revisar: rotas de produto que montam um dict puro, aplicam a
# injeção de falha por último e devolvem JSONResponse explícito.
# ! Motivo: se a resposta saísse pelo response_model do FastAPI, o Pydantic
# revalidaria e desfaria a alteração antes de a resposta ir para a rede — o modo
# type_drift (preco de número para texto) nunca chegaria ao cliente, e é justamente
# esse o sinal de quebra de contrato que o agente precisa interceptar. O
# response_model segue declarado só para gerar a documentação do contrato normal.
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..fault_injection import ErrorFault, apply_fault, apply_fault_lista, resposta_especial, state
from ..models import Produto
from ..schemas import ProdutoOut

router = APIRouter(prefix="/api/produtos", tags=["produtos"])


def _tipo_de_outro(db: Session, produto: Produto) -> str:
    """O rótulo de tipo de um produto de outro tipo (modo chave_de_juncao_errada no detalhe)."""
    outro = db.query(Produto).filter(Produto.id_tipo_produto != produto.id_tipo_produto).first()
    return outro.tipo.rotulo_tipo if outro else produto.tipo.rotulo_tipo


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


# ! Alteração de IA - Revisar: (26/10/2026, ficha 28) as duas rotas passam a chamar
# resposta_especial antes do banco (corpo truncado, vazio, HTML, 429 e 404), a lista passa
# por apply_fault_lista (duplicado, item a menos, tipo girado) e o detalhe trata os modos
# chave_de_juncao_errada (tipo de outro produto) e colecao_no_lugar_de_objeto (lista com um
# item no lugar do objeto).
# ! Motivo: são os modos novos, um por causa que a tela consegue mostrar; antes só o
# malformed_json era tratado aqui, por conta própria.
@router.get("", response_model=list[ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    especial = resposta_especial(entity="produto")
    if especial is not None:
        return especial
    produtos = db.query(Produto).all()
    try:
        data = apply_fault_lista([apply_fault(_to_dict(p), entity="produto") for p in produtos])
    except ErrorFault as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return JSONResponse(content=data)


@router.get("/{produto_id}", response_model=ProdutoOut)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    especial = resposta_especial(entity="produto")
    if especial is not None:
        return especial
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    try:
        data = apply_fault(_to_dict(produto), entity="produto")
    except ErrorFault as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    if state.mode == "chave_de_juncao_errada":
        data = {**data, "tipo": _tipo_de_outro(db, produto)}
    if state.mode == "colecao_no_lugar_de_objeto":
        return JSONResponse(content=[data])
    return JSONResponse(content=data)
