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

    def mutate(self, _, name: str) -> CategoryNode:
        """
        :param _:
        :param name:
        :return:
        """

        category = category_connector.database_helper.create_object(
            category_connector.model, name=name
        )
        category_node = CategoryNode.get_node(_, category.id)
        return category_node


class UpdateCategory(graphene.Mutation):
    class Arguments:
        # TODO: max-length constraint
        primary_key = graphene.Int(required=True)
        name = graphene.String(required=True)

    Output = CategoryNode

    def mutate(self, _, primary_key: int, name: str) -> CategoryNode:
        """
        :param _:
        :param primary_key:
        :param name:
        :return:
        """

        category = category_connector.database_helper.update_object(
            category_connector.model, primary_key, name=name
        )
        category_node = CategoryNode.get_node(_, category.id)
        return category_node
