from typing import Optional
import strawberry


@strawberry.type
class Story:
    id: strawberry.ID
    title: str
    genre: str
    theme: str
    content: str


@strawberry.input
class AddStoryInput:
    title: str
    genre: str
    theme: str
    content: str


@strawberry.type
class UpdateStoryInput:
    id: strawberry.ID
    title: Optional[str] = None
    genre: Optional[str] = None
    theme: Optional[str] = None
    content: Optional[str] = None


@strawberry.type
class AddStoryResponse:
    code: int
    error: Optional[str] = None
    id: strawberry.ID
