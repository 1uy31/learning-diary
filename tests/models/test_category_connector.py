import pytest

###
# Test set up must not rely on DatabaseConnector, as DatabaseConnector should be treated as helper class of
# CategoryConnector.
###


class TestDeleteCategory:
    def test_delete_category_by_name_happy(self, app_with_fresh_database):
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

    def test_delete_category_by_name_raises_not_exist(self, app_with_fresh_database):
        with app_with_fresh_database.app_context():
            from core.models import CategoryConnector

            connector = CategoryConnector()

            with pytest.raises(Exception) as exc:
                connector.delete_category_by_name("Test_Category")
            assert str(exc.value) == "There is no Category with name Test_Category."
