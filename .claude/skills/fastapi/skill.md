---
name: fastapi-backend-development
description: |
  Expert guidance for building secure, authenticated REST APIs with FastAPI,
  SQLModel, Neon PostgreSQL, and JWT authentication integration with Better Auth.
  Focuses on ownership-based authorization and spec-driven development.

proficiency_level: "B2"
category: "Backend Development"
use_when: |
  - Building REST API endpoints with FastAPI
  - Implementing database models with SQLModel
  - Integrating JWT authentication from Better Auth
  - Implementing ownership-based authorization
  - Working with Neon PostgreSQL
  - Following spec-driven backend development
---

# FastAPI Backend Development Skill

## Role
You are an expert FastAPI backend developer specializing in building secure, type-safe REST APIs with SQLModel, PostgreSQL, and JWT authentication.

## Project Context
- **Framework**: FastAPI 0.100+
- **Language**: Python 3.11+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: JWT tokens from Better Auth (Next.js frontend)
- **Validation**: Pydantic v2
- **Testing**: pytest with pytest-asyncio

## Core Responsibilities

### 1. API Endpoint Development
- Design RESTful API endpoints following HTTP conventions
- Implement proper request/response models with Pydantic
- Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Return correct HTTP status codes (200, 201, 204, 400, 401, 403, 404, 500)
- Implement proper error handling with HTTPException
- Use dependency injection for reusable logic
- Document endpoints with OpenAPI/Swagger annotations

### 2. Database Models & Operations
- Define SQLModel models with proper types and constraints
- Implement relationships (one-to-many, many-to-many)
- Add timestamps (created_at, updated_at) to all models
- Use proper indexing for query performance
- Implement soft deletes where appropriate
- Handle database migrations with Alembic
- Use async database operations for better performance

### 3. Authentication & Authorization
- Verify JWT tokens from Better Auth
- Extract user information from JWT payload
- Implement dependency for getting current user
- Enforce ownership-based authorization (users can only access their own data)
- Return 401 for missing/invalid tokens
- Return 403 for authorization failures
- Never trust client-provided user_id; always use JWT claims

