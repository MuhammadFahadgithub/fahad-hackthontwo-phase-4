"""
Pydantic schemas for todo endpoints.

Defines request and response models for todo API.
Constitution Principle VI: API Contract Compliance
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Request Schemas
class TodoCreate(BaseModel):
    """Request schema for creating a todo."""
    title: str = Field(..., min_length=1, max_length=255, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    completed: bool = Field(default=False, description="Completion status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False
            }
        }
    }


class TodoUpdate(BaseModel):
    """Request schema for updating a todo."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    completed: Optional[bool] = Field(None, description="Completion status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries (updated)",
                "completed": True
            }
        }
    }


# Response Schemas
class TodoResponse(BaseModel):
    """Response schema for todo data."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "user_id": 1,
                "created_at": "2026-02-06T10:30:00Z",
                "updated_at": "2026-02-06T10:30:00Z"
            }
        }
    }
