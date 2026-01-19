from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from app.services.stock_price_service import StockPriceService
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/price/{symbol}")
async def get_stock_price(
    symbol: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get current price for a stock symbol
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)
    
    Returns the current market price
    """
    print(f"Price request for {symbol} by user {current_user.username}")
    
    price = StockPriceService.get_current_price(symbol.upper())
    
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock symbol '{symbol}' not found or price unavailable"
        )
    
    return {
        "symbol": symbol.upper(),
        "current_price": price,
        "currency": "USD"
    }

@router.get("/info/{symbol}")
async def get_stock_info(
    symbol: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information for a stock symbol
    
    - **symbol**: Stock ticker symbol
    
    Returns comprehensive stock information including price, market cap, sector, etc.
    """
    print(f"Info request for {symbol} by user {current_user.username}")
    
    info = StockPriceService.get_stock_info(symbol.upper())
    
    if info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock symbol '{symbol}' not found"
        )
    
    return info

@router.get("/history/{symbol}")
async def get_stock_history(
    symbol: str,
    period: str = "1mo",
    current_user: User = Depends(get_current_user)
):
    """
    Get historical prices for a stock symbol
    
    - **symbol**: Stock ticker symbol
    - **period**: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns historical price data
    """
    print(f"History request for {symbol} (period: {period}) by user {current_user.username}")
    
    # Validate period
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    if period not in valid_periods:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}"
        )
    
    history = StockPriceService.get_historical_prices(symbol.upper(), period)
    
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Historical data for '{symbol}' not found"
        )
    
    return {
        "symbol": symbol.upper(),
        "period": period,
        "data": history
    }

@router.post("/validate/{symbol}")
async def validate_stock_symbol(
    symbol: str,
    current_user: User = Depends(get_current_user)
):
    """
    Validate if a stock symbol exists
    
    - **symbol**: Stock ticker symbol to validate
    
    Returns validation result
    """
    print(f"Validation request for {symbol} by user {current_user.username}")
    
    is_valid = StockPriceService.validate_symbol(symbol.upper())
    
    return {
        "symbol": symbol.upper(),
        "is_valid": is_valid,
        "message": "Stock symbol is valid" if is_valid else "Stock symbol not found"
    }
