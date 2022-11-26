from typing import Generator

import pytest
from flask import Flask
from graphene.test import Client

from core import create_app


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    """
    Flask app for testing, database tables are created during setUp and deleted during tearDown.
    :return:
    """
    app = create_app(testing=True)
    with app.app_context():
        # This import is important for create_all() to create all tables
        import core.models  # noqa: F401

        database = app.extensions["migrate"].db
        database.create_all()
        yield app
        # Everything after yield statement works as a teardown code
        database.session.remove()
        database.drop_all()


@pytest.fixture(scope="function")
def app_with_fresh_database(app: Flask) -> Generator[Flask, None, None]:
    """
    Flask app for testing, all created objects during each test are deleted during tearDown.
    :param app:
    :return:
    """
    yield app
    with app.app_context():
        database = app.extensions["migrate"].db
        database.session.execute(
            """
            DO $$
              DECLARE
                r RECORD;
            BEGIN
              FOR r IN
                (
                  SELECT table_name
                  FROM information_schema.tables
                  WHERE table_schema = current_schema()
                )
              LOOP
                 EXECUTE 'TRUNCATE ' || quote_ident(r.table_name) || ' CASCADE';
              END LOOP;
            END $$ ;
            """
        )
        database.session.commit()


@pytest.fixture(scope="function")
def test_client(app_with_fresh_database: Flask) -> Generator[Client, None, None]:
    """
    Client for testing.
    :param app_with_fresh_database:
    :return:
    """
    with app_with_fresh_database.app_context():
        from core.schema import schema

        client = Client(schema)
        yield client
