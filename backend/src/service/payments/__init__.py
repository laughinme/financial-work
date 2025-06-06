from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    TransactionInterface,
    PaymentIntentInterface,
    WalletInterface
)
from service.investments import InvestmentService, get_investment_service
from .yookassa_service import YooKassaService


async def get_yookassa_service(
    uow: UoW = Depends(get_uow),
    invest_service: InvestmentService = Depends(get_investment_service)
) -> YooKassaService:
    intent_repo = PaymentIntentInterface(uow.session)
    transaction_repo = TransactionInterface(uow.session)
    wallet_repo = WalletInterface(uow.session)
    return YooKassaService(
        uow, intent_repo, transaction_repo, wallet_repo, invest_service
    )
