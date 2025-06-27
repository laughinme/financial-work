from fastapi import APIRouter


def get_admin_router() -> APIRouter:
    from .intent import router as intent_router

    router = APIRouter(prefix='/admin')

    router.include_router(intent_router)
    
    return router
