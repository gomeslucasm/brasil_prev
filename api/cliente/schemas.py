from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from api.common.schemas.types import CPFPydanticType


class ClientCreate(BaseModel):
    cpf: CPFPydanticType
    nome: str
    email: EmailStr
    data_de_nascimento: datetime = Field(alias="dataDeNascimento")
    genero: str
    renda_mensal: float = Field(alias="rendaMensal")


class ClientResponse(BaseModel):
    id: UUID

    class Config:
        from_attributes = True
