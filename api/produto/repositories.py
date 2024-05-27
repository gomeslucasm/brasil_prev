from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from api.common.bases.repository import BaseDatabaseRepository
from api.produto.models import Produto
from datetime import datetime
from api.produto.models import Produto
from abc import ABC, abstractmethod


class IProdutoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str | UUID) -> Optional[Produto]: ...

    @abstractmethod
    def create(
        self,
        *,
        nome: str,
        susep: str,
        expiracao_de_venda: datetime,
        valor_minimo_aporte_inicial: float,
        valor_minimo_aporte_extra: float,
        idade_de_entrada: int,
        idade_de_saida: int,
        carencia_inicial_de_resgate: int,
        carencia_entre_resgates: int
    ) -> Produto: ...


class ProdutoDatabaseRepository(BaseDatabaseRepository[Produto]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: str | UUID) -> Optional[Produto]:
        if isinstance(id, str):
            id = UUID(id)
        return self.db.query(Produto).filter(Produto.id == id).first()

    def create(
        self,
        *,
        nome: str,
        susep: str,
        expiracao_de_venda: datetime,
        valor_minimo_aporte_inicial: float,
        valor_minimo_aporte_extra: float,
        idade_de_entrada: int,
        idade_de_saida: int,
        carencia_inicial_de_resgate: int,
        carencia_entre_resgates: int
    ) -> Produto:
        db_obj = Produto(
            nome=nome,
            susep=susep,
            expiracao_de_venda=expiracao_de_venda,
            valor_minimo_aporte_inicial=valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=valor_minimo_aporte_extra,
            idade_de_entrada=idade_de_entrada,
            idade_de_saida=idade_de_saida,
            carencia_inicial_de_resgate=carencia_inicial_de_resgate,
            carencia_entre_resgates=carencia_entre_resgates,
        )
        self.add(db_obj)
        self.commit()
        self.refresh(db_obj)
        return db_obj
