from typing import Optional
import strawberry

from api.types.story import Story
from crud.user import crud_user
from crud.story import crud_story
from crud.user_story import crud_user_story
from crud.follow_relationship import crud_follow_relationship
from crud.utils import get_story_from_json
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
        stories = await crud_story.get_stories_by_author(author_id=self.id)
        return [get_story_from_json(story=story) for story in stories]

    @strawberry.field
    async def following_stories(self) -> list[Story]:
        follow_story_ids: list[str] = []
        with get_db() as db:
            follow_story_ids = crud_user_story.get_user_related_stories(
                db=db, user_id=self.id, relation_type=UserStoryRelationEnum.FOLLOW.value
            )
        stories = await crud_story.get_stories_by_ids(follow_story_ids)
        return [get_story_from_json(story) for story in stories]

    @strawberry.field
    async def read_stories(self) -> list[Story]:
        read_story_ids: list[str] = []
        with get_db() as db:
            read_story_ids = crud_user_story.get_user_related_stories(
                db=db, user_id=self.id, relation_type=UserStoryRelationEnum.READ.value
            )
        stories = await crud_story.get_stories_by_ids(read_story_ids)
        return [get_story_from_json(story) for story in stories]

    @strawberry.field
    async def purchased_stories(self) -> list[Story]:
        purchased_story_ids: list[str] = []
        with get_db() as db:
            purchased_story_ids = crud_user_story.get_user_related_stories(
                db=db,
                user_id=self.id,
                relation_type=UserStoryRelationEnum.PURCHASE.value,
            )
        stories = await crud_story.get_stories_by_ids(purchased_story_ids)
        return [get_story_from_json(story) for story in stories]

    @strawberry.field
    async def followers(self) -> list[UserBase]:
        with get_db() as db:
            follower_ids = crud_follow_relationship.get_follower_ids_from_user_id(
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
