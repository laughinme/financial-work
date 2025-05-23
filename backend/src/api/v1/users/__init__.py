from fastapi import APIRouter


def get_users_router() -> APIRouter:
    from .login import router as login_router
    from .registration import router as register_router
    from .profile import router as profile_router
    
    router = APIRouter(prefix='/users')

    router.include_router(login_router)
    router.include_router(register_router)
    router.include_router(profile_router)
    
    return router
