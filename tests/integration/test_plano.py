from tests.fixtures.api import api_client
from tests.fixtures.db import db
from uuid import uuid4


def create_client(api_client, cpf):
    client_data = {
        "cpf": cpf,
        "nome": "Test User",
        "email": f"testuser{uuid4()}@example.com",
        "dataDeNascimento": "2000-01-01T00:00:00.000Z",
        "genero": "masculino",
        "rendaMensal": 5000.0,
    }
    response = api_client.post("/api/clients", json=client_data)
    assert response.status_code == 200
    return response.json()["id"]


def create_product(api_client):
    product_data = {
        "nome": "Brasilprev Longo Prazo",
        "susep": str(uuid4()).replace("-", ""),
        "expiracaoDeVenda": "2025-01-01T12:00:00.000Z",
        "valorMinimoAporteInicial": 1000.0,
        "valorMinimoAporteExtra": 100.0,
        "idadeDeEntrada": 18,
        "idadeDeSaida": 60,
        "carenciaInicialDeResgate": 60,
        "carenciaEntreResgates": 30,
    }
    response = api_client.post("/api/produtos", json=product_data)
    assert response.status_code == 200
    return response.json()["id"]


def test_create_plano_success(api_client):
    client_id = create_client(api_client, "974.703.670-39")
    product_id = create_product(api_client)

    plano_data = {
        "idCliente": client_id,
        "idProduto": product_id,
        "aporte": 2000.0,
        "dataDaContratacao": "2023-04-05T12:00:00.000Z",
        "idadeDeAposentadoria": 60,
    }
    response = api_client.post("/api/planos", json=plano_data)

    assert response.status_code == 200
    assert "id" in response.json()


def test_aporte_extra_success(api_client):
    client_id = create_client(api_client, "600.275.670-10")
    product_id = create_product(api_client)

    plano_data = {
        "idCliente": client_id,
        "idProduto": product_id,
        "aporte": 2000.0,
        "dataDaContratacao": "2023-04-05T12:00:00.000Z",
        "idadeDeAposentadoria": 60,
    }
    response = api_client.post("/api/planos", json=plano_data)
    assert response.status_code == 200
    plano_id = response.json()["id"]

    aporte_extra_data = {
        "idPlano": plano_id,
        "valorAporte": 500.0,
    }
    response = api_client.post("/api/planos/aporte", json=aporte_extra_data)
    assert response.status_code == 200
    assert "id" in response.json()


def test_retirada_success(api_client):
    client_id = create_client(api_client, "989.644.750-03")
    product_id = create_product(api_client)

    plano_data = {
        "idCliente": client_id,
        "idProduto": product_id,
        "aporte": 2000.0,
        "dataDaContratacao": "2023-04-05T12:00:00.000Z",
        "idadeDeAposentadoria": 60,
    }
    response = api_client.post("/api/planos", json=plano_data)
    assert response.status_code == 200
    plano_id = response.json()["id"]

    retirada_data = {
        "idPlano": plano_id,
        "valorResgate": 1000.0,
    }
    response = api_client.post("/api/planos/retirada", json=retirada_data)
    assert response.status_code == 200
    assert "id" in response.json()
