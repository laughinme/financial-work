from fastapi import APIRouter


def get_payment_webhooks() -> APIRouter:
    router = APIRouter(prefix="/payment")

    from .payment_succeded import router as payment_succeded_router

    router.include_router(payment_succeded_router)

    return router