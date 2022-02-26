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

    def mutate(self, _, **kwargs):
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
