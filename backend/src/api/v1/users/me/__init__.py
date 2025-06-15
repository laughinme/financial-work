from fastapi import APIRouter


def get_me_router() -> APIRouter:
    from .profile import router as profile_router
    from .stripe import get_stripe_router
    
    router = APIRouter(prefix='/me')

    router.include_router(profile_router)
    router.include_router(get_stripe_router())
    
    return router
