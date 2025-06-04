from fastapi import APIRouter


def get_specific_portfolio_router() -> APIRouter:
    from .charts import router as charts_router
    from .info import router as info_router
    
    router = APIRouter(prefix='/{portfolio_id}')

    router.include_router(info_router)
    router.include_router(charts_router)
    
    return router
