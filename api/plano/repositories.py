from sqlalchemy.orm import Session
from api.common.bases.repository import BaseDatabaseRepository
from api.plano.models import Plano, ProdutoPlano
from api.plano.entities import ProdutoData
from typing import Optional, Protocol
from uuid import UUID
from datetime import datetime


class IPlanoRepository(Protocol):
    def create(
        self,
        *,
        id_cliente: UUID,
        produto_data: ProdutoData,
        aporte: float,
        data_da_contratacao: datetime,
        idade_de_aposentadoria: int,
    ) -> Plano: ...


class PlanoDatabaseRepository(BaseDatabaseRepository[Plano]):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        *,
        id_cliente: UUID,
        produto_data: ProdutoData,
        aporte: float,
        data_da_contratacao: datetime,
        idade_de_aposentadoria: int,
    ) -> Plano:
        produto_plano = ProdutoPlano(
            id_produto=produto_data.id_produto,
            nome=produto_data.nome,
            susep=produto_data.susep,
            expiracao_de_venda=produto_data.expiracao_de_venda,
            valor_minimo_aporte_inicial=produto_data.valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=produto_data.valor_minimo_aporte_extra,
            idade_de_entrada=produto_data.idade_de_entrada,
            idade_de_saida=produto_data.idade_de_saida,
            carencia_inicial_de_resgate=produto_data.carencia_inicial_de_resgate,
            carencia_entre_resgates=produto_data.carencia_entre_resgates,
        )
        self.add(produto_plano)
        self.commit()
        self.refresh(produto_plano)

        plano = Plano(
            id_cliente=id_cliente,
            id_produto_plano=produto_plano.id,
            aporte=aporte,
            data_da_contratacao=data_da_contratacao,
            idade_de_aposentadoria=idade_de_aposentadoria,
        )
        self.add(plano)
        self.commit()
        self.refresh(plano)

        return plano
