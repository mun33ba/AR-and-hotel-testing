import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from .model import Hotel

class Hotels(MongoengineObjectType):
    class Meta:
        description = 'Hotel'
        model = Hotel
        interfaces = (Node, )

class Query(graphene.ObjectType):
    node = Node.Field()

    allHotels = MongoengineConnectionField(Hotels)

schema = graphene.Schema(query=Query, types=[Hotels])