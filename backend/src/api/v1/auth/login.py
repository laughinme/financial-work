from fastapi import APIRouter, Depends, Request

from core.config import Config
from service import UserService, get_user_service
from domain.users import UserLogin, UserSchema

config = Config()
router = APIRouter()


@router.post(
    path="/login",
    response_model=UserSchema
)
async def login_user(
    request: Request,
    payload: UserLogin,
    user_service: UserService = Depends(get_user_service)
) -> UserSchema:
    user = await user_service.login(request, payload, config.SESSION_LIFETIME)
    return user
