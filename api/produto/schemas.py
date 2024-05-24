from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ProdutoCreate(BaseModel):
    nome: str
    susep: str
    expiracaoDeVenda: datetime
    valorMinimoAporteInicial: float
    valorMinimoAporteExtra: float
    idadeDeEntrada: int
    idadeDeSaida: int
    carenciaInicialDeResgate: int
    carenciaEntreResgates: int


class ProdutoResponse(BaseModel):
    id: UUID

    class Config:
        from_attributes = True
