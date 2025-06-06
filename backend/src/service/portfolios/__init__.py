from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    PortfolioInterface,
    GainsInterface,
    HoldingsInterface,
    InvestOrderInterface
)
from .portfolio_service import PortfolioService


async def get_portfolio_service(
    uow: UoW = Depends(get_uow),
) -> PortfolioService:
    portfolio_repo = PortfolioInterface(uow.session)
    gains_repo = GainsInterface(uow.session)
    holdings_repo = HoldingsInterface(uow.session)
    invest_order_repo = InvestOrderInterface(uow.session)
    return PortfolioService(
        uow, portfolio_repo, gains_repo, holdings_repo, invest_order_repo
    )
