import asyncio
import stripe
import logging

from database.relational_db import (
    UoW,
    User,
    PaymentIntent,
    PaymentIntentInterface,
    Transaction,
    TransactionInterface,
    WalletInterface,
)
from domain.payments import PaymentStatus, PaymentProvider, CreatePaymentSchema, TransactionType, DepositAction
from service.investments import InvestmentService
from core.config import Config
from .exceptions import PaymentFailed, UnsupportedEvent

config = Config()

stripe.api_key = config.STRIPE_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StripeService:
    def __init__(
        self,
        uow: UoW,
        intent_repo: PaymentIntentInterface,
        t_repo: TransactionInterface,
        w_repo: WalletInterface,
        invest_service: InvestmentService,
    ):
        self.uow, self.intent_repo, self.t_repo, self.w_repo = (
            uow,
            intent_repo,
            t_repo,
            w_repo,
        )
        self.invest_service = invest_service

    async def create_payment(self, payload: CreatePaymentSchema, user: User):
        intent = PaymentIntent(
            user_id=user.id,
            amount=payload.amount,
            currency="USD",
            status=PaymentStatus.PENDING,
            provider=PaymentProvider.STRIPE,
            _metadata=None,
        )
        await self.intent_repo.add(intent)
        await self.uow.session.flush()

        metadata = {
            "intent_id": str(intent.id),
            "user_id": str(user.id),
            "action": payload.action.value,
            "action_id": payload.action_id,
        }

        try:
            session = await asyncio.to_thread(
                StripeService._create_session, payload, metadata
            )
            intent.provider_payment_id = session.id
            return session.url
        except Exception:
            await self.uow.session.rollback()
            intent.status = PaymentStatus.FAILED
            raise PaymentFailed()

    @staticmethod
    def _create_session(payload: CreatePaymentSchema, metadata: dict):
        return stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": payload.description or "Deposit"},
                        "unit_amount": int(payload.amount * 100),
                    },
                    "quantity": 1,
                }
            ],
            metadata=metadata,
            success_url=config.SITE_URL,
            cancel_url=config.SITE_URL,
        )

    async def process_payment(self, body: dict):
        event_type = body.get("type")
        data = body.get("data", {}).get("object", {})
        metadata: dict[str, str] = data.get("metadata", {})
        intent_id = metadata.get("intent_id")
        user_id = metadata.get("user_id")
        
        logger.info(event_type)

        if not intent_id or not user_id:
            logger.warning("No intent metadata")
            raise UnsupportedEvent()

        intent = await self.intent_repo.get(intent_id)
        if intent.status == PaymentStatus.SUCCEEDED:
            logger.info("Duplicate webhook, ignoring")
            return

        match event_type:
            case "checkout.session.completed":
                payment_intent = data.get("payment_intent")
                amount_total = data.get("amount_total") or 0
                amount = (amount_total / 100) if amount_total else 0
                currency = "USD"
                description = data.get("description")

                await self.intent_repo.update_status(
                    intent_id, PaymentStatus.SUCCEEDED
                )
                await self.w_repo.credit(user_id, currency, amount)

                transaction = Transaction(
                    user_id=user_id,
                    intent_id=intent_id,
                    type=TransactionType.DEPOSIT,
                    amount=amount,
                    currency=currency,
                    comment=description,
                )
                await self.t_repo.add(transaction)

                await self.uow.session.commit()

                match metadata.get("action"):
                    case DepositAction.INVEST.value:
                        portfolio_id = int(metadata.get("action_id"))
                        await self.invest_service.invest(
                            portfolio_id, amount, user_id
                        )

                logger.info(
                    f"Payment {payment_intent} for the amount {amount} {currency} has been successfully completed."
                )
            case "payment_intent.payment_failed":
                await self.intent_repo.update_status(intent_id, PaymentStatus.FAILED)
                logger.warning("Payment failed")
            case _:
                logger.warning(f"Unsupported event: {event_type}")
                raise UnsupportedEvent()
