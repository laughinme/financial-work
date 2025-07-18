import asyncio
import stripe
import logging

from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP

from database.relational_db import (
    UoW,
    User,
    PaymentIntent,
    PaymentIntentInterface,
    Transaction,
    TransactionInterface,
    WalletInterface,
)
from domain.payments import PaymentStatus, PaymentProvider, CreatePayment, TransactionType, DepositAction, Onboarding
from service.investments import InvestmentService
from core.config import Config
from .exceptions import PaymentFailed, UnsupportedEvent, NoUSDWallet

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

    async def create_payment(
        self, payload: CreatePayment, user: User
    ) -> stripe.checkout.Session:
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
            return session
        except Exception as e:
            print(e)
            await self.uow.session.rollback()
            intent.status = PaymentStatus.FAILED
            raise PaymentFailed()

    @staticmethod
    def _create_session(
        payload: CreatePayment, metadata: dict
    ) -> stripe.checkout.Session:
        amount_cents = int(payload.amount * 100)
        fee_cents = int((amount_cents + 30) / 0.970) - amount_cents
        metadata['price_no_fee'] = payload.amount
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Deposit"},
                        "unit_amount": amount_cents,
                    },
                    "quantity": 1,
                },
                {
                    "price_data": {
                        "product_data": {"name": "Processing fee"},
                        "currency": "usd",
                        "unit_amount": fee_cents
                    },
                    "quantity": 1
             },
            ],
            metadata=metadata,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
        )
        
        return session


    async def process_webhook(self, body: dict):
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
        if intent.status in (PaymentStatus.SUCCEEDED, PaymentStatus.FAILED):
            logger.info("Duplicate webhook, ignoring")
            return

        match event_type:
            case "checkout.session.completed":
                payment_intent = data.get("payment_intent")
                # amount_total = data.get("amount_total") or 0
                # amount = (amount_total / 100) if amount_total else 0
                amount = Decimal(metadata.get('price_no_fee'))
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
                
            case "payout.paid":
                payout_id = data.get("id")
                amount = (Decimal(data.get('amount')) / 100).quantize(Decimal("0.01"), ROUND_HALF_UP)
                currency = "USD"
                user_id = metadata.get('user_id')
                
                logger.info('WITHDRAWAL')
                await self.w_repo.withdraw(user_id, currency, amount)
                
                transaction = Transaction(
                    user_id=user_id,
                    intent_id=intent_id,
                    type=TransactionType.WITHDRAW,
                    amount=amount,
                    currency=currency
                )
                await self.t_repo.add(transaction)
                
                await self.intent_repo.update_status(intent_id, PaymentStatus.SUCCEEDED)
                
                logger.info(f"Payout succeeded: {payout_id}, amount: {amount} {currency}")
                
            case "payout.failed":
                payout_id = data.get("id")
                amount = (Decimal(data.get('amount')) / 100).quantize(Decimal("0.01"), ROUND_HALF_UP)
                currency = "USD"
                failure_message = data.get("failure_message")
                
                await self.w_repo.cancel_withdrawal(user_id, currency, amount)
                
                await self.intent_repo.update_status(intent_id, PaymentStatus.FAILED)
                
                logger.warning(f"Payout failed: {payout_id}, amount: {amount} {currency}, reason: {failure_message}")
                
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

        user.stripe_account_id = account.id
        return account


    async def connected_account(self, user: User):
        """
        Creates or retrieves a connected account.
        """
        
        return await asyncio.to_thread(
            self._create_connected_account, user
        )

    
    @staticmethod
    def _create_account_link(account_id: str, payload: Onboarding) -> stripe.AccountLink:
        """
        Generates one-time URL that sends the user to Stripe-hosted onboarding.
        """
        link = stripe.AccountLink.create(
            account=account_id,
            type="account_onboarding",
            refresh_url=payload.refresh_url,
            return_url=payload.return_url,
            collection_options={"fields": "eventually_due"},
        )
        return link
    
    
    async def create_account_link(self, account_id: str, payload: Onboarding) -> str:
        return await asyncio.to_thread(
            self._create_account_link, account_id, payload
        )


    @staticmethod
    def _create_transfer(amount: Decimal, account_id: str):
        transfer = stripe.Transfer.create(
          amount=int(amount * 100),
          currency="usd",
          destination=account_id
        )
        
        return transfer
    
    
    async def create_transfer(self, amount: Decimal, account_id: str):
        return await asyncio.to_thread(
            self._create_transfer, amount, account_id
        )
        
    
    @staticmethod
    def _create_payout_connect(amount: Decimal, account_id: str, metadata: dict = {}) -> stripe.Payout:
        payout = stripe.Payout.create(
            amount=int(amount * 100),
            currency="usd",
            stripe_account=account_id,
            metadata=metadata
        )
        return payout

    
    async def create_payout_connect(self, amount: Decimal, account_id: str, user_id: UUID) -> stripe.Payout:
        # try:
        #     balance = await asyncio.to_thread(self._retrieve_balance)
        # except NoUSDWallet:
        #     raise PaymentSystemException
        
        intent = PaymentIntent(
            user_id=user_id,
            amount=amount,
            currency="USD",
            status=PaymentStatus.PENDING,
            provider=PaymentProvider.STRIPE,
            _metadata=None,
        )
        await self.intent_repo.add(intent)
        await self.uow.session.flush()
        
        transaction = Transaction(
            user_id=user_id,
            intent_id=intent.id,
            type=TransactionType.WITHDRAW_PENDING,
            amount=amount,
            currency='USD'
        )
        await self.t_repo.add(transaction)
        
        await self.w_repo.freeze(user_id, 'USD', amount)
        
        await self.uow.session.commit()
        
        metadata = {
            "intent_id": str(intent.id),
            "user_id": str(user_id),
        }
        
        payout = await asyncio.to_thread(
            self._create_payout_connect, amount, account_id, metadata
        )
        
        return payout
