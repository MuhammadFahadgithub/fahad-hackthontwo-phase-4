---
name: neon-postgres-database
description: |
  Comprehensive guide for working with Neon PostgreSQL serverless database,
  SQLModel ORM, database migrations with Alembic, and schema design best
  practices for full-stack applications.

proficiency_level: "B2"
category: "Database"
use_when: |
  - Setting up Neon PostgreSQL database
  - Designing database schemas
  - Creating and managing migrations with Alembic
  - Optimizing database queries and performance
  - Implementing database models with SQLModel
  - Troubleshooting database connection issues
---

# Neon PostgreSQL Database Management

## Role
You are a database specialist focused on Neon PostgreSQL, SQLModel ORM, and database design for full-stack applications.

## Neon PostgreSQL Overview

### What is Neon?
- **Serverless PostgreSQL**: Auto-scaling, pay-per-use database
- **Instant Provisioning**: Create databases in seconds
- **Branching**: Git-like database branches for development
- **Auto-suspend**: Automatically pauses when inactive (saves costs)
- **Connection Pooling**: Built-in connection pooling with PgBouncer

### Key Features
- ✅ Fully managed PostgreSQL
- ✅ Serverless architecture (no server management)
- ✅ Automatic backups and point-in-time recovery
- ✅ Database branching for testing
- ✅ Built-in connection pooling
- ✅ Free tier available

## Setup and Configuration

### Creating a Neon Project

**1. Sign up at Neon:**
```
https://neon.tech
```

**2. Create a new project:**
- Project name: `todo-app`
- Region: Choose closest to your users
- PostgreSQL version: 15 or 16

**3. Get connection string:**
```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

### Environment Configuration

**Backend .env file:**
```bash
# .env
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Alternative: Use connection pooling (recommended for serverless)
DATABASE_URL=postgresql://user:password@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require

# Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# API
API_V1_PREFIX=/api/v1
DEBUG=False
```

**Connection String Components:**
```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
           │      │           │         │            │
           │      │           │         │            └─ SSL required
           │      │           │         └─ Database name
           │      │           └─ Neon host (includes region)
           │      └─ Password (from Neon dashboard)
           └─ Username (from Neon dashboard)
```

### Database Connection Setup

**FastAPI Database Configuration:**
```python
# app/database.py
from sqlmodel import Session, create_engine
from app.config import settings

# Create engine with Neon-optimized settings
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before using
    pool_size=5,          # Connection pool size
    max_overflow=10,      # Max connections beyond pool_size
    pool_recycle=3600,    # Recycle connections after 1 hour
    connect_args={
        "sslmode": "require",  # Require SSL for Neon
        "connect_timeout": 10,  # Connection timeout
    }
)

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database (create tables)."""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
```

**Configuration Settings:**
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Auth
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

## Database Schema Design

### Best Practices

**1. Use Proper Data Types:**
```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Unique fields
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)

    # Hashed password (never store plain text)
    hashed_password: str = Field(max_length=255)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Soft delete
    is_active: bool = Field(default=True)
```

**2. Add Indexes for Performance:**
```python
class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key with index
    user_id: int = Field(foreign_key="users.id", index=True)

    # Searchable fields
    title: str = Field(max_length=255, index=True)
    description: Optional[str] = None

    # Status field (frequently filtered)
    completed: bool = Field(default=False, index=True)

    # Timestamps (useful for sorting)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**3. Use Constraints:**
```python
from sqlmodel import Field, SQLModel, CheckConstraint

class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    __table_args__ = (
        CheckConstraint("length(title) >= 1", name="title_not_empty"),
        CheckConstraint("length(title) <= 255", name="title_max_length"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Complete Schema Example

```python
# app/models/user.py
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship
    todos: List["Todo"] = Relationship(back_populates="user")

# app/models/todo.py
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional

class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255, index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False, index=True)
    priority: Optional[int] = Field(default=0, ge=0, le=5)  # 0-5 priority
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="todos")
```

## Database Migrations with Alembic

### Setup Alembic

**1. Install Alembic:**
```bash
pip install alembic
```

**2. Initialize Alembic:**
```bash
cd backend
alembic init alembic
```

**3. Configure Alembic:**
```python
# alembic/env.py
from logging.config import fileConfig
from sqlmodel import SQLModel
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your models
from app.models.user import User
from app.models.todo import Todo
from app.config import settings

# Alembic Config object
config = context.config

# Set database URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**4. Update alembic.ini:**
```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

# Remove or comment out sqlalchemy.url (we set it in env.py)
# sqlalchemy.url = driver://user:pass@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### Creating Migrations

**1. Create initial migration:**
```bash
alembic revision --autogenerate -m "Initial migration"
```

**2. Review generated migration:**
```python
# alembic/versions/xxx_initial_migration.py
"""Initial migration

