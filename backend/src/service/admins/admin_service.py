from sqlalchemy.exc import IntegrityError

from database.relational_db import (
    UoW, InvestOrderInterface, InvestOrder
)
from domain.investments import InvestOrderStatus
from core.config import Config
from ..payments.stripe_service import StripeService
from ..investments import InvestmentService


config = Config()


class AdminService:
    def __init__(
        self,
        uow: UoW,
        io_repo: InvestOrderInterface,
        stripe_service: StripeService,
        i_service: InvestmentService,
    ):
        self.uow = uow
        self.io_repo = io_repo
        self.stripe_service = stripe_service
        self.i_service = i_service
        
    
    async def settlements(self, orders_quantity: int = 5) -> list[InvestOrder]:
        briefs = await self.io_repo.settlements_brief()
        pids = [b["portfolio_id"] for b in briefs]
        orders = await self.io_repo.aggregated_orders(pids, quantity=orders_quantity)

        for b in briefs:
            b["orders"] = orders.get(b["portfolio_id"], [])
        return briefs
    
    
    async def intent(self, portfolio_id: int):
        delta = await self.io_repo.portfolio_delta(portfolio_id)
        await self.i_service.update_admin(portfolio_id)
