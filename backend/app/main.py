"""
Keem-AI Backend - FastAPI Application
Main entry point for the conversational AI chatbot API
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("🚀 Keem-AI Backend starting...")
    yield
    # Shutdown
    logger.info("🛑 Keem-AI Backend shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="Keem-AI API",
    description="Advanced Conversational AI Chatbot API",
    version="0.1.0",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZIPMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Keem-AI API"}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Keem-AI API",
        "version": "0.1.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


# TODO: Add routers
# from app.routes import auth, chat, users
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
# app.include_router(users.router, prefix="/api/users", tags=["Users"])


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