Revision ID: xxx
Revises:
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers
revision = 'xxx'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create todos table
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todos_user_id'), 'todos', ['user_id'], unique=False)
    op.create_index(op.f('ix_todos_completed'), 'todos', ['completed'], unique=False)
    op.create_index(op.f('ix_todos_created_at'), 'todos', ['created_at'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_todos_created_at'), table_name='todos')
    op.drop_index(op.f('ix_todos_completed'), table_name='todos')
    op.drop_index(op.f('ix_todos_user_id'), table_name='todos')
    op.drop_table('todos')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
```

**3. Apply migration:**
```bash
alembic upgrade head
```

**4. Rollback migration:**
```bash
alembic downgrade -1
```

### Migration Commands

```bash
# Create new migration
alembic revision --autogenerate -m "Add priority field to todos"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --verbose
```

## Database Queries with SQLModel

### Basic CRUD Operations

**Create:**
```python
from sqlmodel import Session
from app.models.todo import Todo

def create_todo(session: Session, todo_data: dict, user_id: int) -> Todo:
    """Create a new todo."""
    todo = Todo(**todo_data, user_id=user_id)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
```

**Read:**
```python
from sqlmodel import Session, select
from app.models.todo import Todo

def get_todos(session: Session, user_id: int) -> list[Todo]:
    """Get all todos for a user."""
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos

def get_todo_by_id(session: Session, todo_id: int, user_id: int) -> Todo | None:
    """Get a specific todo by ID."""
    statement = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == user_id
    )
    todo = session.exec(statement).first()
    return todo
```

**Update:**
```python
from sqlmodel import Session
from app.models.todo import Todo
from datetime import datetime

def update_todo(session: Session, todo: Todo, update_data: dict) -> Todo:
    """Update a todo."""
    for key, value in update_data.items():
        setattr(todo, key, value)

    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
```

**Delete:**
```python
from sqlmodel import Session
from app.models.todo import Todo

def delete_todo(session: Session, todo: Todo) -> None:
    """Delete a todo."""
    session.delete(todo)
    session.commit()
```

### Advanced Queries

**Filtering:**
```python
from sqlmodel import Session, select
from app.models.todo import Todo

def get_completed_todos(session: Session, user_id: int) -> list[Todo]:
    """Get completed todos for a user."""
    statement = select(Todo).where(
        Todo.user_id == user_id,
        Todo.completed == True
    )
    return session.exec(statement).all()

def get_todos_by_priority(session: Session, user_id: int, min_priority: int) -> list[Todo]:
    """Get todos with priority >= min_priority."""
    statement = select(Todo).where(
        Todo.user_id == user_id,
        Todo.priority >= min_priority
    )
    return session.exec(statement).all()
```

**Sorting:**
```python
from sqlmodel import Session, select
from app.models.todo import Todo

def get_todos_sorted(session: Session, user_id: int) -> list[Todo]:
    """Get todos sorted by created_at descending."""
    statement = (
        select(Todo)
        .where(Todo.user_id == user_id)
        .order_by(Todo.created_at.desc())
    )
    return session.exec(statement).all()
```

**Pagination:**
```python
from sqlmodel import Session, select, func
from app.models.todo import Todo

def get_todos_paginated(
    session: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10
) -> tuple[list[Todo], int]:
    """Get paginated todos with total count."""
    # Get total count
    count_statement = select(func.count()).select_from(Todo).where(Todo.user_id == user_id)
    total = session.exec(count_statement).one()

    # Get paginated results
    statement = (
        select(Todo)
        .where(Todo.user_id == user_id)
        .order_by(Todo.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    todos = session.exec(statement).all()

    return todos, total
```

**Search:**
```python
from sqlmodel import Session, select
from app.models.todo import Todo

def search_todos(session: Session, user_id: int, query: str) -> list[Todo]:
    """Search todos by title or description."""
    statement = select(Todo).where(
        Todo.user_id == user_id,
        (Todo.title.ilike(f"%{query}%")) | (Todo.description.ilike(f"%{query}%"))
    )
    return session.exec(statement).all()
```

## Performance Optimization

### Indexing Strategy

**1. Index Foreign Keys:**
```python
user_id: int = Field(foreign_key="users.id", index=True)
```

**2. Index Frequently Filtered Fields:**
```python
completed: bool = Field(default=False, index=True)
created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

**3. Composite Indexes (via Alembic):**
```python
# In migration file
op.create_index(
    'ix_todos_user_completed',
    'todos',
    ['user_id', 'completed']
)
```

### Query Optimization

**1. Use Select Instead of Query:**
```python
# ✅ GOOD - Modern SQLModel style
statement = select(Todo).where(Todo.user_id == user_id)
todos = session.exec(statement).all()

# ❌ OLD - Legacy SQLAlchemy style
todos = session.query(Todo).filter(Todo.user_id == user_id).all()
```

**2. Limit Selected Columns:**
```python
# Only select needed columns
statement = select(Todo.id, Todo.title).where(Todo.user_id == user_id)
results = session.exec(statement).all()
```

**3. Use Eager Loading for Relationships:**
```python
from sqlmodel import select
from sqlalchemy.orm import selectinload

# Load todos with user relationship
statement = select(Todo).options(selectinload(Todo.user))
todos = session.exec(statement).all()
```

**4. Batch Operations:**
```python
# Bulk insert
todos = [Todo(title=f"Todo {i}", user_id=1) for i in range(100)]
session.add_all(todos)
session.commit()
```

### Connection Pooling

**Optimize for Neon:**
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,           # Number of persistent connections
    max_overflow=10,       # Additional connections when pool is full
    pool_timeout=30,       # Wait time for available connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    pool_pre_ping=True,    # Verify connection before using
)
```

## Troubleshooting

### Common Issues

**1. Connection Timeout:**
```
Error: could not connect to server: Connection timed out
```

**Solution:**
```python
# Increase timeout in connection string
DATABASE_URL=postgresql://...?connect_timeout=10

# Or in engine config
connect_args={"connect_timeout": 10}
```

**2. SSL Required:**
```
Error: SSL connection is required
```

**Solution:**
```python
# Add sslmode=require to connection string
DATABASE_URL=postgresql://...?sslmode=require

# Or in engine config
connect_args={"sslmode": "require"}
```

**3. Too Many Connections:**
```
Error: remaining connection slots are reserved
```

**Solution:**
```python
# Use Neon's pooled connection string
DATABASE_URL=postgresql://...-pooler.neon.tech/...

# Or reduce pool size
engine = create_engine(DATABASE_URL, pool_size=3, max_overflow=5)
```

**4. Migration Conflicts:**
```
Error: Target database is not up to date
```

**Solution:**
```bash
# Check current revision
alembic current

# Show history
alembic history

# Upgrade to head
alembic upgrade head

# If conflicts, resolve manually or stamp
alembic stamp head
```

### Debugging Queries

**Enable SQL Logging:**
```python
# In database.py
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Log all SQL queries
)
```

**Use EXPLAIN:**
```python
from sqlalchemy import text

# Analyze query performance
statement = text("EXPLAIN ANALYZE SELECT * FROM todos WHERE user_id = :user_id")
result = session.exec(statement, {"user_id": 1})
print(result.all())
```

## Best Practices

### ✅ DO:
- Use connection pooling
- Add indexes on foreign keys and frequently queried fields
- Use migrations for schema changes
- Implement proper error handling
- Use transactions for multi-step operations
- Close sessions properly (use context managers)
- Use environment variables for credentials
- Implement database backups
- Monitor query performance
- Use prepared statements (SQLModel does this automatically)

### ❌ DON'T:
- Hardcode database credentials
- Skip migrations
- Use raw SQL without parameterization
- Leave connections open
- Store sensitive data unencrypted
- Ignore database errors
- Use SELECT * in production
- Create indexes on every column
- Skip database backups
- Ignore slow query warnings

## Summary

Effective database management requires:
1. **Proper Setup**: Neon configuration with connection pooling
2. **Schema Design**: Well-designed models with proper constraints
3. **Migrations**: Alembic for version-controlled schema changes
4. **Optimized Queries**: Efficient SQLModel queries with indexes
5. **Error Handling**: Robust error handling and logging
6. **Monitoring**: Track performance and optimize as needed

Follow this guide to build a robust, performant database layer for your application.
