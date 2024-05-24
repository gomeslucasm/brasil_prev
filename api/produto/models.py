from sqlalchemy import String, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
import uuid
from api.common.bases.models import BaseDBModel


class Produto(BaseDBModel):
    __tablename__ = "produtos"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = mapped_column(String, nullable=False)
    susep = mapped_column(String, nullable=False)
    expiracao_de_venda = mapped_column(DateTime, nullable=False)
    valor_minimo_aporte_inicial = mapped_column(Float, nullable=False)
    valor_minimo_aporte_extra = mapped_column(Float, nullable=False)
    idade_de_entrada = mapped_column(Integer, nullable=False)
    idade_de_saida = mapped_column(Integer, nullable=False)
    carencia_inicial_de_resgate = mapped_column(Integer, nullable=False)
    carencia_entre_resgates = mapped_column(Integer, nullable=False)
