from uuid import uuid4
from api.cliente.models import Client
from tests.fixtures.api import *
from api.cliente.schemas import ClientCreate
from tests.cliente.fixtures import *
from datetime import datetime


def test_register_client_api_success(
    mock_client_service,
    valid_cpf: str,
    valid_cpf_only_numbers: str,
    create_client,
    api_client,
):
    birth_date = datetime(year=1975, month=4, day=1)

    client_data = {
        "cpf": valid_cpf,
        "nome": "Test User",
        "email": "test@example.com",
        "genero": "feminino",
        "rendaMensal": 1000.0,
    }

    client = create_client(**{"data_de_nascimento": birth_date, **client_data})

    client.id = str(uuid4())

    mock_client_service.create_client.return_value = client

    response = api_client.post(
        "/api/clients",
        json={
            **client_data,
            "dataDeNascimento": birth_date.isoformat(),
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": str(mock_client_service.create_client.return_value.id)
    }

    mock_client_service.create_client.assert_called_once_with(
        ClientCreate(**{"dataDeNascimento": birth_date, **client_data})
    )

    # test other cpf format
    client_data = {
        "cpf": valid_cpf_only_numbers,
        "nome": "Test User",
        "email": "test@example.com",
        "genero": "feminino",
        "rendaMensal": 1000.0,
    }
    response = api_client.post(
        "/api/clients",
        json={
            **client_data,
            "dataDeNascimento": birth_date.isoformat(),
        },
    )
    assert response.status_code == 200


def test_register_client_api_invalid_cpf(api_client):
    client_data = {
        "cpf": "invalid_cpf",
        "nome": "Test User",
        "email": "test@example.com",
        "dataDeNascimento": "2000-01-01T00:00:00.000Z",
        "genero": "masculino",
        "rendaMensal": 1000.0,
    }

    response = api_client.post("/api/clients", json=client_data)
    assert response.status_code == 422
