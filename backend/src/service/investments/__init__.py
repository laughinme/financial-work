from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    PortfolioInterface,
    HoldingsInterface,
    InvestOrderInterface,
    WalletInterface,
    TransactionInterface
)
from .investment_service import InvestmentService


async def get_investment_service(
    uow: UoW = Depends(get_uow),
) -> InvestmentService:
    portfolio_repo = PortfolioInterface(uow.session)
    wallet_repo = WalletInterface(uow.session)
    holdings_repo = HoldingsInterface(uow.session)
    invest_order_repo = InvestOrderInterface(uow.session)
    transaction_repo = TransactionInterface(uow.session)
    return InvestmentService(
        uow, portfolio_repo, holdings_repo, invest_order_repo, wallet_repo, transaction_repo
    )
