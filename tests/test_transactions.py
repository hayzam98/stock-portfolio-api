"""Tests for transaction endpoints"""

def get_auth_token(client):
    """Helper function to register and login a user"""
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]

def test_create_buy_transaction(client):
    """Test creating a buy transaction"""
    token = get_auth_token(client)
    
    response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc.",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.50,
            "notes": "First purchase"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["stock_symbol"] == "AAPL"
    assert data["quantity"] == 10
    assert data["price_per_share"] == 150.50
    assert data["total_amount"] == 1505.0
    assert data["transaction_type"] == "buy"

def test_create_sell_transaction_without_holdings(client):
    """Test selling stock without owning it fails"""
    token = get_auth_token(client)
    
    response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc.",
            "transaction_type": "sell",
            "quantity": 10,
            "price_per_share": 150.50
        }
    )
    
    assert response.status_code == 400
    assert "You only own 0" in response.json()["detail"]

def test_create_sell_transaction_with_holdings(client):
    """Test selling stock after buying it"""
    token = get_auth_token(client)
    
    # First buy
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc.",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.50
        }
    )
    
    # Then sell
    response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc.",
            "transaction_type": "sell",
            "quantity": 5,
            "price_per_share": 160.00
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["transaction_type"] == "sell"
    assert data["quantity"] == 5

def test_get_all_transactions(client):
    """Test retrieving all transactions"""
    token = get_auth_token(client)
    
    # Create some transactions
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.50
        }
    )
    
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "GOOGL",
            "transaction_type": "buy",
            "quantity": 5,
            "price_per_share": 2800.00
        }
    )
    
    # Get all transactions
    response = client.get(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_transaction_by_id(client):
    """Test retrieving a specific transaction by ID"""
    token = get_auth_token(client)
    
    # Create transaction
    create_response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.50
        }
    )
    transaction_id = create_response.json()["id"]
    
    # Get transaction
    response = client.get(
        f"/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["stock_symbol"] == "AAPL"

def test_get_transactions_by_stock(client):
    """Test retrieving transactions for a specific stock"""
    token = get_auth_token(client)
    
    # Create transactions
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.50
        }
    )
    
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "GOOGL",
            "transaction_type": "buy",
            "quantity": 5,
            "price_per_share": 2800.00
        }
    )
    
    # Get AAPL transactions
    response = client.get(
        "/transactions/stock/AAPL",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["stock_symbol"] == "AAPL"

def test_delete_transaction(client):
    """Test deleting a transaction"""
    token = get_auth_token(client)
    
    # Create transaction
    create_response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.50
        }
    )
    transaction_id = create_response.json()["id"]
    
    # Delete transaction
    response = client.delete(
        f"/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(
        f"/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404

def test_get_transactions_requires_auth(client):
    """Test that getting transactions requires authentication"""
    response = client.get("/transactions/")
    assert response.status_code == 401

def test_stock_symbol_uppercase_conversion(client):
    """Test that stock symbols are converted to uppercase"""
    token = get_auth_token(client)
    
    response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "aapl",  # lowercase
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.50
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["stock_symbol"] == "AAPL"  # Should be uppercase
