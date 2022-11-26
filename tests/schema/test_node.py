from faker import Faker

fake = Faker()


class TestCreateNoteMutation:
    def test_create_note_mutation(self, test_client):
        from tests.models_factory import DiaryFactory

        diary = DiaryFactory.create()
        position = fake.pyint()
        text = fake.pystr()
        source_url = fake.domain_name()
        image_url = fake.domain_name()
        variables = {
            "position": position,
            "diaryId": diary.id,
            "sourceUrl": source_url,
            "imageUrl": image_url,
            "text": text,
        }
        res = test_client.execute(
            """
            mutation($position: Int!, $diaryId: Int, $sourceUrl: String, $imageUrl: String, $text: String) {
             createNote
             (position: $position, diaryId: $diaryId, sourceUrl: $sourceUrl, imageUrl: $imageUrl, text: $text) {
                imageUrl,
                sourceUrl,
                text,
                position,
                diary { topic }
             }
            }""",
            None,
            None,
            variables,
        )

        result = dict(res["data"]["createNote"])
        variables.pop("diaryId")
        for key in variables.keys():
            assert result[key] == variables[key]
        assert result["diary"]["topic"] == diary.topic


class TestUpdateNoteMutation:
    def test_update_note_mutation(self, test_client):
        from tests.models_factory import DiaryFactory, NoteFactory

        init_note = NoteFactory.create()
        diary = DiaryFactory.create()
        assert init_note.diary != diary
        assert init_note.text.startswith("text_")
        assert init_note.image_url.startswith("https://")
        assert init_note.source_url.startswith("https://")

        variables = {
            "primaryKey": init_note.id,
            "diaryId": diary.id,
            "sourceUrl": "new_source",
            "imageUrl": "new_image",
            "text": "new_text",
        }
        res = test_client.execute(
            """
            mutation($primaryKey: Int!, $position: Int, $diaryId: Int, $sourceUrl: String, $imageUrl: String,
             $text: String) {
             updateNote
             (primaryKey: $primaryKey, position: $position, diaryId: $diaryId, sourceUrl: $sourceUrl,
              imageUrl: $imageUrl, text: $text) {
                imageUrl,
                sourceUrl,
                text,
                position,
                diary { topic }
             }
            }""",
            None,
            None,
            variables,
        )

        result = dict(res["data"]["updateNote"])
        assert result["diary"]["topic"] == diary.topic
        assert result["sourceUrl"] == "new_source"
        assert result["imageUrl"] == "new_image"
        assert result["text"] == "new_text"
        assert result["position"] == init_note.position


class TestDeleteNoteMutation:
    def test_delete_note_mutation(self, test_client):
        from core.models import NoteConnector
        from tests.models_factory import NoteFactory

        connector = NoteConnector()

        init_note = NoteFactory.create()
        # The object exists in DB:
        retrieved_note = connector.database_helper.get_object_by_id(
            connector.model, init_note.id
        )
        assert retrieved_note == init_note

        res = test_client.execute(
            """
            mutation($primaryKey: Int!) {
             deleteNote
             (primaryKey: $primaryKey) {
                success
             }
            }""",
            None,
            None,
            {"primaryKey": init_note.id},
        )

        result = dict(res["data"]["deleteNote"])
        assert result["success"] is True

        # The object is no longer existed in DB:
        retrieved_note = connector.database_helper.get_object_by_id(
            connector.model, init_note.id
        )
        assert retrieved_note is None
