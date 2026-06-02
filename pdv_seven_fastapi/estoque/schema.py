from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from utils import TipoMovimentacao

class CategoriaSchema(BaseModel):
    id: UUID
    nome: str

class ProdutoSchema(BaseModel):
    id: UUID
    preco: Decimal
    quantidade: int
    categoria: str
    movimentacoes: list

class MovimentacaoEstoqueSchema(BaseModel):
    id: UUID
    produto_id: UUID
    quantidade: int
    tipo: TipoMovimentacao


