from fastapi import APIRouter, Depends, Query

from core.security import auth_user
from domain.users import UserSchema, TelegramAuthSchema
from service.auth import TelegramService, get_telegram_service
from database.relational_db import User


router = APIRouter()


@router.post(
    path='/telegram',
    response_model=UserSchema
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
