from sqlalchemy import DateTime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import mapped_column
from api.infra.db import Base


class BaseDBModel(Base):

    __abstract__ = True

    created_on = mapped_column(DateTime, server_default=now())
    updated_on = mapped_column(DateTime, server_default=now(), onupdate=now())
    deleted_on = mapped_column(DateTime, nullable=True, default=None)
