import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
