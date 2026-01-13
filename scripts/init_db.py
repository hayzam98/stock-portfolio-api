"""
Script to initialize the database and create all tables
Run this after creating the database and before starting the application
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database.connection import engine, Base
from app.models import User, Transaction

def init_database():
    """Create all tables in the database"""
    print("=" * 50)
    print("Initializing Stock Portfolio Database")
    print("=" * 50)
    
    try:
        print("\nCreating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        
        print("\nTables created:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
        
        print("\n" + "=" * 50)
        print("Database initialization complete!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
