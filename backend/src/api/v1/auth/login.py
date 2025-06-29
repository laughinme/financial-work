from typing import Annotated
from fastapi import APIRouter, Depends, Response, Request

from core.config import Config
from core.security import auth_user
from service.auth import CredentialsService, get_credentials_service
from domain.users import UserLogin, AccessToken
from database.relational_db import User

config = Config()
router = APIRouter()


@router.post(
    path="/login",
    response_model=AccessToken,
    responses={401: {"description": "Wrong credentials"}}
)
async def login_user(
    response: Response,
    payload: UserLogin,
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)]
) -> AccessToken:
    access, refresh = await creds_service.login(payload)
    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=config.REFRESH_TTL,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    
    return AccessToken(access_token=access)


@router.post(
    path="/logout",
    status_code=204,
    responses={401: {"description": "Not authorized"}}
)
async def logout(
    request: Request,
    response: Response,
    creds_service: Annotated[CredentialsService, Depends(get_credentials_service)],
    _: Annotated[User, Depends(auth_user)]
) -> None:
    token = request.cookies.get("refresh_token")
    if token:
        await creds_service.logout(token)
        
    response.delete_cookie("refresh_token")
