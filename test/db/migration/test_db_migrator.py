import pytest

from db.repository.person_repository import PersonRepository
from db.db_migrator import DbMigrator


class TestDbMigrator:

    @pytest.mark.integration
    def test_db_migrate(self, graph_db):
        db_migrator = DbMigrator(graph_db)
        db_migrator.migrate()
        person_repository = PersonRepository(graph_db)
        nicole = person_repository.find('nicole@nicole.com')
        assert nicole.first_name == 'Nicole'
