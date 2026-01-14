"""Test portfolio endpoints (requires server running with transactions)"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def get_token():
    """Helper to get auth token"""
    requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": "portfolio@example.com",
            "username": "portfoliotest",
            "password": "testpass123"
        }
    )
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": "portfoliotest",
            "password": "testpass123"
        }
    )
    return response.json()["access_token"]

def create_sample_transactions(token):
    """Create sample transactions for testing"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Buy AAPL
    requests.post(
        f"{BASE_URL}/transactions/",
        headers=headers,
        json={
            "stock_symbol": "AAPL",
            "stock_name": "Apple Inc.",
            "transaction_type": "buy",
            "quantity": 10,
            "price_per_share": 150.00
        }
    )
    
    # Buy GOOGL
    requests.post(
        f"{BASE_URL}/transactions/",
        headers=headers,
        json={
            "stock_symbol": "GOOGL",
            "stock_name": "Alphabet Inc.",
            "transaction_type": "buy",
            "quantity": 5,
            "price_per_share": 2800.00
        }
    )

def test_portfolio_endpoints():
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create sample data
        print("Creating sample transactions...")
        create_sample_transactions(token)
        print("✓ Sample transactions created\n")
        
        # Test 1: Get portfolio summary
        print("Testing portfolio summary...")
        response = requests.get(f"{BASE_URL}/portfolio/summary", headers=headers)
        if response.status_code == 200:
            summary = response.json()
            print(f"✓ Portfolio summary retrieved: {len(summary)} stock(s)")
            for stock in summary:
                print(f"  - {stock['stock_symbol']}: {stock['total_shares']} shares, "
                      f"P/L: ${stock['profit_loss']} ({stock['profit_loss_percentage']}%)")
        else:
            print(f"✗ Portfolio summary failed: {response.status_code}")
            return False
        
        # Test 2: Get stock summary
        print("\nTesting stock summary...")
        response = requests.get(f"{BASE_URL}/portfolio/summary/AAPL", headers=headers)
        if response.status_code == 200:
            stock = response.json()
            print(f"✓ AAPL summary: {stock['total_shares']} shares, "
                  f"Avg price: ${stock['average_buy_price']}")
        else:
            print(f"✗ Stock summary failed: {response.status_code}")
            return False
        
        # Test 3: Get total portfolio value
        print("\nTesting total portfolio value...")
        response = requests.get(f"{BASE_URL}/portfolio/total", headers=headers)
        if response.status_code == 200:
            total = response.json()
            print(f"✓ Total portfolio:")
            print(f"  Current value: ${total['total_current_value']}")
            print(f"  Invested: ${total['total_invested']}")
            print(f"  P/L: ${total['total_profit_loss']} ({total['total_profit_loss_percentage']}%)")
            print(f"  Stocks: {total['number_of_stocks']}")
        else:
            print(f"✗ Total portfolio failed: {response.status_code}")
            return False
        
        # Test 4: Get summary for non-existent stock (should fail)
        print("\nTesting non-existent stock (should fail)...")
        response = requests.get(f"{BASE_URL}/portfolio/summary/INVALID", headers=headers)
        if response.status_code == 404:
            print("✓ Correctly returned 404 for non-existent stock")
        else:
            print(f"✗ Should have returned 404: {response.status_code}")
            return False
        
        print("\n✅ All portfolio endpoint tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Server not running. Start with: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_portfolio_endpoints()
    sys.exit(0 if success else 1)
