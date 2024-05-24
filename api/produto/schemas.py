from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class ProdutoCreate(BaseModel):
    nome: str
    susep: str
    expiracao_de_venda: datetime = Field(alias="expiracaoDeVenda")
    valor_minimo_aporte_inicial: float = Field(alias="valorMinimoAporteInicial")
    valor_minimo_aporte_extra: float = Field(alias="valorMinimoAporteExtra")
    idade_de_entrada: int = Field(alias="idadeDeEntrada")
    idade_de_saida: int = Field(alias="idadeDeSaida")
    carencia_inicial_de_resgate: int = Field(alias="carenciaInicialDeResgate")
    carencia_entre_resgates: int = Field(alias="carenciaEntreResgates")


class ProdutoResponse(BaseModel):
    id: UUID

    class Config:
        from_attributes = True
