import strawberry


@strawberry.type
class LoginResult:
    code: int
    message: str
    access_token: str | None = None
    refresh_token: str | None = None
