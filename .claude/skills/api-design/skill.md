---
name: rest-api-design
description: |
  Comprehensive guide for designing RESTful APIs with best practices for
  endpoints, HTTP methods, status codes, versioning, documentation, error
  handling, and API contracts for full-stack applications.

proficiency_level: "B2"
category: "API Design"
use_when: |
  - Designing new API endpoints
  - Defining API contracts between frontend and backend
  - Implementing RESTful conventions
  - Creating API documentation
  - Versioning APIs
  - Handling API errors consistently
---

# REST API Design Best Practices

## Role
You are an API design specialist focused on creating intuitive, consistent, and well-documented RESTful APIs.

## REST API Fundamentals

### Core Principles

**1. Resource-Based URLs:**
```
✅ GOOD: /api/v1/todos
✅ GOOD: /api/v1/todos/123
✅ GOOD: /api/v1/users/456/todos

❌ BAD: /api/v1/getTodos
❌ BAD: /api/v1/createTodo
❌ BAD: /api/v1/todo-list
```

**2. Use HTTP Methods Correctly:**
```
GET    - Retrieve resource(s)
POST   - Create new resource
PUT    - Update entire resource
PATCH  - Partial update resource
DELETE - Remove resource
```

**3. Use Plural Nouns:**
```
✅ GOOD: /api/v1/todos
✅ GOOD: /api/v1/users

❌ BAD: /api/v1/todo
❌ BAD: /api/v1/user
```

**4. Use HTTP Status Codes:**
```
2xx - Success
3xx - Redirection
4xx - Client errors
5xx - Server errors
```

## API Endpoint Design

### Standard CRUD Endpoints

**Todo Resource Example:**

```
GET    /api/v1/todos           - List all todos (with pagination)
POST   /api/v1/todos           - Create new todo
GET    /api/v1/todos/{id}      - Get specific todo
PUT    /api/v1/todos/{id}      - Update entire todo
PATCH  /api/v1/todos/{id}      - Partial update todo
DELETE /api/v1/todos/{id}      - Delete todo
```

**Implementation:**

```python
# app/api/v1/todos.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.core.auth import get_current_user
from app.models.todo import Todo, TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[TodoResponse])
async def list_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    completed: bool | None = Query(None, description="Filter by completion status"),
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    List todos for the authenticated user.

    - **skip**: Pagination offset (default: 0)
    - **limit**: Max results per page (default: 10, max: 100)
    - **completed**: Filter by completion status (optional)
    """
    statement = select(Todo).where(Todo.user_id == current_user["id"])

    if completed is not None:
        statement = statement.where(Todo.completed == completed)

    statement = statement.offset(skip).limit(limit).order_by(Todo.created_at.desc())
    todos = session.exec(statement).all()
    return todos

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new todo.

    - **title**: Todo title (required, max 255 chars)
    - **description**: Todo description (optional)
    - **completed**: Completion status (default: false)
    """
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
    """Update a todo (full update)."""
    db_todo = session.get(Todo, todo_id)

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    if db_todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

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

    if db_todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this todo"
        )

    session.delete(db_todo)
    session.commit()
    return None
```

### Nested Resources

**When to use nested routes:**
```
✅ GOOD: /api/v1/users/{user_id}/todos
Use when: Resource belongs to parent and context is important

✅ GOOD: /api/v1/todos?user_id={user_id}
Use when: Resource can exist independently

❌ BAD: /api/v1/users/{user_id}/todos/{todo_id}/comments/{comment_id}
Avoid: Deep nesting (max 2 levels)
```

**Example:**
```python
@router.get("/users/{user_id}/todos", response_model=List[TodoResponse])
async def get_user_todos(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Get todos for a specific user (admin only)."""
    # Check if current user is admin or requesting their own todos
    if current_user["id"] != user_id and not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos
```

## HTTP Status Codes

### Success Codes (2xx)

```python
# 200 OK - Successful GET, PUT, PATCH
@router.get("/{id}")
async def get_resource(id: int):
    return resource  # 200 OK

# 201 Created - Successful POST
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_resource(data: ResourceCreate):
    return created_resource  # 201 Created

# 204 No Content - Successful DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(id: int):
    return None  # 204 No Content
```

