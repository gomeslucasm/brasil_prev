from typing import Optional
from sqlalchemy.orm import Session
from api.common.bases.repository import BaseDatabaseRepository
from api.produto.models import Produto
from datetime import datetime
from typing import Protocol
from api.produto.models import Produto


class IProdutoRepository(Protocol):
    def get_by_id(self, id: int) -> Optional[Produto]: ...

    def create(
        self,
        *,
        nome: str,
        susep: str,
        expiracaoDeVenda: datetime,
        valorMinimoAporteInicial: float,
        valorMinimoAporteExtra: float,
        idadeDeEntrada: int,
        idadeDeSaida: int,
        carenciaInicialDeResgate: int,
        carenciaEntreResgates: int
    ) -> Produto: ...


class ProdutoDatabaseRepository(BaseDatabaseRepository[Produto]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: int) -> Optional[Produto]:
        return self.db.query(Produto).filter(Produto.id == id).first()

    def create(
        self,
        *,
        nome: str,
        susep: str,
        expiracaoDeVenda: datetime,
        valorMinimoAporteInicial: float,
        valorMinimoAporteExtra: float,
        idadeDeEntrada: int,
        idadeDeSaida: int,
        carenciaInicialDeResgate: int,
        carenciaEntreResgates: int
    ) -> Produto:
        db_obj = Produto(
            nome=nome,
            susep=susep,
            expiracaoDeVenda=expiracaoDeVenda,
            valorMinimoAporteInicial=valorMinimoAporteInicial,
            valorMinimoAporteExtra=valorMinimoAporteExtra,
            idadeDeEntrada=idadeDeEntrada,
            idadeDeSaida=idadeDeSaida,
            carenciaInicialDeResgate=carenciaInicialDeResgate,
            carenciaEntreResgates=carenciaEntreResgates,
        )
        self.add(db_obj)
        self.commit()
        self.refresh(db_obj)
        return db_obj
