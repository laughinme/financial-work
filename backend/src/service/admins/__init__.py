from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    InvestOrderInterface
)
from .admin_service import AdminService


async def get_admin_service(
    uow: UoW = Depends(get_uow)
) -> AdminService:
    io_repo = InvestOrderInterface(uow.session)
    
    return AdminService(
        uow, io_repo
    )
