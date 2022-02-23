from dataclasses import dataclass
from typing import List, Tuple, Dict, Type

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

    def get_objects_by_ids(self, model_class: Type[Model], ids: Tuple[int]) -> List[Model]:
        database = self.get_database()
        return database.session.get(model_class, ids)

    def get_objects_by_params(self, model_class: Type[Model], params: Dict[any]) -> List[Model]:
        database = self.get_database()
        return database.session.get(model_class, params)

    def delete_object(self, instance: Model):
        """
        Delete object from database.
        :param instance:
        :return:
        """
        database = self.get_database()
        database.session.delete(instance)
        database.session.commit()
