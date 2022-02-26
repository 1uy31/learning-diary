import pytest
from graphene.test import Client

from core import create_app


@pytest.fixture(scope="session")
def app():
    """
    Flask app for testing, test database is created during setUp and deleted during tearDown.
    :return:
    """
    app = create_app(testing=True)
    with app.app_context():
        # TODO: better way to initialise testing database, especially unable to import * here.
        # This import is important for create_all() to create corresponding tables, which is very inconvenient!
        from core.models import Category, Diary, Note  # noqa: F401

        database = app.extensions["migrate"].db
        database.create_all()
        yield app
        # Everything after yield statement works as a teardown code
        database.session.remove()
        database.drop_all()


@pytest.fixture(scope="function")
def app_with_fresh_database(app):
    """
    Flask app for testing, all created objects during each test are deleted during tearDown.
    :param app:
    :return:
    """
    yield app
    with app.app_context():
        # TODO: better way to clean up objects between tests
        from core.models import Category, Diary, Note

        database = app.extensions["migrate"].db
        for model in [Category, Diary, Note]:
            database.session.query(model).delete()
        database.session.commit()


@pytest.fixture(scope="function")
def test_client(app_with_fresh_database):
    """
    Client for testing.
    :param app_with_fresh_database:
    :return:
    """
    with app_with_fresh_database.app_context():
        from core.schema import schema

        client = Client(schema)
        yield client
