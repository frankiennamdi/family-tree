from flask_graphql import GraphQLView


class FamilyGraphQl(GraphQLView):

    def __init__(self, graph_db, **kwargs):
        super(FamilyGraphQl, self).__init__(**kwargs)
        self._graph_db = graph_db

    def get_context(self):
        context = super().get_context()
        context.graph_db = self._graph_db
        return context
