from fastapi import APIRouter


def get_portfolios_router() -> APIRouter:
    from .all import router as all_router
    from .specific import get_specific_portfolio_router
    
    router = APIRouter(prefix='/portfolios', tags=['Portfolios'])

    router.include_router(all_router)
    router.include_router(get_specific_portfolio_router())
    
    return router
