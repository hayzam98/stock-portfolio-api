"""Test transaction endpoints (requires server running)"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def get_token():
    """Helper to get auth token"""
    # Try to register (may fail if exists)
    requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": "transtest@example.com",
            "username": "transtest",
            "password": "testpass123"
        }
    )
    
    # Login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": "transtest",
            "password": "testpass123"
        }
    )
    return response.json()["access_token"]

def test_transaction_endpoints():
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 1: Create buy transaction
        print("Testing create buy transaction...")
        response = requests.post(
            f"{BASE_URL}/transactions/",
            headers=headers,
            json={
                "stock_symbol": "AAPL",
                "stock_name": "Apple Inc.",
                "transaction_type": "buy",
                "quantity": 10,
                "price_per_share": 150.50,
                "notes": "Test purchase"
            }
        )
        if response.status_code == 201:
            trans = response.json()
            trans_id = trans["id"]
            print(f"✓ Buy transaction created: ID={trans_id}, Total=${trans['total_amount']}")
        else:
            print(f"✗ Create transaction failed: {response.status_code} - {response.text}")
            return False
        
        # Test 2: Get all transactions
        print("\nTesting get all transactions...")
        response = requests.get(f"{BASE_URL}/transactions/", headers=headers)
        if response.status_code == 200:
            transactions = response.json()
            print(f"✓ Got {len(transactions)} transaction(s)")
        else:
            print(f"✗ Get transactions failed: {response.status_code}")
            return False
        
        # Test 3: Get transactions by stock
        print("\nTesting get transactions by stock...")
        response = requests.get(f"{BASE_URL}/transactions/stock/AAPL", headers=headers)
        if response.status_code == 200:
            aapl_trans = response.json()
            print(f"✓ Got {len(aapl_trans)} AAPL transaction(s)")
        else:
            print(f"✗ Get stock transactions failed: {response.status_code}")
            return False
        
        # Test 4: Try to sell without enough shares (should fail)
        print("\nTesting sell validation (should fail)...")
        response = requests.post(
            f"{BASE_URL}/transactions/",
            headers=headers,
            json={
                "stock_symbol": "GOOGL",
                "transaction_type": "sell",
                "quantity": 100,
                "price_per_share": 2800.00
            }
        )
        if response.status_code == 400:
            print("✓ Sell validation working (correctly rejected)")
        else:
            print(f"✗ Should have rejected sell: {response.status_code}")
            return False
        
        # Test 5: Valid sell transaction
        print("\nTesting valid sell transaction...")
        response = requests.post(
            f"{BASE_URL}/transactions/",
            headers=headers,
            json={
                "stock_symbol": "AAPL",
                "transaction_type": "sell",
                "quantity": 3,
                "price_per_share": 160.00
            }
        )
        if response.status_code == 201:
            sell_trans = response.json()
            print(f"✓ Sell transaction created: {sell_trans['quantity']} shares @ ${sell_trans['price_per_share']}")
        else:
            print(f"✗ Sell transaction failed: {response.status_code} - {response.text}")
            return False
        
        print("\n✅ All transaction endpoint tests passed!")
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
    success = test_transaction_endpoints()
    sys.exit(0 if success else 1)
