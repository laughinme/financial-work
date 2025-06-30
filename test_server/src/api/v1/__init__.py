from fastapi import APIRouter


def get_v1_router() -> APIRouter:
    from .myfxbook import router as myfx_router
    # from .auth import router as auth_router
    # from .myfxbook import router as myfx_router

    router = APIRouter(prefix='/v1')

    # router.include_router(auth_router)
    router.include_router(myfx_router)
    
    return router
