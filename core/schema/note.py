import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from core.models import Note as NoteModel
from core.models import NoteConnector

note_connector = NoteConnector()


class NoteNode(SQLAlchemyObjectType):
    class Meta:
        model = NoteModel
        interfaces = (relay.Node,)


class CreateNote(graphene.Mutation):
    class Arguments:
        # TODO: constraints
        position = graphene.Int(required=True)
        diary_id = graphene.Int()
        text = graphene.String()
        image_url = graphene.String()
        source_url = graphene.String()

    Output = NoteNode

    def mutate(self, _, **kwargs) -> NoteNode:
        """
        :param _:
        :param kwargs:
        :return:
        """
        note = note_connector.database_helper.create_object(
            note_connector.model, **kwargs
        )
        note_node = NoteNode.get_node(_, note.id)
        return note_node


class UpdateNote(graphene.Mutation):
    class Arguments:
        # TODO: constraints
        primary_key = graphene.Int(required=True)
        position = graphene.Int()
        diary_id = graphene.Int()
        text = graphene.String()
        image_url = graphene.String()
        source_url = graphene.String()

    Output = NoteNode

    def mutate(self, _, **kwargs) -> NoteNode:
        """
        :param _:
        :param kwargs:
        :return:
        """
        primary_key = kwargs.pop("primary_key")
        note = note_connector.database_helper.update_object(
            note_connector.model, primary_key, **kwargs
        )
        note_node = NoteNode.get_node(_, note.id)
        return note_node


class DeleteNote(graphene.Mutation):
    class Arguments:
        primary_key = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, _, primary_key: int) -> NoteNode:
        """
        :param _:
        :param primary_key:
        :return:
        """
        # No need to raise error even if there is no matched object:
        note_connector.database_helper.delete_objects_by_ids(
            note_connector.model, [primary_key]
        )
        return DeleteNote(success=True)
