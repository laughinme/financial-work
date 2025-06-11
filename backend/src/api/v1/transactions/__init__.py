from fastapi import APIRouter


def get_transactions_router() -> APIRouter:
    from .user import router as user_router
    from .admin import get_admin_router

    router = APIRouter(prefix='/transactions', tags=['Transactions'])
    router.include_router(user_router)
    router.include_router(get_admin_router())
    return router
