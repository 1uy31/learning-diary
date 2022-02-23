from dataclasses import dataclass
from typing import Dict, List, Type, Any

from flask import current_app, g
from flask_sqlalchemy import Model, SQLAlchemy


@dataclass
class DatabaseConnector:
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
        """
        database = self.get_database()
        database.session.add_all(instances)
        database.session.commit()

    def save_object(self, instance: Model):
        """
        Save object to database.
        :param instance:
        :return:
        """
        database = self.get_database()
        database.session.add(instance)
        database.session.commit()

    def get_object_by_id(self, model_class: Type[Model], primary_key: Any, **kwargs) -> Model:
        """
        :param model_class:
        :param primary_key:
        :param kwargs: other options documented in linked function of sqlalchemy.orm.session
        :return: object with matched primary key, of specific model.
        """
        database = self.get_database()
        return database.session.get(model_class, primary_key, **kwargs)

    def get_object_by_params(
        self, model_class: Type[Model], params: Dict[str, Any], **kwargs
    ) -> Model:
        """
        :param model_class:
        :param params:
        :param kwargs: other options documented in linked function of sqlalchemy.orm.session
        :return: matched object of specific model.
        """
        database = self.get_database()
        return database.session.get(model_class, params, **kwargs)

    def delete_object(self, instance: Model):
        """
        Delete object from database.
        :param instance:
        :return:
        """
        database = self.get_database()
        database.session.delete(instance)
        database.session.commit()
