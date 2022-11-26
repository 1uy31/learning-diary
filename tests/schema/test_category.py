class TestCategoryQuery:
    def test_category_query(self, test_client):
        from tests.models_factory import CategoryFactory

        CategoryFactory.create(name="Test_Category_B")
        CategoryFactory.create(name="Test_Category_A")
        res = test_client.execute(
            """
            query {
             categories(sort: NAME_ASC) {
                edges {
                  node { name }
                }
             }
            }"""
        )

        result = dict(res["data"]["categories"])
        names = list(map(lambda x: x["node"]["name"], result["edges"]))
        assert names == ["Test_Category_A", "Test_Category_B"]

    def test_category_diaries_query(self, test_client):
        from tests.models_factory import CategoryFactory, DiaryFactory

        category = CategoryFactory.create(name="Test_Category")
        diaries = [DiaryFactory.create(category=category) for _ in range(9)]
        created_topics = list(map(lambda x: x.topic, diaries))

        res = test_client.execute(
            """
            query {
             categories {
                edges {
                  node {
                    name,
                    diaries {
                      edges {
                        node { topic }
                      }
                  } }
                }
             }
            }"""
        )

        result = dict(res["data"]["categories"])
        first_category_node = result["edges"][0]["node"]
        category_name = first_category_node["name"]
        assert category_name == "Test_Category"
        returned_topics = list(
            map(lambda x: x["node"]["topic"], first_category_node["diaries"]["edges"])
        )
        assert returned_topics == created_topics


class TestCreateCategoryMutation:
    def test_create_category_mutation(self, test_client):
        variables = {
            "name": "Test_Category",
        }
        res = test_client.execute(
            """
            mutation($name: String!) {
             createCategory(name: $name) {
                id,
                createdAt,
                name
             }
            }""",
            None,
            None,
            variables,
        )

        result = dict(res["data"]["createCategory"])
        assert result["id"] is not None
        assert result["createdAt"] is not None
        assert result["name"] == "Test_Category"


class TestUpdateCategoryMutation:
    def test_update_category_mutation(self, test_client):
        from tests.models_factory import CategoryFactory

        faked_category = CategoryFactory.create(name="Test_Category")
        variables = {
            "primaryKey": faked_category.id,
            "name": "Renamed_Test_Category",
        }
        res = test_client.execute(
            """
            mutation($primaryKey: Int!, $name: String!) {
             updateCategory(primaryKey: $primaryKey, name: $name) {
                id,
                createdAt,
                updatedAt,
                name
             }
            }""",
            None,
            None,
            variables,
        )

        result = dict(res["data"]["updateCategory"])
        assert result["createdAt"] == faked_category.created_at.isoformat()
        assert result["updatedAt"] is not None
        assert result["name"] == "Renamed_Test_Category"
