# ! Alteração de IA - Revisar
"""
Mapeamento ORM nas MESMAS tabelas que Programacao/CobaiaFront usa (banco
único compartilhado, ver plano). Nomes/tipos de coluna conferidos
diretamente em Programacao/CobaiaFront/banco/bancoatualizado.sql e
schema_completo.sql — não inventados por convenção. Essas tabelas já
existem via esses scripts SQL; esta API nunca roda CREATE TABLE.
"""
from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Tipo(Base):
    __tablename__ = "tbtipos"

    id_tipo: Mapped[int] = mapped_column(Integer, primary_key=True)
    sigla_tipo: Mapped[str] = mapped_column(String(3))
    rotulo_tipo: Mapped[str] = mapped_column(String(15))


class Produto(Base):
    __tablename__ = "tbprodutos"

    id_produto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tipo_produto: Mapped[int] = mapped_column(ForeignKey("tbtipos.id_tipo"))
    descri_produto: Mapped[str] = mapped_column(String(100))
    resumo_produto: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    valor_produto: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(9, 2), nullable=True)
    imagem_produto: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    destaque_produto: Mapped[str] = mapped_column(Enum("Sim", "Não", name="destaque_enum"))

    tipo: Mapped["Tipo"] = relationship()


class Usuario(Base):
    __tablename__ = "tbusuarios"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    login_usuario: Mapped[str] = mapped_column(String(30))
    # nome: adicionada por schema_completo.sql (ALTER TABLE) — não existia
    # no dump original.
    nome: Mapped[str] = mapped_column(String(100))
    senha_usuario: Mapped[str] = mapped_column(String(32))
    nivel_usuario: Mapped[str] = mapped_column(Enum("sup", "cli", name="nivel_enum"))


class PedidoReserva(Base):
    __tablename__ = "tbpedido_reserva"

    id_pedido: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_clientes: Mapped[int] = mapped_column(ForeignKey("tbusuarios.id_usuario"))
    pessoas: Mapped[int] = mapped_column(Integer)
    data_pedido: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(Enum("Em Análise", "Cancelado", name="status_enum"))

    cliente: Mapped["Usuario"] = relationship()
