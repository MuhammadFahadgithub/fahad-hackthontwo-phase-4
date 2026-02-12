"""
Chat service for processing natural language commands in the Todo Chatbot application
"""
import re
from typing import Tuple, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.todo import Todo
from ..models.message import Message
from ..models.conversation import Conversation
from ..utils import log_info, log_error
from ..utils.chat_parser import parse_todo_command, extract_todo_details


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def process_message(self, message: str, user_id: str, conversation_id: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Process a chat message and return a response along with suggested actions
        """
        parsed_command = parse_todo_command(message)
        operation = parsed_command['operation']
        
        if operation == 'add':
            return self._handle_add_todo(parsed_command['text'], user_id)
        elif operation == 'list':
            return self._handle_list_todos(user_id)
        elif operation == 'complete':
            return self._handle_complete_todo(parsed_command['text'], user_id)
        elif operation == 'delete':
            return self._handle_delete_todo(parsed_command['text'], user_id)
        else:
            # Default response if no known intent is detected
            return "I didn't understand that command. You can ask me to add, list, complete, or delete todos.", []

    def _handle_add_todo(self, todo_text: str, user_id: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Handle adding a new todo
        """
        try:
            # Extract detailed information from the todo text
            todo_details = extract_todo_details(todo_text)
            
            # Create a new todo
            new_todo = Todo(
                id=str(len(self.db.query(Todo).filter(Todo.user_id == user_id).all()) + 1),  # Simplified ID generation
                user_id=user_id,
                title=todo_details['title'],
                description=todo_details['description'],
                completed=False,
                priority=todo_details['priority']
            )
            
            self.db.add(new_todo)
            self.db.commit()
            
            response = f"I've added '{todo_details['title']}' to your todos."
            actions = [{"type": "create_todo", "params": {"title": todo_details['title'], "priority": todo_details['priority']}}]
            
            log_info(f"Added new todo: {todo_details['title']} for user: {user_id}")
            
            return response, actions
        except Exception as e:
            log_error(f"Error adding todo: {str(e)}", {"user_id": user_id, "todo_text": todo_text})
            return "Sorry, I couldn't add that todo. Please try again.", []

    def _handle_list_todos(self, user_id: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Handle listing todos
        """
        try:
            todos = self.db.query(Todo).filter(Todo.user_id == user_id).all()
            
            if not todos:
                response = "You don't have any todos yet. You can add one by saying 'Add a todo: ...'"
            else:
                todo_list = [f"- {'✓' if t.completed else '○'} {t.title} [{t.priority}]" for t in todos]
                response = f"Here are your todos:\n" + "\n".join(todo_list)
            
            actions = [{"type": "list_todos", "params": {"count": len(todos)}}]
            
            log_info(f"Listed {len(todos)} todos for user: {user_id}")
            
            return response, actions
        except Exception as e:
            log_error(f"Error listing todos: {str(e)}", {"user_id": user_id})
            return "Sorry, I couldn't retrieve your todos. Please try again.", []

    def _handle_complete_todo(self, todo_text: str, user_id: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Handle completing a todo
        """
        try:
            # Find the todo by title
            todo = self.db.query(Todo).filter(
                Todo.user_id == user_id,
                Todo.title.ilike(f"%{todo_text}%")
            ).first()
            
            if todo:
                todo.completed = True
                self.db.commit()
                
                response = f"I've marked '{todo.title}' as completed."
                actions = [{"type": "update_todo", "params": {"id": todo.id, "completed": True}}]
                
                log_info(f"Completed todo: {todo.title} for user: {user_id}")
            else:
                response = f"I couldn't find a todo with title '{todo_text}'. Please check the spelling."
                actions = []
            
            return response, actions
        except Exception as e:
            log_error(f"Error completing todo: {str(e)}", {"user_id": user_id, "todo_text": todo_text})
            return "Sorry, I couldn't complete that todo. Please try again.", []

    def _handle_delete_todo(self, todo_text: str, user_id: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Handle deleting a todo
        """
        try:
            # Find the todo by title
            todo = self.db.query(Todo).filter(
                Todo.user_id == user_id,
                Todo.title.ilike(f"%{todo_text}%")
            ).first()
            
            if todo:
                self.db.delete(todo)
                self.db.commit()
                
                response = f"I've deleted '{todo.title}' from your todos."
                actions = [{"type": "delete_todo", "params": {"id": todo.id}}]
                
                log_info(f"Deleted todo: {todo.title} for user: {user_id}")
            else:
                response = f"I couldn't find a todo with title '{todo_text}'. Please check the spelling."
                actions = []
            
            return response, actions
        except Exception as e:
            log_error(f"Error deleting todo: {str(e)}", {"user_id": user_id, "todo_text": todo_text})
            return "Sorry, I couldn't delete that todo. Please try again.", []