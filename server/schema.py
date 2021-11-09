import graphene
from graphene_django.debug import DjangoDebug

# import biztyz schema
import biztyz.schema.mutation
import biztyz.schema.query

# import user schema
import users.schema.mutation
import users.schema.query

class Mutation(
    biztyz.schema.mutation.Mutation,
    users.schema.mutation.Mutation, 
    graphene.ObjectType,
    ):
    debug = graphene.Field(DjangoDebug, name='_debug')

class Query(
    biztyz.schema.query.Query,
    users.schema.query.Query, 
    graphene.ObjectType,
    ):
    debug = graphene.Field(DjangoDebug, name='_debug')
    # pass

schema = graphene.Schema(query=Query, mutation=Mutation)
