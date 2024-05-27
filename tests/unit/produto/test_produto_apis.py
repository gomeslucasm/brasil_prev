from uuid import uuid4
from api.produto.models import Produto
from tests.fixtures.api import *
from api.produto.schemas import ProdutoCreate
from tests.unit.produto.fixtures import *
from datetime import datetime


def test_register_produto_api_success(
    mock_produto_service,
    create_produto,
    api_client,
):
    expiracao_de_venda = datetime(year=2021, month=1, day=1)

    produto_data = {
        "nome": "Brasilprev produto",
        "susep": "15414900840201817",
        "expiracaoDeVenda": expiracao_de_venda.isoformat(),
        "valorMinimoAporteInicial": 1000.0,
        "valorMinimoAporteExtra": 100.0,
        "idadeDeEntrada": 18,
        "idadeDeSaida": 60,
        "carenciaInicialDeResgate": 60,
        "carenciaEntreResgates": 30,
    }

    produto = create_produto(
        **{
            "nome": produto_data["nome"],
            "susep": produto_data["susep"],
            "expiracao_de_venda": produto_data["expiracaoDeVenda"],
            "valor_minimo_aporte_inicial": produto_data["valorMinimoAporteInicial"],
            "valor_minimo_aporte_extra": produto_data["valorMinimoAporteExtra"],
            "idade_de_entrada": produto_data["idadeDeEntrada"],
            "idade_de_saida": produto_data["idadeDeSaida"],
            "carencia_inicial_de_resgate": produto_data["carenciaInicialDeResgate"],
            "carencia_entre_resgates": produto_data["carenciaEntreResgates"],
        }
    )

    produto.id = str(uuid4())

    mock_produto_service.create_produto.return_value = produto

    response = api_client.post("/api/produtos", json=produto_data)
    assert response.status_code == 200
    assert response.json() == {"id": str(produto.id)}

    mock_produto_service.create_produto.assert_called_once_with(
        ProdutoCreate(**produto_data)
    )
