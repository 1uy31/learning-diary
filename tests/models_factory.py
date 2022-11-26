import factory
from factory import fuzzy
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


class DiaryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Diary
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    topic = fuzzy.FuzzyText(prefix="topic_")
    category = factory.SubFactory(CategoryFactory)
    source_url = fuzzy.FuzzyText(length=30, prefix="https://")
    review_count = fuzzy.FuzzyInteger(0, 100, 1)
    rate = fuzzy.FuzzyInteger(0, 5, 1)


class NoteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Note
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    diary = factory.SubFactory(DiaryFactory)
    position = factory.Sequence(lambda n: n + 1)
    text = fuzzy.FuzzyText(prefix="text_")
    image_url = fuzzy.FuzzyText(length=30, prefix="https://image")
    source_url = fuzzy.FuzzyText(length=30, prefix="https://source")
