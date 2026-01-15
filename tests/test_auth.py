"""Tests for authentication endpoints"""

def test_register_user(client):
    """Test user registration with valid data"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "hashed_password" not in data  # Password should not be returned

def test_register_duplicate_email(client):
    """Test registration with duplicate email fails"""
    # First registration
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    # Try to register with same email
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_register_duplicate_username(client):
    """Test registration with duplicate username fails"""
    # First registration
    client.post(
        "/auth/register",
        json={
            "email": "test1@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    # Try to register with same username
    response = client.post(
        "/auth/register",
        json={
            "email": "test2@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]

def test_login_user(client):
    """Test user login with valid credentials"""
    # First register
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    """Test login with invalid credentials fails"""
    # Register user
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_get_current_user(client):
    """Test getting current user information"""
    # Register and login
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token fails"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
