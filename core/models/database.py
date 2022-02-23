from dataclasses import dataclass
from typing import List

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

    def save_objects(self, new_objects: List[Model]):
        """
        Save object to database.
        TODO: error handling?
        :param new_objects:
        :return:
        """
        database = self.get_database()
        database.session.add_all(new_objects)
        database.session.commit()

    def add_object(self, instance: Model):
        """
        Save object to database.
        :param instance:
        :return:
        """
        database = self.get_database()
        database.session.add(instance)
        database.session.commit()

    def delete_object(self, instance: Model):
        """
        Delete object from database.
        :param instance:
        :return:
        """
        database = self.get_database()
        database.session.delete(instance)
        database.session.commit()
