from fastapi import APIRouter


def get_auth_routers() -> APIRouter:
    from .external import get_auth_external_routers
    from .login import router as login_router
    from .registration import router as register_router
    
    router = APIRouter(prefix='/auth', tags=['Auth'])
    
    router.include_router(get_auth_external_routers())
    router.include_router(login_router)
    router.include_router(register_router)
    
    return router
