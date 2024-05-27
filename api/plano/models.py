from sqlalchemy import Column, ForeignKey, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from sqlalchemy.orm import relationship, mapped_column
from api.common.bases.models import BaseDBModel


class ProdutoPlano(BaseDBModel):
    __tablename__ = "produto_planos"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id_produto = mapped_column(UUID(as_uuid=True), nullable=False)
    nome = mapped_column(String, nullable=False)
    susep = mapped_column(String, nullable=False)
    expiracao_de_venda = mapped_column(DateTime, nullable=False)
    valor_minimo_aporte_inicial = mapped_column(Float, nullable=False)
    valor_minimo_aporte_extra = mapped_column(Float, nullable=False)
    idade_de_entrada = mapped_column(Integer, nullable=False)
    idade_de_saida = mapped_column(Integer, nullable=False)
    carencia_inicial_de_resgate = mapped_column(Integer, nullable=False)
    carencia_entre_resgates = mapped_column(Integer, nullable=False)


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


class PlanoOperation(BaseDBModel):
    __tablename__ = "plano_operations"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id_plano = mapped_column(
        UUID(as_uuid=True), ForeignKey("planos.id"), nullable=False
    )
    operation_type = mapped_column(
        String, nullable=False
    )  # "aporte", "retirada", "contratacao"
    value = mapped_column(Float, nullable=False)

    plano = relationship("Plano", backref="operations")
