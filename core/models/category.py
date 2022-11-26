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
    diaries = relationship("Diary", back_populates="category")

    def __str__(self):
        return f"<Category: {self.name}>"


@dataclass
class CategoryConnector:
    model = Category
    database_helper = DatabaseConnector()

    def delete_category_by_name(self, name: str) -> None:
        """
        Delete matched Category object from database.
        :param name:
        :return:
        :raise: Exception if fail
        """
        category = db.session.query(self.model).filter(self.model.name == name).first()
        if not category:
            raise Exception(f"There is no Category with name {name}.")
        db.session.delete(category)
        db.session.commit()
