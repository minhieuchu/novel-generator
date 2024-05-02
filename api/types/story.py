import strawberry


@strawberry.type
class Story:
    id: strawberry.ID
    title: str
    genre: str
    theme: str
    content: str


@strawberry.type
class AddStoryInput:
    title: str
    genre: str
    theme: str
    content: str


@strawberry.type
class UpdateStoryInput:
    id: strawberry.ID
    title: str | None
    genre: str | None
    theme: str | None
    content: str | None


@strawberry.type
class AddStoryResponse:
    code: int
    error: str | None
    id: strawberry.ID
