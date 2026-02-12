from typing import List, Optional
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate, ConversationUpdate, ConversationRead
from ..models.message import Message
from datetime import datetime


class ConversationService:
    """
    Service class for handling conversation-related operations
    """
    
    def create_conversation(self, session: Session, conversation_create: ConversationCreate) -> ConversationRead:
        """
        Create a new conversation
        """
        conversation = Conversation.from_orm(conversation_create)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return ConversationRead.from_orm(conversation)
    
    def get_user_conversations(self, session: Session, user_id: str) -> List[ConversationRead]:
        """
        Retrieve all conversations for a specific user
        """
        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        conversations = session.exec(statement).all()
        return [ConversationRead.from_orm(conv) for conv in conversations]
    
    def get_conversation_by_id(self, session: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """
        Retrieve a specific conversation by ID for a user
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id, 
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()
    
    def update_conversation(self, session: Session, conversation_id: str, user_id: str, conversation_update: ConversationUpdate) -> Optional[ConversationRead]:
        """
        Update a specific conversation
        """
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return None
        
        update_data = conversation_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)
        
        conversation.updated_at = conversation.updated_at.now()  # Update timestamp
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return ConversationRead.from_orm(conversation)
    
    def delete_conversation(self, session: Session, conversation_id: str, user_id: str) -> bool:
        """
        Delete a specific conversation
        """
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return False
        
        session.delete(conversation)
        session.commit()
        return True
    
    def get_conversation_history(self, session: Session, conversation_id: str, user_id: str) -> List[dict]:
        """
        Retrieve conversation history with messages
        """
        # First verify the conversation belongs to the user
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []
        
        # Get messages for this conversation
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc())
        messages = session.exec(statement).all()
        
        return [{
            "id": msg.id,
            "sender_type": msg.sender_type,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
            "metadata_str": msg.metadata_str
        } for msg in messages]
    
    def update_conversation_title(self, session: Session, conversation_id: str, user_id: str, title: str) -> Optional[ConversationRead]:
        """
        Update conversation title
        """
        from datetime import datetime
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return None

        conversation.title = title
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return ConversationRead.from_orm(conversation)
    
    def create_conversation_with_first_message(self, session: Session, user_id: str, first_message: str) -> tuple[Optional[ConversationRead], Optional[dict]]:
        """
        Create a new conversation and add the first message
        """
        from ..models.message import MessageCreate, Message
        from datetime import datetime
        import json
        
        # Create conversation
        conversation_create = ConversationCreate(user_id=user_id)
        conversation = self.create_conversation(session, conversation_create)
        
        if not conversation:
            return None, {"status": "error", "message": "Failed to create conversation"}
        
        # Create first message
        message_create = MessageCreate(
            conversation_id=conversation.id,
            sender_type="user",
            content=first_message
        )
        
        message = Message.from_orm(message_create)
        message.timestamp = datetime.utcnow()
        # Handle metadata_str field
        if hasattr(message_create, 'metadata') and message_create.metadata:
            message.metadata_str = json.dumps(message_create.metadata)
        else:
            message.metadata_str = None
        session.add(message)
        session.commit()
        session.refresh(message)
        
        return conversation, {
            "status": "success",
            "message_id": message.id,
            "message": "Conversation created with first message"
        }
    
    def add_message_to_conversation(self, session: Session, conversation_id: str, user_id: str, content: str, sender_type: str) -> Optional[dict]:
        """
        Add a message to an existing conversation
        """
        from ..models.message import MessageCreate, Message
        from datetime import datetime
        import json
        
        # Verify conversation belongs to user
        conversation = self.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return {"status": "error", "message": "Conversation not found or doesn't belong to user"}
        
        # Create message
        message_create = MessageCreate(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content
        )
        
        message = Message.from_orm(message_create)
        message.timestamp = datetime.utcnow()
        # Handle metadata_str field
        if hasattr(message_create, 'metadata') and message_create.metadata:
            message.metadata_str = json.dumps(message_create.metadata)
        else:
            message.metadata_str = None
        session.add(message)
        session.commit()
        session.refresh(message)
        
        return {
            "status": "success",
            "message_id": message.id,
            "conversation_id": conversation_id
        }