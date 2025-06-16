from fastapi import APIRouter


def get_v1_router() -> APIRouter:
    from .myfxbook import router as myfxrouter

    router = APIRouter(prefix='/v1')

    router.include_router(myfxrouter)
    
    return router
