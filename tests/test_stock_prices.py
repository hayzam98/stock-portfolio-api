"""Tests for stock price service and endpoints"""
import pytest
from app.services.stock_price_service import StockPriceService

def test_get_current_price_valid_symbol():
    """Test getting current price for a valid stock symbol"""
    price = StockPriceService.get_current_price("AAPL")
    
    assert price is not None
    assert isinstance(price, float)
    assert price > 0

def test_get_current_price_invalid_symbol():
    """Test getting price for invalid symbol returns None"""
    price = StockPriceService.get_current_price("INVALIDXYZ123")
    
    assert price is None

def test_get_stock_info_valid_symbol():
    """Test getting stock info for valid symbol"""
    info = StockPriceService.get_stock_info("MSFT")
    
    assert info is not None
    assert 'symbol' in info
    assert 'name' in info
    assert 'current_price' in info
    assert info['current_price'] > 0

def test_validate_symbol_valid():
    """Test symbol validation for valid symbol"""
    is_valid = StockPriceService.validate_symbol("GOOGL")
    
    assert is_valid is True

def test_validate_symbol_invalid():
    """Test symbol validation for invalid symbol"""
    is_valid = StockPriceService.validate_symbol("INVALIDXYZ123")
    
    assert is_valid is False

def test_cache_mechanism():
    """Test that price caching works"""
    # Clear cache first
    StockPriceService.clear_cache()
    
    # First call - should fetch from API
    price1 = StockPriceService.get_current_price("AAPL")
    
    # Second call - should use cache
    price2 = StockPriceService.get_current_price("AAPL")
    
    # Prices should be the same (from cache)
    assert price1 == price2
    
    # Clear cache
    StockPriceService.clear_cache()

def get_auth_token(client):
    """Helper function to get authentication token"""
    client.post(
        "/auth/register",
        json={
            "email": "stocktest@example.com",
            "username": "stocktestuser",
            "password": "testpassword123"
        }
    )
    
    response = client.post(
        "/auth/login",
        data={
            "username": "stocktestuser",
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]

def test_get_stock_price_endpoint(client):
    """Test the stock price endpoint"""
    token = get_auth_token(client)
    
    response = client.get(
        "/stocks/price/AAPL",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert 'symbol' in data
    assert 'current_price' in data
    assert data['symbol'] == 'AAPL'

def test_stock_endpoint_requires_auth(client):
    """Test that stock endpoints require authentication"""
    response = client.get("/stocks/price/AAPL")
    assert response.status_code == 401
