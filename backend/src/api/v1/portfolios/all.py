from fastapi import APIRouter, Depends, Query

from core.security import auth_user
from domain.investments import PortfolioPreview
from service.portfolios import PortfolioService, get_portfolio_service
from database.relational_db import User


router = APIRouter()


@router.get(
    path='/',
    response_model=list[PortfolioPreview]
)
async def get_all_portfolios(
    size: int = Query(5, ge=1),
    page: int = Query(1, ge=1),
    with_charts: bool = Query(False, description='Whether to add chart to response or not'),
    portfolio_service: PortfolioService = Depends(get_portfolio_service),
    user: User = Depends(auth_user)
):
    portfolios = await portfolio_service.list_all(user.id, size, page, with_charts)
    return portfolios
