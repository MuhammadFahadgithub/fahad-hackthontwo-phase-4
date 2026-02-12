"""
API v1 router.

Aggregates all v1 API endpoints.
"""
from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# Import and include sub-routers
from app.api.v1 import auth, todos

# Health check endpoint
@api_router.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.

    Returns basic health status of the API.
    """
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "1.0.0"
    }

# Note: Auth router included for User Story 1 (Signup)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Note: Todos router included for Todo Management
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
