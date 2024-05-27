from uuid import uuid4
from api.plano.models import Plano
from api.plano.repositories import PlanoDatabaseRepository
from datetime import datetime
from tests.plano.fixtures import *
from tests.fixtures.db import *
from api.plano.entities import ProdutoData


def test_create_plano(db, delete_entity_on_db):
    repository = PlanoDatabaseRepository(db)
    data_da_contratacao = datetime(year=2022, month=4, day=5)
    produto_data = ProdutoData(
        id_produto=uuid4(),
        nome="Produto Teste",
        susep="123456",
        expiracao_de_venda=data_da_contratacao,
        valor_minimo_aporte_inicial=1000.0,
        valor_minimo_aporte_extra=100.0,
        idade_de_entrada=18,
        idade_de_saida=60,
        carencia_inicial_de_resgate=30,
        carencia_entre_resgates=10,
    )
    plano_data = {
        "id_cliente": uuid4(),
        "produto_data": produto_data,
        "aporte": 2000.0,
        "data_da_contratacao": data_da_contratacao,
        "idade_de_aposentadoria": 60,
    }
    plano = repository.create(**plano_data)
    assert plano.id_cliente == plano_data["id_cliente"]
    assert plano.produto_plano.id_produto == plano_data["produto_data"].id_produto
    assert plano.aporte == plano_data["aporte"]
    assert plano.data_da_contratacao == plano_data["data_da_contratacao"]
    assert plano.idade_de_aposentadoria == plano_data["idade_de_aposentadoria"]

    delete_entity_on_db(plano)
