import toml
from dotenv import dotenv_values
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from instance.base_config import BaseConfig

env_values = dotenv_values(".env")

CONFIG_ENV_MAPPER = {
    "development": "dev_config.toml",
    "testing": "test_config.toml",
    "production": "prod_config.toml",
}


def create_app(testing: bool = False) -> Flask:
    """
    Flask app factory.
    :param testing: if app is created for testing
    :return: Flask app instance
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(BaseConfig())

    flask_env = "testing" if testing else env_values.get("FLASK_ENV") or "production"
    config_file = CONFIG_ENV_MAPPER.get(flask_env) or ""
    app.config.from_file(config_file, load=toml.load)

    # For DB migration:
    database = SQLAlchemy(app)
    Migrate(app, database)

    return app
