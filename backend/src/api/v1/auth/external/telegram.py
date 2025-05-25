from fastapi import APIRouter, Depends, Request, Query

from core.config import Config
from domain.users import UserSchema, TelegramAuthSchema
from service.auth import TelegramService, get_telegram_service


config = Config()
router = APIRouter()


@router.post(
    path='/telegram/callback',
    response_model=UserSchema
)
async def auth_telegram_widget(
    request: Request,
    payload: TelegramAuthSchema,
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    user = await telegram_service.login(request, payload, config.SESSION_LIFETIME)
    return user


# TODO: add redirect page support

# @router.post(
#     path='/telegram',
#     response_model=...
# )
# async def auth_telegram_redirect(
#     request: Request,
#     id: int = Query(...),
#     first_name: str = Query(...),
#     last_name: str | None = Query(None),
#     username: str | None = Query(None),
#     photo_url: str | None = Query(None),
#     auth_date: str = Query(...),
#     hash: str = Query(...),
# ) -> None:
#     pass
