from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
from starlette.requests import Request
from starlette.responses import Response

from service import SessionService

class RefreshTTLMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, ttl: int = 60 * 60):
        super().__init__(app)
        self.ttl = ttl

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)

        session_id = request.cookies.get("session_id")
        if session_id:
            session_service: SessionService = request.app.state.session_service
            await session_service.update_session(session_id, self.ttl)
        return response
