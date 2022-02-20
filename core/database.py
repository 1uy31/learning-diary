from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy


def get_database() -> SQLAlchemy:
    """
    :return: object used for database operations.
    """
    if "database" not in g:
        g.database = current_app.extensions["migrate"].db  # pylint: disable=E0237

    return g.database


def close_database():
    """
    Close database connection.
    """
    database = g.pop("database", None)

    if database is not None:
        database.close()
