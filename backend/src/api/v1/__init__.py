from fastapi import APIRouter


def get_v1_router() -> APIRouter:
    from .users import get_users_router
    from .auth import get_auth_routers

    router = APIRouter(prefix='/v1')

    router.include_router(get_users_router())
    router.include_router(get_auth_routers())
    
    return router
