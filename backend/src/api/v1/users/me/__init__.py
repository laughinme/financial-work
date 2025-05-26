from fastapi import APIRouter


def get_me_router() -> APIRouter:
    from .profile import router as profile_router
    from .auth_methods import get_auth_methods_router
    
    router = APIRouter(prefix='/users')

    router.include_router(profile_router)
    router.include_router(get_auth_methods_router)
    
    return router
