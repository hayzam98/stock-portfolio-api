import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class TransactionType(enum.Enum):
    """Enum for transaction types"""

    BUY = "buy"
    SELL = "sell"


class Transaction(Base):
    """Transaction model for stock buy/sell operations"""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    stock_symbol = Column(String(10), nullable=False, index=True)
    stock_name = Column(String(255))
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    transaction_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    notes = Column(String(500))

    # Relationships
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, symbol='{self.stock_symbol}', type={self.transaction_type.value})>"
