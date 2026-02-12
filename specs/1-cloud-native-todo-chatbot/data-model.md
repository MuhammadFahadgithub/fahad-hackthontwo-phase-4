# Todo Chatbot Data Model

## Overview
This document describes the data structures and relationships for the Todo Chatbot application.

## Entity Relationship Diagram (Conceptual)

```
Users (1) ----< Todos (>1)
Users (1) ----< Conversations (>1)
Conversations (1) ----< Messages (>1)
```

## Entity Definitions

### User
Represents a registered user of the Todo Chatbot application.

**Attributes:**
- id: UUID (Primary Key)
- email: String (unique, required)
- name: String (optional)
- created_at: DateTime
- updated_at: DateTime

### Todo
Represents a single task/todo item owned by a user.

**Attributes:**
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User, required)
- title: String (required, max 200 characters)
- description: Text (optional)
- completed: Boolean (default: false)
- due_date: DateTime (optional)
- priority: String (enum: low, medium, high; default: medium)
- created_at: DateTime
- updated_at: DateTime

### Conversation
Represents a chat session between a user and the Todo Chatbot.

**Attributes:**
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User, required)
- title: String (optional, auto-generated from first message)
- created_at: DateTime
- updated_at: DateTime

### Message
Represents a single message in a conversation.

**Attributes:**
- id: UUID (Primary Key)
- conversation_id: UUID (Foreign Key to Conversation, required)
- sender: String (enum: user, bot; required)
- content: Text (required)
- created_at: DateTime

## API Endpoints

### Todo Management
- GET /api/v1/todos - Retrieve all todos for the authenticated user
- POST /api/v1/todos - Create a new todo
- GET /api/v1/todos/{id} - Retrieve a specific todo
- PUT /api/v1/todos/{id} - Update a specific todo
- DELETE /api/v1/todos/{id} - Delete a specific todo

### Chat Interface
- POST /api/v1/chat/message - Send a message to the chatbot

### User Information
- GET /api/v1/users/me - Retrieve current user information

## Database Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    due_date TIMESTAMP,
    priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender VARCHAR(20) NOT NULL CHECK (sender IN ('user', 'bot')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_completed ON todos(completed);
CREATE INDEX idx_todos_due_date ON todos(due_date);
CREATE INDEX idx_todos_priority ON todos(priority);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## Sample Data

### Sample Todo
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "987e6543-e21b-43d5-a456-426614174999",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits",
  "completed": false,
  "due_date": "2026-02-15T10:00:00Z",
  "priority": "medium",
  "created_at": "2026-02-12T10:00:00Z",
  "updated_at": "2026-02-12T10:00:00Z"
}
```

### Sample Chat Message
```json
{
  "id": "111e4567-e89b-12d3-a456-426614174111",
  "conversation_id": "222e4567-e89b-12d3-a456-426614174222",
  "sender": "user",
  "content": "Add a todo: Buy groceries",
  "created_at": "2026-02-12T10:00:00Z"
}
```