"""
Chat API endpoint for the Todo Chatbot application
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
import re

from ..database import get_db
from ..models.message import Message
from ..models.conversation import Conversation
from ..models.user import User
from .. import schemas
from ..auth import get_current_user
from ..services.chat_service import ChatService

router = APIRouter()


@router.post("/message", response_model=schemas.ChatResponse)
async def send_chat_message(
    chat_message: schemas.ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the chatbot and receive a response
    """
    # Determine conversation ID
    conversation_id = chat_message.context.get("conversation_id") if chat_message.context else None
    
    if not conversation_id:
        # Create a new conversation
        conversation_id = str(uuid4())
        new_conversation = Conversation(
            id=conversation_id,
            user_id=current_user.id,
            title=chat_message.message[:50]  # Use first 50 chars as title
        )
        db.add(new_conversation)
        db.commit()
    else:
        # Verify conversation belongs to user
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    
    # Save the user's message
    user_message = Message(
        id=str(uuid4()),
        conversation_id=conversation_id,
        sender="user",
        content=chat_message.message,
        created_at=datetime.utcnow()
    )
    db.add(user_message)
    db.commit()
    
    # Process the message with the chat service
    chat_service = ChatService(db)
    response_text, actions = chat_service.process_message(
        chat_message.message,
        current_user.id,
        conversation_id
    )
    
    # Save the bot's response
    bot_message = Message(
        id=str(uuid4()),
        conversation_id=conversation_id,
        sender="bot",
        content=response_text,
        created_at=datetime.utcnow()
    )
    db.add(bot_message)
    db.commit()
    
    return schemas.ChatResponse(
        response=response_text,
        conversation_id=conversation_id,
        actions=actions
    )