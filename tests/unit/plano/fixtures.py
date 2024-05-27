import pytest
from typing import Callable, Literal, Optional
from sqlalchemy.orm import Session
from api.plano.types import OperationType, ProdutoData
from api.plano.models import Plano, ProdutoPlano, PlanoOperation
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from api.plano.repositories import IPlanoRepository
from tests.fixtures.db import db
from api.produto.models import Produto
from tests.unit.produto.fixtures import *


@pytest.fixture
def create_plano():
    def fn(
        *,
        id_cliente: UUID,
        id_produto_plano: UUID,
        aporte: float,
        data_da_contratacao: datetime,
        idade_de_aposentadoria: int,
    ) -> Plano:
        return Plano(
            id_cliente=id_cliente,
            id_produto_plano=id_produto_plano,
            aporte=aporte,
            data_da_contratacao=data_da_contratacao,
            idade_de_aposentadoria=idade_de_aposentadoria,
        )

    return fn


@pytest.fixture
def create_produto_plano():
    def fn(
        *,
        produto: Produto,
    ) -> ProdutoPlano:
        return ProdutoPlano(
            id_produto=produto.id,
            nome=produto.nome,
            susep=produto.susep,
            expiracao_de_venda=produto.expiracao_de_venda,
            valor_minimo_aporte_inicial=produto.valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=produto.valor_minimo_aporte_extra,
            idade_de_entrada=produto.idade_de_entrada,
            idade_de_saida=produto.idade_de_saida,
            carencia_inicial_de_resgate=produto.carencia_inicial_de_resgate,
            carencia_entre_resgates=produto.carencia_entre_resgates,
        )

    return fn


@pytest.fixture
def create_plano_on_db(
    db: Session, create_plano, create_produto_plano
) -> Callable[..., Plano]:
    def fn(
        *,
        id_cliente: UUID,
        produto: Produto,
        aporte: float,
        data_da_contratacao: datetime,
        idade_de_aposentadoria: int,
    ) -> Plano:
        produto_plano = create_produto_plano(produto=produto)
        db.add(produto_plano)
        db.commit()
        db.refresh(produto_plano)

        plano = create_plano(
            id_cliente=id_cliente,
            id_produto_plano=produto_plano.id,
            aporte=aporte,
            data_da_contratacao=data_da_contratacao,
            idade_de_aposentadoria=idade_de_aposentadoria,
        )
        db.add(plano)
        db.commit()
        db.refresh(plano)
        return plano

    return fn


@pytest.fixture
def create_plano_operation():
    def fn(
        *,
        id_plano: UUID,
        value: float,
        operation_type: OperationType,
    ) -> PlanoOperation:
        operation = PlanoOperation(
            id_plano=id_plano,
            operation_type=operation_type,
            value=value,
        )
        return operation

    return fn


@pytest.fixture
def create_plano_operation_on_db(create_plano_operation, db):
    def fn(
        *,
        id_plano: UUID,
        value: float,
        operation_type: OperationType,
    ) -> PlanoOperation:
        plano_operation = create_plano_operation(
            id_plano=id_plano,
            operation_type=operation_type,
            value=value,
        )
        db.add(plano_operation)
        db.commit()
        return plano_operation

    return fn


@pytest.fixture
def mock_plano_repository():
    mock_repository = Mock(spec=IPlanoRepository)
    return mock_repository


@pytest.fixture
def mock_plano_service():
    with patch("api.plano.services.PlanoService") as mock:
        mock_service = mock.return_value
        yield mock_service


@pytest.fixture
def create_plano_operation_on_db(db):
    def fn(
        *,
        value: float,
        operation_type: OperationType,
        id_plano: UUID,
        created_on: Optional[datetime] = None,
    ):
        operation = PlanoOperation(
            id_plano=id_plano, operation_type=operation_type, value=value
        )
        db.add(operation)
        db.commit()

        if created_on:
            operation.created_on = created_on
            db.commit()

        return operation

    return fn