### Client Error Codes (4xx)

```python
# 400 Bad Request - Invalid request data
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid request data"
)

# 401 Unauthorized - Missing or invalid authentication
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Authentication required"
)

# 403 Forbidden - Authenticated but not authorized
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access this resource"
)

# 404 Not Found - Resource doesn't exist
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# 409 Conflict - Resource conflict (e.g., duplicate)
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Resource already exists"
)

# 422 Unprocessable Entity - Validation error
# FastAPI handles this automatically with Pydantic
```

### Server Error Codes (5xx)

```python
# 500 Internal Server Error - Unexpected server error
raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error"
)

# 503 Service Unavailable - Service temporarily unavailable
raise HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Service temporarily unavailable"
)
```

## Request/Response Schemas

### Pydantic Models

```python
# app/schemas/todo.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    """Base todo schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Todo title")
    description: Optional[str] = Field(None, description="Todo description")
    completed: bool = Field(False, description="Completion status")

class TodoCreate(TodoBase):
    """Schema for creating a todo."""
    pass

class TodoUpdate(BaseModel):
    """Schema for updating a todo (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    """Schema for todo response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TodoListResponse(BaseModel):
    """Schema for paginated todo list."""
    items: list[TodoResponse]
    total: int
    skip: int
    limit: int
```

### Example Requests/Responses

**Create Todo:**
```http
POST /api/v1/todos
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}

Response: 201 Created
{
  "id": 123,
  "user_id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**List Todos:**
```http
GET /api/v1/todos?skip=0&limit=10&completed=false
Authorization: Bearer <token>

