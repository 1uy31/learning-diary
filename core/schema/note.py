from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.models import Note as NoteModel


class NoteNode(SQLAlchemyObjectType):
    class Meta:
        model = NoteModel
        interfaces = (relay.Node,)
