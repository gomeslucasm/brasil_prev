from api.produto.repositories import ProdutoDatabaseRepository
from datetime import datetime
from tests.unit.produto.fixtures import *
from tests.fixtures.db import *


def test_create_produto(db, delete_entity_on_db):
    repository = ProdutoDatabaseRepository(db)
    expiracao_de_venda = datetime(year=2021, month=1, day=1)
    produto_data = {
        "nome": "Brasilprev Produto",
        "susep": "15414900840201817",
        "expiracao_de_venda": expiracao_de_venda,
        "valor_minimo_aporte_inicial": 1000.0,
        "valor_minimo_aporte_extra": 100.0,
        "idade_de_entrada": 18,
        "idade_de_saida": 60,
        "carencia_inicial_de_resgate": 60,
        "carencia_entre_resgates": 30,
    }
    produto = repository.create(**produto_data)
    assert produto.nome == produto_data["nome"]
    assert produto.susep == produto_data["susep"]
    assert (
        produto.expiracao_de_venda.isoformat()
        == produto_data["expiracao_de_venda"].isoformat()
    )
    assert (
        produto.valor_minimo_aporte_inicial
        == produto_data["valor_minimo_aporte_inicial"]
    )
    assert (
        produto.valor_minimo_aporte_extra == produto_data["valor_minimo_aporte_extra"]
    )
    assert produto.idade_de_entrada == produto_data["idade_de_entrada"]
    assert produto.idade_de_saida == produto_data["idade_de_saida"]
    assert (
        produto.carencia_inicial_de_resgate
        == produto_data["carencia_inicial_de_resgate"]
    )
    assert produto.carencia_entre_resgates == produto_data["carencia_entre_resgates"]

    delete_entity_on_db(produto)


def test_get_produto_by_id(db, new_produto):
    repository = ProdutoDatabaseRepository(db)
    produto = repository.get_by_id(id=new_produto.id)

    assert produto
    assert produto.id == new_produto.id
    assert produto.nome == new_produto.nome
    assert produto.susep == new_produto.susep
