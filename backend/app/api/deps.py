"""
API dependencies for FastAPI endpoints.

Provides reusable dependencies for authentication, database sessions, etc.
"""
from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from app.core.auth import get_current_user


# Re-export dependencies for easy import
__all__ = ["get_session", "get_current_user"]


# Example of additional dependencies that can be added:
# - Rate limiting
# - Pagination
# - Query filters
# - Permission checks
