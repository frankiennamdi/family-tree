import graphene

from views.model.mutation import Mutations
from views.model.query import Query

schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
