from datetime import datetime
from typing import Optional
import strawberry

from api.permission import IsAuthenticated
from api.types.chapter import AddChapterInput, UpdateChapterInput
from api.types.story import (
    AddStoryInput,
    AddStoryResponse,
    StoryStatusEnum,
    UpdateStoryInput,
)
from api.types.user import SignUpInput, SignUpResponse
from crud.chapter import crud_chapter
from crud.comment import crud_comment
from crud.story import crud_story
from crud.user import crud_user
from crud.user_story import crud_user_story
from crud.follow_relationship import crud_follow_relationship
from db.session import get_db
from models.user_story import UserStoryRelationEnum
from schemas.comment import CommentCreate
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
    async def add_story(self, add_story_input: AddStoryInput) -> AddStoryResponse:
        story_input = add_story_input.__dict__
        story_input.update(
            {
                "view_count": 0,
                "ranking": 0,
                "status": StoryStatusEnum.ONGOING.value,
                "publish_date": int(datetime.now().timestamp()),
            }
        )
        inserted_id = await crud_story.add_story(story_input)
        return AddStoryResponse(code=200, id=strawberry.ID(inserted_id))

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_story(
        self, update_story_input: UpdateStoryInput
    ) -> MutationResponse:
        status = await crud_story.update_story(update_story_input.__dict__)
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
    def purchase_story(self, user_id: str, story_id: str) -> MutationResponse:
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
    def comment_story(
        self, user_id: str, story_id: str, content: str
    ) -> MutationResponse:
        with get_db() as db:
            status, record_id = crud_user_story.create(
                db=db,
                create_object=UserStoryCreate(
                    user_id=user_id,
                    story_id=story_id,
                    relation_type=UserStoryRelationEnum.COMMENT.value,
                ),
            )
            if not status:
                return MutationResponse(code=500, error="Could not comment on story")

            status, _ = crud_comment.create(
                db=db,
                create_object=CommentCreate(user_story_id=record_id, content=content),
            )

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
    async def add_chapter(self, add_chapter_input: AddChapterInput) -> MutationResponse:
        await crud_chapter.add_chapter(add_chapter_input.__dict__)
        return MutationResponse(code=200)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_chapter(
        self, update_chapter_input: UpdateChapterInput
    ) -> MutationResponse:
        status = await crud_chapter.update_chapter(update_chapter_input.__dict__)
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
