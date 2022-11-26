import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from core.schema.category import CategoryNode, CreateCategory, UpdateCategory
from core.schema.diary import CreateDiary, DeleteDiary, DiaryNode, UpdateDiary
from core.schema.note import CreateNote, DeleteNote, NoteNode, UpdateNote


class RootQuery(graphene.ObjectType):
    node = relay.Node.Field()

    categories = SQLAlchemyConnectionField(CategoryNode.connection)
    diaries = SQLAlchemyConnectionField(DiaryNode.connection)
    notes = SQLAlchemyConnectionField(NoteNode.connection)


class RootMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    create_diary = CreateDiary.Field()
    update_diary = UpdateDiary.Field()
    delete_diary = DeleteDiary.Field()
    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()
    delete_note = DeleteNote.Field()


schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
    types=[CategoryNode, DiaryNode, NoteNode],
)
