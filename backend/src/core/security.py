from typing import Annotated
from fastapi import Depends, Request, HTTPException, APIRouter

from domain.users import Role
from database.relational_db import User
from service import get_user_service, UserService


async def auth_user(
    request: Request,
    service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    user = await service.get_me(request)
    if not user:
        raise HTTPException(401, detail="Not authorized")
    
    return user


async def auth_admin(
    request: Request,
    service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    user = await service.get_me(request)
    if not user:
        raise HTTPException(401, detail="Not authorized")
    if user.role.value < Role.ADMIN.value:
        raise HTTPException(403, detail="You don't have permission to do this")
    
    return user


class AuthRouter(APIRouter):
    """Router that enforces authenticated access for all endpoints."""

    def __init__(self, *args, **kwargs) -> None:
        # dependencies = list(kwargs.pop("dependencies", []))
        # dependencies.append(Depends(auth_user))
        # kwargs["dependencies"] = dependencies

        responses = kwargs.pop("responses", {})
        responses[401] = {"description": "Not authorized"}
        kwargs["responses"] = responses

        super().__init__(*args, **kwargs)
