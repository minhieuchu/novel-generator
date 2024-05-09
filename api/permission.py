from functools import cached_property
import typing
import strawberry
from strawberry.fastapi import BaseContext
from strawberry.permission import BasePermission

from api.types.user import User
from security import get_current_user


class Context(BaseContext):
    @cached_property
    def user(self) -> typing.Optional[User]:
        if not self.request:
            return None

        if "Authorization" in self.request.headers:
            bearer_token = self.request.headers["Authorization"][7:]
            user = get_current_user(token=bearer_token)
            return user

        return None


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(
        self, source: typing.Any, info: strawberry.Info[Context], **kwargs
    ) -> bool:
        if info.context.user is None:
            return False
        return True
