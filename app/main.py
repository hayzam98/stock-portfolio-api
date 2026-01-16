from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import text
from contextlib import asynccontextmanager
from app.database.connection import engine, Base, SessionLocal
from app.routers import auth, transactions, portfolio
from app.config import settings
from pathlib import Path

# Lifespan context manager (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    Replaces the deprecated @app.on_event decorators
    """
    # Startup
    print(f"\n{'='*60}")
    print(f"🚀 {settings.app_name} v{settings.app_version}")
    print(f"{'='*60}")
    print(f"🌐 Web Interface: http://localhost:8000/")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🏥 Health Check: http://localhost:8000/health")
    print(f"{'='*60}\n")
    
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)
    
    yield  # Application runs here
    
    # Shutdown
    print(f"\n{'='*60}")
    print(f"👋 {settings.app_name} shutting down...")
    print(f"{'='*60}\n")

# Initialize FastAPI application with lifespan
app = FastAPI(
    title=settings.app_name,
    description="A RESTful API for tracking stock purchases and sales with user authentication",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,  # Use lifespan instead of on_event
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

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(portfolio.router)

@app.get("/", include_in_schema=False)
async def serve_spa():
    """
    Serve the web interface (SPA)
    
    Returns the main HTML file for the web application
    """
    return FileResponse("app/templates/index.html")

@app.get("/api", tags=["Root"])
async def root():
    """
    Root API endpoint with information
    
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
        "web_interface": "/",
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
