import hmac
import hashlib

from fastapi import Request

from database.relational_db import (
    UserInterface,
    User,
    TelegramInterface,
    TelegramProvider,
    AuthProvidersInterface,
    AuthProvider,
    UoW
)
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
        session_service: SessionService,
        uow: UoW
    ):
        self.tg_repo = tg_repo
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        self.session_service = session_service
        self.uow = uow
        

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
        
        identifier = str(payload.id)
        
        async with self.uow:
            user = await self.tg_repo.get_user_by_tg(identifier)
            if user is None:
                user = self.user_repo.create()
                auth = AuthProvider(
                    provider=Provider.TELEGRAM,
                    provider_user_id=identifier,
                    telegram=TelegramProvider(
                        first_name=payload.first_name,
                        last_name=payload.last_name,
                        username=payload.username,
                        photo_url=payload.photo_url,
                    )
                )
                user.providers.append(auth)
            await self.user_repo.add(user)
        
        session_id = await self.session_service.create_session(user.id, ttl)
        request.session['session_id'] = session_id
        
        return user
