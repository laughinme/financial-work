from uuid import UUID

from database.relational_db import (
    UoW, Portfolio, PortfolioInterface, Holding, HoldingsInterface
)


class DashboardService:
    def __init__(
        self,
        uow: UoW,
        p_repo: PortfolioInterface,
        h_repo: HoldingsInterface
    ):
        self.uow = uow
        self.p_repo = p_repo
        self.h_repo = h_repo


    async def allocation(self, user_id: UUID):
        return await self.h_repo.allocation(user_id)
