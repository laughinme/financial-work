from fastapi import APIRouter


def get_payments_router() -> APIRouter:
    from .create import router as create_router
    from .payout import router as payout_router
    
    router = APIRouter(prefix='/payments')

    router.include_router(create_router)
    router.include_router(payout_router)
    
    return router
