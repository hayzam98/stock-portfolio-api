from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.transaction import PortfolioSummary, PortfolioTotal
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/summary", response_model=List[PortfolioSummary])
async def get_portfolio_summary(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get complete portfolio summary with all stocks

    Returns detailed information for each stock including:
    - Current holdings (shares)
    - Average buy price
    - Current value
    - Total invested
    - Profit/loss (amount and percentage)
    """
    summaries = PortfolioService.calculate_portfolio_summary(current_user.id, db)
    return summaries


@router.get("/summary/{stock_symbol}", response_model=PortfolioSummary)
async def get_stock_summary(
    stock_symbol: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get summary for a specific stock

    Returns detailed portfolio information for the specified stock symbol
    """
    summary = PortfolioService.calculate_stock_summary(
        current_user.id, stock_symbol, db
    )

    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No holdings found for stock {stock_symbol.upper()}",
        )

    return summary


@router.get("/total", response_model=PortfolioTotal)
async def get_total_portfolio_value(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get total portfolio value and statistics

    Returns aggregated statistics across all stocks:
    - Total current value
    - Total amount invested
    - Total profit/loss (amount and percentage)
    - Number of different stocks owned
    """
    totals = PortfolioService.get_total_portfolio_value(current_user.id, db)
    return totals
