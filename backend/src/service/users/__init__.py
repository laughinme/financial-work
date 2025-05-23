from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.relational_db import UserInterface, get_db
from .user_service import UserService
from ..session import get_session_service, SessionService


async def get_user_service(
    session_service: SessionService = Depends(get_session_service),
    session: AsyncSession = Depends(get_db)
) -> UserService:
    user_repo = UserInterface(session)
    return UserService(user_repo, session_service)
    