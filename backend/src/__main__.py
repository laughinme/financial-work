import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from api import get_api_routers
from webhooks import get_webhooks
from service import SessionService
from core.config import Config
from core.middlewares import RefreshTTLMiddleware
from database.redis import get_redis, SessionRepo
from scheduler import init_scheduler


config = Config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure session service for RefreshTTLMiddleware
    redis: Redis = get_redis()
    app.state.session_service = SessionService(SessionRepo(redis))
    
    # Start APScheduler
    scheduler = init_scheduler()
    app.state.scheduler = scheduler
    
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)
        await redis.aclose()


app = FastAPI(
    lifespan=lifespan,
    title='Finance',
    debug=True
)

# Including routers
app.include_router(get_api_routers())
app.include_router(get_webhooks())

@app.get('/ping')
async def ping():
    return {'status': 'ok'}


# Adding middlewares
app.add_middleware(
    SessionMiddleware,
    secret_key=config.SESSION_SECRET_KEY,
    max_age=config.SESSION_LIFETIME,
    session_cookie="session_id",
    same_site='none',
    https_only=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://76ca-79-127-249-67.ngrok-free.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
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
