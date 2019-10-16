import json
from urllib.parse import urlencode

from db.model.person import Person


def response_json(response):
    return json.loads(response.data.decode())


def to_json(**kwargs):
    return json.dumps(kwargs)


def url_string(**url_params):
    string = '/api/family-tree'
    if url_params:
        string += '?' + urlencode(url_params)

    return string


def prepare_query(query_str):
    return query_str.replace('\r', ' ').replace('\n', ' ')


def assert_equals(list_of_dict_one, list_of_dict_two):
    pairs = zip(list_of_dict_one, list_of_dict_two)
    assert any(x != y for x, y in pairs)


def query(service, email):
    query_str = """
            query {
              %s(email: "%s"){
                    email
                    first_name
                    last_name
                    phone_number
                    address
                    birthday
                }
            }
            """ % (service, email)
    return to_json(query=prepare_query(query_str))


def update_nicole_firstname():
    query_str = """
            mutation {
              update_person(person_input: {
                email: "nicole@nicole.com"
                first_name: "Nicole2"
              }){
                    updated_person {
                      email
                      first_name
                      last_name
                      phone_number
                      address
                      birthday
                    }
                    success
                }
            }
            """

    return to_json(query=prepare_query(query_str))


def create_new_person_daren():
    query_str = """
            mutation {
                  create_person(person_input: {
                    email: "daren@daren.com"
                    first_name: "Darent"
                    last_name: "TheDarent"
                    phone_number:"322-222-4444"
                    address: "daren's home"
                    birthday: "2019-10-12"
                    
                  }) 
                  {
                    updated_person {
                      email
                      first_name
                      last_name
                      phone_number
                      address
                      birthday
                    }
                    success
                  }
                }
            """

    return to_json(query=prepare_query(query_str))


class TestFamilyGraphQlView:

    def test_find_person(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=query('person', 'nicole@nicole.com'),
                                          content_type='application/json')

        assert response.status_code == 200
        persons = person_repository.find_list(['nicole@nicole.com'])
        data = response_json(response)['data']['person']
        assert_equals([data], Person.sort_list_as_dict(persons))

    def test_find_siblings(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=query('siblings', 'nicole@nicole.com'),
                                          content_type='application/json')
        persons = person_repository.find_list(['drew@drew.com', 'jakie@jakie.com', 'mary@mary.com'])
        assert response.status_code == 200
        data = response_json(response)['data']['siblings']
        assert_equals([data], Person.sort_list_as_dict(persons))

    def test_find_children(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=query('children', 'jared@jared.com'),
                                          content_type='application/json')
        persons = person_repository.find_list(['gil@gil.com', 'marcus@marcus.com'])
        assert response.status_code == 200
        data = response_json(response)['data']['children']
        assert_equals([data], Person.sort_list_as_dict(persons))

    def test_find_cousins(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=query('cousins', 'nicole@nicole.com'),
                                          content_type='application/json')
        persons = person_repository.find_list(['gil@gil.com', 'marcus@marcus.com', 'jack@jack.com'])
        assert response.status_code == 200
        data = response_json(response)['data']['cousins']
        assert_equals([data], Person.sort_list_as_dict(persons))

    def test_find_parents(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=query('parents', 'nicole@nicole.com'),
                                          content_type='application/json')
        persons = person_repository.find_list(['mark@mark.com', 'nancy@nancy.com'])
        assert response.status_code == 200
        data = response_json(response)['data']['parents']
        assert_equals([data], Person.sort_list_as_dict(persons))

    def test_find_grandparents(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=query('grandparents', 'nicole@nicole.com'),
                                          content_type='application/json')
        persons = person_repository.find_list(['tosh@tosh.com', 'prisca@prisca.com'])
        assert response.status_code == 200
        data = response_json(response)['data']['grandparents']
        assert_equals([data], Person.sort_list_as_dict(persons))

    def test_update_person(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=update_nicole_firstname(),
                                          content_type='application/json')
        persons = person_repository.find_list(['nicole@nicole.com'])
        assert response.status_code == 200
        data = response_json(response)['data']['update_person']['updated_person']
        assert_equals([data], Person.sort_list_as_dict(persons))

    def test_create_person(self, flask_test_client, person_repository):
        response = flask_test_client.post(url_string(), data=create_new_person_daren(),
                                          content_type='application/json')
        persons = person_repository.find_list(['daren@daren.com'])
        assert response.status_code == 200
        data = response_json(response)['data']['create_person']['updated_person']
        assert_equals([data], Person.sort_list_as_dict(persons))
