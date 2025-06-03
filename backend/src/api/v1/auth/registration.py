from fastapi import APIRouter, Depends, Request

from core.config import Config
from service.auth import CredentialsService, get_credentials_service
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
    creds_service: CredentialsService = Depends(get_credentials_service)
) -> UserSchema:
    user = await creds_service.register(request, payload, config.SESSION_LIFETIME)
    return user
