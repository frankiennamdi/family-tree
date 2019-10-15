from py2neo import Graph

from support.config import Config


class Neo4JClientFactory:
    """
        Factory for create py2neo neo4j client
    """
    @classmethod
    def new_client(cls, app_config):
        return Graph(
            host=app_config.get_value(Config.NEO4J_CONFIG, Config.NEO4J_HOST),
            port=app_config.get_value(Config.NEO4J_CONFIG, Config.NEO4J_PORT),
            user=app_config.get_value(Config.NEO4J_CONFIG, Config.NEO4J_USER),
            password=app_config.get_value(Config.NEO4J_CONFIG, Config.NEO4J_PASSWORD),
        )
