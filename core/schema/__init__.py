import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from core.schema.category import CategoryNode, CreateCategory, UpdateCategory
from core.schema.diary import DiaryNode
from core.schema.note import NoteNode


class RootQuery(graphene.ObjectType):
    node = relay.Node.Field()

    categories = SQLAlchemyConnectionField(CategoryNode.connection)
    diaries = SQLAlchemyConnectionField(DiaryNode.connection)
    notes = SQLAlchemyConnectionField(NoteNode.connection)


class RootMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()


schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
    types=[CategoryNode, DiaryNode, NoteNode],
)
