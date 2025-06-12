from uuid import uuid4, UUID
from datetime import datetime, UTC
from dataclasses import dataclass
from database.redis import SessionRepo
from fastapi import Request


class SessionService:
    def __init__(self, repo: SessionRepo):
        self.repo = repo

    async def create_session(self, user_id: UUID, ttl: int, **data) -> str:
        session_id = str(uuid4())
        payload = {
            'sub': str(user_id),
            'iat': datetime.now(UTC).isoformat(),
            **data
        }
        await self.repo.set(session_id, payload, ttl)
        
        return session_id
    
    async def get_session(self, session_id: str) -> dict | None:
        data = await self.repo.get(session_id)
        return data

    async def revoke_session(self, session_id: str) -> None:
        await self.repo.delete(session_id)
        
    async def update_session(self, session_id: str, ttl: int) -> None:
        await self.repo.update(session_id, ttl)
