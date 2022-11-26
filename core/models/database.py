import uuid
from dataclasses import dataclass
from typing import Any, List, Type

from flask import current_app, g
from flask_sqlalchemy import Model, SQLAlchemy

PRIMARY_KEY_TYPE = int | str | uuid.UUID


@dataclass
class DatabaseConnector:
    """
    Contain reusable helper functions for connector layer.
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

    def create_objects(self, instances: List[Model]):
        """
        Bulk create objects to database.
        :param instances:
        :return:
        :raise: Exception if fail
        """
        database = self.get_database()
        # The Session, whenever it is used to talk to the database,
        # begins a database transaction as soon as it starts communicating.
        # This transaction remains in progress until the Session is rolled back, committed, or closed.

        # The Session will begin a new transaction if it is used again, subsequent to the previous transaction ending;
        # from this it follows that the Session is capable of having a lifespan across many transactions,
        # though only one at a time.
        try:
            database.session.add_all(instances)
            database.session.commit()
        except Exception as exc:
            database.session.rollback()
            raise exc

    def create_object(self, model_class: Type[Model], **kwargs) -> Model:
        """
        Create new object.
        :param model_class:
        :param kwargs:
        :return:
        :raise: Exception if fail
        """
        database = self.get_database()

        instance = model_class(**kwargs)
        database.session.add(instance)
        database.session.commit()
        return instance

    def update_object(
        self, model_class: Type[Model], primary_key: PRIMARY_KEY_TYPE, **kwargs
    ) -> Model:
        """
        Update object.
        :param model_class:
        :param primary_key:
        :param kwargs:
        :return: updated object
        :raise: Exception if fail
        """
        database = self.get_database()

        instance = self.get_object_by_id(model_class, primary_key, with_for_update=True)
        if not instance:
            raise Exception(
                f"There is no {model_class.__name__} with ID {primary_key}."
            )
        update_fields = list(kwargs.keys())
        for field in update_fields:
            setattr(instance, field, kwargs.get(field))

        database.session.add(instance)
        database.session.commit()
        return instance

    def get_object_by_id(
        self, model_class: Type[Model], primary_key: PRIMARY_KEY_TYPE, **kwargs
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
        self, model_class: Type[Model], primary_keys: List[PRIMARY_KEY_TYPE]
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
        except Exception as exc:
            database.session.rollback()
            raise exc

        return len(instances)
