from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Watchlist(Base):
    """Watchlist model for tracking stocks"""

    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    stock_symbol = Column(String(10), nullable=False)
    stock_name = Column(String(255))
    added_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="watchlist")

    def __repr__(self):
        return f"<Watchlist(id={self.id}, user_id={self.user_id}, symbol='{self.stock_symbol}')>"
    