import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from core.models import Category as CategoryModel
from core.models import Diary as DiaryModel
from core.models import Note as NoteModel
from core.schema.category import CategoryNode, CreateCategory
from core.schema.diary import DiaryNode
from core.schema.note import NoteNode


class SearchResult(graphene.Union):
    class Meta:
        types = (CategoryNode, DiaryNode, NoteNode)


class RootQuery(graphene.ObjectType):
    node = relay.Node.Field()

    search = graphene.List(
        SearchResult, q=graphene.String()
    )  # List field for search results

    # Normal fields
    all_categories = SQLAlchemyConnectionField(CategoryNode.connection)
    all_diaries = SQLAlchemyConnectionField(DiaryNode.connection)
    all_notes = SQLAlchemyConnectionField(NoteNode.connection)

    def resolve_search(self, info, **args):
        """
        TODO: complete the function
        :param info:
        :param args:
        :return:
        """
        keyword = args.get("q")  # Search query

        # Get queries
        categories_query = CategoryNode.get_query(info)
        diaries_query = DiaryNode.get_query(info)
        notes_query = NoteNode.get_query(info)

        # Query categories
        categories = categories_query.filter(CategoryModel.name.contains(keyword)).all()

        # Query diaries
        diaries = diaries_query.filter(
            DiaryModel.topic.contains(keyword)
            | (DiaryModel.category.any(CategoryModel.name.contains(keyword)))
        ).all()

        # Query notes
        notes = notes_query.filter(
            NoteModel.text.contains(keyword)
            | (DiaryModel.note.any(NoteModel.text.contains(keyword)))
        ).all()

        return categories + diaries + notes  # Combine lists


class RootMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()


schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
    types=[CategoryNode, DiaryNode, NoteNode, SearchResult],
)
