from typing import Annotated
from fastapi import APIRouter, Depends

from core.config import Config
from service.auth import CredentialsService, get_credentials_service
from domain.users import UserRegister, UserSchema

config = Config()
router = APIRouter()


@router.post(
    path='/register',
    response_model=UserSchema,
    status_code=201,
    responses={
        409: {"description": "User with provided credentials already exists"}
    }
)
async def register_user(
    payload: UserRegister,
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)]
) -> UserSchema:
    user = await creds_service.register(payload, config.SESSION_LIFETIME)
    return user
