from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


class TipoMovimentacao(str, Enum):
    ENTRADA = 'entrada'
    VENDA = 'venda'
    AJUSTE = 'ajuste'
    PERDA = 'perda'


@mapped_as_dataclass(table_registry)
class Categoria:
    __tablename__ = 'categorias'

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    nome: Mapped[str] = mapped_column(nullable=False)

    produtos: Mapped[list['Produto']] = relationship(
        'Produto', back_populates='categoria', init=False
    )


@mapped_as_dataclass(table_registry)
class Produto:
    __tablename__ = 'produtos'

    id: Mapped[UUID] = mapped_column(
        primary_key=True, default_factory=uuid4, init=False
    )

    categoria_id: Mapped[UUID] = mapped_column(
        ForeignKey('categorias.id', ondelete='RESTRICT'), nullable=False
    )

    codigo_de_barras: Mapped[str] = mapped_column(
        unique=True, nullable=False, index=True
    )

    nome: Mapped[str] = mapped_column(nullable=False)

    # Precisão decimal para evitar erros em centavos
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    quantidade: Mapped[int] = mapped_column(nullable=False, default=0)

    data_criacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    categoria: Mapped['Categoria'] = relationship(
        'Categoria', back_populates='produtos', init=False
    )

    movimentacoes: Mapped[list['MovimentacaoEstoque']] = relationship(
        'MovimentacaoEstoque', back_populates='produto', init=False
    )


@mapped_as_dataclass(table_registry)
class MovimentacaoEstoque:
    __tablename__ = 'movimentacoes_estoque'

    id: Mapped[UUID] = mapped_column(
        primary_key=True, default_factory=uuid4, init=False
    )

    produto_id: Mapped[UUID] = mapped_column(
        ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False
    )

    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[TipoMovimentacao] = mapped_column(String, nullable=False)
    observacao: Mapped[str | None] = mapped_column(
        String, nullable=True, default=None
    )

    data_movimentacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    produto: Mapped['Produto'] = relationship(
        'Produto', back_populates='movimentacoes', init=False
    )
