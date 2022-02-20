import graphene

from core.schema import CategoryNode, DiaryNode, NoteNode


class SearchResult(graphene.Union):
    class Meta:
        types = (CategoryNode, DiaryNode, NoteNode)
