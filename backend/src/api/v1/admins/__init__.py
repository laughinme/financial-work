from fastapi import APIRouter


def get_admins_router() -> APIRouter:
    from .settlements import router as settlements_router
    from .p_id import get_p_id_router
    from .users import get_users_router
    
    router = APIRouter(prefix='/admins', tags=['Admins'])

    router.include_router(settlements_router)
    router.include_router(get_p_id_router())
    router.include_router(get_users_router())
    
    return router
