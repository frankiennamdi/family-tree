import graphene

from db.model.person import Person
from db.repository.person_repository import PersonRepository
from views.model.person_schema import PersonSchema


class Query(graphene.ObjectType):
    updated_person = graphene.Field(PersonSchema)
    person = graphene.Field(lambda: PersonSchema, email=graphene.String())
    siblings = graphene.List(lambda: PersonSchema, email=graphene.String())
    cousins = graphene.List(lambda: PersonSchema, email=graphene.String())
    children = graphene.List(lambda: PersonSchema, email=graphene.String())
    parents = graphene.List(lambda: PersonSchema, email=graphene.String())
    grandparents = graphene.List(lambda: PersonSchema, email=graphene.String())

    def resolve_person(self, info, email):
        repository = PersonRepository(info.context.graph_db)
        person = repository.find(email)
        return PersonSchema(**person.as_dict())

    def resolve_parents(self, info, email):
        repository = PersonRepository(info.context.graph_db)
        return list_to_schema(repository.find_parents(email))

    def resolve_grandparents(self, info, email):
        repository = PersonRepository(info.context.graph_db)
        return list_to_schema(repository.find_grandparents(email))

    def resolve_siblings(self, info, email):
        repository = PersonRepository(info.context.graph_db)
        return list_to_schema(repository.find_siblings(email))

    def resolve_cousins(self, info, email):
        repository = PersonRepository(info.context.graph_db)
        return list_to_schema(repository.find_cousins(email))

    def resolve_children(self, info, email):
        repository = PersonRepository(info.context.graph_db)
        return list_to_schema(repository.find_children(email))


def list_to_schema(persons):
    person_dicts_sorted = Person.sort_list_as_dict(persons)
    return [PersonSchema(**person_dict) for person_dict in person_dicts_sorted]
