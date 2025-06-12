from fastapi import APIRouter


def get_p_id_router() -> APIRouter:
    from .intent import router as intent_router
    
    router = APIRouter(prefix='/{portfolio_id}')

    router.include_router(intent_router)
    
    return router
