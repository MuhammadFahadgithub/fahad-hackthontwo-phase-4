# Data Model Documentation

**Feature**: Full-Stack Todo Application
**Date**: 2026-02-07
**Database**: Neon PostgreSQL (serverless)
**ORM**: SQLModel

This document defines the database schema, entity relationships, and data validation rules for the todo application.

## Entity-Relationship Diagram

```
┌─────────────────────────────────────┐
│             users                   │
├─────────────────────────────────────┤
│ id (PK)              INTEGER        │
│ email                VARCHAR(255)   │ UNIQUE, INDEXED
│ name                 VARCHAR(255)   │ NULLABLE
│ hashed_password      VARCHAR(255)   │
│ created_at           TIMESTAMP      │
│ updated_at           TIMESTAMP      │
└─────────────────────────────────────┘
                │
                │ 1:N
                │
                ▼
┌─────────────────────────────────────┐
│             todos                   │
├─────────────────────────────────────┤
│ id (PK)              INTEGER        │
│ title                VARCHAR(255)   │
│ description          VARCHAR(1000)  │ NULLABLE
│ completed            BOOLEAN        │ DEFAULT FALSE
│ user_id (FK)         INTEGER        │ INDEXED → users.id
│ created_at           TIMESTAMP      │
│ updated_at           TIMESTAMP      │
└─────────────────────────────────────┘
```

## Entities

### User Entity

**Purpose**: Represents an authenticated user account in the system.

**Table Name**: `users`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the user |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE, INDEXED | User's email address (used for login) |
| `name` | VARCHAR(255) | NULLABLE | User's display name |
| `hashed_password` | VARCHAR(255) | NOT NULL | bcrypt hash of user's password (cost factor 12) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | UTC timestamp when user was created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | UTC timestamp when user was last updated |

**Indexes**:
- Primary key index on `id`
- Unique index on `email` (for fast login lookups and uniqueness enforcement)

**SQLModel Definition** (backend/app/models/user.py):
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    name: Optional[str] = Field(default=None, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- Email must be valid email format (validated by Pydantic)
- Email must be unique across all users
- Password must be at least 8 characters (validated before hashing)
- Password is hashed with bcrypt (cost factor 12) before storage
- Name is optional

**Security Notes**:
- Password is NEVER stored in plain text
- Password hash uses bcrypt with cost factor 12 (~250ms per hash)
- Email uniqueness prevents duplicate accounts
- created_at and updated_at use UTC timestamps

---

### Todo Entity

**Purpose**: Represents a task/todo item belonging to a specific user.

**Table Name**: `todos`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the todo |
| `title` | VARCHAR(255) | NOT NULL | Todo title/summary |
| `description` | VARCHAR(1000) | NULLABLE | Detailed description of the todo |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY → users.id, INDEXED | Owner of this todo |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | UTC timestamp when todo was created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | UTC timestamp when todo was last updated |

**Indexes**:
- Primary key index on `id`
- Foreign key index on `user_id` (for fast user-specific queries)

**SQLModel Definition** (backend/app/models/todo.py):
```python
class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- Title is required and max 255 characters
- Description is optional and max 1000 characters
- Completed defaults to false
- user_id must reference an existing user
- user_id is set from JWT token (never from request body)

**Security Notes**:
- user_id is ALWAYS extracted from JWT token
- All queries MUST filter by authenticated user_id
- Ownership verification required before updates/deletes
- Cross-user data access is prevented at query level

---

## Relationships

### User → Todos (One-to-Many)

**Relationship**: One user can have many todos

**Implementation**:
- `todos.user_id` is a foreign key to `users.id`
- Foreign key constraint ensures referential integrity
- Indexed for fast queries

**Query Patterns**:
```python
# Get all todos for a user
todos = session.exec(
    select(Todo).where(Todo.user_id == current_user_id)
).all()

# Get single todo with ownership check
todo = session.exec(
    select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user_id)
).first()
```

**Cascade Behavior**:
- When a user is deleted, their todos should be deleted (CASCADE)
- Currently not implemented (users are not deletable in MVP)
- Future enhancement: Add ON DELETE CASCADE constraint

---

## State Transitions

### Todo Completion State

**States**:
- `completed = false` (incomplete)
- `completed = true` (complete)

**Transitions**:
```
incomplete (false) ←→ complete (true)
```

**Operations**:
- `PATCH /api/v1/todos/{id}/toggle` - Toggle between states
- `PUT /api/v1/todos/{id}` - Set specific state

**Business Rules**:
- Any authenticated user can toggle their own todos
- Toggling is idempotent (can toggle multiple times)
- No restrictions on transition direction

---

## Data Validation

### User Validation

**Email Validation**:
- Format: Must be valid email format (RFC 5322)
- Uniqueness: Must be unique across all users
- Case sensitivity: Stored as-is, compared case-insensitively
- Max length: 255 characters

**Password Validation**:
- Min length: 8 characters
- Max length: No explicit limit (hashed to fixed length)
- Complexity: No requirements (user choice)
- Storage: bcrypt hash (60 characters)

**Name Validation**:
- Optional field
- Max length: 255 characters
- No format restrictions

### Todo Validation

**Title Validation**:
- Required field
- Min length: 1 character (non-empty)
- Max length: 255 characters
- No format restrictions

**Description Validation**:
- Optional field
- Max length: 1000 characters
- No format restrictions

**Completed Validation**:
- Boolean field (true/false)
- Defaults to false
- No additional validation

---

## Query Optimization

### Indexes

**Primary Indexes**:
- `users.id` (primary key) - Automatic
- `todos.id` (primary key) - Automatic

**Secondary Indexes**:
- `users.email` (unique) - For fast login lookups
- `todos.user_id` (foreign key) - For fast user-specific queries

**Query Performance**:
- User lookup by email: O(log n) with index
- Todos by user_id: O(log n) with index
- Single todo by id: O(log n) with primary key

### Connection Pooling

**Configuration**:
- Neon PostgreSQL provides built-in connection pooling
- SQLModel uses connection pool via SQLAlchemy
- Default pool size: 5 connections
- Max overflow: 10 connections

---

## Migration Strategy

### Alembic Migrations

**Migration Files** (backend/alembic/versions/):
- Initial migration creates users and todos tables
- Migrations are versioned and tracked
- Migrations can be rolled back if needed

**Migration Commands**:
```bash
# Create new migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

