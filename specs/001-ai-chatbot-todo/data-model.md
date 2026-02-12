# Data Model: Todo AI Chatbot with Natural Language Interface

## Overview
This document defines the data models for the Todo AI Chatbot system, including entities, their fields, relationships, and validation rules.

## Entity: Task

**Description**: Represents a user's todo item

**Fields**:
- `id` (UUID/String): Unique identifier for the task
- `user_id` (String): Reference to the user who owns this task
- `description` (String): The text description of the task
- `completed` (Boolean): Whether the task has been completed
- `created_at` (DateTime): Timestamp when the task was created
- `updated_at` (DateTime): Timestamp when the task was last updated
- `due_date` (DateTime, Optional): When the task is due (if applicable)

**Validation Rules**:
- `description` must be between 1 and 500 characters
- `user_id` must reference a valid user
- `completed` defaults to false

**State Transitions**:
- `pending` → `completed` when task is marked as complete
- `completed` → `pending` when task is marked as incomplete

## Entity: Conversation

**Description**: Represents a user's conversation session with the AI chatbot

**Fields**:
- `id` (UUID/String): Unique identifier for the conversation
- `user_id` (String): Reference to the user who owns this conversation
- `created_at` (DateTime): Timestamp when the conversation was started
- `updated_at` (DateTime): Timestamp when the conversation was last updated
- `title` (String, Optional): Auto-generated title based on first message or topic

**Validation Rules**:
- `user_id` must reference a valid user
- `title` must be between 1 and 100 characters if provided

## Entity: Message

**Description**: Represents individual messages within a conversation

**Fields**:
- `id` (UUID/String): Unique identifier for the message
- `conversation_id` (String): Reference to the conversation this message belongs to
- `sender_type` (Enum: 'user' | 'assistant'): Who sent the message
- `content` (String): The text content of the message
- `timestamp` (DateTime): When the message was sent
- `metadata` (JSON, Optional): Additional data about the message (tool calls, etc.)

**Validation Rules**:
- `conversation_id` must reference a valid conversation
- `sender_type` must be either 'user' or 'assistant'
- `content` must be between 1 and 10000 characters
- `timestamp` defaults to current time

## Relationships

```
User (1) → (Many) Task
User (1) → (Many) Conversation  
Conversation (1) → (Many) Message
```

## Indexes

**Task**:
- Index on `(user_id, created_at)` for efficient user task retrieval
- Index on `(user_id, completed)` for filtering completed/incomplete tasks

**Conversation**:
- Index on `user_id` for efficient user conversation retrieval
- Index on `updated_at` for ordering conversations by recency

**Message**:
- Index on `conversation_id` for efficient conversation message retrieval
- Index on `timestamp` for chronological ordering