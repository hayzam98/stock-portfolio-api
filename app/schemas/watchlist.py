from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WatchlistItemCreate(BaseModel):
    """Schema for creating a watchlist item"""
    stock_symbol: str
    stock_name: Optional[str] = None


class WatchlistItemUpdate(BaseModel):
    """Schema for updating a watchlist item"""
    stock_name: Optional[str] = None


class WatchlistItemResponse(BaseModel):
    """Schema for watchlist item response"""
    id: int
    stock_symbol: str
    stock_name: Optional[str]
    added_at: datetime

    class Config:
        from_attributes = True


class WatchlistResponse(BaseModel):
    """Schema for watchlist response with current price"""
    id: int
    stock_symbol: str
    stock_name: Optional[str]
    current_price: Optional[float] = None
    added_at: datetime

    class Config:
        from_attributes = True
