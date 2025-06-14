from fastapi import Depends

from database.relational_db import UoW, get_uow, TransactionInterface, HoldingsInterface, PortfolioInterface
from .service import DashboardService


async def get_dashboard_service(
    uow: UoW = Depends(get_uow),
) -> DashboardService:
    p_repo = PortfolioInterface(uow.session)
    h_repo = HoldingsInterface(uow.session)
    tx_repo = TransactionInterface(uow.session)
    return DashboardService(uow, p_repo, h_repo, tx_repo)
