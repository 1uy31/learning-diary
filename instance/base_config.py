class BaseConfig:
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@host:port/db_name"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
