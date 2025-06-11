from fastapi import APIRouter


def get_users_router() -> APIRouter:
    from .transactions import router as transactions_router

    router = APIRouter(prefix='/users')
    router.include_router(transactions_router)
    return router
