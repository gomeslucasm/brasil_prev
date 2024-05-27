from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID


@dataclass
class ProdutoData:
    id_produto: UUID
    nome: str
    susep: str
    expiracao_de_venda: datetime
    valor_minimo_aporte_inicial: float
    valor_minimo_aporte_extra: float
    idade_de_entrada: int
    idade_de_saida: int
    carencia_inicial_de_resgate: int
    carencia_entre_resgates: int


@dataclass
class PlanoData:
    id: UUID
    id_cliente: UUID
    aporte: float
    data_da_contratacao: datetime
    idade_de_aposentadoria: int
    created_on: datetime
    produto_nome: str
    produto_susep: str
    produto_expiracao_de_venda: datetime
    produto_valor_minimo_aporte_inicial: float
    produto_valor_minimo_aporte_extra: float
    produto_idade_de_entrada: int
    produto_idade_de_saida: int
    produto_carencia_inicial_de_resgate: int
    produto_carencia_entre_resgates: int


class OperationType(StrEnum):
    CONTRATACAO = "contratacao"
    RESGATE = "resgate"
    APORTE = "aporte"
