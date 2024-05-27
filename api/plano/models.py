from sqlalchemy import Column, ForeignKey, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from sqlalchemy.orm import relationship, mapped_column
from api.common.bases.models import BaseDBModel


class ProdutoPlano(BaseDBModel):
    __tablename__ = "produto_planos"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id_produto = mapped_column(UUID(as_uuid=True), nullable=False)
    nome = Column(String, nullable=False)
    susep = Column(String, nullable=False)
    expiracao_de_venda = Column(DateTime, nullable=False)
    valor_minimo_aporte_inicial = Column(Float, nullable=False)
    valor_minimo_aporte_extra = Column(Float, nullable=False)
    idade_de_entrada = Column(Integer, nullable=False)
    idade_de_saida = Column(Integer, nullable=False)
    carencia_inicial_de_resgate = Column(Integer, nullable=False)
    carencia_entre_resgates = Column(Integer, nullable=False)


class Plano(BaseDBModel):
    __tablename__ = "planos"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id_cliente = mapped_column(
        UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False
    )
    id_produto_plano = mapped_column(
        UUID(as_uuid=True), ForeignKey("produto_planos.id"), nullable=False
    )
    aporte = mapped_column(Float, nullable=False)
    data_da_contratacao = mapped_column(DateTime, nullable=False)
    idade_de_aposentadoria = mapped_column(Integer, nullable=False)

    produto_plano = relationship("ProdutoPlano", backref="plano")
