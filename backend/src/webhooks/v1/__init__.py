from fastapi import APIRouter


def get_v1_webhooks() -> APIRouter:
    router = APIRouter(prefix="/v1")

    from .payments import get_payment_webhooks

    router.include_router(get_payment_webhooks())

    return router