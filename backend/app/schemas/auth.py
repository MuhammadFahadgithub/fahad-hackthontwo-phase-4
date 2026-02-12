"""
Pydantic schemas for authentication endpoints.

Defines request and response models for auth API.
Constitution Principle VI: API Contract Compliance
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# Request Schemas
class SignUpRequest(BaseModel):
    """Request schema for user signup."""
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=255, description="User full name")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "securepassword123"
            }
        }
    }


class LoginRequest(BaseModel):
    """Request schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    }


class PasswordResetRequest(BaseModel):
    """Request schema for password reset request."""
    email: EmailStr = Field(..., description="User email address")


class PasswordResetConfirm(BaseModel):
    """Request schema for password reset confirmation."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")


# Response Schemas
class UserResponse(BaseModel):
    """Response schema for user data."""
    id: int
    email: str
    name: str
    email_verified: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "name": "John Doe",
                "email_verified": False,
                "created_at": "2026-02-06T10:30:00Z"
            }
        }
    }


class TokenResponse(BaseModel):
    """Response schema for authentication with JWT token."""
    user: UserResponse
    token: str = Field(..., description="JWT access token")
    expires_at: datetime = Field(..., description="Token expiration timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "name": "John Doe",
                    "email_verified": False,
                    "created_at": "2026-02-06T10:30:00Z"
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_at": "2026-02-13T10:30:00Z"
            }
        }
    }


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Operation completed successfully"
            }
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response format."""
    detail: str
    errors: Optional[list] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Validation error",
                "errors": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "code": "value_error.email"
                    }
                ]
            }
        }
    }
