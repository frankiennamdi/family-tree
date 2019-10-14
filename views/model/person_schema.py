import graphene


class PersonAttributes:
    email = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    phone_number = graphene.String()
    address = graphene.String()
    birthday = graphene.String()


class CreatePersonAttributes:
    email = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    address = graphene.String(required=True)
    birthday = graphene.String(required=True)


class PersonSchema(graphene.ObjectType, PersonAttributes):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
