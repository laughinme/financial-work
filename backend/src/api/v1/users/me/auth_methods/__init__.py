from fastapi import APIRouter


def get_auth_methods_router() -> APIRouter:
    from .telegram import router as telegram_router
    # from .credentials import router as credentials_router
    
    router = APIRouter(prefix='/auth_methods')

    router.include_router(telegram_router)
    
    return router
