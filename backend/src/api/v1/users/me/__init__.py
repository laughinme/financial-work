from fastapi import APIRouter


def get_me_router() -> APIRouter:
    from .profile import router as profile_router
    
    router = APIRouter(prefix='/me')

    router.include_router(profile_router)
    
    return router
