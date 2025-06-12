from fastapi import APIRouter, Depends, Request

from core.config import Config
from service.auth import CredentialsService, get_credentials_service
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
    creds_service: CredentialsService = Depends(get_credentials_service)
) -> UserSchema:
    user = await creds_service.login(request, payload, config.SESSION_LIFETIME)
    return user
