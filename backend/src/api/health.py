"""
Health check endpoints for the Todo Chatbot application
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Health check endpoint to verify the application is running
    """
    return {"status": "healthy", "service": "todo-chatbot-backend"}


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint to verify the application is ready to serve traffic
    """
    # Here you would typically check database connectivity, external services, etc.
    # For now, we'll just return that we're ready
    return {"status": "ready", "service": "todo-chatbot-backend"}


@router.get("/live")
async def liveness_check():
    """
    Liveness check endpoint to verify the application is alive
    """
    # Here you would typically check if the application is hung or having issues
    # For now, we'll just return that we're live
    return {"status": "alive", "service": "todo-chatbot-backend"}