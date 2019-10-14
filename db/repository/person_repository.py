import logging
from enum import Enum

from py2neo import Node, Relationship

from db.model.person import Person
from db.model.person_input_validator import PersonInputValidator, ValidationResult


class RelationshipType(Enum):
    MARRIED = 1
    PARENT = 2


class InvalidUpdateOperation(Exception):
    pass


class PersonRepository:
    """
     data access for person
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, graph):
        self._graph = graph

    def relative(self, email):
        return self.find_grandparents(email) + self.find_children(email) + \
               self.find_parents(email) + self.find_cousins(email) + \
               self.find_siblings(email)

    def add_relation(self, from_person_email, to_person_email, relationship_type):
        print(relationship_type.name)
        exiting_relationship = self.check_related(from_person_email, to_person_email)
        has_current_relationship = exiting_relationship[0]
        if has_current_relationship:
            raise InvalidUpdateOperation("{} and {} are in the same family tree".format(from_person_email, to_person_email))

        if relationship_type == RelationshipType.MARRIED:
            partner_query = f"MATCH (person:Person {{email:'{from_person_email}'}})-[:MARRIED]-(partner) " \
                            f"RETURN partner UNION MATCH (person:Person {{email:'{to_person_email}'}})-[:MARRIED]-(partner) " \
                            f"RETURN partner"
            partners = self._scan_result_set(self._graph.run(partner_query))
            if len(partners) > 0:
                raise InvalidUpdateOperation("{} or {} are in currently married".format(from_person_email, to_person_email))

        relationship = Relationship.type(relationship_type.name)
        tx = self._graph.begin()
        from_node = Node("Person", **exiting_relationship[1].as_dict())
        to_node = Node("Person", **exiting_relationship[2].as_dict())
        new_relationship = relationship(from_node, to_node)
        tx.merge(new_relationship, Person.__primarylabel__, Person.__primarykey__)
        tx.push(new_relationship)
        tx.commit()
        return True

    def check_related(self, from_person_email, to_person_email):
        """
        check if two person have any relatives in common
        """
        from_person = self.find(from_person_email)
        to_person = self.find(to_person_email)
        if not from_person:
            raise ValueError("person with {} email does not exist.".format(from_person_email))

        if not to_person:
            raise ValueError("person with {} email does not exist.".format(to_person_email))

        from_person_relatives_emails = [person.email for person in self.relative(from_person_email)]
        to_person_relatives_emails = [person.email for person in self.relative(to_person_email)]
        is_related = len(set(from_person_relatives_emails).intersection(set(to_person_relatives_emails))) > 0
        return is_related, from_person, to_person

    def update_or_create(self, person_input_dict):
        email_validation_result = PersonInputValidator.validate_email(**person_input_dict)
        if email_validation_result == ValidationResult.ABSENT or \
                email_validation_result == ValidationResult.INVALID:
            self._logger.warning("valid email is required to insert or update person")
            raise ValueError("valid email is required to insert or update person")

        birthday_validation_result = PersonInputValidator.validate_birthday(**person_input_dict)
        if not birthday_validation_result.ABSENT and birthday_validation_result.INVALID:
            self._logger.warning("provided birthday must be valid iso date")
            raise ValueError("provided birthday must be valid iso date")

        person = self.find(person_input_dict['email'])
        property_dict = {}
        if not person:
            properties_validation = PersonInputValidator.has_all_properties(**person_input_dict)
            if len(properties_validation) > 0:
                properties = Person.all_properties()
                self._logger.warning("new person requires all properties: " + ",".join(properties))
                raise ValueError("new person requires all properties: " + ",".join(properties))
        else:
            property_dict = person.as_dict()

        for key, value in person_input_dict.items():
            property_dict[key] = value
        tx = self._graph.begin()
        node = Node("Person", **property_dict)
        tx.merge(node, Person.__primarylabel__, Person.__primarykey__)
        tx.push(node)
        tx.commit()
        return self.find(property_dict['email'])

    def find(self, email):
        person = Person(email=email).find(self._graph)
        return person

    def find_list(self, emails):
        return [self.find(email) for email in emails]

    def find_parents(self, email):
        cousins_query = f"MATCH (person:Person{{email:'{email}'}})<-[:PARENT]-(parent) RETURN parent " \
                        f"UNION MATCH (person:Person{{email:'{email}'}})<-[:PARENT]-(by_marriage)-" \
                        f"[:MARRIED]-(parent) RETURN parent"
        return self._scan_result_set(self._graph.run(cousins_query))

    def find_grandparents(self, email):
        cousins_query = f"MATCH (person:Person{{email:'{email}'}})<-[:PARENT*2]-(grandparent) " \
                        f"RETURN grandparent UNION MATCH " \
                        f"(person:Person{{email:'{email}'}})<-[:PARENT*2]-" \
                        f"(grand_by_marriage)-[:MARRIED]-(grandparent) RETURN grandparent"
        return self._scan_result_set(self._graph.run(cousins_query))

    def find_cousins(self, email):
        cousins_query = f"MATCH (person:Person{{email:'{email}'}})<-[:PARENT*2]-(grandparent)-[:PARENT]->" \
                        f"(sibling)-[:MARRIED]->(partner)<-[:PARENT]-(partner_parents)-[:PARENT]->(partner_sibling)-" \
                        f"[:PARENT]->(cousins) RETURN cousins UNION MATCH (person:Person{{email:'{email}'}})" \
                        f"<-[:PARENT*2]-(grandparent), (grandparent)-[:PARENT]->(sibling)-[:PARENT]->(cousins) RETURN cousins"
        return self._scan_result_set(self._graph.run(cousins_query))

    def find_children(self, email):
        children_query = f"MATCH (person:Person{{email:'{email}'}})-[:MARRIED]-(partner)-[:PARENT]->(children) " \
                         f"RETURN children UNION MATCH (person:Person{{email:'{email}'}})-[:PARENT]->(children) " \
                         f"RETURN children"
        return self._scan_result_set(self._graph.run(children_query))

    def find_siblings(self, email):
        siblings_query = f"MATCH (person:Person{{email:'{email}'}})<-[:PARENT]-(parent)-[:PARENT]->(sibling) " \
                         f"RETURN sibling UNION MATCH (person:Person{{email:'{email}'}})<-[:PARENT]" \
                         f"-(parent)-[:MARRIED]-(partner)-[:PARENT]->(sibling) " \
                         f"WHERE NOT(sibling.email = '{email}') RETURN  sibling"
        return self._scan_result_set(self._graph.run(siblings_query))

    def _scan_result_set(self, result_set):
        result = []
        while result_set.forward():
            current = result_set.current
            for value in current.values():
                result.append(Person(email=value['email'],
                                     first_name=value['first_name'],
                                     last_name=value['last_name'],
                                     phone_number=value['phone_number'],
                                     address=value['address'],
                                     birthday=value['birthday']))

        return result
