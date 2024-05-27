from uuid import uuid4
from api.plano.models import Plano
from tests.fixtures.api import *
from api.plano.schemas import PlanoCreate
from tests.plano.fixtures import *
from datetime import datetime


def test_register_plano_api_success(
    mock_plano_service,
    create_plano: Callable[..., Plano],
    api_client,
):
    data_da_contratacao = datetime(year=2022, month=4, day=3)

    plano_data = {
        "idCliente": "18dfeb91-459a-4bc7-9cdd-d93b41f7bf62",
        "idProduto": "30f6b23f-c93d-4cf9-8916-bcdb9fac83df",
        "aporte": 2000.0,
        "dataDaContratacao": data_da_contratacao.isoformat(),
        "idadeDeAposentadoria": 60,
    }

    produto_plano_id = str(uuid4())

    plano = create_plano(
        id_cliente=plano_data["idCliente"],
        id_produto_plano=produto_plano_id,
        aporte=plano_data["aporte"],
        data_da_contratacao=data_da_contratacao,
        idade_de_aposentadoria=plano_data["idadeDeAposentadoria"],
    )

    plano.id = str(uuid4())

    mock_plano_service.create_plano.return_value = plano

    response = api_client.post("/api/planos", json=plano_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": str(mock_plano_service.create_plano.return_value.id)
    }

    mock_plano_service.create_plano.assert_called_once_with(PlanoCreate(**plano_data))


def test_register_plano_api_invalid_data(api_client):
    plano_data = {
        "idCliente": "invalid_id",
        "idProduto": "invalid_id",
        "aporte": "invalid_value",
        "dataDaContratacao": "invalid_date",
        "idadeDeAposentadoria": "invalid_value",
    }

    response = api_client.post("/api/planos", json=plano_data)
    assert response.status_code == 422
