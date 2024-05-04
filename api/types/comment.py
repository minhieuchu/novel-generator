from typing import Optional
import strawberry

from crud.user import crud_user
from db.session import get_db


@strawberry.type
class CommentUserBase:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class Comment:
    id: strawberry.ID
    user_id: strawberry.ID
    story_id: strawberry.ID
    content: str

    @strawberry.field
    def user(self) -> Optional[CommentUserBase]:
        with get_db() as db:
            _, user_model = crud_user.get(db=db, id=self.user_id)
            if user_model is None:
                return None
            return CommentUserBase(
                id=strawberry.ID(user_model.id),
                name=user_model.name,
                email=user_model.email,
            )
