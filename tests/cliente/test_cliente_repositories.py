from typing import Callable
from api.cliente.models import Client
from api.cliente.repositories import ClientDatabaseRepository
from datetime import datetime
from tests.cliente.fixtures import *
from tests.fixtures.db import *


def test_create_client(db, delete_entity_on_db, valid_cpf_only_numbers: str):
    repository = ClientDatabaseRepository(db)
    birth_date = datetime(year=1996, month=11, day=11)
    client_data = {
        "cpf": valid_cpf_only_numbers,
        "nome": "Test User",
        "email": "test@example.com",
        "data_de_nascimento": birth_date,
        "genero": "masculino",
        "renda_mensal": 1000.0,
    }
    client = repository.create(**client_data)
    assert client.cpf == client_data["cpf"]
    assert client.nome == client_data["nome"]
    assert client.email == client_data["email"]
    assert (
        client.data_de_nascimento.isoformat()
        == client_data["data_de_nascimento"].isoformat()
    )
    assert client.genero == client_data["genero"]
    assert client.renda_mensal == client_data["renda_mensal"]

    delete_entity_on_db(client)


def test_get_client_by_cpf(db, new_client):
    repository = ClientDatabaseRepository(db)
    client = repository.get_by_cpf(cpf=new_client.cpf)
    assert client.cpf == new_client.cpf
    assert client.id == new_client.id


def test_get_client_by_id(db, new_client):
    repository = ClientDatabaseRepository(db)
    client = repository.get_by_id(id=new_client.id)
    assert client
    assert client.id == new_client.id
