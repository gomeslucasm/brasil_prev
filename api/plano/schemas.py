from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class PlanoCreate(BaseModel):
    id_cliente: UUID = Field(alias="idCliente")
    id_produto: UUID = Field(alias="idProduto")
    aporte: float
    data_da_contratacao: datetime = Field(alias="dataDaContratacao")
    idade_de_aposentadoria: int = Field(alias="idadeDeAposentadoria")


class PlanoResponse(BaseModel):
    id: UUID

    class Config:
        from_attributes = True
        populate_by_name = True
