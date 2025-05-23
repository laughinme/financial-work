from fastapi import APIRouter, Depends, Request

from core.config import Config
from core.security import auth_user
from database.relational_db import User
from ..schemas import UserSchema

config = Config()
router = APIRouter()


@router.get(
    path="/me",
    response_model=UserSchema
)
async def get_me(
    user: User = Depends(auth_user)
) -> UserSchema:
    return user