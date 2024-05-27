from sqlalchemy import and_
from sqlalchemy.orm import Session
from api.common.bases.repository import BaseDatabaseRepository
from api.plano.models import Plano, ProdutoPlano, PlanoOperation
from api.plano.types import OperationType, PlanoData, ProdutoData
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

    def aporte_extra(self, *, id_plano: UUID, value: float) -> Plano: ...

    def get_plano_data(self, *, id_plano: UUID) -> Optional[PlanoData]: ...

    def resgate(self, *, id_plano: UUID, value: float) -> PlanoOperation: ...

    def get_last_resgate(self, *, id_plano: UUID) -> Optional[PlanoOperation]: ...


class PlanoDatabaseRepository(BaseDatabaseRepository[Plano]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_plano_data(self, *, id_plano: UUID) -> Optional[PlanoData]:
        plano_data = (
            self.db.query(
                Plano.id.label("id"),
                Plano.id_cliente.label("id_cliente"),
                Plano.aporte.label("aporte"),
                Plano.data_da_contratacao.label("data_da_contratacao"),
                Plano.idade_de_aposentadoria.label("idade_de_aposentadoria"),
                Plano.created_on.label("created_on"),
                ProdutoPlano.nome.label("produto_nome"),
                ProdutoPlano.susep.label("produto_susep"),
                ProdutoPlano.expiracao_de_venda.label("produto_expiracao_de_venda"),
                ProdutoPlano.valor_minimo_aporte_inicial.label(
                    "produto_valor_minimo_aporte_inicial"
                ),
                ProdutoPlano.valor_minimo_aporte_extra.label(
                    "produto_valor_minimo_aporte_extra"
                ),
                ProdutoPlano.idade_de_entrada.label("produto_idade_de_entrada"),
                ProdutoPlano.idade_de_saida.label("produto_idade_de_saida"),
                ProdutoPlano.carencia_inicial_de_resgate.label(
                    "produto_carencia_inicial_de_resgate"
                ),
                ProdutoPlano.carencia_entre_resgates.label(
                    "produto_carencia_entre_resgates"
                ),
            )
            .join(
                ProdutoPlano,
                and_(
                    ProdutoPlano.deleted_on.is_(None),
                    ProdutoPlano.id == Plano.id_produto_plano,
                ),
            )
            .filter(
                and_(Plano.deleted_on.is_(None), Plano.id == id_plano),
            )
        ).first()

        return plano_data

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

        operation = PlanoOperation(
            id_plano=plano.id,
            operation_type=OperationType.CONTRATACAO,
            value=aporte,
        )
        self.add(operation)
        self.commit()
        self.refresh(operation)

        return plano

    def aporte_extra(self, *, id_plano: UUID, value: float) -> PlanoOperation:
        operation = PlanoOperation(
            id_plano=id_plano,
            operation_type=OperationType.APORTE,
            value=value,
        )
        self.db.query(Plano).filter(Plano.id == id_plano).update(
            {Plano.aporte: Plano.aporte + value}, synchronize_session="fetch"
        )

        self.add(operation)
        self.commit()
        return operation

    def resgate(self, *, id_plano: UUID, value: float) -> PlanoOperation:
        operation = PlanoOperation(
            id_plano=id_plano,
            operation_type=OperationType.RESGATE,
            value=value,
        )
        self.db.query(Plano).filter(Plano.id == id_plano).update(
            {Plano.aporte: Plano.aporte - value}, synchronize_session="fetch"
        )

        self.add(operation)
        self.commit()
        return operation

    def get_last_resgate(self, *, id_plano: UUID) -> Optional[PlanoOperation]:
        return (
            self.db.query(PlanoOperation)
            .filter(
                PlanoOperation.id_plano == id_plano,
                PlanoOperation.deleted_on.isnot(True),
                PlanoOperation.operation_type == OperationType.RESGATE,
            )
            .order_by(PlanoOperation.created_on.desc())
        ).first()
