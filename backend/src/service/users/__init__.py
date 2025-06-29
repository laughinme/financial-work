from fastapi import Depends

from database.relational_db import UserInterface, get_uow, UoW
from .user_service import UserService
from ..auth.tokens import TokenService, get_token_service


async def get_user_service(
    session_service: TokenService = Depends(get_token_service),
    uow: UoW = Depends(get_uow)
) -> UserService:
    user_repo = UserInterface(uow.session)
    return UserService(user_repo, session_service)
