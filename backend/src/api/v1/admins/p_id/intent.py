from typing import Annotated
from fastapi import APIRouter, Depends, Path

from core.security import auth_admin, auth_user
from service.admins import AdminService, get_admin_service
from database.relational_db import User


router = APIRouter()


@router.post(
    path='/intent',
    status_code=204,
    responses={
        403: {"description": "You don't have permission to do this"}
    }
)
async def settlement_intent(
    portfolio_id: Annotated[int, Path(...)],
    service: Annotated[AdminService, Depends(get_admin_service)],
    _: Annotated[User, Depends(auth_admin)]
):
    await service.intent(portfolio_id)
