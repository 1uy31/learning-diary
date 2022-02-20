import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from core.models import Category as CategoryModel
from core.models import Diary as DiaryModel
from core.models import Note as NoteModel
from core.schema.category import CategoryNode
from core.schema.diary import DiaryNode
from core.schema.note import NoteNode
from core.schema.search import SearchResult


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
        q = args.get("q")  # Search query

        # Get queries
        categories_query = CategoryNode.get_query(info)
        diaries_query = DiaryNode.get_query(info)
        notes_query = NoteNode.get_query(info)

        # Query categories
        categories = categories_query.filter(CategoryModel.name.contains(q)).all()

        # Query diaries
        diaries = diaries_query.filter(
            DiaryModel.topic.contains(q)
            | (DiaryModel.category.any(CategoryModel.name.contains(q)))
        ).all()

        # Query notes
        notes = notes_query.filter(
            NoteModel.text.contains(q)
            | (DiaryModel.note.any(NoteModel.text.contains(q)))
        ).all()

        return categories + diaries + notes  # Combine lists


schema = graphene.Schema(
    query=RootQuery, types=[CategoryNode, DiaryNode, NoteNode, SearchResult]
)
