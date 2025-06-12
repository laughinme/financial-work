import asyncio
import yookassa
import logging
# import uuid_utils # I'm hatin it
from uuid import uuid4
from yookassa.domain.notification import WebhookNotification

from database.relational_db import (
    UoW,
    User,
    PaymentIntent,
    PaymentIntentInterface,
    Transaction,
    TransactionInterface, 
    WalletInterface
)
from domain.payments import PaymentStatus, PaymentProvider, CreatePaymentSchema, TransactionType, DepositAction
from service.investments import InvestmentService
from core.config import Config
from .exceptions import PaymentFailed, UnsupportedEvent

config = Config()

yookassa.Configuration.account_id = config.YOOKASSA_ACCOUNT_ID
yookassa.Configuration.secret_key = config.YOOKASSA_SECRET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YooKassaService:
    def __init__(
        self,
        uow: UoW,
        intent_repo: PaymentIntentInterface,
        t_repo: TransactionInterface,
        w_repo: WalletInterface,
        invest_service: InvestmentService
    ):
        self.uow, self.intent_repo, self.t_repo, self.w_repo = uow, intent_repo, t_repo, w_repo
        self.invest_service = invest_service


    async def create_payment(self, payload: CreatePaymentSchema, user: User):
        intent = PaymentIntent(
            user_id=user.id,
            amount=payload.amount,
            currency=payload.currency,
            status=PaymentStatus.PENDING,
            provider=PaymentProvider.YOOKASSA,
            _metadata=None
        )
        await self.intent_repo.add(intent)
        await self.uow.session.flush()
        
        metadata = {
            'intent_id': str(intent.id),
            'user_id': str(user.id),
            'action': payload.action.value,
            'action_id': payload.action_id
        }
        
        try:
            payment = await asyncio.to_thread(
                YooKassaService._create_payment, payload, metadata
            )
            
            intent.provider_payment_id = payment.id
            return payment.confirmation.confirmation_url
            
        except Exception as e:
            await self.uow.session.rollback()

            intent.status = PaymentStatus.FAILED
            raise PaymentFailed()


    @staticmethod
    def _create_payment(payload: CreatePaymentSchema, metadata: dict = {}):
        return yookassa.Payment.create(
        {
            "amount": {
                "value": payload.amount,
                "currency": payload.currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": config.SITE_URL
            },
            "description": payload.description,
            "capture": True,
            "metadata": metadata
        }, str(uuid4())
        )
    
    
    async def get_payment_info(self, uuid: str) -> dict:
        return await asyncio.to_thread(YooKassaService._get_payment_info, uuid)

    @staticmethod
    def _get_payment_info(uuid: str) -> dict:
        return yookassa.Payment.find_one(uuid)
    
    
    async def payout(self, payload):
        return await asyncio.to_thread(YooKassaService._payout, payload)
    
    @staticmethod
    def _payout(payload):
        return yookassa.Payout.create(
            {
                "amount": {
                    "value": payload.value,
                    "currency": payload.currency
                },
                "payout_destination_data": {
                    "type": "bank_card",
                    "card": {
                        "number": payload.card_number
                    }
                },
                "description": payload.description,
            }, str(uuid4())
        )
        
    
    async def process_payment(self, body: str):
        notification_object = WebhookNotification(body)
        event = notification_object.event
        payment = notification_object.object
        metadata: dict[str, str] = payment.metadata
        intent_id, user_id = metadata['intent_id'], metadata['user_id']
        
        intent = await self.intent_repo.get(intent_id)
        if intent.status == PaymentStatus.SUCCEEDED:
            logger.info("Duplicate webhook, ignoring")
            return

        match event:
            case 'payment.succeeded':
                payment_id = payment.id
                amount = payment.amount.value
                currency = payment.amount.currency.upper()
                description = payment.description
                
                await self.intent_repo.update_status(intent_id, PaymentStatus.SUCCEEDED)
                
                await self.w_repo.credit(user_id, currency, amount)
                
                transaction = Transaction(
                    user_id=user_id,
                    intent_id=intent_id,
                    type=TransactionType.DEPOSIT,
                    amount=amount,
                    currency=currency,
                    comment=description
                )
                await self.t_repo.add(transaction)
                
                await self.uow.session.commit()
                
                match metadata['action']:
                    case DepositAction.INVEST.value:
                        portfolio_id = int(metadata.get('action_id'))
                        await self.invest_service.invest(portfolio_id, amount, user_id)
                
                logger.info(f"Payment {payment_id} for the amount {amount} {currency} has been successfully completed.")
                
            case 'payment.failed':
                await self.intent_repo.update_status(intent_id, PaymentStatus.FAILED)
                
                logger.warning(f"Payment failed: {event}")
            
            case _:
                logger.warning(f"Unsupported event: {event}")
                raise UnsupportedEvent()
