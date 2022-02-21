from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declared_attr


class ModelMixin:
    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return cls.__name__.lower()  # type: ignore

    id = Column(Integer, primary_key=True)


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
