"""
Todo database model.

Defines the Todo entity with user ownership.
Constitution Principle III: User Identity & Isolation
Constitution Principle IV: Query-Level Authorization
"""
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional


class Todo(SQLModel, table=True):
    """
    Todo model for task management.

    Each todo belongs to a specific user (user_id foreign key).
    Constitution Principle IV: All queries MUST filter by user_id.
    """
    __tablename__ = "todos"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
