import strawberry

from api.types.user import User

from .query import Query
from .mutation import Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation, types=[User])
