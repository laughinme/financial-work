from fastapi import Depends

from database.relational_db import UserInterface, get_uow, UoW
from .user_service import UserService
from ..auth.session import get_session_service, SessionService


async def get_user_service(
    session_service: SessionService = Depends(get_session_service),
    uow: UoW = Depends(get_uow)
) -> UserService:
    user_repo = UserInterface(uow.session)
    return UserService(user_repo, session_service)
