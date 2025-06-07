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
from domain.investments import InvestOrderStatus
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
        
        p_currency = portfolio.currency
        
        order = InvestOrder(
            user_id=user_id,
            portfolio_id=portfolio_id,
            init_amount=amount,
            init_currency=currency,
            currency=p_currency,
            status=InvestOrderStatus.PENDING
        )
        await self.io_repo.add(order)
        
        wallet = await self.w_repo.freeze(user_id, currency, amount)
        if wallet is None:
            raise PaymentRequired()
        
        # TODO: add transaction with status INVEST_PENDING
        
        
    async def convert_to_usd(self):
        ready_total_usd = Decimal("0")
        


    async def update_batch(self, portfolio_ids: set[int]):
        orders = await self.io_repo.get_by_pids(portfolio_ids)
        
        for order in orders:
            portfolio = await self.p_repo.get_isolated(order.portfolio)
            
            user_id = order.user_id
            amount = order.amount
            nav_price = portfolio.nav_price
            
            wallet = await self.w_repo.withdraw(user_id, order.currency, amount)
            if wallet is None:
                order.status = InvestOrderStatus.FAILED
                continue
            order.status = InvestOrderStatus.EXECUTED
            
            units = (amount / nav_price).quantize(Decimal("0.00000001"))
            portfolio.equity += amount
            portfolio.units_total += units
            
            await self.h_repo.issue_units(user_id, units, amount)
            
            transaction = Transaction(
                user_id=user_id,
                portfolio_id=order.portfolio_id,
                type=TransactionType.INVEST,
                amount=amount,
                currency=order.currency,
                # comment=
            )
            await self.t_repo.add(transaction)
