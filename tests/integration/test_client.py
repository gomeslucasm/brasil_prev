from tests.fixtures.api import api_client
from tests.fixtures.db import db
from api.common.errors import ValidationError
import pytest


def test_create_client_success(api_client):
    client_data = {
        "cpf": "974.703.670-39",
        "nome": "Test User",
        "email": "testuser55555555@example.com",
        "dataDeNascimento": "2000-01-01T00:00:00.000Z",
        "genero": "masculino",
        "rendaMensal": 5000.0,
    }
    response = api_client.post("/api/clients", json=client_data)

    assert response.status_code == 200
    assert "id" in response.json()


def test_create_client_error_cpf(api_client):
    client_data = {
        "cpf": "974.703.670-39",
        "nome": "Test User",
        "email": "testuser55555555@example.com",
        "dataDeNascimento": "2000-01-01T00:00:00.000Z",
        "genero": "masculino",
        "rendaMensal": 5000.0,
    }
    api_client.post("/api/clients", json=client_data)

    with pytest.raises(
        ValidationError,
        match=f"Client with this CPF=97470367039 already exists",
    ):
        api_client.post("/api/clients", json=client_data)
