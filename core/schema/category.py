import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.models import Category as CategoryModel
from core.models import CategoryConnector

category_connector = CategoryConnector()


class CategoryNode(SQLAlchemyObjectType):
    class Meta:
        model = CategoryModel
        interfaces = (relay.Node,)


class CreateCategory(graphene.Mutation):
    class Arguments:
        # TODO: max-length constraint
        name = graphene.String(required=True)

    Output = CategoryNode

    def mutate(self, _, name):
        """
        :param _:
        :param name:
        :return:
        """

        category = category_connector.create_category(name=name)
        category_node = CategoryNode.get_node(_, category.id)
        return category_node
