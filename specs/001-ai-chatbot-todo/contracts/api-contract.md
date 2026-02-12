# API Contract: Todo AI Chatbot with Natural Language Interface

## Overview
This document defines the API contracts for the Todo AI Chatbot system, specifying endpoints, request/response formats, and error handling.

## Base URL
`https://api.todo-ai-chatbot.com/v1` (production)
`http://localhost:8000/api/v1` (development)

## Authentication
All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Endpoints

### Chat Endpoint
**POST** `/chat`

Process natural language input and return AI-generated response with task operations.

#### Request
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-existing-conversation-id"
}
```

#### Response (Success)
```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "conversation_id": "new-or-existing-conversation-id",
  "task_operations": [
    {
      "operation": "add_task",
      "task_id": "generated-task-id",
      "description": "buy groceries",
      "status": "success"
    }
  ],
  "timestamp": "2026-02-08T10:00:00Z"
}
```

#### Response (Error)
```json
{
  "error": "Invalid request format",
  "message": "Detailed error message",
  "timestamp": "2026-02-08T10:00:00Z"
}
```

### Task Management Endpoints
**GET** `/tasks`

Retrieve all tasks for the authenticated user.

#### Request
```
Headers:
Authorization: Bearer <jwt-token>
```

#### Response (Success)
```json
{
  "tasks": [
    {
      "id": "task-id-1",
      "description": "Buy groceries",
      "completed": false,
      "created_at": "2026-02-08T09:00:00Z",
      "updated_at": "2026-02-08T09:00:00Z"
    },
    {
      "id": "task-id-2", 
      "description": "Walk the dog",
      "completed": true,
      "created_at": "2026-02-08T08:00:00Z",
      "updated_at": "2026-02-08T08:30:00Z"
    }
  ]
}
```

**POST** `/tasks`

Create a new task directly (bypassing AI interpretation).

#### Request
```json
{
  "description": "New task description"
}
```

#### Response (Success)
```json
{
  "task": {
    "id": "new-task-id",
    "description": "New task description",
    "completed": false,
    "created_at": "2026-02-08T10:00:00Z",
    "updated_at": "2026-02-08T10:00:00Z"
  }
}
```

**PUT** `/tasks/{task_id}`

Update an existing task.

#### Request
```json
{
  "description": "Updated task description",
  "completed": true
}
```

#### Response (Success)
```json
{
  "task": {
    "id": "existing-task-id",
    "description": "Updated task description",
    "completed": true,
    "created_at": "2026-02-08T09:00:00Z",
    "updated_at": "2026-02-08T10:00:00Z"
  }
}
```

**DELETE** `/tasks/{task_id}`

Delete a task.

#### Response (Success)
```json
{
  "message": "Task deleted successfully"
}
```

**POST** `/tasks/{task_id}/complete`

Mark a task as complete.

#### Response (Success)
```json
{
  "task": {
    "id": "existing-task-id",
    "description": "Task description",
    "completed": true,
    "created_at": "2026-02-08T09:00:00Z",
    "updated_at": "2026-02-08T10:00:00Z"
  }
}

### Conversation Endpoints

**GET** `/conversations`

Retrieve all conversations for the authenticated user.

#### Response (Success)
```json
{
  "conversations": [
    {
      "id": "conv-id-1",
      "title": "Grocery shopping",
      "created_at": "2026-02-08T09:00:00Z",
      "updated_at": "2026-02-08T10:00:00Z"
    }
  ]
}
```

**GET** `/conversations/{conversation_id}/messages`

Retrieve messages for a specific conversation.

#### Response (Success)
```json
{
  "messages": [
    {
      "id": "msg-id-1",
      "sender_type": "user",
      "content": "Add a task to buy groceries",
      "timestamp": "2026-02-08T09:00:00Z"
    },
    {
      "id": "msg-id-2", 
      "sender_type": "assistant",
      "content": "I've added the task 'buy groceries' to your list.",
      "timestamp": "2026-02-08T09:00:01Z"
    }
  ]
}
```

## Common Error Responses

### 400 Bad Request
```json
{
  "error": "validation_error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "description",
      "message": "Field is required"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Authentication token is invalid or missing"
}
```

### 403 Forbidden
```json
{
  "error": "forbidden", 
  "message": "Access denied - insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "Requested resource does not exist"
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_server_error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting
All endpoints are subject to rate limiting:
- 100 requests per minute per IP
- 1000 requests per hour per authenticated user