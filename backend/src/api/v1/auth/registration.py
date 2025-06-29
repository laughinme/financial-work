from typing import Annotated
from fastapi import APIRouter, Depends, Response

from core.config import Config
from service.auth import CredentialsService, get_credentials_service
from domain.users import UserRegister, AccessToken

config = Config()
router = APIRouter()


@router.post(
    path='/register',
    response_model=AccessToken,
    status_code=201,
    responses={
        409: {"description": "User with provided credentials already exists"}
    }
)
async def register_user(
    response: Response,
    payload: UserRegister,
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)]
) -> AccessToken:
    access, refresh = await creds_service.register(payload)
    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=config.REFRESH_TTL,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    
    return AccessToken(access_token=access)
