import datetime

from py2neo.ogm import GraphObject, Property


class Person(GraphObject):
    """
        db model class for person
    """
    __primarykey__ = 'email'
    __primarylabel__ = 'Person'
    first_name = Property()
    last_name = Property()
    phone_number = Property()
    email = Property()
    address = Property()
    birthday = Property()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError("{0} is an unknown property".format(key))

    def find(self, graph):
        return Person.match(graph, self.email).first()

    def as_dict(self):
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'birthday': datetime.date.fromisoformat(str(self.birthday)),
        }

    @staticmethod
    def sort_list_as_dict(persons):
        person_dicts = [person.as_dict() for person in persons]
        return sorted(person_dicts, key=lambda k: k['email'])

    @staticmethod
    def all_properties():
        return Person(birthday='2019-10-12').as_dict().keys()
