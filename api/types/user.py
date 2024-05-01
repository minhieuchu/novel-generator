import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class SignUpResponse:
    code: int
    error: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None


@strawberry.input
class SignUpInput:
    email: str
    name: str
    password: str
