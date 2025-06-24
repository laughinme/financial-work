from fastapi import Depends

from core.security import auth_user, AuthRouter
from database.relational_db import User
from domain.users import UserSchema


router = AuthRouter()


@router.get(
    path="/",
    response_model=UserSchema
)
async def get_me(user: User = Depends(auth_user)) -> UserSchema:
    return user
