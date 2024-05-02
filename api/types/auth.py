from typing import Optional
import strawberry


@strawberry.type
class LoginResult:
    code: int
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
