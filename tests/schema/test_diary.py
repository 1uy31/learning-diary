from faker import Faker

fake = Faker()


class TestCreateDiaryMutation:
    def test_create_diary_mutation(self, test_client):
        from tests.models_factory import CategoryFactory

        category = CategoryFactory.create(name="Backend")
        source_url = fake.domain_name()
        review_count = fake.pyint()
        rate = fake.pyint()
        variables = {
            "topic": "Flask x Graphql x SQLAlchemy",
            "categoryId": category.id,
            "sourceUrl": source_url,
            "reviewCount": review_count,
            "rate": rate,
        }
        res = test_client.execute(
            """
            mutation($topic: String!, $categoryId: Int, $sourceUrl: String, $reviewCount: Int, $rate: Int) {
             createDiary
             (topic: $topic, categoryId: $categoryId, sourceUrl: $sourceUrl, reviewCount: $reviewCount, rate: $rate) {
                topic,
                sourceUrl,
                reviewCount,
                rate,
                category { name }
             }
            }""",
            None,
            None,
            variables,
        )

        result = dict(res["data"]["createDiary"])
        variables.pop("categoryId")
        for key in variables.keys():
            assert result[key] == variables[key]
        assert result["category"]["name"] == "Backend"


class TestUpdateDiaryMutation:
    def test_update_diary_mutation(self, test_client):
        from tests.models_factory import CategoryFactory, DiaryFactory

        init_diary = DiaryFactory.create()
        assert init_diary.topic.startswith("topic_")
        assert init_diary.category.name.startswith("category_")
        variables = {
            "primaryKey": init_diary.id,
            "topic": "Flask x Graphql x SQLAlchemy",
            "categoryId": CategoryFactory.create(name="New-Category").id,
        }
        res = test_client.execute(
            """
            mutation($primaryKey: Int!, $topic: String, $categoryId: Int, $sourceUrl: String, $reviewCount: Int,
            $rate: Int) {
             updateDiary
             (primaryKey: $primaryKey, topic: $topic, categoryId: $categoryId, sourceUrl: $sourceUrl,
             reviewCount: $reviewCount, rate: $rate) {
                topic,
                category { name }
             }
            }""",
            None,
            None,
            variables,
        )

        result = dict(res["data"]["updateDiary"])
        assert result["topic"] == "Flask x Graphql x SQLAlchemy"
        assert result["category"]["name"] == "New-Category"


class TestDeleteDiaryMutation:
    def test_delete_diary_mutation(self, test_client):
        from core.models import DiaryConnector
        from tests.models_factory import DiaryFactory

        connector = DiaryConnector()

        init_diary = DiaryFactory.create()
        # The object exists in DB:
        retrieved_diary = connector.database_helper.get_object_by_id(
            connector.model, init_diary.id
        )
        assert retrieved_diary == init_diary

        res = test_client.execute(
            """
            mutation($primaryKey: Int!) {
             deleteDiary
             (primaryKey: $primaryKey) {
                success
             }
            }""",
            None,
            None,
            {"primaryKey": init_diary.id},
        )

        result = dict(res["data"]["deleteDiary"])
        assert result["success"] is True

        # The object is no longer existed in DB:
        retrieved_diary = connector.database_helper.get_object_by_id(
            connector.model, init_diary.id
        )
        assert retrieved_diary is None
