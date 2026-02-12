"""
Todo service for managing todo operations in the Todo Chatbot application
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.todo import Todo
from .. import schemas
from ..utils import log_info, log_error


class TodoService:
    def __init__(self, db: Session):
        self.db = db

    def get_todos(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Todo]:
        """
        Retrieve a list of todos for a user with optional filtering
        """
        try:
            query = self.db.query(Todo).filter(Todo.user_id == user_id)

            if status == "pending":
                query = query.filter(Todo.completed == False)
            elif status == "completed":
                query = query.filter(Todo.completed == True)

            todos = query.offset(skip).limit(limit).all()
            
            log_info(f"Retrieved {len(todos)} todos for user: {user_id}", {
                "skip": skip,
                "limit": limit,
                "status": status
            })
            
            return todos
        except Exception as e:
            log_error(f"Error retrieving todos: {str(e)}", {
                "user_id": user_id,
                "skip": skip,
                "limit": limit,
                "status": status
            })
            raise

    def get_todo(self, todo_id: str, user_id: str) -> Optional[Todo]:
        """
        Retrieve a specific todo by ID for a user
        """
        try:
            todo = self.db.query(Todo).filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            ).first()
            
            if todo:
                log_info(f"Retrieved todo: {todo_id} for user: {user_id}")
            else:
                log_info(f"Todo not found: {todo_id} for user: {user_id}")
            
            return todo
        except Exception as e:
            log_error(f"Error retrieving todo: {str(e)}", {
                "todo_id": todo_id,
                "user_id": user_id
            })
            raise

    def create_todo(self, todo_create: schemas.TodoCreate, user_id: str) -> Todo:
        """
        Create a new todo for a user
        """
        try:
            new_todo = Todo(
                id=str(len(self.db.query(Todo).filter(Todo.user_id == user_id).all()) + 1),  # Simplified ID generation
                user_id=user_id,
                title=todo_create.title,
                description=todo_create.description,
                completed=getattr(todo_create, 'completed', False),
                due_date=todo_create.due_date,
                priority=todo_create.priority or "medium"
            )
            
            self.db.add(new_todo)
            self.db.commit()
            self.db.refresh(new_todo)
            
            log_info(f"Created new todo: {new_todo.id} for user: {user_id}", {
                "title": todo_create.title
            })
            
            return new_todo
        except Exception as e:
            log_error(f"Error creating todo: {str(e)}", {
                "user_id": user_id,
                "title": todo_create.title
            })
            raise

    def update_todo(self, todo_id: str, todo_update: schemas.TodoUpdate, user_id: str) -> Optional[Todo]:
        """
        Update a specific todo for a user
        """
        try:
            todo = self.db.query(Todo).filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            ).first()
            
            if not todo:
                log_info(f"Todo not found for update: {todo_id} for user: {user_id}")
                return None
            
            # Update fields that were provided
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.description is not None:
                todo.description = todo_update.description
            if todo_update.completed is not None:
                todo.completed = todo_update.completed
            if todo_update.due_date is not None:
                todo.due_date = todo_update.due_date
            if todo_update.priority is not None:
                todo.priority = todo_update.priority
            
            todo.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(todo)
            
            log_info(f"Updated todo: {todo_id} for user: {user_id}")
            
            return todo
        except Exception as e:
            log_error(f"Error updating todo: {str(e)}", {
                "todo_id": todo_id,
                "user_id": user_id
            })
            raise

    def delete_todo(self, todo_id: str, user_id: str) -> bool:
        """
        Delete a specific todo for a user
        """
        try:
            todo = self.db.query(Todo).filter(
                Todo.id == todo_id,
                Todo.user_id == user_id
            ).first()
            
            if not todo:
                log_info(f"Todo not found for deletion: {todo_id} for user: {user_id}")
                return False
            
            self.db.delete(todo)
            self.db.commit()
            
            log_info(f"Deleted todo: {todo_id} for user: {user_id}")
            
            return True
        except Exception as e:
            log_error(f"Error deleting todo: {str(e)}", {
                "todo_id": todo_id,
                "user_id": user_id
            })
            raise