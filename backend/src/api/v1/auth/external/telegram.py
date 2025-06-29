from fastapi import APIRouter, Depends, Response

from core.config import Config
from domain.users import AccessToken, TelegramAuthSchema
from service.auth import TelegramService, get_telegram_service


config = Config()
router = APIRouter()


@router.post(
    path='/telegram/callback',
    response_model=AccessToken,
    responses={401: {"description": "Invalid telegram signature"}}
)
async def auth_telegram_widget(
    response: Response,
    payload: TelegramAuthSchema,
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    access, refresh = await telegram_service.login(payload)
    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=config.REFRESH_TTL,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return AccessToken(access_token=access)


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