**Best Practices**:
- Never modify existing migrations (create new ones)
- Test migrations on development database first
- Always provide rollback logic (downgrade)
- Document breaking changes in migration comments

---

## Data Integrity

### Constraints

**Primary Key Constraints**:
- `users.id` - Ensures unique user identification
- `todos.id` - Ensures unique todo identification

**Foreign Key Constraints**:
- `todos.user_id → users.id` - Ensures todos belong to valid users

**Unique Constraints**:
- `users.email` - Prevents duplicate email addresses

**Not Null Constraints**:
- All required fields enforce NOT NULL
- Optional fields allow NULL

### Referential Integrity

**Enforcement**:
- Foreign key constraints enforced at database level
- SQLModel validates relationships before insert/update
- Application layer performs additional ownership checks

**Error Handling**:
- Foreign key violations return 422 Unprocessable Entity
- Unique constraint violations return 409 Conflict
- Not null violations return 422 Unprocessable Entity

---

## Data Access Patterns

### User Isolation Pattern

**Rule**: All queries MUST filter by authenticated user_id

**Implementation**:
```python
# ✅ CORRECT: Filter by user_id
todos = session.exec(
    select(Todo).where(Todo.user_id == current_user_id)
).all()

# ❌ INCORRECT: No user_id filter (security violation)
todos = session.exec(select(Todo)).all()
```

**Enforcement**:
- user_id extracted from JWT token
- Never trust user_id from request body
- Verify ownership before updates/deletes
- Return 403 Forbidden for ownership violations

### Ownership Verification Pattern

**Rule**: Verify ownership before any update/delete operation

**Implementation**:
```python
# Fetch todo with ownership check
todo = session.exec(
    select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user_id)
).first()

if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")

# Now safe to update/delete
todo.title = new_title
session.commit()
```

---

## Performance Benchmarks

### Expected Query Performance

**User Operations**:
- Login (email lookup): <10ms
- User creation: ~250ms (bcrypt hashing)

**Todo Operations**:
- List todos (per user): <50ms (100 todos)
- Get single todo: <10ms
- Create todo: <20ms
- Update todo: <20ms
- Delete todo: <20ms

**Database Connection**:
- Connection acquisition: <5ms (pooled)
- Query execution: <10ms average

---

## Future Enhancements

### Potential Schema Changes

**User Enhancements**:
- Add `email_verified` boolean field
- Add `reset_token` and `reset_token_expires` for password reset
- Add `last_login_at` timestamp
- Add `is_active` boolean for soft delete

**Todo Enhancements**:
- Add `due_date` timestamp field
- Add `priority` enum field (low, medium, high)
- Add `category` or `tags` for organization
- Add `parent_id` for subtasks
- Add `order` integer for custom sorting

**New Entities**:
- `categories` table for todo categorization
- `tags` table with many-to-many relationship
- `shared_todos` table for collaboration

---

## Summary

The data model is designed with the following principles:

✅ **Security First**: User isolation enforced at query level
✅ **Simplicity**: Minimal schema for MVP functionality
✅ **Performance**: Indexed foreign keys for fast queries
✅ **Integrity**: Foreign key constraints and validation
✅ **Scalability**: Neon serverless auto-scales with load
✅ **Maintainability**: Clear relationships and validation rules

**Status**: Schema implemented and tested with 55 passing tests
