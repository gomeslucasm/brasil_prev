import pytest
from datetime import datetime, timedelta
from api.common.errors import NotFoundError, ValidationError
from api.plano.schemas import PlanoAporteExtra, PlanoCreate, PlanoRetirada
from api.plano.services import PlanoService
from unittest.mock import Mock
from uuid import uuid4
from api.plano.entities import ProdutoData
from tests.unit.plano.fixtures import *
from tests.unit.produto.fixtures import *
from tests.unit.cliente.fixtures import *


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

    produto = Mock(
        id=plano_data.id_produto,
        expiracao_de_venda=datetime(2023, 1, 1),
        valor_minimo_aporte_inicial=1000.0,
        idade_de_entrada=18,
        idade_de_saida=65,
        nome="Produto Teste",
        susep="123456",
        valor_minimo_aporte_extra=100.0,
        carencia_inicial_de_resgate=30,
        carencia_entre_resgates=10,
    )

    cliente = Mock(id=uuid4(), data_de_nascimento=datetime(1980, 1, 1))

    mock_produto_repository.get_by_id.return_value = produto
    mock_client_repository.get_by_id.return_value = cliente
    mock_plano_repository.create.return_value = plano_data

    new_plano = service.create_plano(plano_data)

    assert new_plano == plano_data

    produto_data = ProdutoData(
        id_produto=produto.id,
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

    mock_produto_repository.get_by_id.return_value = produto
    mock_client_repository.get_by_id.return_value = None
    mock_plano_repository.create.return_value = plano_data

    with pytest.raises(NotFoundError, match="Cliente não encontrado."):
        new_plano = service.create_plano(plano_data)

    mock_produto_repository.get_by_id.return_value = None
    mock_client_repository.get_by_id.return_value = cliente
    mock_plano_repository.create.return_value = plano_data

    with pytest.raises(NotFoundError, match="Produto não encontrado."):
        new_plano = service.create_plano(plano_data)


def test_validate_plano():
    mock_plano_repository = Mock()
    mock_produto_repository = Mock()
    mock_cliente_repository = Mock()

    plano_service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_cliente_repository
    )

    produto = Mock(
        id=uuid4(),
        nome="Produto Teste",
        susep="123456",
        expiracao_de_venda=datetime(year=2023, month=1, day=1),
        valor_minimo_aporte_inicial=1000.0,
        valor_minimo_aporte_extra=100.0,
        idade_de_entrada=18,
        idade_de_saida=65,
        carencia_inicial_de_resgate=30,
        carencia_entre_resgates=10,
    )

    cliente = Client(
        id=uuid4(),
        data_de_nascimento=datetime(year=2000, month=1, day=1),
    )

    plano_data = PlanoCreate(
        idCliente=cliente.id,
        idProduto=produto.id,
        aporte=2000.0,
        dataDaContratacao=datetime(year=2022, month=4, day=5),
        idadeDeAposentadoria=60,
    )

    produto_data = plano_service.validate_plano(
        produto=produto, cliente=cliente, plano=plano_data
    )
    assert produto_data.id_produto == produto.id

    plano_data.data_da_contratacao = datetime(year=2024, month=1, day=1)
    with pytest.raises(
        ValidationError,
        match="Não é possível contratar um produto com prazo de venda expirado.",
    ):
        plano_service.validate_plano(produto=produto, cliente=cliente, plano=plano_data)

    plano_data.data_da_contratacao = datetime(year=2022, month=4, day=5)
    plano_data.aporte = 500.0
    with pytest.raises(
        ValidationError, match="O valor do aporte é menor que o valor mínimo permitido."
    ):
        plano_service.validate_plano(produto=produto, cliente=cliente, plano=plano_data)

    plano_data.aporte = 2000.0
    cliente.data_de_nascimento = datetime(year=2010, month=1, day=1)
    with pytest.raises(
        ValidationError, match="O cliente não atende à idade mínima de entrada."
    ):
        plano_service.validate_plano(produto=produto, cliente=cliente, plano=plano_data)

    cliente.data_de_nascimento = datetime(year=2000, month=1, day=1)
    plano_data.idade_de_aposentadoria = 70
    with pytest.raises(
        ValidationError,
        match="A idade de aposentadoria é maior que a idade máxima de saída.",
    ):
        plano_service.validate_plano(produto=produto, cliente=cliente, plano=plano_data)


