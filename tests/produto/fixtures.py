from typing import Callable, Optional
import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session
from api.produto.models import Produto
from api.produto.services import ProdutoService
from api.produto.repositories import IProdutoRepository
from datetime import datetime
from tests.fixtures.db import *


@pytest.fixture
def create_produto():
    def fn(
        *,
        nome: str,
        susep: str,
        expiracaoDeVenda: datetime,
        valorMinimoAporteInicial: float,
        valorMinimoAporteExtra: float,
        idadeDeEntrada: int,
        idadeDeSaida: int,
        carenciaInicialDeResgate: int,
        carenciaEntreResgates: int,
    ) -> Produto:
        return Produto(
            nome=nome,
            susep=susep,
            expiracaoDeVenda=expiracaoDeVenda,
            valorMinimoAporteInicial=valorMinimoAporteInicial,
            valorMinimoAporteExtra=valorMinimoAporteExtra,
            idadeDeEntrada=idadeDeEntrada,
            idadeDeSaida=idadeDeSaida,
            carenciaInicialDeResgate=carenciaInicialDeResgate,
            carenciaEntreResgates=carenciaEntreResgates,
        )

    return fn


@pytest.fixture
def create_produto_on_db(
    db: Session, create_produto: Callable[..., Produto]
) -> Callable[..., Produto]:
    def fn(
        *,
        nome: str,
        susep: str,
        expiracaoDeVenda: datetime,
        valorMinimoAporteInicial: float,
        valorMinimoAporteExtra: float,
        idadeDeEntrada: int,
        idadeDeSaida: int,
        carenciaInicialDeResgate: int,
        carenciaEntreResgates: int,
    ) -> Produto:
        produto = create_produto(
            nome=nome,
            susep=susep,
            expiracaoDeVenda=expiracaoDeVenda,
            valorMinimoAporteInicial=valorMinimoAporteInicial,
            valorMinimoAporteExtra=valorMinimoAporteExtra,
            idadeDeEntrada=idadeDeEntrada,
            idadeDeSaida=idadeDeSaida,
            carenciaInicialDeResgate=carenciaInicialDeResgate,
            carenciaEntreResgates=carenciaEntreResgates,
        )
        db.add(produto)
        db.commit()
        db.refresh(produto)
        return produto

    return fn


@pytest.fixture
def new_produto(create_produto_on_db, delete_entity_on_db):
    expiracao_de_venda = datetime(year=2021, month=1, day=1)
    produto = create_produto_on_db(
        nome="Brasilprev Produto",
        susep="15414900840201817",
        expiracaoDeVenda=expiracao_de_venda,
        valorMinimoAporteInicial=1000.0,
        valorMinimoAporteExtra=100.0,
        idadeDeEntrada=18,
        idadeDeSaida=60,
        carenciaInicialDeResgate=60,
        carenciaEntreResgates=30,
    )

    yield produto

    delete_entity_on_db(produto)


@pytest.fixture
def get_produto_on_db(db: Session) -> Callable[..., Optional[Produto]]:
    def fn(
        *,
        id: int,
    ) -> Optional[Produto]:
        return db.query(Produto).filter(Produto.id == id).first()

    return fn


@pytest.fixture
def mock_produto_repository():
    mock_repository = Mock(spec=IProdutoRepository)
    return mock_repository


@pytest.fixture
def produto_service(mock_produto_repository):
    return ProdutoService(produto_repository=mock_produto_repository)


@pytest.fixture
def mock_produto_service():
    with patch("api.produto.apis.ProdutoService") as mock:
        mock_service = mock.return_value
        yield mock_service
