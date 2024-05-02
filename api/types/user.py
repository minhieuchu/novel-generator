from typing import Optional
import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


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
