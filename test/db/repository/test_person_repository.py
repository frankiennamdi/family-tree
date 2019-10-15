import logging

import pytest

from db.repository.person_repository import RelationshipType, InvalidUpdateOperation


class TestPersonRepository:
    _logger = logging.getLogger(__name__)

    @pytest.mark.run_migration
    def test_update_existing_person(self, person_repository):
        updated_person = person_repository.update_or_create(
            {'email': 'nicole@nicole.com', 'first_name': 'Nicole Jonny'})
        self.log_person_list([updated_person])
        assert updated_person.first_name == 'Nicole Jonny'

    @pytest.mark.run_migration
    def test_create_person(self, person_repository):
        updated_person = person_repository.update_or_create(
            {'email': 'frankie@frankie.com', 'first_name': 'Frankie Jonny', 'last_name': 'Marks',
             'phone_number': '322-222-4444', 'address': 'Marks Home', 'birthday': '2019-10-12'}
        )
        self.log_person_list([updated_person])
        assert updated_person.first_name == 'Frankie Jonny'

    @pytest.mark.run_migration
    def test_check_related(self, person_repository):
        nicole_related_drew = person_repository.check_related('nicole@nicole.com', 'drew@drew.com')
        assert nicole_related_drew[0] is True
        new_email = 'frankie@frankie.com'
        self.new_person(new_email, person_repository)
        nicole_related_frankie = person_repository.check_related('nicole@nicole.com', new_email)
        assert nicole_related_frankie[0] is False

    @pytest.mark.run_migration
    def test_add_parent_relationship(self, person_repository):
        new_email = 'frankie@frankie.com'
        parent_email = 'nicole@nicole.com'
        self.new_person(new_email, person_repository)
        assert person_repository.add_relation(parent_email, new_email, RelationshipType.PARENT)
        nicole_children = person_repository.find_children(parent_email)
        assert sorted([children.email for children in nicole_children]) == sorted([new_email])

    @pytest.mark.run_migration
    @pytest.mark.parametrize(
        "from_email,to_email,expectation",
        [
            ('nicole@nicole.com', 'drew@drew.com', pytest.raises(InvalidUpdateOperation)),
        ]
    )
    def test_add_bad_parent_relationship(self, person_repository, from_email, to_email, expectation):
        with expectation as info:
            person_repository.add_relation(from_email, to_email, RelationshipType.PARENT)
            assert 'in the same family tree' in str(info.value)

    @pytest.mark.run_migration
    @pytest.mark.parametrize(
        "from_email,new_email,expectation",
        [
            ('nancy@nancy.com', 'frankie@frankie.com', pytest.raises(InvalidUpdateOperation)),
        ]
    )
    def test_add_bad_married_relationship(self, person_repository, from_email, new_email, expectation):
        with expectation as info:
            self.new_person(new_email, person_repository)
            assert person_repository.add_relation(from_email, new_email, RelationshipType.MARRIED)
            assert "are currently married" in str(info.value)

    @pytest.mark.run_migration
    def test_partners_can_marry_each_other(self, person_repository):
        keith_email = 'keith@keith.com'
        nicole_email = 'nicole@nicole.com'
        self.new_person(keith_email, person_repository)
        assert person_repository.add_relation(keith_email, nicole_email, RelationshipType.MARRIED)
        assert person_repository.add_relation(nicole_email, keith_email, RelationshipType.MARRIED)

    @pytest.mark.run_migration
    def test_partners_can_have_new_relationship_with_partners_tree(self, person_repository):
        keith_email = 'keith@keith.com'
        nicole_email = 'nicole@nicole.com'
        tosh_email = 'tosh@tosh.com'  # nicole's grandfather
        self.new_person(keith_email, person_repository)
        assert person_repository.add_relation(keith_email, nicole_email, RelationshipType.MARRIED)
        with pytest.raises(InvalidUpdateOperation) as info:
            person_repository.add_relation(keith_email, tosh_email, RelationshipType.PARENT)
            assert 'in the same family tree' in str(info.value)

    @pytest.mark.run_migration
    def test_add_married_and_parent_relationship(self, person_repository):
        frankie_email = 'frankie@frankie.com'
        keith_email = 'keith@keith.com'
        nicole_email = 'nicole@nicole.com'
        self.new_person(frankie_email, person_repository)
        self.new_person(keith_email, person_repository)

        assert person_repository.add_relation(keith_email, frankie_email, RelationshipType.PARENT)
        assert person_repository.add_relation(nicole_email, keith_email, RelationshipType.MARRIED)

        nicole_children = person_repository.find_children('nicole@nicole.com')
        assert sorted([children.email for children in nicole_children]) == sorted([frankie_email])

        # add nicole as parent to frankie, so she is directly connected
        assert person_repository.add_relation(nicole_email, frankie_email, RelationshipType.PARENT)
        nicole_children = person_repository.find_children(nicole_email)
        assert sorted([children.email for children in nicole_children]) == sorted([frankie_email])

        # check frankie cannot parent nicole
        with pytest.raises(InvalidUpdateOperation) as info:
            person_repository.add_relation(frankie_email, nicole_email, RelationshipType.PARENT)
            assert 'in the same family tree' in str(info.value)

    @pytest.mark.run_migration
    def test_create_person_fails_when_data_is_missing(self, person_repository):
        with pytest.raises(ValueError) as info:
            person_repository.update_or_create(
                {'email': 'frankie@frankie.com',
                 'first_name': 'Frankie Jonny',
                 'last_name': 'Marks',
                 'phone_number': '322-222-4444',
                 'birthday': '2019-10-12'
                 }
            )
            assert 'new person requires all properties' in str(info.value)

    @pytest.mark.run_migration
    @pytest.mark.parametrize("email,first_name",
                             [('nicole@nicole.com', 'Nicole'),
                              ('drew@drew.com', 'Drew')])
    def test_find_person_by_email(self, person_repository, email, first_name):
        person = person_repository.find(email)
        self.log_person_list([person])
        assert person.email == email
        assert person.first_name == first_name

    @pytest.mark.run_migration
    @pytest.mark.parametrize("email,cousins_count",
                             [('nicole@nicole.com', 3),
                              ('gil@gil.com', 4)])
    def test_find_cousins_by_email(self, person_repository, email, cousins_count):
        cousins = person_repository.find_cousins(email)
        self.log_person_list(cousins)
        assert len(cousins) == cousins_count

    @pytest.mark.run_migration
    @pytest.mark.parametrize("email,sibling_count",
                             [('nicole@nicole.com', 3),
                              ('drew@drew.com', 3),
                              ('jared@jared.com', 1)])
    def test_find_siblings_by_email(self, person_repository, email, sibling_count):
        siblings = person_repository.find_siblings(email)
        self.log_person_list(siblings)
        assert len(siblings) == sibling_count

    @pytest.mark.run_migration
    @pytest.mark.parametrize("email,parent_emails",
                             [('nicole@nicole.com', ['mark@mark.com', 'nancy@nancy.com'])])
    def test_find_parents_by_email(self, person_repository, email, parent_emails):
        parents = person_repository.find_parents(email)
        self.log_person_list(parents)
        assert sorted([parent.email for parent in parents]) == sorted(parent_emails)

    @pytest.mark.run_migration
    @pytest.mark.parametrize("email,grand_parent_emails",
                             [('nicole@nicole.com', ['tosh@tosh.com', 'prisca@prisca.com'])])
    def test_find_grandparents_by_email(self, person_repository, email, grand_parent_emails):
        parents = person_repository.find_grandparents(email)
        self.log_person_list(parents)
        assert sorted([parent.email for parent in parents]) == sorted(grand_parent_emails)

    @pytest.mark.run_migration
    @pytest.mark.parametrize("email,children_count",
                             [('nicole@nicole.com', 0),
                              ('drew@drew.com', 0),
                              ('jared@jared.com', 2),
                              ('mark@mark.com', 4)])
    def test_find_children_by_email(self, person_repository, email, children_count):
        children = person_repository.find_children(email)
        self.log_person_list(children)
        assert len(children) == children_count

    def log_person_list(self, persons):
        for person in persons:
            self._logger.info(person.as_dict())

    def new_person(self, email, person_repository):
        person_repository.update_or_create(
            {'email': email,
             'first_name': email,
             'last_name': email,
             'phone_number': '322-222-4444',
             'address': email,
             'birthday': '2019-10-12'
             }
        )
