from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError


class TestCreateObject:
    def test_create_object_happy(self, app_with_fresh_database):
        with app_with_fresh_database.app_context():
            from core.models import Category
            from core.models.database import DatabaseConnector

            connector = DatabaseConnector()
            category = connector.create_object(Category, name="Test_Category")
            assert category.name == "Test_Category"
            assert category.id is not None
            assert category.created_at is not None
            assert category.updated_at is None

    def test_create_object_violates_unique_name_constraint(
        self, app_with_fresh_database
    ):
        with app_with_fresh_database.app_context():
            from core.models import Category
            from core.models.database import DatabaseConnector

            connector = DatabaseConnector()
            connector.create_object(Category, name="Test_Category")
            with pytest.raises(IntegrityError) as exc:
                connector.create_object(Category, name="Test_Category")
            assert "UniqueViolation" in str(exc.value)


class TestUpdateObject:
    def test_update_object_happy(self, app_with_fresh_database):
        with app_with_fresh_database.app_context():
            from core.models import Category
            from core.models.database import DatabaseConnector

            database = app_with_fresh_database.extensions["migrate"].db

            connector = DatabaseConnector()
            # Setup
            category = Category(name="Test_Category")
            database.session.add(category)
            database.session.commit()
            assert category.id is not None

            now = datetime.now()
            updated_category = connector.update_object(
                Category,
                category.id,
                name="New_Test_Category",
                dummy_field="This_Will_Be_Ignored",
                created_at=now,
            )
            assert updated_category.id == category.id
            assert updated_category.created_at == category.created_at
            assert updated_category.created_at != now
            assert updated_category.name == "New_Test_Category"
            assert updated_category.updated_at is not None

    def test_update_object_raises_not_exist(self, app_with_fresh_database):
        with app_with_fresh_database.app_context():
            from core.models import Category
            from core.models.database import DatabaseConnector

            connector = DatabaseConnector()
            with pytest.raises(Exception) as exc:
                connector.update_object(Category, 10, name="Test_Category")
            assert str(exc.value) == "There is no Category with ID 10."


class TestDeleteObject:
    def test_delete_objects_by_ids_happy(self, app_with_fresh_database):
        with app_with_fresh_database.app_context():
            from core.models import Category
            from core.models.database import DatabaseConnector

            database = app_with_fresh_database.extensions["migrate"].db

            connector = DatabaseConnector()

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
            number_of_del_objs = connector.delete_objects_by_ids(
                Category, [category.id for category in categories]
            )
            assert number_of_del_objs == 3
            for category in categories:
                retrieve_category = database.session.get(Category, category.id)
                assert retrieve_category is None

    def test_delete_objects_by_ids_return_0(self, app_with_fresh_database):
        with app_with_fresh_database.app_context():
            from core.models import Category
            from core.models.database import DatabaseConnector

            connector = DatabaseConnector()
            number_of_del_objs = connector.delete_objects_by_ids(
                Category, [i for i in range(9)]
            )
            assert number_of_del_objs == 0
