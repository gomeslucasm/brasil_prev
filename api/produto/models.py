from sqlalchemy import String, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column

import uuid

from api.common.bases.models import BaseDBModel


Base = declarative_base()


class Produto(BaseDBModel):
    __tablename__ = "produtos"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = mapped_column(String, nullable=False)
    susep = mapped_column(String, nullable=False)
    expiracaoDeVenda = mapped_column(DateTime, nullable=False)
    valorMinimoAporteInicial = mapped_column(Float, nullable=False)
    valorMinimoAporteExtra = mapped_column(Float, nullable=False)
    idadeDeEntrada = mapped_column(Integer, nullable=False)
    idadeDeSaida = mapped_column(Integer, nullable=False)
    carenciaInicialDeResgate = mapped_column(Integer, nullable=False)
    carenciaEntreResgates = mapped_column(Integer, nullable=False)
