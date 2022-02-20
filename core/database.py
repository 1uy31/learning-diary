from typing import Union

from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

from core.models import Category, Diary, Note


def get_database() -> SQLAlchemy:
    """
    :return: object used for database operations.
    """
    if "database" not in g:
        g.database = current_app.extensions["migrate"].db  # pylint: disable=assigning-non-slot

    return g.database


def close_database():
    """
    Close database connection.
    """
    database = g.pop("database", None)

    if database is not None:
        database.close()


def save_object_to_database(new_object: Union[Category, Diary, Note]):
    """
    Save object to database.
    TODO: error handling?
    """
    database = get_database()
    database.session.add(new_object)
    database.session.commit()
