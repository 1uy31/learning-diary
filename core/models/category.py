from dataclasses import dataclass
from typing import List

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

    @property
    def not_editable_fields(self):
        return ["id", "created_at", "updated_at"]

@dataclass
class CategoryConnector:
    model = Category
    database_connector = DatabaseConnector()

    def create_category(self, **kwargs) -> Category:
        """
        :param kwargs:
        :return: Category object, which is just saved to DB.
        """
        for field in self.model().not_editable_fields:
            kwargs.pop(field, None)

        category = self.model(**kwargs)
        self.database_connector.save_objects([category])
        return category

    def update_category(self, primary_key: int, **kwargs) -> Category:
        """
        TODO: consider remove this kind of proxy
        Update Category object.
        :param primary_key:
        :param kwargs:
        :return:
        :raise: Exception if fail
        """
        return self.database_connector.update_object(self.model, primary_key, **kwargs)

    def delete_categories_by_ids(self, primary_keys: List[int]) -> int:
        """
        TODO: consider remove this kind of proxy
        Delete matched Category objects from database.
        :param primary_keys:
        :return: number of deleted objects
        :raise: Exception if fail
        """
        return self.database_connector.delete_objects_by_ids(self.model, primary_keys)

    def delete_category_by_name(self, name: str):
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
