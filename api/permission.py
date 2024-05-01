import typing
import strawberry
from strawberry.permission import BasePermission
from starlette.requests import Request
from starlette.websockets import WebSocket

from security import get_current_user


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(
        self, source: typing.Any, info: strawberry.Info, **kwargs
    ) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]

        if "Authorization" in request.headers:
            bearer_token = request.headers["Authorization"][7:]
            user = get_current_user(token=bearer_token)

            if user is None:
                return False

            return True

        return False
