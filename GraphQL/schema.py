from graphene import ObjectType, Schema, String, relay, Field, Int
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import sys
sys.path.append("..")
from MySQL.database import MySQL, Hotels


class Hotel(SQLAlchemyObjectType):
    class Meta:
        model = Hotels
        interfaces = (relay.Node, )

class Query(ObjectType):
    node = relay.Node.Field()
    # hotels = SQLAlchemyConnectionField(Hotel)
    hotels = Field(Hotel)

    def resolve_hotels(self, args, context, info):
        query = Hotel.get_query()
        name = args.get()
        print(name)
        return query.get(name)
    
schema = Schema(query=Query)