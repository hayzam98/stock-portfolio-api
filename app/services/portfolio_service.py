from typing import Dict, List

from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import PortfolioSummary


class PortfolioService:
    """Service for portfolio calculations and analysis"""

    @staticmethod
    def calculate_portfolio_summary(
        user_id: int, db: Session
    ) -> List[PortfolioSummary]:
        """
        Calculate portfolio summary for all stocks owned by a user

        Args:
            user_id: The user's ID
            db: Database session

        Returns:
            List of PortfolioSummary objects for each stock
        """
        # Get all transactions for the user
        transactions = (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.stock_symbol, Transaction.transaction_date)
            .all()
        )

        # Group transactions by stock symbol
        stocks_data: Dict[str, dict] = {}

        for trans in transactions:
            symbol = trans.stock_symbol

            # Initialize stock data if first time seeing this symbol
            if symbol not in stocks_data:
                stocks_data[symbol] = {
                    "stock_name": trans.stock_name,
                    "total_shares": 0,
                    "total_invested": 0,
                    "total_sold_value": 0,
                    "buy_transactions": [],
                }

            # Process buy transactions
            if trans.transaction_type == TransactionType.BUY:
                stocks_data[symbol]["total_shares"] += trans.quantity
                stocks_data[symbol]["total_invested"] += trans.total_amount
                stocks_data[symbol]["buy_transactions"].append(
                    {
                        "quantity": trans.quantity,
                        "price": trans.price_per_share,
                        "total": trans.total_amount,
                    }
                )
            # Process sell transactions
            else:  # SELL
                stocks_data[symbol]["total_shares"] -= trans.quantity
                stocks_data[symbol]["total_sold_value"] += trans.total_amount

        # Calculate summary for each stock
        summaries = []
        for symbol, data in stocks_data.items():
            # Only include stocks still held (positive shares)
            if data["total_shares"] > 0:
                # Calculate average buy price
                avg_buy_price = (
                    data["total_invested"]
                    / sum(t["quantity"] for t in data["buy_transactions"])
                    if data["buy_transactions"]
                    else 0
                )

                # Use last transaction price as "current" price
                # In a real app, you'd fetch this from a stock price API
                last_trans = [t for t in transactions if t.stock_symbol == symbol][-1]
                current_price = last_trans.price_per_share

                # Calculate values
                current_value = data["total_shares"] * current_price
                cost_basis = data["total_shares"] * avg_buy_price
                profit_loss = current_value - cost_basis
                profit_loss_pct = (
                    (profit_loss / cost_basis * 100) if cost_basis > 0 else 0
                )

                summaries.append(
                    PortfolioSummary(
                        stock_symbol=symbol,
                        stock_name=data["stock_name"],
                        total_shares=round(data["total_shares"], 4),
                        average_buy_price=round(avg_buy_price, 2),
                        current_value=round(current_value, 2),
                        total_invested=round(cost_basis, 2),
                        profit_loss=round(profit_loss, 2),
                        profit_loss_percentage=round(profit_loss_pct, 2),
                    )
                )

        return summaries

    @staticmethod
    def calculate_stock_summary(
        user_id: int, stock_symbol: str, db: Session
    ) -> PortfolioSummary:
        """
        Calculate summary for a specific stock

        Args:
            user_id: The user's ID
            stock_symbol: Stock ticker symbol
            db: Database session

        Returns:
            PortfolioSummary for the specified stock, or None if not found
        """
        all_summaries = PortfolioService.calculate_portfolio_summary(user_id, db)

        for summary in all_summaries:
            if summary.stock_symbol.upper() == stock_symbol.upper():
                return summary

        return None

    @staticmethod
    def get_total_portfolio_value(user_id: int, db: Session) -> Dict[str, float]:
        """
        Get total portfolio statistics across all stocks

        Args:
            user_id: The user's ID
            db: Database session

        Returns:
            Dictionary with total portfolio statistics
        """
        summaries = PortfolioService.calculate_portfolio_summary(user_id, db)

        # Calculate totals
        total_current_value = sum(s.current_value for s in summaries)
        total_invested = sum(s.total_invested for s in summaries)
        total_profit_loss = total_current_value - total_invested
        total_profit_loss_pct = (
            (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        )

        return {
            "total_current_value": round(total_current_value, 2),
            "total_invested": round(total_invested, 2),
            "total_profit_loss": round(total_profit_loss, 2),
            "total_profit_loss_percentage": round(total_profit_loss_pct, 2),
            "number_of_stocks": len(summaries),
        }
