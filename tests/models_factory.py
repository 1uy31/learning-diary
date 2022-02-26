import factory
from faker import Faker
from flask import current_app

from core.models import Category, Diary, Note

fake = Faker()

with current_app.app_context():
    db = current_app.extensions["migrate"].db


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.fuzzy.FuzzyText(prefix="category_")


class NoteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Note
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    position = factory.fuzzy.FuzzyInteger(1, 50, 1)
    text = factory.fuzzy.FuzzyText(prefix="text_")
    image_url = factory.fuzzy.FuzzyText(length=30, prefix="https://image")
    source_url = factory.fuzzy.FuzzyText(length=30, prefix="https://source")


class DiaryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Diary
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    topic = factory.fuzzy.FuzzyText(prefix="topic_")
    category = factory.SubFactory(CategoryFactory)
    note = factory.SubFactory(NoteFactory)
    source_url = factory.fuzzy.FuzzyText(length=30, prefix="https://")
    review_count = factory.fuzzy.FuzzyInteger(0, 100, 1)
    rate = factory.fuzzy.FuzzyInteger(0, 5, 1)
