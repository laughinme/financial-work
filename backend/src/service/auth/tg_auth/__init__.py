from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.relational_db import (
    get_db,
    TelegramInterface,
    AuthProvidersInterface,
    UserInterface,
)
from .telegram_service import TelegramService
from ..session import get_session_service, SessionService


async def get_telegram_service(
    session: AsyncSession = Depends(get_db),
    session_service: SessionService = Depends(get_session_service),
) -> TelegramService:
    tg_repo = TelegramInterface(session)
    auth_repo = AuthProvidersInterface(session)
    user_repo = UserInterface(session)
    
    return TelegramService(
        tg_repo, auth_repo, user_repo, session_service
    )
