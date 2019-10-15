import flask_cors
from flask import Flask, jsonify

from db.db_migrator import DbMigrator
from db.neo4j_client_factory import Neo4JClientFactory
from views import health_check
from views.family_graphql import FamilyGraphQl
from views.model import schema

cors = flask_cors.CORS()


def create_app(app_config):
    app = Flask(__name__)
    cors.init_app(app)
    app.debug = True

    graph_db = Neo4JClientFactory.new_client(app_config)
    db_migrator = DbMigrator(graph_db)
    # every restart clean up the db and start afresh
    db_migrator.clean_db()
    # run migration
    db_migrator.migrate()

    app.register_blueprint(health_check.blueprint, url_prefix='/api')
    app.add_url_rule('/api/family-tree',
                     view_func=FamilyGraphQl.as_view("family-tree", graph_db, schema=schema, batch=True, graphiql=True))

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'Endpoint Resource Not Found.'}), 404

    return app
