from fastapi import APIRouter, Depends, Request

from core.config import Config
from service import UserService, get_user_service
from domain.users import UserRegister, UserSchema

config = Config()
router = APIRouter()


@router.post(
    path='/register',
    response_model=UserSchema,
    status_code=201
)
async def register_user(
    request: Request,
    payload: UserRegister,
    user_service: UserService = Depends(get_user_service)
) -> UserSchema:
    user = await user_service.register(request, payload, config.SESSION_LIFETIME)
    return user
