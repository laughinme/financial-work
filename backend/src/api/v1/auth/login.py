from typing import Annotated
from fastapi import APIRouter, Depends

from core.config import Config
from core.security import auth_user
from service.auth import CredentialsService, get_credentials_service
from domain.users import UserLogin, UserSchema
from database.relational_db import User

config = Config()
router = APIRouter()


@router.post(
    path="/login",
    response_model=UserSchema,
    responses={401: {"description": "Wrong credentials"}}
)
async def login_user(
    payload: UserLogin,
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)]
) -> UserSchema:
    user = await creds_service.login(payload, config.SESSION_LIFETIME)
    return user


@router.post(
    path="/logout",
    status_code=204,
    responses={401: {"description": "Not authorized"}}
)
async def logout(
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)],
    _: Annotated[User, Depends(auth_user)]
) -> None:
    await creds_service.logout()
