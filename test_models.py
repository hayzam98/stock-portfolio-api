"""Test database models"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

try:
    # Test imports
    from app.models import User, Transaction, TransactionType
    print("✓ All models imported successfully")
    
    # Test User model attributes
    user_columns = [c.name for c in User.__table__.columns]
    expected_user_cols = ['id', 'email', 'username', 'hashed_password', 'created_at', 'updated_at']
    assert all(col in user_columns for col in expected_user_cols)
    print("✓ User model has all required columns")
    
    # Test Transaction model attributes
    trans_columns = [c.name for c in Transaction.__table__.columns]
    expected_trans_cols = ['id', 'user_id', 'stock_symbol', 'transaction_type', 'quantity', 'price_per_share']
    assert all(col in trans_columns for col in expected_trans_cols)
    print("✓ Transaction model has all required columns")
    
    # Test TransactionType enum
    assert hasattr(TransactionType, 'BUY')
    assert hasattr(TransactionType, 'SELL')
    print("✓ TransactionType enum defined correctly")
    
    # Test relationships
    assert hasattr(User, 'transactions')
    assert hasattr(Transaction, 'user')
    print("✓ Model relationships defined")
    
    print("\n✅ All model tests passed!")
    
except AssertionError as e:
    print(f"✗ Assertion failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
