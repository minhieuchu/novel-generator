import strawberry

from api.types.user import User
from crud.user import crud_user
from db.session import get_db


@strawberry.type
class Query:
    @strawberry.field
    def users(self, info: strawberry.Info) -> list[User]:
        with get_db() as db:
            _, user_models = crud_user.get_multi(db=db)
            return [
                User(
                    id=strawberry.ID(user_model.id),
                    name=user_model.name,
                    email=user_model.email,
                )
                for user_model in user_models
            ]

    @strawberry.field
    def user(self, id: strawberry.ID) -> User | None:
        with get_db() as db:
            status, user_model = crud_user.get(db=db, id=id)
            if not status or user_model is None:
                return None

            return User(
                id=strawberry.ID(user_model.id),
                name=user_model.name,
                email=user_model.email,
            )
