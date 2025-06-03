# from fastapi import APIRouter, Depends, Request

# from core.config import Config
# from core.security import auth_user
# from service.auth import CredentialsService, get_credentials_service
# from domain.users import UserRegister, UserSchema
# from database.relational_db import User

# config = Config()
# router = APIRouter()


# @router.post(
#     path='/credentials',
#     response_model=UserSchema,
#     status_code=200
# )
# async def link_credentials(
#     payload: UserRegister,
#     creds_service: CredentialsService = Depends(get_credentials_service),
#     user: User = Depends(auth_user)
# ) -> UserSchema:
#     user = await creds_service.register(payload, user)
#     return user

# TODO: when auth0 module will be connected, make credentials link possible