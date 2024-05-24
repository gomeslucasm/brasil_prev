from datetime import datetime
from typing import Protocol
from sqlalchemy.orm import Session
from api.common.bases.repository import BaseDatabaseRepository
from api.cliente.models import Client


class IClientRepository(Protocol):
    def __init__(self, db: Session): ...

    def get_by_id(self, id: int) -> Client: ...

    def get_by_cpf(self, cpf: str) -> Client: ...

    def create(
        self,
        *,
        cpf: str,
        nome: str,
        email: str,
        dataDeNascimento: datetime,
        genero: str,
        rendaMensal: float
    ) -> Client: ...


class ClientDatabaseRepository(BaseDatabaseRepository[Client]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: int) -> Client:
        return self.db.query(Client).filter(Client.id == id).first()

    def get_by_cpf(self, cpf: str) -> Client:
        return self.db.query(Client).filter(Client.cpf == cpf).first()

    def create(
        self,
        *,
        cpf: str,
        nome: str,
        email: str,
        dataDeNascimento: datetime,
        genero: str,
        rendaMensal: float
    ) -> Client:
        db_obj = Client(
            cpf=cpf,
            nome=nome,
            email=email,
            dataDeNascimento=dataDeNascimento,
            genero=genero,
            rendaMensal=rendaMensal,
        )
        self.add(db_obj)
        self.commit()
        self.refresh(db_obj)
        return db_obj
