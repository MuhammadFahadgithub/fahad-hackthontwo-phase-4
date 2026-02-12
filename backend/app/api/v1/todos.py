"""
Todo CRUD endpoints.

Handles todo creation, reading, updating, and deletion with ownership enforcement.
Constitution Principles III-V compliance.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.database import get_session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.core.auth import get_current_user


router = APIRouter()


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo.

    Constitution SR-002: JWT authentication required
    Constitution SR-006: User identity from JWT only
    Constitution Principle IV: User_id from JWT, never from request body

    Args:
        todo_data: Todo information (title, description, completed)
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TodoResponse with created todo data

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 422: Invalid input data
    """
    # Create new todo with user_id from JWT (Constitution Principle III)
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed,
        user_id=current_user["id"],  # From JWT only, never from request
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)

    return new_todo


@router.get("", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def list_todos(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all todos for the authenticated user.

    Constitution Principle IV: Query-level authorization with user_id filtering
    Constitution Principle V: Zero cross-user data access

    Args:
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        List of TodoResponse for the current user

    Raises:
        HTTPException 401: Not authenticated
    """
    # Query with user_id filter (Constitution Principle IV)
    statement = select(Todo).where(Todo.user_id == current_user["id"])
    todos = session.exec(statement).all()

    return todos


@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def get_todo(
    todo_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID.

    Constitution Principle V: Ownership verification required

    Args:
        todo_id: Todo ID
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TodoResponse with todo data

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Not authorized (wrong owner)
        HTTPException 404: Todo not found
    """
    # Get todo
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify ownership (Constitution Principle V)
    if todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )

    return todo


@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a todo.

    Constitution Principle V: Ownership verification required

    Args:
        todo_id: Todo ID
        todo_data: Updated todo information
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TodoResponse with updated todo data

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Not authorized (wrong owner)
        HTTPException 404: Todo not found
    """
    # Get todo
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify ownership (Constitution Principle V)
    if todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

    # Update fields (only provided fields)
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.delete("/{todo_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_todo(
    todo_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a todo.

    Constitution Principle V: Ownership verification required

    Args:
        todo_id: Todo ID
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Not authorized (wrong owner)
        HTTPException 404: Todo not found
    """
    # Get todo
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify ownership (Constitution Principle V)
    if todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this todo"
        )

    session.delete(todo)
    session.commit()

    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/toggle", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def toggle_todo_completion(
    todo_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle todo completion status.

    Constitution Principle V: Ownership verification required

    Args:
        todo_id: Todo ID
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TodoResponse with updated todo data

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Not authorized (wrong owner)
        HTTPException 404: Todo not found
    """
    # Get todo
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify ownership (Constitution Principle V)
    if todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

    # Toggle completion status
    todo.completed = not todo.completed
    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo
