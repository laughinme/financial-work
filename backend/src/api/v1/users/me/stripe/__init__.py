from fastapi import APIRouter


def get_stripe_router() -> APIRouter:
    from .accounts import router as accounts_router
    
    router = APIRouter(prefix='/stripe')

    router.include_router(accounts_router)
    
    return router
