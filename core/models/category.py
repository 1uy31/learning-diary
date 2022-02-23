from dataclasses import dataclass

from flask import current_app
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import ModelMixin, TimestampMixin
from .database import DatabaseConnector

with current_app.app_context():
    # Need to use db.Model for migrations to be detected.
    db = current_app.extensions["migrate"].db


class Category(ModelMixin, TimestampMixin, db.Model):  # type: ignore
    name = Column(String(256), nullable=False, unique=True)
    diaries = relationship("Diary")

    def __str__(self):
        return f"<Category: {self.name}>"


@dataclass
class CategoryConnector:
    database_connector = DatabaseConnector()

    def create_category(self, **kwargs) -> Category:
        """
        :param kwargs:
        :return: Category object, which is just saved to DB.
        """
        for field in ["id", "created_at", "updated_at"]:
            kwargs.pop(field, None)

        category = Category(**kwargs)
        self.database_connector.save_objects([category])
        return category