Response: 200 OK
{
  "items": [
    {
      "id": 123,
      "user_id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

## Error Handling

### Consistent Error Format

```python
# app/schemas/error.py
from pydantic import BaseModel
from typing import Optional, List

class ErrorDetail(BaseModel):
    """Detailed error information."""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None

class ErrorResponse(BaseModel):
    """Standard error response format."""
    detail: str
    errors: Optional[List[ErrorDetail]] = None
```

### Custom Exception Handler

```python
# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "code": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Resource conflict",
            "errors": [{"message": "Resource already exists or violates constraints"}]
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error"
        }
    )
```

## API Versioning

### URL Versioning (Recommended)

```python
# app/main.py
from fastapi import FastAPI
from app.api.v1 import todos as todos_v1
from app.api.v2 import todos as todos_v2

app = FastAPI()

# Version 1
app.include_router(todos_v1.router, prefix="/api/v1", tags=["v1"])

# Version 2 (with breaking changes)
app.include_router(todos_v2.router, prefix="/api/v2", tags=["v2"])
```

**Advantages:**
- ✅ Clear and explicit
- ✅ Easy to route
- ✅ Can run multiple versions simultaneously
- ✅ Easy to deprecate old versions

### Header Versioning (Alternative)

```python
from fastapi import Header, HTTPException

async def get_api_version(
    api_version: str = Header(default="v1", alias="X-API-Version")
) -> str:
    """Extract API version from header."""
    if api_version not in ["v1", "v2"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {api_version}"
        )
    return api_version
```

## Pagination

### Offset-Based Pagination

```python
from fastapi import Query
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    skip: int
    limit: int
    has_more: bool

@router.get("/todos", response_model=PaginatedResponse[TodoResponse])
async def list_todos(
    skip: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, ge=1, le=100, description="Limit"),
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """List todos with pagination."""
    # Get total count
    count_statement = select(func.count()).select_from(Todo).where(
        Todo.user_id == current_user["id"]
    )
    total = session.exec(count_statement).one()

    # Get paginated results
    statement = (
        select(Todo)
        .where(Todo.user_id == current_user["id"])
        .order_by(Todo.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    items = session.exec(statement).all()

    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
        has_more=(skip + limit) < total
    )
```

### Cursor-Based Pagination (For Large Datasets)

```python
@router.get("/todos/cursor")
async def list_todos_cursor(
    cursor: Optional[int] = Query(None, description="Cursor (last todo ID)"),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """List todos with cursor-based pagination."""
    statement = select(Todo).where(Todo.user_id == current_user["id"])

    if cursor:
        statement = statement.where(Todo.id < cursor)

    statement = statement.order_by(Todo.id.desc()).limit(limit + 1)
    items = session.exec(statement).all()

    has_more = len(items) > limit
    if has_more:
        items = items[:limit]

    next_cursor = items[-1].id if items and has_more else None

    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more
    }
```

## Filtering and Sorting

### Query Parameters

```python
from enum import Enum

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class TodoSortField(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"

@router.get("/todos")
async def list_todos(
    # Filtering
    completed: Optional[bool] = Query(None, description="Filter by completion"),
    search: Optional[str] = Query(None, description="Search in title/description"),

    # Sorting
    sort_by: TodoSortField = Query(TodoSortField.CREATED_AT, description="Sort field"),
    sort_order: SortOrder = Query(SortOrder.DESC, description="Sort order"),

    # Pagination
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),

    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """List todos with filtering, sorting, and pagination."""
    statement = select(Todo).where(Todo.user_id == current_user["id"])

    # Apply filters
    if completed is not None:
        statement = statement.where(Todo.completed == completed)

    if search:
        statement = statement.where(
            (Todo.title.ilike(f"%{search}%")) |
            (Todo.description.ilike(f"%{search}%"))
        )

    # Apply sorting
    sort_column = getattr(Todo, sort_by.value)
    if sort_order == SortOrder.DESC:
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    # Apply pagination
    statement = statement.offset(skip).limit(limit)

    items = session.exec(statement).all()
    return items
```

## API Documentation

### OpenAPI/Swagger Configuration

```python
# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Todo API",
    description="A RESTful API for managing todos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

def custom_openapi():
    """Customize OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Todo API",
        version="1.0.0",
        description="A RESTful API for managing todos with authentication",
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Endpoint Documentation

```python
@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
    description="Create a new todo item for the authenticated user",
    response_description="The created todo",
    responses={
        201: {
            "description": "Todo created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "user_id": 1,
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "completed": false,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"}
    }
)
async def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new todo with the following information:

    - **title**: Todo title (required, 1-255 characters)
    - **description**: Detailed description (optional)
    - **completed**: Completion status (default: false)

    Returns the created todo with generated ID and timestamps.
    """
    db_todo = Todo(**todo.model_dump(), user_id=current_user["id"])
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
```

## Rate Limiting

```python
# app/middleware/rate_limit.py
from fastapi import Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# app/main.py
from app.middleware.rate_limit import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/todos")
@limiter.limit("10/minute")
async def create_todo(request: Request, todo: TodoCreate):
    """Create todo with rate limiting (10 requests per minute)."""
    pass
```

## Best Practices Summary

### ✅ DO:
- Use RESTful conventions
- Use plural nouns for resources
- Use HTTP methods correctly
- Return appropriate status codes
- Implement pagination for lists
- Version your API
- Document all endpoints
- Use consistent error format
- Implement rate limiting
- Use query parameters for filtering/sorting
- Validate all input
- Use proper authentication
- Implement CORS correctly

### ❌ DON'T:
- Use verbs in URLs
- Return 200 for errors
- Skip pagination on large datasets
- Break API contracts without versioning
- Expose internal errors to clients
- Skip input validation
- Use deeply nested routes (>2 levels)
- Return inconsistent response formats
- Skip API documentation
- Ignore rate limiting
- Use GET for state-changing operations
- Return sensitive data unnecessarily

## API Contract Example

```typescript
// Shared types between frontend and backend
// types/api.ts

export interface Todo {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;  // ISO 8601
  updated_at: string;  // ISO 8601
}

export interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
}

export interface ErrorResponse {
  detail: string;
  errors?: Array<{
    field?: string;
    message: string;
    code?: string;
  }>;
}
```

## Summary

Well-designed APIs are:
1. **Intuitive**: Follow REST conventions
2. **Consistent**: Uniform patterns across endpoints
3. **Well-documented**: Clear OpenAPI/Swagger docs
4. **Versioned**: Support multiple versions
5. **Secure**: Proper authentication and authorization
6. **Performant**: Pagination, filtering, caching
7. **Reliable**: Proper error handling and status codes

Follow these guidelines to create APIs that are easy to use, maintain, and scale.
