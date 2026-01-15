from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database.connection import engine, Base, SessionLocal
from app.routers import auth, transactions, portfolio
from app.config import settings

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A RESTful API for tracking stock purchases and sales with user authentication",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration and login operations"
        },
        {
            "name": "Transactions",
            "description": "Stock transaction management (buy/sell)"
        },
        {
            "name": "Portfolio",
            "description": "Portfolio analysis and statistics"
        }
    ]
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(portfolio.router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    
    Returns basic information about the API and links to documentation
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "authentication": "/auth",
            "transactions": "/transactions",
            "portfolio": "/portfolio"
        },
        "status": "operational"
    }

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    
    Tests database connectivity and returns service status
    """
    try:
        # Test database connection
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
        health_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"
        health_status = "unhealthy"
    
    return {
        "status": health_status,
        "version": settings.app_version,
        "database": db_status
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Actions to perform on application startup"""
    print(f"\n{'='*60}")
    print(f"🚀 {settings.app_name} v{settings.app_version}")
    print(f"{'='*60}")
    print(f"📚 Documentation: http://localhost:8000/docs")
    print(f"🏥 Health Check: http://localhost:8000/health")
    print(f"{'='*60}\n")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Actions to perform on application shutdown"""
    print(f"\n{'='*60}")
    print(f"👋 {settings.app_name} shutting down...")
    print(f"{'='*60}\n")
