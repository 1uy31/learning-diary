from dataclasses import dataclass
from typing import Any, List, Type

from flask import current_app, g
from flask_sqlalchemy import Model, SQLAlchemy


@dataclass
class DatabaseConnector:
    """
    Contain reusable helper functions for connector layer.
    Most of the functions do not have tests covered, as:
        - they only be used by model connectors
        - they should be tested already with model connectors (CategoryConnector, DiaryConnector, NoteConnector, etc.)
        - they act on abstract models, so testing them individually would anyway requires specific models
        like Category, etc.
    """

    def get_database(self) -> SQLAlchemy:
        """
        :return: object used for database operations.
        """
        if "database" not in g:
            g.database = current_app.extensions[  # pylint: disable=assigning-non-slot
                "migrate"
            ].db

        return g.database

    def close_database(self):
        """
        Close database connection.
        """
        database = g.pop("database", None)

        if database is not None:
            database.close()

    def save_objects(self, instances: List[Model]):
        """
        Save objects to database.
        :param instances:
        :return:
        :raise: Exception if fail
        """
        database = self.get_database()
        try:
            database.session.add_all(instances)
            database.session.commit()
        except Exception as exc:
            database.session.rollback()
            raise exc

    def update_object(self, model_class: Type[Model], primary_key: Any, **kwargs) -> Model:
        """
        Update object.
        :param model_class:
        :param primary_key:
        :param kwargs:
        :return: updated object
        :raise: Exception if fail
        """
        database = self.get_database()

        if getattr(type(model_class()), 'not_editable_fields', None):
            for field in model_class().not_editable_fields:
                kwargs.pop(field, None)

        instance = self.get_object_by_id(model_class, primary_key, with_for_update=True)
        if not instance:
            raise Exception(f"There is no {model_class} with ID {primary_key}.")
        update_fields = list(kwargs.keys())
        for field in update_fields:
            setattr(instance, field, kwargs.get(field))

        database.session.add(instance)
        database.session.commit()
        return instance

    def get_object_by_id(
        self, model_class: Type[Model], primary_key: Any, **kwargs
    ) -> Model:
        """
        :param model_class:
        :param primary_key:
        :param kwargs: other options documented in linked function of sqlalchemy.orm.session
        :return: object with matched primary key, of specific model.
        """
        database = self.get_database()
        return database.session.get(model_class, primary_key, **kwargs)

    def delete_objects_by_ids(
        self, model_class: Type[Model], primary_keys: List[Any]
    ) -> int:
        """
        Delete matched objects from database.
        :param model_class:
        :param primary_keys:
        :return: number of deleted objects
        :raise: Exception if fail
        """
        database = self.get_database()
        instances = (
            database.session.query(model_class)
            .filter(model_class.id.in_(primary_keys))
            .all()
        )
        try:
            for instance in instances:
                database.session.delete(instance)
            database.session.commit()
            return len(instances)
        except Exception as exc:
            database.session.rollback()
            raise exc
