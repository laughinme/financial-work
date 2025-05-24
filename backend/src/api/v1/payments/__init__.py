from fastapi import APIRouter


def get_payments_router() -> APIRouter:
    from .create import router as create_router
    
    router = APIRouter(prefix='/payments')

    router.include_router(create_router)
    
    return router
