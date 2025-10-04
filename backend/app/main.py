from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import engine, get_db
from app.models import user, exercise, progress, reminder
from app.api import auth, exercises, progress as progress_api, reminders
from app.services.scheduler import automation_scheduler
from app.services.ai_agent import ArthritisAIAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
user.Base.metadata.create_all(bind=engine)
exercise.Base.metadata.create_all(bind=engine)
progress.Base.metadata.create_all(bind=engine)
reminder.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Agent Arthritis API...")
    
    # Start the automation scheduler
    automation_scheduler.start()
    logger.info("Automation scheduler started")
    
    # Initialize AI agent
    ai_agent = ArthritisAIAgent()
    logger.info("AI agent initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agent Arthritis API...")
    automation_scheduler.stop()
    logger.info("Automation scheduler stopped")


# Create FastAPI app
app = FastAPI(
    title="Agent Arthritis API",
    description="AI-powered arthritis management system with personalized exercises and automated reminders",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
app.include_router(progress_api.router, prefix="/progress", tags=["Progress"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Agent Arthritis API",
        "version": "1.0.0",
        "description": "AI-powered arthritis management system",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        
        # Check scheduler status
        scheduler_status = automation_scheduler.get_scheduler_status()
        
        return {
            "status": "healthy",
            "database": "connected",
            "scheduler": scheduler_status,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2024-01-01T00:00:00Z"
            }
        )


@app.get("/api/info")
def api_info():
    """API information endpoint"""
    return {
        "name": "Agent Arthritis API",
        "version": "1.0.0",
        "environment": settings.environment,
        "features": [
            "User authentication and profiles",
            "AI-powered exercise generation",
            "Progress tracking and analytics",
            "Automated email reminders",
            "Personalized insights and recommendations"
        ],
        "endpoints": {
            "auth": "/auth",
            "exercises": "/exercises",
            "progress": "/progress",
            "reminders": "/reminders"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )