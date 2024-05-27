import pytest
from datetime import datetime
from api.plano.schemas import PlanoCreate
from api.plano.services import PlanoService
from unittest.mock import Mock
from uuid import uuid4
from api.plano.entities import ProdutoData
from tests.plano.fixtures import *
from tests.produto.fixtures import *
from tests.cliente.fixtures import *


def test_create_plano_service(
    mock_plano_repository, mock_produto_repository, mock_client_repository
):
    service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_client_repository
    )

    plano_data = PlanoCreate(
        idCliente=uuid4(),
        idProduto=uuid4(),
        aporte=2000.0,
        dataDaContratacao=datetime(2022, 4, 5),
        idadeDeAposentadoria=60,
    )

    produto = Mock()
    produto.expiracao_de_venda = datetime(2023, 1, 1)
    produto.valor_minimo_aporte_inicial = 1000.0
    produto.idade_de_entrada = 18
    produto.idade_de_saida = 65
    produto.nome = "Produto Teste"
    produto.susep = "123456"
    produto.valor_minimo_aporte_extra = 100.0
    produto.carencia_inicial_de_resgate = 30
    produto.carencia_entre_resgates = 10

    cliente = Mock()
    cliente.data_de_nascimento = datetime(1980, 1, 1)

    mock_produto_repository.get_by_id.return_value = produto
    mock_client_repository.get_by_id.return_value = cliente
    mock_plano_repository.create.return_value = plano_data

    new_plano = service.create_plano(plano_data)

    assert new_plano == plano_data

    produto_data = ProdutoData(
        id_produto=plano_data.id_produto,
        nome=produto.nome,
        susep=produto.susep,
        expiracao_de_venda=produto.expiracao_de_venda,
        valor_minimo_aporte_inicial=produto.valor_minimo_aporte_inicial,
        valor_minimo_aporte_extra=produto.valor_minimo_aporte_extra,
        idade_de_entrada=produto.idade_de_entrada,
        idade_de_saida=produto.idade_de_saida,
        carencia_inicial_de_resgate=produto.carencia_inicial_de_resgate,
        carencia_entre_resgates=produto.carencia_entre_resgates,
    )

    mock_plano_repository.create.assert_called_once_with(
        id_cliente=plano_data.id_cliente,
        produto_data=produto_data,
        aporte=plano_data.aporte,
        data_da_contratacao=plano_data.data_da_contratacao,
        idade_de_aposentadoria=plano_data.idade_de_aposentadoria,
    )


def test_validate_plano_service(
    mock_plano_repository, mock_produto_repository, mock_client_repository
):
    service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_client_repository
    )

    plano_data = PlanoCreate(
        idCliente=uuid4(),
        idProduto=uuid4(),
        aporte=2000.0,
        dataDaContratacao=datetime(2022, 4, 5),
        idadeDeAposentadoria=60,
    )

    produto = Mock()
    produto.expiracao_de_venda = datetime(2023, 1, 1)
    produto.valor_minimo_aporte_inicial = 1000.0
    produto.idade_de_entrada = 18
    produto.idade_de_saida = 65
    produto.nome = "Produto Teste"
    produto.susep = "123456"
    produto.valor_minimo_aporte_extra = 100.0
    produto.carencia_inicial_de_resgate = 30
    produto.carencia_entre_resgates = 10

    cliente = Mock()
    cliente.data_de_nascimento = datetime(1980, 1, 1)

    mock_produto_repository.get_by_id.return_value = produto
    mock_client_repository.get_by_id.return_value = cliente

    produto_data = service.validate_plano(
        cliente=cliente, produto=produto, plano=plano_data
    )

    expected_produto_data = ProdutoData(
        id_produto=plano_data.id_produto,
        nome=produto.nome,
        susep=produto.susep,
        expiracao_de_venda=produto.expiracao_de_venda,
        valor_minimo_aporte_inicial=produto.valor_minimo_aporte_inicial,
        valor_minimo_aporte_extra=produto.valor_minimo_aporte_extra,
        idade_de_entrada=produto.idade_de_entrada,
        idade_de_saida=produto.idade_de_saida,
        carencia_inicial_de_resgate=produto.carencia_inicial_de_resgate,
        carencia_entre_resgates=produto.carencia_entre_resgates,
    )

    assert produto_data == expected_produto_data

    produto.expiracao_de_venda = datetime(2021, 1, 1)
    mock_produto_repository.get_by_id.return_value = produto
    with pytest.raises(
        Exception,
        match="Não é possível contratar um produto com prazo de venda expirado.",
    ):
        service.validate_plano(cliente=cliente, produto=produto, plano=plano_data)

    produto.expiracao_de_venda = datetime(2023, 1, 1)
    produto.valor_minimo_aporte_inicial = 3000.0
    mock_produto_repository.get_by_id.return_value = produto
    with pytest.raises(
        Exception, match="O valor do aporte é menor que o valor mínimo permitido."
    ):
        service.validate_plano(cliente=cliente, produto=produto, plano=plano_data)

    produto.valor_minimo_aporte_inicial = 1000.0
    cliente.data_de_nascimento = datetime(2010, 1, 1)
    mock_client_repository.get_by_id.return_value = cliente
    with pytest.raises(
        Exception, match="O cliente não atende à idade mínima de entrada."
    ):
        service.validate_plano(cliente=cliente, produto=produto, plano=plano_data)

    cliente.data_de_nascimento = datetime(1980, 1, 1)
    plano_data.idade_de_aposentadoria = 70
    with pytest.raises(
        Exception, match="A idade de aposentadoria é maior que a idade máxima de saída."
    ):
        service.validate_plano(cliente=cliente, produto=produto, plano=plano_data)
