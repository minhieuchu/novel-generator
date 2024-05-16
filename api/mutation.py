from datetime import datetime
from typing import Optional
import strawberry

from api.permission import Context, IsAuthenticated
from api.types.chapter import AddChapterInput, UpdateChapterInput
from api.types.comment import AddCommentInput
from api.types.story import (
    AddStoryInput,
    AddStoryResponse,
    StoryStatusEnum,
    UpdateStoryInput,
)
from api.types.user import SignUpInput, SignUpResponse
from crud.story import crud_story
from crud.user import crud_user
from crud.user_story import crud_user_story
from crud.follow_relationship import crud_follow_relationship
from db.session import get_db
from models.user_story import UserStoryRelationEnum
from schemas.user import UserCreate
from schemas.user_story import UserStoryCreate
from schemas.user_user import UserUserCreate
from security import create_access_token, create_refresh_token, get_password_hash


@strawberry.type
class MutationResponse:
    code: int
    error: Optional[str] = None


@strawberry.type
class Mutation:
    # ========== Auth ==========
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

    # ========== Story ==========
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_story(
        self, add_story_input: AddStoryInput, info: strawberry.Info[Context]
    ) -> AddStoryResponse:
        if add_story_input.author_id != info.context.user.id.__str__():
            return AddStoryResponse(code=400, error="")

        with get_db() as db:
            _, author = crud_user.get(db=db, id=add_story_input.author_id)
            if author is None:
                return AddStoryResponse(code=400, error="Author does not exist")

        story_input = add_story_input.__dict__
        story_input.update(
            {
                "view_count": 0,
                "ranking": 0,
                "status": StoryStatusEnum.ONGOING.value,
                "publish_date": int(datetime.now().timestamp()),
                "author": {"id": author.id, "name": author.name, "email": author.email},
            }
        )
        inserted_id = await crud_story.add_story(story_input)
        return AddStoryResponse(code=200, id=str(inserted_id))

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_story(
        self, update_story_input: UpdateStoryInput, info: strawberry.Info[Context]
    ) -> MutationResponse:
        existing_story = await crud_story.get_story(id=update_story_input.id)
        if existing_story.get("author_id") != info.context.user.id.__str__():
            return MutationResponse(
                code=400, error="Could not update story of other user"
            )

        status = await crud_story.update_story(
            existing_story, update_story_input.__dict__
        )
        if status:
            return MutationResponse(code=200)
        return MutationResponse(code=500, error="Could not update story")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def follow_story(self, user_id: str, story_id: str) -> MutationResponse:
        with get_db() as db:
            status, _ = crud_user_story.create(
                db=db,
                create_object=UserStoryCreate(
                    user_id=user_id,
                    story_id=story_id,
                    relation_type=UserStoryRelationEnum.FOLLOW.value,
                ),
            )
            if status:
                return MutationResponse(code=200)

            return MutationResponse(code=500, error="Could not follow story")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def read_story(self, user_id: str, story_id: str) -> MutationResponse:
        with get_db() as db:
            status, _ = crud_user_story.create(
                db=db,
                create_object=UserStoryCreate(
                    user_id=user_id,
                    story_id=story_id,
                    relation_type=UserStoryRelationEnum.READ.value,
                ),
            )
            if status:
                return MutationResponse(code=200)

            return MutationResponse(code=500, error="")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def purchase_story(self, user_id: str, story_id: str) -> MutationResponse:
        story = await crud_story.get_story(id=story_id)
        if story.get("author_id") == user_id:
            return MutationResponse(code=400, error="Could not purchase your story")

        with get_db() as db:
            status, _ = crud_user_story.create(
                db=db,
                create_object=UserStoryCreate(
                    user_id=user_id,
                    story_id=story_id,
                    relation_type=UserStoryRelationEnum.PURCHASE.value,
                ),
            )
            if status:
                return MutationResponse(code=200)

            return MutationResponse(code=500, error="Could not purchase story")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_comment(self, add_comment_input: AddCommentInput) -> MutationResponse:
        with get_db() as db:
            _, user = crud_user.get(db=db, id=add_comment_input.user_id)
        if user is None:
            return MutationResponse(code=400, error="")

        comment_data = add_comment_input.__dict__
        comment_data.update(
            {
                "user": {"id": user.id, "name": user.name, "email": user.email},
                "created_at": int(datetime.now().timestamp()),
            }
        )
        status = await crud_story.add_comment(comment_data)
        if status:
            return MutationResponse(code=200)

        return MutationResponse(code=500, error="Could not comment on story")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def unfollow_story(self, user_id: str, story_id: str) -> MutationResponse:
        with get_db() as db:
            existing_record = crud_user_story.get_record(
                db=db,
                user_id=user_id,
                story_id=story_id,
                relation_type=UserStoryRelationEnum.FOLLOW.value,
            )
            if existing_record is None:
                return MutationResponse(code=400, error="")
            status = crud_user_story.delete(db=db, id=existing_record.id)
            if status:
                return MutationResponse(code=200)

            return MutationResponse(code=500, error="Could not unfollow story")

    # ========== Chapter ==========
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_chapter(
        self, add_chapter_input: AddChapterInput, info: strawberry.Info[Context]
    ) -> MutationResponse:
        story = await crud_story.get_story(id=add_chapter_input.story_id)
        if story is None:
            return MutationResponse(code=400)

        author_id = story.get("author").get("id")
        if info.context.user.id.__str__() != author_id:
            return MutationResponse(
                code=400, error="Can not add chapter to other users' story"
            )
        await crud_story.add_chapter(add_chapter_input.__dict__)
        return MutationResponse(code=200)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_chapter(
        self, update_chapter_input: UpdateChapterInput, info: strawberry.Info[Context]
    ) -> MutationResponse:
        story = await crud_story.get_story(id=update_chapter_input.story_id)
        author_id = story.get("author").get("id")
        if info.context.user.id.__str__() != author_id:
            return MutationResponse(
                code=400, error="Can not update chapter of other users' story"
            )
        status = await crud_story.update_chapter(update_chapter_input.__dict__)
        if status:
            return MutationResponse(code=200)
        return MutationResponse(code=500, error="Could not update chapter")

    # ========== User ==========
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def follow_user(self, follower_id: str, followee_id: str) -> MutationResponse:
        with get_db() as db:
            status, _ = crud_follow_relationship.create(
                db=db,
                create_object=UserUserCreate(
                    follower_id=follower_id, followee_id=followee_id
                ),
            )
            if status:
                return MutationResponse(code=200)

            return MutationResponse(code=500, error="Could not follow user")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def unfollow_user(self, follower_id: str, followee_id: str) -> MutationResponse:
        with get_db() as db:
            existing_record = crud_follow_relationship.get_record(
                db=db, follower_id=follower_id, followee_id=followee_id
            )
            if existing_record is None:
                return MutationResponse(code=400, error="")
            status = crud_follow_relationship.delete(db=db, id=existing_record.id)
            if status:
                return MutationResponse(code=200)

            return MutationResponse(code=500, error="Could not unfollow user")
