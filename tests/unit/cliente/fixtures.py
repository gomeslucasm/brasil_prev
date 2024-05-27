from typing import Callable, Optional
import pytest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session
from api.cliente.models import Client
from api.cliente.services import ClientService
from api.cliente.repositories import IClientRepository
from datetime import datetime
from tests.fixtures.db import *


@pytest.fixture
def create_client():
    def fn(
        *,
        cpf: str,
        nome: str,
        email: str,
        data_de_nascimento: datetime,
        genero: str,
        renda_mensal: float,
    ) -> Client:
        return Client(
            cpf=cpf,
            nome=nome,
            email=email,
            data_de_nascimento=data_de_nascimento,
            genero=genero,
            renda_mensal=renda_mensal,
        )

    return fn


@pytest.fixture
def create_client_on_db(
    db: Session, create_client: Callable[..., Client]
) -> Callable[..., Client]:
    def fn(
        *,
        cpf: str,
        nome: str,
        email: str,
        data_de_nascimento: datetime,
        genero: str,
        renda_mensal: float,
    ) -> Client:
        client = create_client(
            cpf=cpf,
            nome=nome,
            email=email,
            data_de_nascimento=data_de_nascimento,
            genero=genero,
            renda_mensal=renda_mensal,
        )
        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    return fn


@pytest.fixture
def new_client(create_client_on_db, delete_entity_on_db):
    birth_date = datetime(year=1975, month=4, day=1)
    client = create_client_on_db(
        cpf="12345678900",
        nome="Test User",
        email="test@example.com",
        data_de_nascimento=birth_date,
        genero="masculino",
        renda_mensal=1000.0,
    )

    yield client

    delete_entity_on_db(client)


@pytest.fixture
def get_client_on_db(db: Session) -> Callable[..., Optional[Client]]:
    def fn(
        *,
        id: Optional[int],
        cpf: Optional[int],
    ) -> Optional[Client]:
        query = db.query(Client)

        if id:
            query.filter(Client.id == id)
        elif cpf:
            query.filter(Client.cpf == cpf)
        else:
            raise Exception("Need cpf or id")

        return query.first()

    return fn


@pytest.fixture
def mock_client_repository():
    mock_repository = Mock(spec=IClientRepository)
    return mock_repository


@pytest.fixture
def client_service(mock_client_repository):
    return ClientService(client_repository=mock_client_repository)


@pytest.fixture
def mock_client_service():
    with patch("api.cliente.apis.ClientService") as mock:
        mock_service = mock.return_value
        yield mock_service


@pytest.fixture
def valid_cpf():
    return "814.444.612-73"


@pytest.fixture
def valid_cpf_only_numbers():
    return "81444461273"
