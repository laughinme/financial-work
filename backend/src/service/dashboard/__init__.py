from fastapi import Depends

from database.relational_db import UoW, get_uow, TransactionInterface, HoldingsInterface
from .service import DashboardService


async def get_dashboard_service(
    uow: UoW = Depends(get_uow),
) -> DashboardService:
    tx_repo = TransactionInterface(uow.session)
    h_repo = HoldingsInterface(uow.session)
    return DashboardService(uow, tx_repo, h_repo)
