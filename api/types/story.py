import enum
from typing import Optional
import strawberry

from api.types.comment import Comment
from crud.user import crud_user
from crud.story import crud_story
from db.session import get_db


@strawberry.enum
class StoryStatusEnum(enum.Enum):
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"


@strawberry.type
class AuthorBase:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class Story:
    id: strawberry.ID
    author_id: strawberry.ID
    title: str
    genre: str
    theme: str
    content: str
    description: str
    view_count: int
    publish_date: int
    ranking: int
    status: StoryStatusEnum

    @strawberry.field
    def author(self) -> Optional[AuthorBase]:
        with get_db() as db:
            _, user_model = crud_user.get(db=db, id=self.author_id)
            if user_model is None:
                return None

            return AuthorBase(
                id=strawberry.ID(user_model.id),
                name=user_model.name,
                email=user_model.email,
            )

    @strawberry.field
    def comments(self) -> list[Comment]:
        with get_db() as db:
            comments = crud_story.get_story_comments(db=db, story_id=str(self.id))
            return [
                Comment(
                    id=strawberry.ID(comment.get("_id")),
                    user_id=comment.get("user_id"),
                    story_id=comment.get("story_id"),
                    content=comment.get("content"),
                )
                for comment in comments
            ]


@strawberry.input
class AddStoryInput:
    author_id: strawberry.ID
    title: str
    genre: str
    theme: str
    content: str
    description: str


@strawberry.type
class UpdateStoryInput:
    id: strawberry.ID
    author_id: Optional[strawberry.ID]
    title: Optional[str] = None
    genre: Optional[str] = None
    theme: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None


@strawberry.type
class AddStoryResponse:
    code: int
    error: Optional[str] = None
    id: strawberry.ID
