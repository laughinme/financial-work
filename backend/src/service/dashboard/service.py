from uuid import UUID

from database.relational_db import (
    UoW, PortfolioInterface, HoldingsInterface, TransactionInterface
)


class DashboardService:
    def __init__(
        self,
        uow: UoW,
        p_repo: PortfolioInterface,
        h_repo: HoldingsInterface,
        tx_repo: TransactionInterface
    ):
        self.uow = uow
        self.p_repo = p_repo
        self.h_repo = h_repo
        self.tx_repo = tx_repo


    async def allocation(self, user_id: UUID) -> list:
        return await self.h_repo.allocation(user_id)

    
    async def cashflow(self, user_id: UUID, days: int):
        return await self.tx_repo.cash_flow(user_id, days)
