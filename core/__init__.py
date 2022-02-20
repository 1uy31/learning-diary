from dotenv import dotenv_values
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from instance.config import DefaultConfig

env_values = dotenv_values(".env")


def create_app(testing: bool = False) -> Flask:
    """
    Flask app factory.
    :param testing: if app is created for testing
    :return: Flask app instance
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(DefaultConfig())

    config_file = (
        "dev_config.py"
        if env_values.get("FLASK_ENV", "production") == "development"
        else "prod_config.py"
    )
    if testing:
        config_file = "test_config.py"

    app.config.from_pyfile(config_file, silent=True)

    # For DB migration:
    database = SQLAlchemy(app)
    Migrate(app, database)

    return app
