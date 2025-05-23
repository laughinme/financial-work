from fastapi import Depends, Request, HTTPException
from database.relational_db import User
from service import get_user_service, UserService


async def auth_user(
    request: Request,
    user_service: UserService = Depends(get_user_service)
) -> User:
    user = await user_service.get_me(request)
    if not user:
        raise HTTPException(401, detail="Not authorized")
    
    return user
