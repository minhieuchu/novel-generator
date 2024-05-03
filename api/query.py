from typing import Optional
import strawberry

from api.permission import IsAuthenticated
from api.types.auth import LoginResult
from api.types.user import User
from api.types.story import Story
from crud.story import get_stories
from crud.user import crud_user
from db.session import get_db
from security import (
    create_access_token,
    create_refresh_token,
    get_user_by_email,
    verify_password,
)


@strawberry.type
class Query:
    @strawberry.field
    def login(self, username: str, password: str) -> LoginResult:
        user = get_user_by_email(username)
        if user is None:
            return LoginResult(
                code=401,
                message="Email is invalid",
            )

        if not verify_password(password, user.password):
            return LoginResult(
                code=401,
                message="Incorrect password",
            )

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        return LoginResult(
            code=200,
            message="Login successfully",
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @strawberry.field(permission_classes=[IsAuthenticated])
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

    @strawberry.field(permission_classes=[IsAuthenticated])
    def user(self, id: strawberry.ID) -> Optional[User]:
        with get_db() as db:
            status, user_model = crud_user.get(db=db, id=id)
            if not status or user_model is None:
                return None

            return User(
                id=strawberry.ID(user_model.id),
                name=user_model.name,
                email=user_model.email,
            )

    @strawberry.field
    async def stories(self) -> list[Story]:
        stories = await get_stories()
        return stories
