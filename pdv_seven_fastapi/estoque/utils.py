from enum import Enum

class TipoMovimentacao(str, Enum):
    ENTRADA = 'entrada'
    VENDA = 'venda'
    AJUSTE = 'ajuste'
    PERDA = 'perda'