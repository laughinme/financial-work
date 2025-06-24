from fastapi import APIRouter


def get_payments_router() -> APIRouter:
    from .deposit import router as create_router
    from .withdraw import router as payout_router
    from .balance import router as balance_router
    
    router = APIRouter(prefix='/payments', tags=['Payments'])

    router.include_router(create_router)
    router.include_router(payout_router)
    router.include_router(balance_router)
    
    return router
