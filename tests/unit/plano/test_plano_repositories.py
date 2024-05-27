from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session
from api.plano.models import Plano, ProdutoPlano, PlanoOperation
from api.plano.repositories import PlanoDatabaseRepository
from api.plano.types import ProdutoData
from tests.fixtures.db import db
from tests.unit.plano.fixtures import *
from tests.unit.cliente.fixtures import *


def test_create_plano(db: Session, new_client, new_produto):

    repository = PlanoDatabaseRepository(db)

    produto_data = ProdutoData(
        id_produto=new_produto.id,
        nome=new_produto.nome,
        susep=new_produto.susep,
        expiracao_de_venda=new_produto.expiracao_de_venda,
        valor_minimo_aporte_inicial=new_produto.valor_minimo_aporte_inicial,
        valor_minimo_aporte_extra=new_produto.valor_minimo_aporte_extra,
        idade_de_entrada=new_produto.idade_de_entrada,
        idade_de_saida=new_produto.idade_de_saida,
        carencia_inicial_de_resgate=new_produto.carencia_inicial_de_resgate,
        carencia_entre_resgates=new_produto.carencia_entre_resgates,
    )

    plano = repository.create(
        id_cliente=new_client.id,
        produto_data=produto_data,
        aporte=2000,
        data_da_contratacao=datetime.now(),
        idade_de_aposentadoria=60,
    )

    assert plano.id is not None
    assert plano.aporte == 2000.0
    assert plano.produto_plano.nome == new_produto.nome
    assert plano.produto_plano.valor_minimo_aporte_inicial == 1000.0

    operations = (
        db.query(PlanoOperation).filter(PlanoOperation.id_plano == plano.id).all()
    )
    assert len(operations) == 1
    assert operations[0].operation_type == OperationType.CONTRATACAO
    assert operations[0].value == 2000.0


def test_aporte_extra(
    db: Session, create_plano_on_db, create_produto_on_db, get_plano_by_id
):
    produto = create_produto_on_db(
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

    aporte_inicial = 2000.0

    plano = create_plano_on_db(
        id_cliente=uuid4(),
        produto=produto,
        aporte=aporte_inicial,
        data_da_contratacao=datetime(year=2022, month=4, day=5),
        idade_de_aposentadoria=60,
    )

    repository = PlanoDatabaseRepository(db)
    valor_aporte = 500.0
    operation = repository.aporte_extra(id_plano=plano.id, value=valor_aporte)

    assert operation.id is not None
    assert operation.value == valor_aporte
    assert operation.operation_type == OperationType.APORTE

    updated_plano = get_plano_by_id(id_plano=plano.id)
    assert updated_plano
    assert updated_plano.aporte == aporte_inicial + valor_aporte


def test_resgate(
    db: Session, create_plano_on_db, create_produto_on_db, get_plano_by_id
):
    produto = create_produto_on_db(
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

    aporte_inicial = 2000.0

    plano = create_plano_on_db(
        id_cliente=uuid4(),
        produto=produto,
        aporte=aporte_inicial,
        data_da_contratacao=datetime(year=2022, month=4, day=5),
        idade_de_aposentadoria=60,
    )

    repository = PlanoDatabaseRepository(db)
    valor_resgate = 1000.0

    operation = repository.resgate(id_plano=plano.id, value=valor_resgate)

    assert operation.id is not None
    assert operation.value == valor_resgate
    assert operation.operation_type == OperationType.RESGATE

    updated_plano = get_plano_by_id(id_plano=plano.id)

    assert updated_plano
    assert updated_plano.aporte == aporte_inicial - valor_resgate


def test_get_plano_data(db: Session, create_plano_on_db, create_produto_on_db):
    produto = create_produto_on_db(
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

    plano = create_plano_on_db(
        id_cliente=uuid4(),
        produto=produto,
        aporte=2000.0,
        data_da_contratacao=datetime(year=2022, month=4, day=5),
        idade_de_aposentadoria=60,
    )

    repository = PlanoDatabaseRepository(db)
    plano_data = repository.get_plano_data(id_plano=plano.id)

    assert plano_data is not None
    assert plano_data.id == plano.id
    assert plano_data.produto_nome == produto.nome
    assert (
        plano_data.produto_valor_minimo_aporte_inicial
        == produto.valor_minimo_aporte_inicial
    )


def test_get_last_resgate(
    db: Session, create_plano_on_db, create_produto_on_db, create_plano_operation_on_db
):
    produto = create_produto_on_db(
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

    plano = create_plano_on_db(
        id_cliente=uuid4(),
        produto=produto,
        aporte=2000.0,
        data_da_contratacao=datetime(year=2022, month=4, day=5),
        idade_de_aposentadoria=60,
    )

    repository = PlanoDatabaseRepository(db)
    last_resgate = repository.get_last_resgate(id_plano=plano.id)

    assert not last_resgate

    create_plano_operation_on_db(
        id_plano=plano.id, value=100, operation_type=OperationType.APORTE
    )

    last_resgate = repository.get_last_resgate(id_plano=plano.id)

    assert not last_resgate

    create_plano_operation_on_db(
        id_plano=plano.id,
        value=100,
        operation_type=OperationType.RESGATE,
        created_on=datetime.now() + timedelta(days=1),
    )

    correct_last_resgate = create_plano_operation_on_db(
        id_plano=plano.id,
        value=100,
        operation_type=OperationType.RESGATE,
        created_on=datetime.now() + timedelta(days=2),
    )

    last_resgate = repository.get_last_resgate(id_plano=plano.id)

    assert last_resgate
    assert correct_last_resgate.id == last_resgate.id
