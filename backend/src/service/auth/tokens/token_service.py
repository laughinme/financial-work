import jwt

from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone

from core.config import Config
from database.redis import CacheRepo
from database.relational_db import UserInterface

config = Config()
PRIVATE_KEY = config.JWT_PRIVATE_KEY.encode()
PUBLIC_KEY = config.JWT_PUBLIC_KEY.encode()

class TokenService:
    def __init__(self, repo: CacheRepo, u_repo: UserInterface):
        self.repo = repo
        self.u_repo = u_repo

    async def create_tokens(
        self,
        user_id: UUID,
        need_email: bool | None = False
    ) -> tuple[str, str]:
        now = datetime.now(timezone.utc)
        
        access_payload = {
            'sub': str(user_id),
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(seconds=config.ACCESS_TTL)).timestamp()),
            'need_email': need_email
        }
        access = jwt.encode(access_payload, PRIVATE_KEY, algorithm=config.JWT_ALGO)

        jti = str(uuid4())
        refresh_payload = {
            'sub': str(user_id),
            'jti': jti,
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(seconds=config.REFRESH_TTL)).timestamp())
        }
        refresh = jwt.encode(refresh_payload, PRIVATE_KEY, algorithm=config.JWT_ALGO)
        await self.repo.set(f'refresh:{jti}', str(user_id), config.REFRESH_TTL)
        
        return access, refresh

    async def refresh_tokens(self, refresh_token: str) -> tuple[str, str] | None:
        try:
            payload = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=[config.JWT_ALGO])
            jti = payload.get('jti')
            if not jti:
                return None
            
            stored = await self.repo.get(f'refresh:{jti}')
            if stored is None:
                return None
            
            await self.repo.delete(f'refresh:{jti}')
            user_id = UUID(payload['sub'])
            
            user = await self.u_repo.get_by_id(user_id)
            return await self.create_tokens(user_id, need_email=not bool(user.email))
        
        except jwt.PyJWTError:
            return None

    async def revoke(self, refresh_token: str) -> None:
        try:
            payload = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=[config.JWT_ALGO])
            jti = payload.get('jti')
            if jti:
                await self.repo.delete(f'refresh:{jti}')
        except jwt.PyJWTError:
            pass

    def decode_access(self, token: str) -> dict:
        return jwt.decode(token, PUBLIC_KEY, algorithms=[config.JWT_ALGO])
