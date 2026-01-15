"""Test authentication system"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

try:
    from app.auth import verify_password, get_password_hash, create_access_token, decode_access_token
    print("✓ Auth utilities imported successfully")
    
    # Test password hashing
    password = "testpassword123"
    hashed = get_password_hash(password)
    print(f"✓ Password hashed: {hashed[:20]}...")
    
    # Test password verification
    assert verify_password(password, hashed) == True
    print("✓ Password verification works (correct password)")
    
    assert verify_password("wrongpassword", hashed) == False
    print("✓ Password verification works (wrong password)")
    
    # Test JWT token creation
    token = create_access_token(data={"sub": "testuser"})
    print(f"✓ JWT token created: {token[:20]}...")
    
    # Test JWT token decoding
    username = decode_access_token(token)
    assert username == "testuser"
    print(f"✓ JWT token decoded correctly: {username}")
    
    # Test invalid token
    invalid_username = decode_access_token("invalid.token.here")
    assert invalid_username is None
    print("✓ Invalid token returns None")
    
    print("\n✅ All auth system tests passed!")
    
except AssertionError as e:
    print(f"✗ Assertion failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
