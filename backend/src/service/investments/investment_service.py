import logging

from decimal import Decimal
from uuid import UUID
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError

from database.relational_db import (
    UoW,
    PortfolioInterface,
    WalletInterface,
    HoldingsInterface,
    InvestOrder,
    InvestOrderInterface,
    Transaction,
    TransactionInterface
)
from database.redis import CacheRepo
from domain.investments import InvestOrderStatus, OrderDirection
from domain.payments import TransactionType
from core.config import Config
from .exceptions import PortfolioNotFound, PaymentRequired


config = Config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvestmentService:
    def __init__(
        self,
        uow: UoW,
        p_repo: PortfolioInterface,
        h_repo: HoldingsInterface,
        io_repo: InvestOrderInterface,
        w_repo: WalletInterface,
        t_repo: TransactionInterface
    ):
        self.uow, self.p_repo, self.w_repo = uow, p_repo, w_repo
        self.h_repo, self.io_repo, self.t_repo = h_repo, io_repo, t_repo
        
        
    async def invest(
        self,
        portfolio_id: int,
        amount: Decimal,
        currency: str,
        user_id: UUID
    ) -> None:
        portfolio = await self.p_repo.get_by_id(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFound()
        
        order = InvestOrder(
            user_id=user_id,
            portfolio_id=portfolio_id,
            direction=OrderDirection.INVEST,
            amount=amount,
            currency=currency,
            status=InvestOrderStatus.PENDING
        )
        await self.io_repo.add(order)
        
        wallet = await self.w_repo.freeze(user_id, currency, amount)
        if wallet is None:
            raise PaymentRequired()
        
        transaction = Transaction(
            user_id=user_id,
            portfolio_id=order.portfolio_id,
            type=TransactionType.INVEST_PENDING,
            amount=amount,
            currency=currency,
        )
        await self.t_repo.add(transaction)
        

    async def update_batch(self, portfolio_ids: set[int]):
        for p_id in portfolio_ids:
            async with self.p_repo.get_isolated(p_id) as portfolio:
                orders = await self.io_repo.get_by_pid(p_id, InvestOrderStatus.ACCEPTED)

                nav_price = portfolio.nav_price
                issued_total = Decimal('0')
                
                for order in orders:
                    user_id = order.user_id
                    amount = order.amount
                    
                    wallet = await self.w_repo.withdraw(user_id, order.currency, amount)
                    if wallet is None:
                        order.status = InvestOrderStatus.FAILED
                        continue
                    order.status = InvestOrderStatus.EXECUTED
                    
                    units = (amount / nav_price).quantize(Decimal("0.00000001"))
                    issued_total += units
                    
                    await self.h_repo.issue_units(user_id, units, amount)
                    
                    transaction = Transaction(
                        user_id=user_id,
                        portfolio_id=order.portfolio_id,
                        type=TransactionType.INVEST,
                        amount=amount,
                        currency=order.currency,
                    )
                    await self.t_repo.add(transaction)
                
                portfolio.units_total += issued_total
                portfolio.nav_price = (portfolio.equity / portfolio.units_total).quantize(Decimal("0.00000001"))


    async def update_admin(
        self,
        p_id: int
    ) -> None:
        orders = await self.io_repo.get_by_pid(p_id, status=InvestOrderStatus.PENDING)
        for order in orders:
            order.status = InvestOrderStatus.ACCEPTED
    
    
    async def user_portfolio(
        self,
        user_id: UUID,
        p_id: int
    ):
        holding = await self.h_repo.user_portfolio_holding(user_id, p_id)
        
        return holding
    
    
    async def user_summary(
        self,
        user_id: UUID
    ):
        result = await self.h_repo.user_summary(user_id)
        return result
