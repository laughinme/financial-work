from fastapi import APIRouter


def get_specific_portfolio_router() -> APIRouter:
    from .charts import router as charts_router
    from .info import router as info_router
    from .invest import router as invest_router
    from .user_holdings import router as holdings_router
    
    router = APIRouter(prefix='/{portfolio_id}')

    router.include_router(info_router)
    router.include_router(charts_router)
    router.include_router(invest_router)
    router.include_router(holdings_router)
    
    return router
