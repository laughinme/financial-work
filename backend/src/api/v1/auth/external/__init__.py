from fastapi import APIRouter


def get_auth_external_routers() -> APIRouter:
    from .telegram import router as telegram_router
    
    router = APIRouter(prefix='/external')
    
    router.include_router(telegram_router)
    
    return router
