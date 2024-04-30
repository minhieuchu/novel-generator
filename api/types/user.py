import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class AddUserPayload:
    code: int
    success: bool
    message: str
    user: User | None


@strawberry.input
class AddUserInput:
    email: str
    name: str
    password: str
