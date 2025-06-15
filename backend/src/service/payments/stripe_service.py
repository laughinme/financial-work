import asyncio
import stripe
import logging

from decimal import Decimal

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
from .exceptions import PaymentFailed, UnsupportedEvent, NoUSDWallet, PaymentSystemException

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
    
    
    @staticmethod
    def _retrieve_balance() -> stripe.Balance:
        balance = stripe.Balance.retrieve()
        logger.info(balance)
        for wallet in balance.available:
            if wallet.currency == 'usd':
                return wallet.amount
        else:
            raise NoUSDWallet
        
        
    @staticmethod
    async def _create_payout(amount: Decimal) -> stripe.Payout:
       return await asyncio.to_thread(
            stripe.Payout.create(
                amount=amount, currency="usd", description='Payout to bank account'
            )
        )
    
    async def create_payout(self, amount: Decimal) -> stripe.Payout:
        try:
            balance = await asyncio.to_thread(self._retrieve_balance)
        except NoUSDWallet:
            raise PaymentSystemException
        
        logger.info('amount: %s', amount)
        logger.info('balance: %s', balance)
        payout = await self._create_payout(int(amount))
        return payout


    @staticmethod
    def _create_connected_account(user: User) -> stripe.Account:
        if user.stripe_account_id:
            return stripe.Account.retrieve(user.stripe_account_id)

        account = stripe.Account.create(
            # type="custom",
            business_type="individual",
            controller={
                "stripe_dashboard": {
                "type": "none",
                },
                "fees": {
                "payer": "application"
                },
                "losses": {
                "payments": "application"
                },
                "requirement_collection": "application",
            },
            # individual={
            #     "first_name": user.first_name,
            #     "last_name":  user.last_name,
            #     "email":      user.email,
            # },
            capabilities={
                "transfers": {"requested": True},
                # "card_payments": {"requested": True},
            },
            metadata={"platform_user_id": str(user.id)}
        )

        user.stripe_account_id = account.get('id')
        return account


    async def connected_account(self, user: User):
        """
        Creates or retrieves a connected account.
        """
        
        return await asyncio.to_thread(
            self._create_connected_account, user
        )

    
    @staticmethod
    def _create_account_link(account_id: str) -> stripe.AccountLink:
        """
        Generates one-time URL that sends the user to Stripe-hosted onboarding.
        """
        link = stripe.AccountLink.create(
            account=account_id,
            type="account_onboarding",
            refresh_url=config.SITE_URL,
            return_url=config.SITE_URL,
            collection_options={"fields": "eventually_due"},
        )
        return link
    
    
    async def create_account_link(self, account_id: str) -> str:
        return await asyncio.to_thread(
            self._create_account_link, account_id
        )
