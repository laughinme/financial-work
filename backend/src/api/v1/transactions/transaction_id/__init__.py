from fastapi import APIRouter


def get_tx_id_router() -> APIRouter:
    from .detail import router as detail_router

    router = APIRouter(prefix='/{transaction_id}')
    
    router.include_router(detail_router)
    
    return router
