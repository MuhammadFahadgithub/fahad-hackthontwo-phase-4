"""
Todo API endpoints for the Todo Chatbot application
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models.todo import Todo
from ..models.user import User
from .. import schemas
from ..auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.Todo])
async def get_todos(
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    status_param: Optional[str] = Query(None, regex="^(all|pending|completed)$"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of todos for the current user
    """
    query = db.query(Todo).filter(Todo.user_id == current_user.id)

    if status_param == "pending":
        query = query.filter(Todo.completed == False)
    elif status_param == "completed":
        query = query.filter(Todo.completed == True)

    todos = query.offset(skip).limit(limit).all()
    return todos


@router.post("/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: schemas.TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo for the current user
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=False,
        due_date=todo.due_date,
        priority=todo.priority or "medium",
        user_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/{todo_id}", response_model=schemas.Todo)
async def get_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific todo by ID
    """
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/{todo_id}", response_model=schemas.Todo)
async def update_todo(
    todo_id: str,
    todo_update: schemas.TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a specific todo by ID
    """
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
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

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific todo by ID
    """
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    db.delete(todo)
    db.commit()
    return