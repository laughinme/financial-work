from fastapi import APIRouter


def get_users_router() -> APIRouter:
    from .user_id import get_user_id_router

    router = APIRouter(prefix='/users')
    
    router.include_router(get_user_id_router())
    
    return router
