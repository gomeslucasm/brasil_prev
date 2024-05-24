from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from api.common.schemas.types import CPFPydanticType


class ClientCreate(BaseModel):
    cpf: CPFPydanticType
    nome: str
    email: EmailStr
    dataDeNascimento: datetime
    genero: str
    rendaMensal: float


class ClientResponse(BaseModel):
    id: UUID

    class Config:
        from_attributes = True
