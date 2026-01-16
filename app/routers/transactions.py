from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new stock transaction (buy or sell)

    - **stock_symbol**: Stock ticker symbol (e.g., AAPL, GOOGL)
    - **stock_name**: Company name (optional)
    - **transaction_type**: "buy" or "sell"
    - **quantity**: Number of shares
    - **price_per_share**: Price per share at transaction time
    - **notes**: Additional notes (optional)

    For sell transactions, validates that user owns enough shares
    """
    # Calculate total amount
    total_amount = transaction_data.quantity * transaction_data.price_per_share

    # If selling, verify user has enough shares
    if transaction_data.transaction_type == TransactionType.SELL:
        # Get all buy transactions for this stock
        buys = (
            db.query(Transaction)
            .filter(
                Transaction.user_id == current_user.id,
                Transaction.stock_symbol == transaction_data.stock_symbol.upper(),
                Transaction.transaction_type == TransactionType.BUY,
            )
            .all()
        )

        # Get all sell transactions for this stock
        sells = (
            db.query(Transaction)
            .filter(
                Transaction.user_id == current_user.id,
                Transaction.stock_symbol == transaction_data.stock_symbol.upper(),
                Transaction.transaction_type == TransactionType.SELL,
            )
            .all()
        )

        # Calculate current holdings
        total_bought = sum(t.quantity for t in buys)
        total_sold = sum(t.quantity for t in sells)
        current_holdings = total_bought - total_sold

        # Check if user has enough shares to sell
        if transaction_data.quantity > current_holdings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot sell {transaction_data.quantity} shares. You only own {current_holdings} shares of {transaction_data.stock_symbol}.",
            )

    # Create new transaction
    new_transaction = Transaction(
        user_id=current_user.id,
        stock_symbol=transaction_data.stock_symbol.upper(),
        stock_name=transaction_data.stock_name,
        transaction_type=transaction_data.transaction_type,
        quantity=transaction_data.quantity,
        price_per_share=transaction_data.price_per_share,
        total_amount=total_amount,
        notes=transaction_data.notes,
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.get("/", response_model=List[TransactionResponse])
async def get_all_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all transactions for the current user

    - **skip**: Number of transactions to skip (for pagination)
    - **limit**: Maximum number of transactions to return (default: 100)

    Returns transactions ordered by date (newest first)
    """
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(Transaction.transaction_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific transaction by ID

    Only returns transactions owned by the current user
    """
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id, Transaction.user_id == current_user.id
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    return transaction


@router.get("/stock/{stock_symbol}", response_model=List[TransactionResponse])
async def get_transactions_by_stock(
    stock_symbol: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all transactions for a specific stock

    Returns transactions for the given stock symbol, ordered by date (newest first)
    """
    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.stock_symbol == stock_symbol.upper(),
        )
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

    return transactions


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a transaction

    Only allows deletion of transactions owned by the current user
    """
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id, Transaction.user_id == current_user.id
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return None
