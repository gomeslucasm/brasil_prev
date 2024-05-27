from uuid import uuid4
from api.plano.models import Plano
from tests.fixtures.api import *
from api.plano.schemas import PlanoAporteExtra, PlanoCreate, PlanoRetirada
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


def test_aporte_extra_api(api_client, mock_plano_service):
    id_plano = uuid4()
    aporte_extra = {"idPlano": str(id_plano), "valorAporte": 1000}

    aporte_extra_mock = PlanoAporteExtra(
        idPlano=id_plano,
        valorAporte=1000,
    )

    id_operation = uuid4()

    mock_plano_service.validate_aporte_extra.return_value = True
    mock_plano_service.aporte_extra.return_value = Mock(id=id_operation)

    response = api_client.post("/api/planos/aporte", json=aporte_extra)

    mock_plano_service.validate_aporte_extra.assert_called_once_with(
        id_plano=aporte_extra_mock.id_plano, value=aporte_extra_mock.value
    )

    mock_plano_service.aporte_extra.assert_called_once_with(aporte_extra_mock)

    assert response.json()["id"] == str(id_operation)
    assert response.status_code == 200


def test_aporte_extra_api_invalid_data(api_client, mock_plano_service):
    id_plano = uuid4()
    aporte_extra = {"idPlano": str(id_plano), "valorAporte": "invalid"}

    response = api_client.post("/api/planos/aporte", json=aporte_extra)

    assert response.status_code == 422

    aporte_extra = {"idPlano": "invalid", "valorAporte": 1000}

    response = api_client.post("/api/planos/aporte", json=aporte_extra)

    assert response.status_code == 422


def test_retirada_api(api_client, mock_plano_service):
    id_plano = uuid4()
    aporte_extra = {"idPlano": str(id_plano), "valorResgate": 1000}

    plano_retirada_mock = PlanoRetirada(
        idPlano=id_plano,
        valorResgate=1000,
    )

    id_operation = uuid4()

    mock_plano_service.validate_retirada.return_value = True
    mock_plano_service.retirada.return_value = Mock(id=id_operation)

    response = api_client.post("/api/planos/retirada", json=aporte_extra)

    mock_plano_service.validate_retirada.assert_called_once_with(
        id_plano=plano_retirada_mock.id_plano, value=plano_retirada_mock.value
    )

    mock_plano_service.retirada.assert_called_once_with(plano_retirada_mock)

    assert response.json()["id"] == str(id_operation)
    assert response.status_code == 200


def test_retirada_api_invalid_data(api_client):
    id_plano = uuid4()
    aporte_extra = {"idPlano": str(id_plano), "valorResgate": "invalid"}

    response = api_client.post("/api/planos/retirada", json=aporte_extra)

    assert response.status_code == 422

    aporte_extra = {"idPlano": "invalid", "valorResgate": 1000}

    response = api_client.post("/api/planos/retirada", json=aporte_extra)

    assert response.status_code == 422
