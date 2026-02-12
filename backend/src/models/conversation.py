"""
Conversation model for the Todo Chatbot application
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from ..database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)  # Foreign key to users table
    title = Column(String, nullable=True)  # Auto-generated from first message
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id})>"