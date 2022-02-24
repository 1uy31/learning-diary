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
    def test_update_category_mutation(self, test_client, category_factory):
        faked_category = category_factory(shallow=False, name="Test_Category")
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
