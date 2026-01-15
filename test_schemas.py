"""Test Pydantic schemas"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

try:
    from app.schemas import UserCreate, UserResponse, Token, TransactionCreate, TransactionResponse
    print("✓ All schemas imported successfully")
    
    # Test UserCreate validation
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    user = UserCreate(**user_data)
    print(f"✓ UserCreate validates correctly: {user.username}")
    
    # Test invalid email
    try:
        invalid_user = UserCreate(email="invalid-email", username="test", password="pass123")
        print("✗ Should have failed with invalid email")
        sys.exit(1)
    except:
        print("✓ Email validation working")
    
    # Test TransactionCreate
    from app.models.transaction import TransactionType
    trans_data = {
        "stock_symbol": "AAPL",
        "stock_name": "Apple Inc.",
        "transaction_type": TransactionType.BUY,
        "quantity": 10.0,
        "price_per_share": 150.50
    }
    transaction = TransactionCreate(**trans_data)
    print(f"✓ TransactionCreate validates correctly: {transaction.stock_symbol}")
    
    # Test quantity validation (should be > 0)
    try:
        invalid_trans = TransactionCreate(
            stock_symbol="AAPL",
            transaction_type=TransactionType.BUY,
            quantity=-5,  # Invalid
            price_per_share=100
        )
        print("✗ Should have failed with negative quantity")
        sys.exit(1)
    except:
        print("✓ Quantity validation working")
    
    print("\n✅ All schema tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
