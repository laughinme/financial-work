from fastapi import APIRouter


def get_user_id_router() -> APIRouter:
    from .transactions import router as transactions_router

    router = APIRouter(prefix='/{user_id}')
    
    router.include_router(transactions_router)
    
    return router
