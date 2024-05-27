from tests.fixtures.api import api_client
from tests.fixtures.db import db
from api.common.errors import ValidationError
import pytest


def test_create_product_success(api_client):
    product_data = {
        "nome": "Brasilprev Longo Prazo",
        "susep": "15414900840201817",
        "expiracaoDeVenda": "2021-01-01T12:00:00.000Z",
        "valorMinimoAporteInicial": 1000.0,
        "valorMinimoAporteExtra": 100.0,
        "idadeDeEntrada": 18,
        "idadeDeSaida": 60,
        "carenciaInicialDeResgate": 60,
        "carenciaEntreResgates": 30,
    }
    response = api_client.post("/api/produtos", json=product_data)

    assert response.status_code == 200
    assert "id" in response.json()
