"""Test portfolio service logic"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

try:
    from app.services.portfolio_service import PortfolioService
    print("✓ PortfolioService imported successfully")
    
    # Verify methods exist
    assert hasattr(PortfolioService, 'calculate_portfolio_summary')
    assert hasattr(PortfolioService, 'calculate_stock_summary')
    assert hasattr(PortfolioService, 'get_total_portfolio_value')
    print("✓ All service methods defined")
    
    # Test that methods are static
    import inspect
    assert isinstance(inspect.getattr_static(PortfolioService, 'calculate_portfolio_summary'), staticmethod)
    print("✓ Methods are static methods")
    
    print("\n✅ Portfolio service structure tests passed!")
    print("Note: Full functionality tests require database and transactions")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
