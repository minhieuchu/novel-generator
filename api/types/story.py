import enum
from typing import Optional
import strawberry

from api.types.chapter import Chapter
from api.types.comment import Comment


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
    author: AuthorBase
    title: str
    genre: str
    theme: str
    description: str
    view_count: int
    publish_date: int
    ranking: int
    status: StoryStatusEnum
    chapters: list[Chapter]
    comments: list[Comment]


@strawberry.input
class AddStoryInput:
    author_id: str
    title: str
    genre: str
    theme: str
    description: str
    has_multiple_chapters: bool


@strawberry.input
class UpdateStoryInput:
    id: str
    title: Optional[str] = None
    genre: Optional[str] = None
    theme: Optional[str] = None
    description: Optional[str] = None
    view_count: Optional[int] = None
    ranking: Optional[int] = None
    status: Optional[StoryStatusEnum] = None
    has_multiple_chapters: Optional[bool] = None


@strawberry.type
class AddStoryResponse:
    code: int
    error: Optional[str] = None
    id: Optional[str] = None
