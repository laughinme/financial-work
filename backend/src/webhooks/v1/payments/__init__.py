from fastapi import APIRouter


def get_payment_webhooks() -> APIRouter:
    router = APIRouter(prefix="/payments")

    from .payment_status import router as payment_status_router

    router.include_router(payment_status_router)

    return router