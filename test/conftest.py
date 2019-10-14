import pytest

from app import create_app
from db.db_migrator import DbMigrator
from db.neo4j_client_factory import Neo4JClientFactory
from db.repository.person_repository import PersonRepository
from support.file_config import FileConfig


@pytest.fixture
def test_app_config():
    return FileConfig()


@pytest.fixture
def app(test_app_config):
    app = create_app(test_app_config)
    app.testing = True
    return app


@pytest.fixture
def graph_db(test_app_config):
    return Neo4JClientFactory.new_client(test_app_config)


@pytest.fixture
def flask_test_client(app):
    with app.test_client() as test_client:
        return test_client


@pytest.fixture(autouse=True)
def run_migration(request, graph_db):
    db_migrator = DbMigrator(graph_db)
    db_migrator.clean_db()
    if 'run_migration' in request.keywords:
        db_migrator.migrate()



@pytest.fixture(autouse=True)
def person_repository(graph_db):
    return PersonRepository(graph_db)
