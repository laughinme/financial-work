import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager, suppress
import asyncio
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from api import get_api_routers
from core.config import Config
from domain import simulate_realtime


config = Config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(simulate_realtime())
    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


app = FastAPI(
    lifespan=lifespan,
    title='Test Server',
    debug=True
)

# Including routers
app.include_router(get_api_routers())

@app.get('/ping')
async def ping():
    return {'status': 'ok'}


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


if __name__ == "__main__":
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
