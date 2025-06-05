from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    PortfolioInterface
)
from .portfolio_service import PortfolioService


async def get_portfolio_service(
    uow: UoW = Depends(get_uow),  
) -> PortfolioService:
    portfolio_repo = PortfolioInterface(uow.session)
    return PortfolioService(uow, portfolio_repo)
