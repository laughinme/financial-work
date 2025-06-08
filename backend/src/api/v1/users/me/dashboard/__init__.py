from fastapi import APIRouter


def get_me_router() -> APIRouter:
    from .summary import router as summary_router
    
    router = APIRouter(prefix='/dashboard')

    router.include_router(summary_router)
    
    return router
