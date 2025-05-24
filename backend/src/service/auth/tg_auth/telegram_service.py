import hmac
import hashlib

from fastapi import Request

from database.relational_db import UserInterface, User, TelegramInterface, AuthProvidersInterface
from domain.users import TelegramAuthSchema, Provider
from core.config import Config
from .exceptions import InvalidTelegramSignature
from ..session import SessionService


config = Config()


class TelegramService():
    def __init__(
        self,
        tg_repo: TelegramInterface,
        auth_repo: AuthProvidersInterface,
        user_repo: UserInterface,
        session_service: SessionService
    ):
        self.tg_repo = tg_repo
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.session_service = session_service
        

    @staticmethod
    def verify(payload: TelegramAuthSchema):
        data = payload.model_dump()
        check_hash = data.pop("hash")
        
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
        secret_key = hashlib.sha256(config.BOT_TOKEN.encode()).digest()
        hmac_hash = hmac.new(
            secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if hmac_hash != check_hash:
            raise InvalidTelegramSignature()
        
        # TODO: check if authorization is expired
    
    
    async def login(
        self,
        request: Request,
        payload: TelegramAuthSchema,
        ttl: int
    ) -> User:
        self.verify(payload)
        
        provider = await self.auth_repo.find_for_provider(Provider.TELEGRAM, payload.id)
        if provider is None:
            user = await self.user_repo.create()
            provider = await self.auth_repo.create(Provider.TELEGRAM, str(payload.id), user)
            await self.tg_repo.create(payload, provider.id)
        else:
            await self.tg_repo.get_by_id(provider.id)
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
