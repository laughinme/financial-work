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
from .exceptions import PortfolioNotFound, InsufficientFunds


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
        
    
    @staticmethod
    def calc_nav_price(equity: Decimal, units_total: Decimal) -> Decimal:
        if units_total == 0:
            nav_price = Decimal('1') 
        else:
            nav_price = (equity / units_total).quantize(Decimal('0.00000001'))
        return nav_price
        
        
    async def invest(
        self,
        portfolio_id: int,
        amount: Decimal,
        # currency: str,
        user_id: UUID
    ) -> None:
        portfolio = await self.p_repo.get_by_id(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFound()
        
        currency = portfolio.currency
        
        wallet = await self.w_repo.freeze(user_id, currency, amount)
        if wallet is None:
            raise InsufficientFunds()
        
        order = InvestOrder(
            user_id=user_id,
            portfolio_id=portfolio_id,
            direction=OrderDirection.INVEST,
            amount=amount,
            currency=currency,
            status=InvestOrderStatus.PENDING
        )
        await self.io_repo.add(order)
        
        transaction = Transaction(
            user_id=user_id,
            portfolio_id=portfolio_id,
            type=TransactionType.INVEST_PENDING,
            amount=amount,
            currency=currency,
        )
        await self.t_repo.add(transaction)
        
        
    async def withdraw(
        self,
        p_id: int,
        amount: Decimal,
        user_id: UUID,
    ):
        portfolio = await self.p_repo.get_by_id(p_id)
        if portfolio is None:
            raise PortfolioNotFound()
        
        currency = portfolio.currency
        
        holding = await self.h_repo.user_portfolio_holding(user_id, p_id)
        if holding is None or holding.current_value < amount:
            raise InsufficientFunds()
        
        order = InvestOrder(
            user_id=user_id,
            portfolio_id=p_id,
            direction=OrderDirection.PAYBACK,
            amount=amount,
            currency=currency,
            status=InvestOrderStatus.PENDING
        )
        await self.io_repo.add(order)
        
        transaction = Transaction(
            user_id=user_id,
            portfolio_id=p_id,
            type=TransactionType.PAYBACK_PENDING,
            amount=amount,
            currency=currency,
        )
        await self.t_repo.add(transaction)
        

    async def update_batch(self, portfolio_ids: set[int]):
        for p_id in portfolio_ids:
            async with self.p_repo.get_isolated(p_id) as portfolio:
                orders = await self.io_repo.get_by_pid(p_id, InvestOrderStatus.ACCEPTED)

                nav_price = portfolio.nav_price
                issued_total, burned_total = Decimal('0'), Decimal('0')
                
                for order in orders:
                    user_id = order.user_id
                    amount = order.amount
                    
                    if order.direction == OrderDirection.INVEST:
                        wallet = await self.w_repo.withdraw(user_id, order.currency, amount)
                        if wallet is None:
                            order.status = InvestOrderStatus.FAILED
                            continue
                        order.status = InvestOrderStatus.EXECUTED
                        
                        units = (amount / nav_price).quantize(Decimal("0.00000001"))
                        issued_total += units
                        
                        await self.h_repo.issue_units(user_id, p_id, units, amount, nav_price)
                        
                        tx_type = TransactionType.INVEST
                    
                    elif order.direction == OrderDirection.PAYBACK:                        
                        units = (amount / nav_price).quantize(Decimal("0.00000001"))
                        
                        if not await self.h_repo.burn_units(user_id, p_id, units, amount, nav_price):
                            order.status = InvestOrderStatus.FAILED
                            continue
                        
                        await self.w_repo.credit(user_id, order.currency, amount)
                        order.status = InvestOrderStatus.EXECUTED
                        burned_total += units
                        
                        tx_type = TransactionType.PAYBACK
                        
                    else: continue
                    
                    transaction = Transaction(
                        user_id=user_id,
                        portfolio_id=order.portfolio_id,
                        type=tx_type,
                        amount=amount,
                        currency=order.currency,
                    )
                    await self.t_repo.add(transaction)
                
                portfolio.units_total += issued_total - burned_total
                portfolio.nav_price = self.calc_nav_price(portfolio.equity, portfolio.units_total)


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
