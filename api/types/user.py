from typing import Optional
import strawberry

from api.types.comment import Comment
from api.types.story import Story
from crud.comment import crud_comment
from crud.user import crud_user
from crud.story import get_stories_by_author, get_stories_by_ids
from crud.user_story import crud_user_story
from crud.user_user import crud_user_user
from db.session import get_db
from models.user_story import UserStoryRelationEnum


@strawberry.type
class UserBase:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str

    @strawberry.field
    async def stories(self) -> list[Story]:
        stories = await get_stories_by_author(author_id=self.id)
        return stories

    @strawberry.field
    async def following_stories(self) -> list[Story]:
        follow_story_ids: list[str] = []
        with get_db() as db:
            follow_story_ids = crud_user_story.get_user_related_stories(
                db=db, user_id=self.id, relation_type=UserStoryRelationEnum.FOLLOW.value
            )
        stories = await get_stories_by_ids(follow_story_ids)
        return stories

    @strawberry.field
    async def read_stories(self) -> list[Story]:
        read_story_ids: list[str] = []
        with get_db() as db:
            read_story_ids = crud_user_story.get_user_related_stories(
                db=db, user_id=self.id, relation_type=UserStoryRelationEnum.READ.value
            )
        stories = await get_stories_by_ids(read_story_ids)
        return stories

    @strawberry.field
    async def purchased_stories(self) -> list[Story]:
        purchased_story_ids: list[str] = []
        with get_db() as db:
            purchased_story_ids = crud_user_story.get_user_related_stories(
                db=db,
                user_id=self.id,
                relation_type=UserStoryRelationEnum.PURCHASE.value,
            )
        stories = await get_stories_by_ids(purchased_story_ids)
        return stories

    @strawberry.field
    async def followers(self) -> list[UserBase]:
        with get_db() as db:
            follower_ids = crud_user_user.get_follower_ids_from_user_id(
                db=db, user_id=self.id
            )
            user_models = crud_user.get_users_from_ids(db=db, ids=follower_ids)
            return [
                UserBase(
                    id=strawberry.ID(user_model.id),
                    name=user_model.name,
                    email=user_model.email,
                )
                for user_model in user_models
            ]

    @strawberry.field
    async def comments_on_story(self, story_id: str) -> list[Comment]:
        comments: list[Comment] = []
        with get_db() as db:
            record = crud_user_story.get_record(
                db=db,
                user_id=self.id,
                story_id=story_id,
                relation_type=UserStoryRelationEnum.COMMENT.value,
            )
            if record is None:
                return comments

            _, comment_models = crud_comment.filter_by(
                db=db, filter_dict={"user_story_id": record.id}
            )

            return [
                Comment(
                    id=strawberry.ID(comment.id),
                    user_id=record.user_id,
                    story_id=record.story_id,
                    content=comment.content,
                )
                for comment in comment_models
            ]


@strawberry.type
class SignUpResponse:
    code: int
    error: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


@strawberry.input
class SignUpInput:
    email: str
    name: str
    password: str
