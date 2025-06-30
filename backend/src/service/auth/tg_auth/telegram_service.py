import hmac
import hashlib
import logging
import secrets
from datetime import datetime, UTC

from fastapi import Request
from sqlalchemy.exc import IntegrityError

from database.relational_db import (
    UserInterface,
    User,
    IdentityInterface,
    Identity,
    UoW,
    Wallet
)
from domain.users import TelegramAuthSchema, Provider
from core.config import Config
from .exceptions import InvalidTelegramSignature, AlreadyLinked
from ..session import SessionService


config = Config()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(
        self,
        identity_repo: IdentityInterface,
        user_repo: UserInterface,
        session_service: SessionService,
        uow: UoW,
    ):
        self.identity_repo = identity_repo
        self.user_repo = user_repo
        self.session_service = session_service
        self.uow = uow
        

    @staticmethod
    def _verify(payload: TelegramAuthSchema) -> None:
        data = payload.model_dump(exclude_none=True)
        check_hash = data.pop("hash")
        
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
        secret_key = hashlib.sha256(config.BOT_TOKEN.encode()).digest()
        hmac_hash = hmac.new(
            secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if not secrets.compare_digest(hmac_hash, check_hash):
            logger.error('Invalid Hash')
            raise InvalidTelegramSignature()
        
        # Reject payloads that are older than 24 hours to prevent replay attacks
        now_ts = int(datetime.now(UTC).timestamp())
        if now_ts - data["auth_date"] > 60 * 60 * 24:
            logger.error('Login expired')
            raise InvalidTelegramSignature()
        
        
    @staticmethod
    def _fill_profile_from_tg(user: User, payload: TelegramAuthSchema) -> None:
        if not user.display_name:
            user.display_name = payload.first_name or payload.username or f"tg_{payload.id}"
        if not user.first_name:
            user.first_name = payload.first_name
        if not user.last_name:
            user.last_name = payload.last_name
        if not user.avatar_url and payload.photo_url:
            user.avatar_url = payload.photo_url
    
    
    async def login(
        self,
        request: Request,
        payload: TelegramAuthSchema,
        ttl: int
    ) -> User:
        self._verify(payload)
        
        identifier = str(payload.id)
        
        async with self.uow:
            user = await self.identity_repo.get_user_by_provider(Provider.TELEGRAM, identifier)
            if user is None:
                user = self.user_repo.create()
                identity = Identity(
                    provider=Provider.TELEGRAM,
                    external_id=identifier,
                    meta={
                        "first_name": payload.first_name,
                        "last_name": payload.last_name,
                        "username": payload.username,
                        "photo_url": payload.photo_url,
                    },
                    # last_login_at=datetime.now(UTC)
                )
                user.identities.append(identity)
                    
                wallet = Wallet(currency='USD')
                user.wallets.append(wallet)
                
            await self.user_repo.add(user)
            self._fill_profile_from_tg(user, payload)
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
    
    
    async def link(
        self,
        payload: TelegramAuthSchema,
        user: User,
        replace_fields: bool = False
    ) -> None:
        self._verify(payload)
        
        identifier = str(payload.id)
        
        identity = Identity(
            user_id=user.id,
            provider=Provider.TELEGRAM,
            external_id=identifier,
            meta={
                "first_name": payload.first_name,
                "last_name": payload.last_name,
                "username": payload.username,
                "photo_url": payload.photo_url,
            },
            # last_login_at=datetime.now(UTC)
        )
        await self.identity_repo.add(identity)
        
        if replace_fields:
            self._fill_profile_from_tg(user, payload)
        
        try:
            await self.uow.session.flush()
        except IntegrityError:
            raise AlreadyLinked()
            
        return user
