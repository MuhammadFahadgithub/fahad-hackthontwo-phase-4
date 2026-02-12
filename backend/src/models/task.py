from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    description: str = Field(min_length=1, max_length=500)
    user_id: str = Field(index=True)


class Task(TaskBase, table=True):
    """
    Represents a user's todo item
    """
    id: Optional[str] = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = Field(default=None)


class TaskRead(TaskBase):
    id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]


class TaskUpdate(SQLModel):
    description: Optional[str] = Field(default=None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass