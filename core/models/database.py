from dataclasses import dataclass

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

    def save_object_to_database(self, new_object: Model):
        """
        Save object to database.
        TODO: error handling?
        :param new_object:
        :return:
        """
        database = self.get_database()
        database.session.add(new_object)
        database.session.commit()
