from typing import Callable, Optional
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from api.plano.models import Plano, ProdutoPlano
from api.plano.services import PlanoService, create_plano_service
from api.plano.repositories import IPlanoRepository
from datetime import datetime
from uuid import uuid4
from tests.fixtures.db import *
from api.plano.entities import ProdutoData


@pytest.fixture
def create_plano():
    def fn(
        *,
        id_cliente: str,
        id_produto_plano: str,
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
def create_plano_on_db(
    db: Session, create_plano: Callable[..., Plano]
) -> Callable[..., Plano]:
    def fn(
        *,
        id_cliente: str,
        id_produto_plano: str,
        aporte: float,
        data_da_contratacao: datetime,
        idade_de_aposentadoria: int,
    ) -> Plano:
        plano = create_plano(
            id_cliente=id_cliente,
            id_produto_plano=id_produto_plano,
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
def new_plano(db: Session, create_plano_on_db, delete_entity_on_db):
    produto_plano = ProdutoPlano(
        id_produto=uuid4(),
        nome="Produto Teste",
        susep="123456",
        expiracao_de_venda=datetime(year=2023, month=1, day=1),
        valor_minimo_aporte_inicial=1000.0,
        valor_minimo_aporte_extra=100.0,
        idade_de_entrada=18,
        idade_de_saida=65,
        carencia_inicial_de_resgate=30,
        carencia_entre_resgates=10,
    )

    db.add(produto_plano)
    db.commit()
    db.refresh(produto_plano)

    plano = create_plano_on_db(
        id_cliente=uuid4(),
        id_produto_plano=produto_plano.id,
        aporte=2000.0,
        data_da_contratacao=datetime(year=2022, month=4, day=5),
        idade_de_aposentadoria=60,
    )

    yield plano

    delete_entity_on_db(plano)
    delete_entity_on_db(produto_plano)


@pytest.fixture
def get_plano_on_db(db: Session) -> Callable[..., Optional[Plano]]:
    def fn(
        *,
        id: Optional[int] = None,
    ) -> Optional[Plano]:
        query = db.query(Plano)

        if id:
            query = query.filter(Plano.id == id)
        else:
            raise Exception("Need id")

        return query.first()

    return fn


@pytest.fixture
def mock_plano_repository():
    mock_repository = Mock(spec=IPlanoRepository)
    return mock_repository


@pytest.fixture
def plano_service(
    mock_plano_repository, mock_produto_repository, mock_cliente_repository
):
    return PlanoService(
        plano_repository=mock_plano_repository,
        produto_repository=mock_produto_repository,
        cliente_repository=mock_cliente_repository,
    )


@pytest.fixture
def mock_plano_service():
    with patch("api.plano.apis.create_plano_service") as mock:
        mock_service = mock.return_value
        yield mock_service
