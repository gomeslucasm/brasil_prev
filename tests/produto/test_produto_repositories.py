from typing import Callable
from api.produto.models import Produto
from api.produto.repositories import ProdutoDatabaseRepository
from datetime import datetime
from tests.produto.fixtures import *
from tests.fixtures.db import *


def test_create_produto(db, delete_entity_on_db):
    repository = ProdutoDatabaseRepository(db)
    expiracao_de_venda = datetime(year=2021, month=1, day=1)
    produto_data = {
        "nome": "Brasilprev Produto",
        "susep": "15414900840201817",
        "expiracaoDeVenda": expiracao_de_venda,
        "valorMinimoAporteInicial": 1000.0,
        "valorMinimoAporteExtra": 100.0,
        "idadeDeEntrada": 18,
        "idadeDeSaida": 60,
        "carenciaInicialDeResgate": 60,
        "carenciaEntreResgates": 30,
    }
    produto = repository.create(**produto_data)
    assert produto.nome == produto_data["nome"]
    assert produto.susep == produto_data["susep"]
    assert (
        produto.expiracaoDeVenda.isoformat()
        == produto_data["expiracaoDeVenda"].isoformat()
    )
    assert produto.valorMinimoAporteInicial == produto_data["valorMinimoAporteInicial"]
    assert produto.valorMinimoAporteExtra == produto_data["valorMinimoAporteExtra"]
    assert produto.idadeDeEntrada == produto_data["idadeDeEntrada"]
    assert produto.idadeDeSaida == produto_data["idadeDeSaida"]
    assert produto.carenciaInicialDeResgate == produto_data["carenciaInicialDeResgate"]
    assert produto.carenciaEntreResgates == produto_data["carenciaEntreResgates"]

    delete_entity_on_db(produto)


def test_get_produto_by_id(db, new_produto):
    repository = ProdutoDatabaseRepository(db)
    produto = repository.get_by_id(id=new_produto.id)

    assert produto
    assert produto.id == new_produto.id
    assert produto.nome == new_produto.nome
    assert produto.susep == new_produto.susep
