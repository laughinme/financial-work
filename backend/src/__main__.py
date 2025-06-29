import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from api import get_api_routers
from webhooks import get_webhooks
from core.config import Config
from scheduler import init_scheduler


config = Config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start APScheduler
    scheduler = init_scheduler()
    app.state.scheduler = scheduler
    
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)

app = FastAPI(
    lifespan=lifespan,
    title='Finance',
    debug=False
)

# Including routers
app.include_router(get_api_routers())
app.include_router(get_webhooks())

@app.get('/ping')
async def ping():
    return {'status': 'ok'}


# Adding middlewares
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

if __name__ == "__main__":
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
