from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    InvestOrderInterface
)
from .admin_service import AdminService
from ..payments import StripeService, get_stripe_service
from ..investments import InvestmentService, get_investment_service


async def get_admin_service(
    uow: UoW = Depends(get_uow),
    s_service: StripeService = Depends(get_stripe_service),
    i_service: InvestmentService = Depends(get_investment_service)
) -> AdminService:
    io_repo = InvestOrderInterface(uow.session)
    
    return AdminService(
        uow, io_repo, s_service, i_service
    )
