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

# ==================== WATCHLIST ENDPOINTS ====================

from app.database.connection import SessionLocal
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistItemCreate, WatchlistItemResponse, WatchlistResponse


@router.post("/watchlist", response_model=WatchlistItemResponse, tags=["Stocks"])
async def add_to_watchlist(
    item: WatchlistItemCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Add a stock to the user's watchlist
    
    - **stock_symbol**: Stock ticker symbol (e.g., AAPL, GOOGL)
    - **stock_name**: Optional company name
    
    Returns the created watchlist item
    """
    db = SessionLocal()
    
    try:
        # Validate symbol exists
        info = StockPriceService.get_stock_info(item.stock_symbol.upper())
        if not info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stock symbol '{item.stock_symbol}' not found"
            )
        
        # Check if already in watchlist
        existing = db.query(Watchlist).filter(
            Watchlist.user_id == current_user.id,
            Watchlist.stock_symbol == item.stock_symbol.upper()
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{item.stock_symbol}' is already in your watchlist"
            )
        
        # Create new watchlist item
        watchlist_item = Watchlist(
            user_id=current_user.id,
            stock_symbol=item.stock_symbol.upper(),
            stock_name=item.stock_name or info.get("name")
        )
        
        db.add(watchlist_item)
        db.commit()
        db.refresh(watchlist_item)
        
        return watchlist_item
    
    finally:
        db.close()


@router.get("/watchlist", response_model=List[WatchlistResponse], tags=["Stocks"])
async def get_watchlist(
    current_user: User = Depends(get_current_user)
):
    """
    Get the user's watchlist with current prices
    
    Returns all stocks in the user's watchlist with current market prices
    """
    db = SessionLocal()
    
    try:
        items = db.query(Watchlist).filter(
            Watchlist.user_id == current_user.id
        ).all()
        
        # Fetch current prices for each stock
        result = []
        for item in items:
            price = StockPriceService.get_current_price(item.stock_symbol)
            result.append({
                "id": item.id,
                "stock_symbol": item.stock_symbol,
                "stock_name": item.stock_name,
                "current_price": price,
                "added_at": item.added_at
            })
        
        return result
    
    finally:
        db.close()


@router.delete("/watchlist/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Stocks"])
async def remove_from_watchlist(
    watchlist_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Remove a stock from the user's watchlist
    
    - **watchlist_id**: ID of the watchlist item to remove
    
    Returns 204 No Content on success
    """
    db = SessionLocal()
    
    try:
        # Find and delete watchlist item
        item = db.query(Watchlist).filter(
            Watchlist.id == watchlist_id,
            Watchlist.user_id == current_user.id
        ).first()
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist item not found"
            )
        
        db.delete(item)
        db.commit()
        
    finally:
        db.close()


@router.delete("/watchlist/symbol/{symbol}", status_code=status.HTTP_204_NO_CONTENT, tags=["Stocks"])
async def remove_from_watchlist_by_symbol(
    symbol: str,
    current_user: User = Depends(get_current_user)
):
    """
    Remove a stock from the user's watchlist by symbol
    
    - **symbol**: Stock ticker symbol to remove
    
    Returns 204 No Content on success
    """
    db = SessionLocal()
    
    try:
        # Find and delete watchlist item
        item = db.query(Watchlist).filter(
            Watchlist.user_id == current_user.id,
            Watchlist.stock_symbol == symbol.upper()
        ).first()
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stock '{symbol}' not found in watchlist"
            )
        
        db.delete(item)
        db.commit()
        
    finally:
        db.close()
