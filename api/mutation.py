import strawberry

from api.permission import IsAuthenticated
from api.types.story import AddStoryInput, AddStoryResponse
from api.types.user import SignUpInput, SignUpResponse
from crud.story import add_story, delete_stories
from crud.user import crud_user
from db.session import get_db
from schemas.user import UserCreate
from security import create_access_token, create_refresh_token, get_password_hash


@strawberry.type
class Mutation:
    @strawberry.mutation
    def signup(self, signup_input: SignUpInput) -> SignUpResponse:
        user_create = UserCreate(
            email=signup_input.email,
            name=signup_input.name,
            password=get_password_hash(signup_input.password),
        )
        status = False
        with get_db() as db:
            status, _ = crud_user.create(db=db, create_object=user_create)

        if not status:
            return SignUpResponse(
                code=500,
                error="Could not create user.",
            )

        access_token = create_access_token({"sub": signup_input.email})
        refresh_token = create_refresh_token({"sub": signup_input.email})
        return SignUpResponse(
            code=200, access_token=access_token, refresh_token=refresh_token
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_story(self, add_story_input: AddStoryInput) -> AddStoryResponse:
        inserted_id = await add_story(add_story_input)
        return AddStoryResponse(code=200, id=strawberry.ID(inserted_id))

    # For development only
    @strawberry.mutation
    def delete_stories(self) -> None:
        delete_stories()
