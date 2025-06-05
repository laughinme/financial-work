import hmac
import hashlib

from fastapi import Request
from sqlalchemy.exc import IntegrityError

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
from .exceptions import InvalidTelegramSignature, AlreadyLinked
from ..session import SessionService


config = Config()


class TelegramService:
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
    def _verify(payload: TelegramAuthSchema) -> None:
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
        
        auth = AuthProvider(
            user_id=user.id,
            provider=Provider.TELEGRAM,
            provider_user_id=identifier,
            telegram=TelegramProvider(
                first_name=payload.first_name,
                last_name=payload.last_name,
                username=payload.username,
                photo_url=payload.photo_url,
            )
        )
        await self.auth_repo.add(auth)
        
        if replace_fields:
            self._fill_profile_from_tg(user, payload)
        
        try:
            await self.uow.session.flush()
        except IntegrityError:
            raise AlreadyLinked()
            
        return user
