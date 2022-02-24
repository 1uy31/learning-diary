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
