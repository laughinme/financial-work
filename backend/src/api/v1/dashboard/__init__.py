from fastapi import APIRouter


def get_dashboard_router() -> APIRouter:
    from .summary import router as summary_router
    from .charts import router as charts_router
    
    router = APIRouter(prefix='/dashboard', tags=['Dashboard'])

    router.include_router(summary_router)
    router.include_router(charts_router)
    
    return router
