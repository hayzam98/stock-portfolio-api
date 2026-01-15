"""Test database configuration"""
import sys
from pathlib import Path
from sqlalchemy import text

sys.path.append(str(Path(__file__).parent))

try:
    from app.config import settings
    print("✓ Config loaded successfully")
    print(f"  App Name: {settings.app_name}")
    print(f"  Version: {settings.app_version}")

    from app.database.connection import engine, get_db
    print("✓ Database connection module loaded")
    
    # Test database connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as test"))
        print(f"✓ Database connection successful (Result: {result.scalar()})")
        
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("\n✅ All database config tests passed!")
