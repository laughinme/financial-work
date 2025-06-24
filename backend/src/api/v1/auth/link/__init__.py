from fastapi import APIRouter


def get_link_router() -> APIRouter:
    from .telegram import router as telegram_router
    from .credentials import router as credentials_router
    
    router = APIRouter(prefix='/link')

    router.include_router(telegram_router)
    router.include_router(credentials_router)
    
    return router
