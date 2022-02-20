from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.models import Category as CategoryModel


class CategoryNode(SQLAlchemyObjectType):
    class Meta:
        model = CategoryModel
        interfaces = (relay.Node,)
