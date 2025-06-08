from fastapi import APIRouter, Depends, Query

from core.security import auth_user
from domain.users import UserSchema, TelegramAuthSchema
from service.auth import TelegramService, get_telegram_service
from database.relational_db import User


router = APIRouter()


@router.post(
    path='/',
    response_model=UserSchema
)
async def dashboard(
    telegram_service: TelegramService = Depends(get_telegram_service),
    user: User = Depends(auth_user)
):
    pass
