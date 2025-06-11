from fastapi import APIRouter


def get_admins_router() -> APIRouter:
    from .settlements import router as settlements_router
    
    router = APIRouter(prefix='/admins', tags=['Admins'])

    router.include_router(settlements_router)
    
    return router
