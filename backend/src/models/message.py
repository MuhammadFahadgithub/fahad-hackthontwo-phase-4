"""
Message model for the Todo Chatbot application
"""
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, nullable=False)  # Foreign key to conversations table
    sender = Column(String, nullable=False)  # 'user' or 'bot'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Message(id={self.id}, sender={self.sender}, conversation_id={self.conversation_id})>"