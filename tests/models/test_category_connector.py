import pytest
from sqlalchemy.exc import IntegrityError

###
# Test set up must not rely on DatabaseConnector, as DatabaseConnector should be treated as helper class of
# CategoryConnector.
###


def test_create_category_happy(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import CategoryConnector

        connector = CategoryConnector()
        category = connector.database_connector.create_object(connector.model, name="Test_Category")
        assert category.name == "Test_Category"
        assert category.id is not None
        assert category.created_at is not None
        assert category.updated_at is None


def test_create_category_violates_unique_name_constraint(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import CategoryConnector

        connector = CategoryConnector()
        connector.database_connector.create_object(connector.model, name="Test_Category")
        with pytest.raises(IntegrityError) as exc:
            connector.database_connector.create_object(connector.model, name="Test_Category")
        assert "UniqueViolation" in str(exc.value)


def test_delete_category_by_name_happy(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import Category, CategoryConnector

        database = app_with_fresh_database.extensions["migrate"].db

        connector = CategoryConnector()

        # Setup
        category = Category(name="Test_Category")
        database.session.add(category)
        database.session.commit()
        assert category.id is not None

        # Test:
        connector.delete_category_by_name("Test_Category")
        retrieve_category = database.session.get(Category, category.id)
        assert retrieve_category is None


def test_delete_category_by_name_raises_not_exist(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import CategoryConnector

        connector = CategoryConnector()

        with pytest.raises(Exception) as exc:
            connector.delete_category_by_name("Test_Category")
        assert str(exc.value) == "There is no Category with name Test_Category."


def test_delete_category_by_ids_happy(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import Category, CategoryConnector

        database = app_with_fresh_database.extensions["migrate"].db

        connector = CategoryConnector()

        # Setup
        category1 = Category(name="Test_Category1")
        category2 = Category(name="Test_Category2")
        category3 = Category(name="Test_Category3")
        categories = [category1, category2, category3]
        database.session.add_all(categories)
        database.session.commit()
        for category in categories:
            assert category.id is not None

        # Test:
        number_of_del_objs = connector.delete_categories_by_ids(
            [category.id for category in categories]
        )
        assert number_of_del_objs == 3
        for category in categories:
            retrieve_category = database.session.get(Category, category.id)
            assert retrieve_category is None


def test_delete_category_by_ids_return_0(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import CategoryConnector

        connector = CategoryConnector()
        number_of_del_objs = connector.delete_categories_by_ids([i for i in range(9)])
        assert number_of_del_objs == 0
