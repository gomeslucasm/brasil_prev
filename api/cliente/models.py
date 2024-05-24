from sqlalchemy import DECIMAL, NUMERIC, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import mapped_column

from api.common.bases.models import BaseDBModel


class Client(BaseDBModel):
    __tablename__ = "clientes"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf = mapped_column(String, unique=True, nullable=False)
    nome = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    data_de_nascimento = mapped_column(DateTime, nullable=False)
    genero = mapped_column(String, nullable=False)
    renda_mensal = mapped_column(NUMERIC(precision=10, scale=2), nullable=False)
