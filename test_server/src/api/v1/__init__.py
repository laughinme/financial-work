from fastapi import APIRouter


def get_v1_router() -> APIRouter:
    # from .users import get_users_router

    router = APIRouter(prefix='/v1')

    # router.include_router(get_admins_router())
    
    return router
