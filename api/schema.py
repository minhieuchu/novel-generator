import strawberry

from api.types.user import User

from .query import Query

schema = strawberry.Schema(query=Query, types=[User])
