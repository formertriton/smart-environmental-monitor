"""
Main Application Entry Point
Smart Environmental Monitoring System

This demonstrates a production-ready application structure with:
- Proper startup/shutdown lifecycle management
- Dependency injection
- Error handling
- Logging configuration
- Health checks
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger

from config.settings import get_settings, Settings
from src.api.routes import router as api_router
from src.data_ingestion.sensor_simulator import SensorSimulator
from src.processing.data_processor import DataProcessor


class Application:
    """Main application class - demonstrates clean architecture"""
    
    def __init__(self):
        self.settings = get_settings()
        self.sensor_simulator: SensorSimulator = None
        self.data_processor: DataProcessor = None
        self.background_tasks = []
        
    async def startup(self):
        """Application startup tasks"""
        logger.info("🚀 Starting Environmental Monitor System")
        
        try:
            # Initialize components
            self.sensor_simulator = SensorSimulator(self.settings.sensors)
            self.data_processor = DataProcessor(self.settings)
            
            # Start background services
            await self._start_background_services()
            
            logger.info("✅ System startup complete")
            
        except Exception as e:
            logger.error(f"❌ Startup failed: {e}")
            raise
    
    async def shutdown(self):
        """Application shutdown tasks"""
        logger.info("🛑 Shutting down Environmental Monitor System")
        
        try:
            # Stop background tasks
            for task in self.background_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
            # Stop sensors
            if self.sensor_simulator:
                await self.sensor_simulator.stop()
            
            # Stop data processor
            if self.data_processor:
                await self.data_processor.stop()
                
            logger.info("✅ Shutdown complete")
            
        except Exception as e:
            logger.error(f"❌ Shutdown error: {e}")
    
    async def _start_background_services(self):
        """Start background services"""
        
        # Start sensor simulation
        sensor_task = asyncio.create_task(
            self.sensor_simulator.start(),
            name="sensor_simulator"
        )
        self.background_tasks.append(sensor_task)
        
        # Start data processing
        processor_task = asyncio.create_task(
            self.data_processor.start(),
            name="data_processor"
        )
        self.background_tasks.append(processor_task)
        
        logger.info("🔄 Background services started")


# Global application instance
app_instance = Application()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager"""
    # Startup
    await app_instance.startup()
    yield
    # Shutdown
    await app_instance.shutdown()


def create_app() -> FastAPI:
    """Create FastAPI application instance"""
    
    settings = get_settings()
    
    # Configure logging
    configure_logging(settings)
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.api.title,
        version=settings.api.version,
        debug=settings.debug,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """System health check"""
        return {
            "status": "healthy",
            "environment": settings.environment,
            "version": settings.api.version,
            "services": {
                "sensors": app_instance.sensor_simulator.is_running if app_instance.sensor_simulator else False,
                "processor": app_instance.data_processor.is_running if app_instance.data_processor else False,
            }
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """API information"""
        return {
            "name": settings.api.title,
            "version": settings.api.version,
            "environment": settings.environment,
            "docs": "/docs",
            "health": "/health"
        }
    
    return app


def configure_logging(settings: Settings):
    """Configure application logging"""
    
    # Remove default logger
    logger.remove()
    
    # Console logging
    if settings.log_format == "json":
        logger.add(
            sys.stdout,
            level=settings.log_level,
            serialize=True,
            backtrace=True,
            diagnose=True
        )
    else:
        logger.add(
            sys.stdout,
            level=settings.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            backtrace=True,
            diagnose=True
        )
    
    # File logging
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        level=settings.log_level,
        backtrace=True,
        diagnose=True
    )


# Create app instance
app = create_app()


if __name__ == "__main__":
    """Run the application"""
    
    settings = get_settings()
    
    logger.info(f"🌍 Starting {settings.api.title}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug: {settings.debug}")
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Run with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )