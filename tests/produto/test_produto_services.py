from api.produto.schemas import ProdutoCreate
from tests.produto.fixtures import *
from datetime import datetime
from uuid import uuid4


def test_create_produto_service(
    produto_service, mock_produto_repository, create_produto
):
    expiracao_de_venda = datetime(year=2021, month=1, day=1)
    produto_data = ProdutoCreate(
        nome="Brasilprev Produto",
        susep="15414900840201817",
        expiracaoDeVenda=expiracao_de_venda,
        valorMinimoAporteInicial=1000.0,
        valorMinimoAporteExtra=100.0,
        idadeDeEntrada=18,
        idadeDeSaida=60,
        carenciaInicialDeResgate=60,
        carenciaEntreResgates=30,
    )

    produto = create_produto(**produto_data.model_dump())

    mock_produto_repository.create.return_value = produto

    new_produto = produto_service.create_produto(produto_data)

    mock_produto_repository.create.assert_called_once_with(
        nome=produto_data.nome,
        susep=produto_data.susep,
        expiracaoDeVenda=produto_data.expiracaoDeVenda,
        valorMinimoAporteInicial=produto_data.valorMinimoAporteInicial,
        valorMinimoAporteExtra=produto_data.valorMinimoAporteExtra,
        idadeDeEntrada=produto_data.idadeDeEntrada,
        idadeDeSaida=produto_data.idadeDeSaida,
        carenciaInicialDeResgate=produto_data.carenciaInicialDeResgate,
        carenciaEntreResgates=produto_data.carenciaEntreResgates,
    )
    assert new_produto == produto
