import pytest
from sqlalchemy.exc import IntegrityError


def test_create_category_happy(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import CategoryConnector

        connector = CategoryConnector()
        category = connector.create_category(name="Test_Category")
        assert category.name == "Test_Category"
        assert category.id is not None
        assert category.created_at is not None
        assert category.updated_at is None


def test_create_category_violates_unique_name_constraint(app_with_fresh_database):
    with app_with_fresh_database.app_context():
        from core.models import CategoryConnector

        connector = CategoryConnector()
        connector.create_category(name="Test_Category")
        with pytest.raises(IntegrityError) as exc:
            connector.create_category(name="Test_Category")
        assert "UniqueViolation" in str(exc.value)
