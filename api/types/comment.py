import strawberry


@strawberry.type
class CommentUserBase:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class Comment:
    user: CommentUserBase
    content: str
    created_at: int


@strawberry.input
class AddCommentInput:
    user_id: str
    story_id: str
    content: str
