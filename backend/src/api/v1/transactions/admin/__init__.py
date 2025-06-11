from fastapi import APIRouter


def get_admin_router() -> APIRouter:
    from .users import router as users_router

    router = APIRouter(prefix='/admin')
    router.include_router(users_router)
    return router
