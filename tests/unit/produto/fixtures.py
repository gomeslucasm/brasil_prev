from typing import Callable, Optional
from uuid import UUID
import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session
from api.plano.models import Plano
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
        expiracao_de_venda: datetime,
        valor_minimo_aporte_inicial: float,
        valor_minimo_aporte_extra: float,
        idade_de_entrada: int,
        idade_de_saida: int,
        carencia_inicial_de_resgate: int,
        carencia_entre_resgates: int,
    ) -> Produto:
        return Produto(
            nome=nome,
            susep=susep,
            expiracao_de_venda=expiracao_de_venda,
            valor_minimo_aporte_inicial=valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=valor_minimo_aporte_extra,
            idade_de_entrada=idade_de_entrada,
            idade_de_saida=idade_de_saida,
            carencia_inicial_de_resgate=carencia_inicial_de_resgate,
            carencia_entre_resgates=carencia_entre_resgates,
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
        expiracao_de_venda: datetime,
        valor_minimo_aporte_inicial: float,
        valor_minimo_aporte_extra: float,
        idade_de_entrada: int,
        idade_de_saida: int,
        carencia_inicial_de_resgate: int,
        carencia_entre_resgates: int,
    ) -> Produto:
        produto = create_produto(
            nome=nome,
            susep=susep,
            expiracao_de_venda=expiracao_de_venda,
            valor_minimo_aporte_inicial=valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=valor_minimo_aporte_extra,
            idade_de_entrada=idade_de_entrada,
            idade_de_saida=idade_de_saida,
            carencia_inicial_de_resgate=carencia_inicial_de_resgate,
            carencia_entre_resgates=carencia_entre_resgates,
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
        expiracao_de_venda=expiracao_de_venda,
        valor_minimo_aporte_inicial=1000.0,
        valor_minimo_aporte_extra=100.0,
        idade_de_entrada=18,
        idade_de_saida=60,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
    )

    yield produto

    delete_entity_on_db(produto)


@pytest.fixture
def get_plano_by_id(db):
    def fn(*, id_plano: UUID):
        plano = db.query(Plano).filter(Plano.id == id_plano).first()
        print("plano.id=", plano.id)

        return plano

    return fn


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
