from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    IdentityInterface,
    UserInterface,
)
from .telegram_service import TelegramService
from ..tokens import TokenService, get_token_service


async def get_telegram_service(
    uow: UoW = Depends(get_uow),  
    token_service: TokenService = Depends(get_token_service),
) -> TelegramService:
    identity_repo = IdentityInterface(uow.session)
    user_repo = UserInterface(uow.session)

    return TelegramService(
        identity_repo, user_repo, token_service, uow
    )
