from fastapi import APIRouter


def get_webhooks() -> APIRouter:
    router = APIRouter(prefix="/webhooks", tags=['Webhooks'])

    from .v1 import get_v1_webhooks

    router.include_router(get_v1_webhooks())

    return router