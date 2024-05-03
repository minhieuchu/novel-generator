import strawberry


@strawberry.type
class Comment:
    id: strawberry.ID
    user_id: strawberry.ID
    story_id: strawberry.ID
    content: str
