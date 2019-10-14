from importlib import import_module


class DbMigrator:
    def __init__(self, graph_db):
        self._graph_db = graph_db

    def migrate(self):
        migrations = ['1_initial_data']
        tx = self._graph_db.begin()
        for migration in migrations:
            module = import_module("db.migrations.{0}".format(migration))
            migrate_function = getattr(module, 'migrate')
            migrate_function(tx)
        tx.commit()

    def clean_db(self):
        tx = self._graph_db.begin()
        tx.graph.delete_all()
        tx.commit()
