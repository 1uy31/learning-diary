from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.models import Diary as DiaryModel


class DiaryNode(SQLAlchemyObjectType):
    class Meta:
        model = DiaryModel
        interfaces = (relay.Node,)
