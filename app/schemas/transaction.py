from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    """Base transaction schema"""
    stock_symbol: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    stock_name: Optional[str] = Field(None, max_length=255, description="Company name")
    transaction_type: TransactionType
    quantity: float = Field(..., gt=0, description="Number of shares")
    price_per_share: float = Field(..., gt=0, description="Price per share")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")

class TransactionCreate(TransactionBase):
    """Schema for creating a transaction"""
    pass

class TransactionResponse(TransactionBase):
    """Schema for transaction response"""
    id: int
    user_id: int
    total_amount: float
    transaction_date: datetime
    
    class Config:
        from_attributes = True

class PortfolioSummary(BaseModel):
    """Schema for portfolio summary by stock"""
    stock_symbol: str
    stock_name: Optional[str]
    total_shares: float
    average_buy_price: float
    current_value: float
    total_invested: float
    profit_loss: float
    profit_loss_percentage: float

class PortfolioTotal(BaseModel):
    """Schema for total portfolio statistics"""
    total_current_value: float
    total_invested: float
    total_profit_loss: float
    total_profit_loss_percentage: float
    number_of_stocks: int
