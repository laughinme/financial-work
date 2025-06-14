from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    IdentityInterface,
    UserInterface,
)
from .telegram_service import TelegramService
from ..session import get_session_service, SessionService


async def get_telegram_service(
    uow: UoW = Depends(get_uow),  
    session_service: SessionService = Depends(get_session_service),
) -> TelegramService:
    identity_repo = IdentityInterface(uow.session)
    user_repo = UserInterface(uow.session)

    return TelegramService(
        identity_repo, user_repo, session_service, uow
    )
