# ! Alteração de IA - Revisar
"""
Contratos "normais" da API — usados só pra gerar a doc OpenAPI (/docs). As
rotas retornam JSONResponse(dict) explícito em vez de deixar o FastAPI
serializar via response_model, justamente pra permitir que a fault injection
altere o formato de verdade (ver fault_injection.py) — response_model
sozinho filtraria/validaria essas alterações antes de sair pela rede.
"""
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ProdutoOut(BaseModel):
    id: int
    nome: str
    resumo: Optional[str] = None
    tipo: str
    preco: Decimal
    imagem: Optional[str] = None
    destaque: bool


class PedidoOut(BaseModel):
    id_pedido: int
    pessoas: int
    data_pedido: date
    status: str
    nome: str
    cpf: str


class PedidoCreate(BaseModel):
    id_clientes: int
    pessoas: int
    data_pedido: date


class FaultModeIn(BaseModel):
    mode: str
    target_field: Optional[str] = None
    probability: float = 1.0


class FaultModeOut(BaseModel):
    mode: str
    target_field: Optional[str] = None
    probability: float
