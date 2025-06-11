from fastapi import APIRouter


def get_transactions_router() -> APIRouter:
    from .transactions import router as tx_router
    from .transaction_id import get_tx_id_router

    router = APIRouter(prefix='/transactions', tags=['Transactions'])
    
    router.include_router(tx_router)
    router.include_router(get_tx_id_router())
    
    return router
