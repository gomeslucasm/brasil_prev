from typing import Generic, TypeVar, Type, List
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class IRepository(Generic[ModelType]):
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
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def refresh(self, obj: ModelType):
        raise NotImplementedError
