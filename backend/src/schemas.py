"""
Pydantic schemas for the Todo Chatbot application
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    due_date: Optional[datetime] = None
    priority: Optional[str] = "medium"  # low, medium, high


class TodoCreate(TodoBase):
    title: str  # Required field for creation


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None


class Todo(TodoBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    email: str
    password: str


class User(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    message: str
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    actions: Optional[list] = []