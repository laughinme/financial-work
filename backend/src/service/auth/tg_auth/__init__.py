from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    TelegramInterface,
    AuthProvidersInterface,
    UserInterface,
)
from .telegram_service import TelegramService
from ..session import get_session_service, SessionService


async def get_telegram_service(
    uow: UoW = Depends(get_uow),  
    session_service: SessionService = Depends(get_session_service),
) -> TelegramService:
    tg_repo = TelegramInterface(uow.session)
    auth_repo = AuthProvidersInterface(uow.session)
    user_repo = UserInterface(uow.session)
    
    return TelegramService(
        tg_repo, auth_repo, user_repo, session_service, uow
    )
