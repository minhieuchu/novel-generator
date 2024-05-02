from typing import Optional
import strawberry


@strawberry.type
class Story:
    id: strawberry.ID
    author_id: strawberry.ID
    title: str
    genre: str
    theme: str
    content: str


@strawberry.input
class AddStoryInput:
    author_id: strawberry.ID
    title: str
    genre: str
    theme: str
    content: str


@strawberry.type
class UpdateStoryInput:
    id: strawberry.ID
    author_id: Optional[strawberry.ID]
    title: Optional[str] = None
    genre: Optional[str] = None
    theme: Optional[str] = None
    content: Optional[str] = None


@strawberry.type
class AddStoryResponse:
    code: int
    error: Optional[str] = None
    id: strawberry.ID
