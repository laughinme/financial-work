from fastapi import APIRouter


def get_v1_router() -> APIRouter:
    from .users import get_users_router
    from .dashboard import get_dashboard_router
    from .auth import get_auth_routers
    from .payments import get_payments_router
    from .portfolios import get_portfolios_router

    router = APIRouter(prefix='/v1')

    router.include_router(get_users_router())
    router.include_router(get_dashboard_router())
    router.include_router(get_auth_routers())
    router.include_router(get_payments_router())
    router.include_router(get_portfolios_router())
    
    return router
