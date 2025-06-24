from typing import Annotated
from fastapi import Depends

from core.config import Config
from core.security import auth_user, AuthRouter
from service.auth import CredentialsService, get_credentials_service
from domain.users import UserRegister, UserSchema
from database.relational_db import User

config = Config()
router = AuthRouter()


@router.post(
    path='/email',
    status_code=204
)
async def link_email(
    payload: UserRegister,
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)],
    user: Annotated[User, Depends(auth_user)]
):
    await creds_service.link(payload.email, user)


@router.post(
    path='/phone',
    status_code=204
)
async def link_phone(
    payload: UserRegister,
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)],
    user: Annotated[User, Depends(auth_user)]
):
    await creds_service.link(payload.phone_number, user)

# TODO: when auth0 module will be connected, rework credentials linking