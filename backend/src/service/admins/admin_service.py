from sqlalchemy.exc import IntegrityError

from database.relational_db import (
    UoW, InvestOrderInterface, InvestOrder
)
from domain.investments import InvestOrderStatus
from core.config import Config


config = Config()


class AdminService:
    def __init__(
        self,
        uow: UoW,
        io_repo: InvestOrderInterface
    ):
        self.uow = uow
        self.io_repo = io_repo
        
    
    async def settlements(self, orders_quantity: int = 5) -> list[InvestOrder]:
        briefs = await self.io_repo.settlements_brief()
        pids = [b["portfolio_id"] for b in briefs]
        orders = await self.io_repo.aggregated_orders(pids, quantity=orders_quantity)

        for b in briefs:
            b["orders"] = orders.get(b["portfolio_id"], [])
        return briefs
    
    

    