from typing import Annotated
from fastapi import APIRouter, Depends, Query

from core.security import auth_admin, auth_user
from service.admins import AdminService, get_admin_service
from database.relational_db import User
from domain.admins import Settlement


router = APIRouter()


@router.get(
    path='/settlements',
    response_model=list[Settlement]
)
async def settlements(
    service: Annotated[AdminService, Depends(get_admin_service)],
    orders_quantity: int = Query(
        5, description='Number of orders to return for each settlement'
    ),
    _: User = Depends(auth_admin)
):
    return await service.settlements(orders_quantity)
