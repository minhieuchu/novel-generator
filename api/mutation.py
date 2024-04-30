import strawberry

from api.types.user import AddUserInput, AddUserPayload, User
from crud.user import crud_user
from db.session import get_db
from schemas.user import UserCreate
from security import get_password_hash


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, user_input: AddUserInput) -> AddUserPayload:
        user_create = UserCreate(
            email=user_input.email,
            name=user_input.name,
            password=get_password_hash(user_input.password),
        )
        status = False
        created_user_id = None
        with get_db() as db:
            status, created_user_id = crud_user.create(db=db, create_object=user_create)

        if not status:
            return AddUserPayload(
                code=500,
                success=False,
                message="Could not create user.",
                user=None,
            )

        return AddUserPayload(
            code=200,
            success=True,
            message="Successfully added user.",
            user=User(
                id=strawberry.ID(created_user_id),
                name=user_create.name,
                email=user_create.email,
            ),
        )