def test_validate_aporte_extra():
    mock_plano_repository = Mock(spec=IPlanoRepository)
    mock_produto_repository = Mock()
    mock_cliente_repository = Mock()

    plano_service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_cliente_repository
    )

    id_plano = uuid4()

    plano_data = Mock(id=id_plano, produto_valor_minimo_aporte_extra=1000)

    mock_plano_repository.get_plano_data.return_value = plano_data

    with pytest.raises(
        ValidationError, match="O valor de aporte extra é menor que o permitido"
    ):
        plano_service.validate_aporte_extra(id_plano=id_plano, value=500)

    assert plano_service.validate_aporte_extra(id_plano=id_plano, value=1000)
    mock_plano_repository.get_plano_data.assert_called_with(id_plano=id_plano)
    assert plano_service.validate_aporte_extra(id_plano=id_plano, value=1500)
    mock_plano_repository.get_plano_data.assert_called_with(id_plano=id_plano)

    mock_plano_repository.get_plano_data.return_value = None

    with pytest.raises(Exception, match="Plano not found"):
        plano_service.validate_aporte_extra(id_plano=id_plano, value=1500)


def test_aporte_extra():
    mock_plano_repository = Mock(spec=IPlanoRepository)
    mock_produto_repository = Mock()
    mock_cliente_repository = Mock()

    plano_service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_cliente_repository
    )

    plano_aporte_extra = Mock(id_plano=uuid4(), value=1500)

    plano_service.aporte_extra(plano_aporte_extra)

    mock_plano_repository.aporte_extra.assert_called_once_with(
        id_plano=plano_aporte_extra.id_plano, value=plano_aporte_extra.value
    )


def test_validate_retirada():
    mock_plano_repository = Mock(spec=IPlanoRepository)
    mock_produto_repository = Mock()
    mock_cliente_repository = Mock()

    plano_service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_cliente_repository
    )

    id_plano = uuid4()

    plano_data = Mock(id=id_plano, aporte=1000)

    mock_plano_repository.get_plano_data.return_value = plano_data

    with pytest.raises(
        ValidationError, match="O valor de aporte é menor que o de resgate"
    ):
        plano_service.validate_retirada(id_plano=id_plano, value=1500)

    plano_data = Mock(
        id=id_plano,
        aporte=1000,
        produto_carencia_inicial_de_resgate=60,
        data_da_contratacao=(datetime.now() - timedelta(days=10)),
    )

    mock_plano_repository.get_plano_data.return_value = plano_data

    with pytest.raises(
        ValidationError,
        match=f"Ainda não é possível fazer resgatas devido ao tempo de carencia inicial de {plano_data.produto_carencia_inicial_de_resgate}",
    ):
        plano_service.validate_retirada(id_plano=id_plano, value=1000)

    plano_data = Mock(
        id=id_plano,
        aporte=1000,
        produto_carencia_inicial_de_resgate=60,
        produto_carencia_entre_resgates=20,
        data_da_contratacao=datetime.now() - timedelta(days=70),
    )

    mock_plano_repository.get_plano_data.return_value = plano_data
    mock_plano_repository.get_last_retirada.return_value = Mock(
        created_on=datetime.now()
        + timedelta(days=plano_data.produto_carencia_entre_resgates - 1),
    )

    with pytest.raises(
        ValidationError,
        match=f"Não é possível fazer o resgate por que o último resgate foi feito a menos de {plano_data.produto_carencia_entre_resgates} dias",
    ):
        plano_service.validate_retirada(id_plano=id_plano, value=1000)

    plano_data = Mock(
        id=id_plano,
        aporte=1000,
        produto_carencia_inicial_de_resgate=60,
        produto_carencia_entre_resgates=20,
        data_da_contratacao=datetime.now() - timedelta(days=70),
    )

    mock_plano_repository.get_plano_data.return_value = plano_data
    mock_plano_repository.get_last_retirada.return_value = None

    assert plano_service.validate_retirada(id_plano=id_plano, value=1000)

    plano_data = Mock(
        id=id_plano,
        aporte=1000,
        produto_carencia_inicial_de_resgate=10,
        produto_carencia_entre_resgates=20,
        data_da_contratacao=datetime.now() - timedelta(days=70),
    )

    mock_plano_repository.get_plano_data.return_value = plano_data
    mock_plano_repository.get_last_retirada.return_value = Mock(
        created_on=plano_data.data_da_contratacao
        + timedelta(days=plano_data.produto_carencia_entre_resgates + 1)
    )

    assert plano_service.validate_retirada(id_plano=id_plano, value=1000)


def test_retirada():
    mock_plano_repository = Mock(spec=IPlanoRepository)
    mock_produto_repository = Mock()
    mock_cliente_repository = Mock()

    plano_service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_cliente_repository
    )

    plano_service = PlanoService(
        mock_plano_repository, mock_produto_repository, mock_cliente_repository
    )

    aporte_extra = PlanoRetirada(idPlano=uuid4(), valorResgate=1000)

    plano_service.retirada(aporte_extra)
    mock_plano_repository.retirada.assert_called_once_with(
        id_plano=aporte_extra.id_plano, value=aporte_extra.value
    )
