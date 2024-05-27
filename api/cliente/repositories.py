from datetime import datetime
from typing import Optional, Protocol
from uuid import UUID
from sqlalchemy.orm import Session
from api.common.bases.repository import BaseDatabaseRepository
from api.cliente.models import Client
from abc import ABC, abstractmethod


class IClientRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str | UUID) -> Optional[Client]: ...

    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Optional[Client]: ...

    @abstractmethod
    def create(
        self,
        *,
        cpf: str,
        nome: str,
        email: str,
        data_de_nascimento: datetime,
        genero: str,
        renda_mensal: float
    ) -> Client: ...


class ClientDatabaseRepository(BaseDatabaseRepository[Client]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: str | UUID) -> Optional[Client]:
        if isinstance(id, str):
            id = UUID(id)

        return self.db.query(Client).filter(Client.id == id).first()

    def get_by_cpf(self, cpf: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.cpf == cpf).first()

    def create(
        self,
        *,
        cpf: str,
        nome: str,
        email: str,
        data_de_nascimento: datetime,
        genero: str,
        renda_mensal: float
    ) -> Client:
        db_obj = Client(
            cpf=cpf,
            nome=nome,
            email=email,
            data_de_nascimento=data_de_nascimento,
            genero=genero,
            renda_mensal=renda_mensal,
        )
        self.add(db_obj)
        self.commit()
        self.refresh(db_obj)
        return db_obj
