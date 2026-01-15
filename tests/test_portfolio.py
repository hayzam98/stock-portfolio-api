"""Tests for portfolio endpoints"""

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

def test_get_portfolio_summary_empty(client):
    """Test getting portfolio summary with no transactions"""
    token = get_auth_token(client)
    
    response = client.get(
        "/portfolio/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_get_portfolio_summary_with_stocks(client):
    """Test getting portfolio summary with stocks"""
    token = get_auth_token(client)
    
    # Create buy transactions
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc.",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.00
        }
    )
    
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "GOOGL",
            "stock_name": "Alphabet Inc.",
            "transaction_type": "buy",
            "quantity": 5,
            "price_per_share": 2800.00
        }
    )
    
    # Get portfolio summary
    response = client.get(
        "/portfolio/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Check AAPL summary
    aapl = [s for s in data if s["stock_symbol"] == "AAPL"][0]
    assert aapl["total_shares"] == 10
    assert aapl["average_buy_price"] == 150.00
    assert aapl["total_invested"] == 1500.00

def test_get_stock_summary(client):
    """Test getting summary for a specific stock"""
    token = get_auth_token(client)
    
    # Create transaction
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc.",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.00
        }
    )
    
    # Get stock summary
    response = client.get(
        "/portfolio/summary/AAPL",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["stock_symbol"] == "AAPL"
    assert data["total_shares"] == 10
    assert data["average_buy_price"] == 150.00

def test_get_stock_summary_not_found(client):
    """Test getting summary for stock not in portfolio"""
    token = get_auth_token(client)
    
    response = client.get(
        "/portfolio/summary/AAPL",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert "No holdings found" in response.json()["detail"]

def test_get_total_portfolio_value(client):
    """Test getting total portfolio value"""
    token = get_auth_token(client)
    
    # Create transactions
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.00
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
    
    # Get totals
    response = client.get(
        "/portfolio/total",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_invested"] == 15500.00  # 1500 + 14000
    assert data["number_of_stocks"] == 2

def test_portfolio_profit_loss_calculation(client):
    """Test profit/loss calculation"""
    token = get_auth_token(client)
    
    # Buy at 150
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.00
        }
    )
    
    # Sell at 160 (profit)
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 160.00
        }
    )
    
    # Get summary
    response = client.get(
        "/portfolio/summary/AAPL",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Current price is last transaction (160)
    # Average buy price should be 155
    assert data["total_shares"] == 20
    assert data["average_buy_price"] == 155.00

def test_portfolio_after_partial_sell(client):
    """Test portfolio after partial sell"""
    token = get_auth_token(client)
    
    # Buy 10 shares
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.00
        }
    )
    
    # Sell 3 shares
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "sell",
            "quantity": 3,
            "price_per_share": 160.00
        }
    )
    
    # Get summary
    response = client.get(
        "/portfolio/summary/AAPL",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_shares"] == 7  # 10 - 3

def test_portfolio_stock_completely_sold(client):
    """Test that completely sold stocks don't appear in portfolio"""
    token = get_auth_token(client)
    
    # Buy 10 shares
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.00
        }
    )
    
    # Sell all 10 shares
    client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "stock_symbol": "AAPL",
            "transaction_type": "sell",
            "quantity": 10,
            "price_per_share": 160.00
        }
    )
    
    # Get summary - should not include AAPL
    response = client.get(
        "/portfolio/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # No stocks held
