from fastapi import Depends, Query

from core.security import auth_user, AuthRouter
from domain.users import UserSchema, TelegramAuthSchema
from service.auth import TelegramService, get_telegram_service
from database.relational_db import User


router = AuthRouter()


@router.post(
    path='/telegram',
    response_model=UserSchema,
    responses={
        403: {"description": "Invalid telegram signature"},
        409: {"description": "Telegram account already linked"}
    }
)
async def link_telegram(
    payload: TelegramAuthSchema,
    replace_fields: bool = Query(
        default=False, 
        description="Whether to replace empty fields with info from Telegram profile"
    ),
    telegram_service: TelegramService = Depends(get_telegram_service),
    user: User = Depends(auth_user)
):
    await telegram_service.link(payload, user, replace_fields)
    return user
