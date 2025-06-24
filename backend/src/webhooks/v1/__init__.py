from fastapi import APIRouter


def get_v1_webhooks() -> APIRouter:
    from .stripe import router as stripe_router
    
    router = APIRouter(prefix="/v1")

    router.include_router(stripe_router)

    return router
