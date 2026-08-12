from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.config.settings import settings
from app.execution.process_manager import process_manager
from app.services.postgres import postgres_service
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for application startup and shutdown events."""
    logger.info(f"Starting {settings.APP_NAME} in environment '{settings.APP_ENV}'...")
    postgres_service.initialize()
    yield
    logger.info("Shutting down application and stopping processes...")
    await process_manager.stop_all()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Multi-Agent System for Autonomous Software Development",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint welcoming users and providing documentation links."""
    return {
        "message": "Welcome to Multi-Agent System API",
        "status": "online",
        "health_check": "/health",
        "api_docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
