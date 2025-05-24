from fastapi import APIRouter


def get_users_router() -> APIRouter:
    from .profile import router as profile_router
    
    router = APIRouter(prefix='/users')

    router.include_router(profile_router)
    
    return router
