from typing import Generic, List, TypeVar
from sqlalchemy.orm import Session
from api.common.interfaces.repository import IRepository

ModelType = TypeVar("ModelType")


class BaseDatabaseRepository(Generic[ModelType], IRepository[ModelType]):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    def get_all(self, *args, **kwargs) -> List[ModelType]:
        raise NotImplementedError

    def create(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    def update(self, db: Session, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    def remove(self, *args, **kwargs) -> ModelType:
        raise NotImplementedError

    def add(self, obj: ModelType):
        self.db.add(obj)

    def commit(self):
        self.db.commit()

    def refresh(self, obj: ModelType):
        self.db.refresh(obj)
