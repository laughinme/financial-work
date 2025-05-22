from fastapi import APIRouter, Depends, Request

from core.config import Config
from core.security import auth_user
from database.relational_db import User
from service import UserService, get_user_service
from domain.users import UserRegister, UserLogin
from .schemas import UserSchema

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


@router.post(
    path="/login",
    response_model=UserSchema
)
async def login_user(
    request: Request,
    payload: UserLogin,
    user_service: UserService = Depends(get_user_service)
) -> UserSchema:
    user = await user_service.login(payload, request)
    return user


@router.get(
    path="/me",
    response_model=UserSchema
)
async def get_me(
    user: User = Depends(auth_user)
) -> UserSchema:
    return user
