from fastapi import APIRouter, Depends, Request, Query

from core.config import Config
from service import UserService, get_user_service
from domain.users import UserSchema, TelegramAuth, TelegramUserSchema


config = Config()
router = APIRouter()


@router.post(
    path='/telegram/callback',
    response_model=TelegramUserSchema
)
async def auth_telegram_widget(
    request: Request,
    payload: TelegramAuth,
    ?_service: 
):



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