### 4. Security Best Practices
- Validate all input data with Pydantic models
- Sanitize database queries (SQLModel handles this)
- Implement rate limiting for API endpoints
- Use CORS middleware with proper configuration
- Never log sensitive data (passwords, tokens)
- Use environment variables for secrets
- Implement proper error messages (don't leak internal details)

### 5. Error Handling
- Use HTTPException for expected errors
- Implement global exception handlers for unexpected errors
- Return consistent error response format
- Log errors with appropriate severity levels
- Handle database connection errors gracefully
- Implement proper validation error messages

### 6. Testing
- Write unit tests for business logic
- Write integration tests for API endpoints
- Test authentication and authorization flows
- Test database operations with test database
- Mock external dependencies
- Test error cases and edge cases
- Aim for high test coverage (>80%)

## Development Guidelines

### Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database connection
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── todos.py
│   │       └── users.py
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── auth.py          # JWT verification
│   │   └── security.py      # Security utilities
│   └── tests/               # Test files
│       ├── __init__.py
│       ├── conftest.py
│       └── test_todos.py
├── alembic/                 # Database migrations
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── pytest.ini              # Pytest configuration
```

### Database Model Pattern
```python
# app/models/todo.py
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TodoBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
```

### JWT Authentication Pattern
```python
# app/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional

security = HTTPBearer()

def verify_jwt_token(token: str) -> dict:
    """Verify JWT token from Better Auth."""
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Dependency to get current authenticated user."""
    token = credentials.credentials
    payload = verify_jwt_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return {"id": int(user_id), "email": payload.get("email")}
```

### API Endpoint Pattern with Authorization
```python
# app/api/v1/todos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.core.auth import get_current_user
from app.models.todo import Todo, TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=list[TodoResponse])
async def get_todos(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Get all todos for the current user."""
    statement = select(Todo).where(Todo.user_id == current_user["id"])
    todos = session.exec(statement).all()
    return todos

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Create a new todo for the current user."""
    db_todo = Todo(**todo.model_dump(), user_id=current_user["id"])
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific todo by ID."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Ownership check
    if todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )

    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Update a todo."""
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Ownership check
    if db_todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

    # Update only provided fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db_todo.updated_at = datetime.utcnow()
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Delete a todo."""
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Ownership check
    if db_todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this todo"
        )

    session.delete(db_todo)
    session.commit()
    return None
```

### Database Connection Pattern (Neon)
```python
# app/database.py
from sqlmodel import Session, create_engine
from app.config import settings

# Neon PostgreSQL connection
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session
```

### Configuration Pattern
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Authentication
    BETTER_AUTH_SECRET: str

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Todo API"
    DEBUG: bool = False

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Testing Pattern
```python
# app/tests/test_todos.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.main import app
from app.database import get_session
from app.core.auth import get_current_user

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL)

def override_get_session():
    with Session(test_engine) as session:
        yield session

def override_get_current_user():
    return {"id": 1, "email": "test@example.com"}

app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

def test_create_todo():
    response = client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo", "description": "Test Description"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["user_id"] == 1

def test_get_todos():
    # Create a todo first
    client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo"}
    )

    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Todo"

def test_unauthorized_access():
    # Override to return different user
    app.dependency_overrides[get_current_user] = lambda: {"id": 2, "email": "other@example.com"}

    # Create todo as user 1
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.post("/api/v1/todos/", json={"title": "User 1 Todo"})
    todo_id = response.json()["id"]

    # Try to access as user 2
    app.dependency_overrides[get_current_user] = lambda: {"id": 2, "email": "other@example.com"}
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 403
```

## Best Practices

### Security Checklist
- ✅ Always verify JWT tokens on protected endpoints
- ✅ Always check resource ownership before operations
- ✅ Never trust client-provided user_id
- ✅ Use Pydantic models for input validation
- ✅ Return appropriate HTTP status codes
- ✅ Don't leak internal error details to clients
- ✅ Use environment variables for secrets
- ✅ Implement rate limiting on public endpoints
- ✅ Use HTTPS in production
- ✅ Enable CORS only for trusted origins

### Database Best Practices
- Use indexes on foreign keys and frequently queried fields
- Always filter by user_id for user-owned resources
- Use transactions for multi-step operations
- Handle database connection errors gracefully
- Use connection pooling for better performance
- Implement proper database migrations with Alembic
- Use UTC for all timestamps
- Add created_at and updated_at to all models

### API Design Best Practices
- Use plural nouns for resource endpoints (/todos, not /todo)
- Use HTTP methods correctly (GET, POST, PUT, DELETE)
- Return 201 for successful creation
- Return 204 for successful deletion
- Return 404 when resource not found
- Return 403 for authorization failures
- Return 422 for validation errors
- Include pagination for list endpoints
- Version your API (/api/v1/)

### Code Quality
- Use type hints for all function parameters and returns
- Write docstrings for all public functions
- Keep functions small and focused (single responsibility)
- Use dependency injection for testability
- Avoid circular imports
- Use async/await for I/O operations
- Handle exceptions at appropriate levels
- Log important events and errors

## Common Tasks

### Adding a New Resource
1. Create SQLModel in `app/models/`
2. Create Pydantic schemas for Create/Update/Response
3. Create API router in `app/api/v1/`
4. Implement CRUD endpoints with ownership checks
5. Add database migration with Alembic
6. Write tests for all endpoints
7. Update API documentation

### Implementing a Protected Endpoint
1. Add `current_user: dict = Depends(get_current_user)` to endpoint
2. Filter queries by `user_id == current_user["id"]`
3. Check ownership before update/delete operations
4. Return 403 if ownership check fails
5. Write tests for authorization scenarios

### Adding Database Migration
```bash
# Create migration
alembic revision --autogenerate -m "Add todos table"

# Review migration file in alembic/versions/

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

## Anti-Patterns to Avoid

❌ **Don't trust client-provided user_id**
```python
# BAD
@router.post("/todos/")
async def create_todo(todo: TodoCreate, user_id: int):
    db_todo = Todo(**todo.dict(), user_id=user_id)  # Client can fake user_id!
```

✅ **Always use JWT user_id**
```python
# GOOD
@router.post("/todos/")
async def create_todo(
    todo: TodoCreate,
    current_user: dict = Depends(get_current_user)
):
    db_todo = Todo(**todo.dict(), user_id=current_user["id"])
```

❌ **Don't skip ownership checks**
```python
# BAD
@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    session.delete(todo)  # Any user can delete any todo!
```

✅ **Always verify ownership**
```python
# GOOD
@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if todo.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    session.delete(todo)
```

❌ **Don't return internal error details**
```python
# BAD
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))  # Leaks internal info
```

✅ **Return generic error messages**
```python
# GOOD
except Exception as e:
    logger.error(f"Error creating todo: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

❌ **Don't use synchronous database operations in async endpoints**
```python
# BAD - blocks event loop
@router.get("/todos/")
async def get_todos():
    todos = session.query(Todo).all()  # Synchronous query
```

✅ **Use async operations or sync endpoints**
```python
# GOOD - sync endpoint for sync operations
@router.get("/todos/")
def get_todos():
    todos = session.query(Todo).all()
```

## Success Criteria
- All endpoints require authentication (except public ones)
- All operations enforce ownership-based authorization
- All input is validated with Pydantic models
- All endpoints return appropriate HTTP status codes
- All database models have proper constraints and indexes
- All endpoints have comprehensive tests
- No sensitive data is logged or exposed
- API documentation is complete and accurate
- Code follows Python best practices (PEP 8, type hints)
- Error handling is consistent and user-friendly

## Integration with Frontend
- Frontend sends JWT token in Authorization header: `Bearer <token>`
- Backend verifies token and extracts user_id
- Backend filters all queries by user_id
- Backend returns consistent JSON responses
- Backend handles CORS for frontend origin
- Backend provides clear error messages for frontend to display
