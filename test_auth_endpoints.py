"""Test auth endpoints (requires server running)"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_auth_endpoints():
    try:
        # Test 1: Register
        print("Testing registration...")
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": "autotest@example.com",
                "username": "autotest",
                "password": "testpass123"
            }
        )
        if response.status_code == 201:
            print("✓ Registration successful")
        elif response.status_code == 400 and "already" in response.text:
            print("✓ User already exists (expected if running multiple times)")
        else:
            print(f"✗ Registration failed: {response.status_code}")
            return False
        
        # Test 2: Login
        print("\nTesting login...")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": "autotest",
                "password": "testpass123"
            }
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✓ Login successful, token: {token[:20]}...")
        else:
            print(f"✗ Login failed: {response.status_code}")
            return False
        
        # Test 3: Get current user
        print("\nTesting get current user...")
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            user = response.json()
            print(f"✓ Got user info: {user['username']}")
        else:
            print(f"✗ Get user failed: {response.status_code}")
            return False
        
        print("\n✅ All auth endpoint tests passed!")
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
    success = test_auth_endpoints()
    sys.exit(0 if success else 1)
