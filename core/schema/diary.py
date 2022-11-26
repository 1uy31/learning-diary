import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.models import Diary as DiaryModel
from core.models import DiaryConnector

diary_connector = DiaryConnector()


class DiaryNode(SQLAlchemyObjectType):
    class Meta:
        model = DiaryModel
        interfaces = (relay.Node,)


class CreateDiary(graphene.Mutation):
    class Arguments:
        # TODO: constraints
        topic = graphene.String(required=True)
        category_id = graphene.Int()
        source_url = graphene.String()
        review_count = graphene.Int()
        rate = graphene.Int()

    Output = DiaryNode

    def mutate(self, _, **kwargs) -> DiaryNode:
        """
        :param _:
        :param kwargs:
        :return:
        """

        diary = diary_connector.database_helper.create_object(
            diary_connector.model, **kwargs
        )
        diary_node = DiaryNode.get_node(_, diary.id)
        return diary_node


class UpdateDiary(graphene.Mutation):
    class Arguments:
        # TODO: constraints
        primary_key = graphene.Int(required=True)
        topic = graphene.String()
        category_id = graphene.Int()
        source_url = graphene.String()
        review_count = graphene.Int()
        rate = graphene.Int()

    Output = DiaryNode

    def mutate(self, _, **kwargs) -> DiaryNode:
        """
        :param _:
        :param kwargs:
        :return:
        """
        primary_key = kwargs.pop("primary_key")
        diary = diary_connector.database_helper.update_object(
            diary_connector.model, primary_key, **kwargs
        )
        diary_node = DiaryNode.get_node(_, diary.id)
        return diary_node


class DeleteDiary(graphene.Mutation):
    class Arguments:
        primary_key = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, _, primary_key: int) -> DiaryNode:
        """
        :param _:
        :param primary_key:
        :return:
        """
        # No need to raise error even if there is no matched object:
        diary_connector.database_helper.delete_objects_by_ids(
            diary_connector.model, [primary_key]
        )
        return DeleteDiary(success=True)
