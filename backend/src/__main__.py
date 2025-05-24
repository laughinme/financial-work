import uvicorn
import yookassa
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from api import get_api_routers
from service import SessionService
from core.config import Config
from core.middlewares import RefreshTTLMiddleware
from database.redis import get_redis_manually, SessionRepo


config = Config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis: Redis = await get_redis_manually()
    app.state.session_service = SessionService(SessionRepo(redis))
    try:
        yield
    finally:
        await redis.close()


app = FastAPI(
    lifespan=lifespan,
    title='Finance'
)

# Including routers
app.include_router(get_api_routers())

# Adding middlewares
app.add_middleware(
    SessionMiddleware,
    secret_key=config.SESSION_SECRET_KEY,
    max_age=config.SESSION_LIFETIME,
    session_cookie="session_id"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

app.add_middleware(
    RefreshTTLMiddleware,
    ttl=config.SESSION_LIFETIME
)


if __name__ == "__main__":
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
