from datetime import datetime
from decimal import Decimal
from utils import TipoMovimentacao
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()




@table_registry.mapped_as_dataclass
class Categoria:
    __tablename__ = 'categorias'

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    nome: Mapped[str] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
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

    categoria: Mapped['Categoria'] = relationship(
        'Categoria', back_populates='produtos', init=False
    )

    movimentacoes: Mapped[list['MovimentacaoEstoque']] = relationship(
        'MovimentacaoEstoque', back_populates='produto', init=False
    )


@table_registry.mapped_as_dataclass
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
