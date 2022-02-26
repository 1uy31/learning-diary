import factory
from faker import Faker
from flask import current_app

from core.models import Category

fake = Faker()

with current_app.app_context():
    db = current_app.extensions["migrate"].db


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = fake.color_name()
