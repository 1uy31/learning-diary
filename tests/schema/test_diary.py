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
