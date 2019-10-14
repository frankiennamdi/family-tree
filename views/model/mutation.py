import graphene

from db.repository.person_repository import PersonRepository, RelationshipType
from views.model.person_schema import PersonAttributes, PersonSchema, CreatePersonAttributes


def input_to_dictionary(person_input):
    dictionary = {}
    for key in person_input:
        dictionary[key] = person_input[key]
    return dictionary


class InputRelationshipType(graphene.Enum):
    MARRIED = 1
    PARENT = 2


class UpdatePersonInput(graphene.InputObjectType, PersonAttributes):
    pass


class CreatePersonInput(graphene.InputObjectType, CreatePersonAttributes):
    pass


class BasePersonMutation(graphene.Mutation):
    success = graphene.Boolean()
    updated_person = graphene.Field(lambda: PersonSchema)

    def mutate(self, info, person_input):
        input_data = input_to_dictionary(person_input)
        repository = PersonRepository(info.context.graph_db)
        person = repository.update_or_create(input_data)
        return BasePersonMutation(updated_person=person, success=True)


class UpdatePerson(BasePersonMutation):
    class Arguments:
        person_input = UpdatePersonInput(required=True)


class CreatePerson(BasePersonMutation):
    class Arguments:
        person_input = CreatePersonInput(required=True)


class AddRelationship(graphene.Mutation):
    class Arguments:
        from_email = graphene.String(required=True)
        to_email = graphene.String(required=True)
        relationship_type = InputRelationshipType(required=True)

    success = graphene.Boolean()

    def mutate(self, info, **kwargs):
        from_email = kwargs.pop('from_email')
        to_email = kwargs.pop('to_email')
        relationship_type = kwargs.pop('relationship_type')
        repository = PersonRepository(info.context.graph_db)
        success = repository.add_relation(from_email, to_email, RelationshipType[
            InputRelationshipType.get(relationship_type).name])
        return AddRelationship(success=success)


class Mutations(graphene.ObjectType):
    update_person = UpdatePerson.Field()
    create_person = CreatePerson.Field()
    add_relationship = AddRelationship.Field()
