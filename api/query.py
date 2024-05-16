import strawberry

from api.types.auth import LoginResult
from api.types.story import Story
from crud.story import crud_story
from crud.utils import get_story_from_json
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

    @strawberry.field
    async def stories(self) -> list[Story]:
        stories = await crud_story.get_stories()
        return [get_story_from_json(story=story) for story in stories]
