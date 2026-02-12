---
name: fullstack-todo-spec-driven
description: |
  Guides the implementation of a spec-driven, authenticated full-stack Todo
  web application using Next.js, FastAPI, SQLModel, Neon PostgreSQL, and
  Better Auth with JWT.

proficiency_level: "B2"
category: "Full-Stack Development"
use_when: |
  - Implementing a Todo application from console to web
  - Building REST APIs with FastAPI and SQLModel
  - Integrating Better Auth JWT with a Python backend
  - Following Spec-Kit and spec-driven development workflows
  - Coordinating frontend and backend development
  - Implementing end-to-end authentication flows
---

# Full-Stack Todo Application - Spec-Driven Development

## Role
You are an expert full-stack developer orchestrating the development of a complete Todo application using modern web technologies and spec-driven development practices.

## Project Overview

### Technology Stack
**Frontend:**
- Next.js 14+ (App Router)
- TypeScript
- Better Auth (JWT-based authentication)
- Tailwind CSS
- React 18+

**Backend:**
- FastAPI (Python 3.11+)
- SQLModel (ORM)
- Neon PostgreSQL (serverless)
- JWT verification
- Pydantic v2

**Development Approach:**
- Spec-Driven Development (SDD)
- Test-Driven Development (TDD)
- API-first design
- Ownership-based authorization

## Core Principles

### 1. Spec-Driven Development Workflow
```
Requirements → Spec → Plan → Tasks → Implementation → Testing → Deployment
```

**Workflow Steps:**
1. **Specification Phase** (`/sp.specify`)
   - Define feature requirements
   - Document user stories
   - Identify acceptance criteria
   - Create spec.md

2. **Planning Phase** (`/sp.plan`)
   - Design architecture
   - Define API contracts
   - Identify dependencies
   - Make architectural decisions
   - Create plan.md

3. **Task Breakdown** (`/sp.tasks`)
   - Break down into testable tasks
   - Define task dependencies
   - Create tasks.md

4. **Implementation** (`/sp.implement`)
   - Execute tasks in order
   - Follow TDD practices
   - Implement frontend and backend

5. **Testing & Validation**
   - Unit tests
   - Integration tests
   - End-to-end tests

6. **Documentation** (`/sp.phr`, `/sp.adr`)
   - Record prompt history
   - Document architectural decisions

### 2. Authentication Flow Architecture

**Complete JWT Flow:**
```
1. User signs up/logs in via Next.js frontend
2. Better Auth generates JWT token
3. Frontend stores token (localStorage/cookies)
4. Frontend sends token in Authorization header
5. FastAPI backend verifies JWT signature
6. Backend extracts user_id from token payload
7. Backend filters all queries by user_id
8. Backend returns user-specific data
```

**Security Guarantees:**
- ✅ All API endpoints require valid JWT (except public ones)
- ✅ User identity comes from JWT, never from client input
- ✅ All database queries filter by authenticated user_id
- ✅ Cross-user data access is impossible
- ✅ Token verification happens on every request

### 3. API Contract Design

**Standard Todo API Endpoints:**
```
POST   /api/v1/todos          - Create todo (requires auth)
GET    /api/v1/todos          - List user's todos (requires auth)
GET    /api/v1/todos/{id}     - Get specific todo (requires auth + ownership)
PUT    /api/v1/todos/{id}     - Update todo (requires auth + ownership)
DELETE /api/v1/todos/{id}     - Delete todo (requires auth + ownership)
```

**Request/Response Contracts:**
```typescript
// Create Todo Request
{
  "title": "string (required, max 255)",
  "description": "string (optional)",
  "completed": "boolean (optional, default: false)"
}

// Todo Response
{
  "id": "number",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "user_id": "number",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}

// Error Response
{
  "detail": "string (error message)"
}
```

**HTTP Status Codes:**
- 200: Success (GET, PUT)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation error)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (ownership violation)
- 404: Not Found (resource doesn't exist)
- 422: Unprocessable Entity (Pydantic validation)
- 500: Internal Server Error

## Development Workflow

### Phase 1: Specification
**Command:** `/sp.specify`

**Deliverable:** `specs/<feature>/spec.md`

**Contents:**
- Feature description
- User stories
- Acceptance criteria
- Non-functional requirements
- Security requirements
- API contracts (preliminary)

**Example Spec Structure:**
```markdown
# Todo Management Feature

## Overview
Users can create, read, update, and delete their personal todo items.

## User Stories
- As a user, I want to create todos so I can track my tasks
- As a user, I want to view all my todos so I can see what needs to be done
- As a user, I want to mark todos as complete so I can track progress
- As a user, I want to delete todos so I can remove completed tasks

## Acceptance Criteria
- Users can only see their own todos
- Todos persist across sessions
- Todos have title (required), description (optional), completed status
- All operations require authentication

## Security Requirements
- JWT authentication required for all endpoints
- Ownership verification on all operations
- No cross-user data access
```

### Phase 2: Planning
**Command:** `/sp.plan`

**Deliverable:** `specs/<feature>/plan.md`

**Contents:**
- Architecture decisions
- Database schema
- API endpoint specifications
- Frontend component structure
- Authentication integration plan
- Testing strategy

**Example Plan Structure:**
```markdown
# Todo Feature Implementation Plan

## Architecture Decisions

### Database Schema
- Table: todos
- Columns: id, user_id (FK), title, description, completed, created_at, updated_at
- Indexes: user_id, created_at

### API Design
- RESTful endpoints following standard conventions
- JWT verification middleware
- Ownership-based authorization

### Frontend Architecture
- Server Components for initial data loading
- Client Components for interactivity
- Custom hooks for API calls
- Context for auth state

## Implementation Order
1. Backend database models
2. Backend API endpoints
3. Backend tests
4. Frontend API client
5. Frontend components
6. Frontend tests
7. Integration tests
```

### Phase 3: Task Breakdown
**Command:** `/sp.tasks`

**Deliverable:** `specs/<feature>/tasks.md`

**Contents:**
- Ordered list of implementation tasks
- Task dependencies
- Test cases for each task
- Acceptance criteria per task

**Example Tasks Structure:**
```markdown
# Todo Feature Tasks

## Backend Tasks

### Task 1: Create Todo Database Model
**Dependencies:** None
**Files:** `backend/app/models/todo.py`
**Test Cases:**
- Model can be instantiated with required fields
- Timestamps are auto-generated
- Foreign key to users table works

### Task 2: Implement Create Todo Endpoint
**Dependencies:** Task 1
**Files:** `backend/app/api/v1/todos.py`
**Test Cases:**
- Authenticated user can create todo
- Todo is associated with correct user_id
- Unauthenticated request returns 401
- Invalid data returns 422

## Frontend Tasks

### Task 5: Create Todo API Client
**Dependencies:** Task 2
**Files:** `frontend/lib/api/todos.ts`
**Test Cases:**
- API client sends JWT token
- API client handles errors
- API client returns typed responses
```

### Phase 4: Implementation
**Command:** `/sp.implement`

**Process:**
1. Execute tasks in dependency order
2. Follow TDD: Write test → Implement → Verify
3. Commit after each task completion
4. Run integration tests after major milestones

**Backend Implementation Checklist:**
- [ ] Database models with SQLModel
- [ ] JWT verification dependency
- [ ] API endpoints with ownership checks
- [ ] Pydantic schemas for validation
- [ ] Error handling
- [ ] Unit tests for each endpoint
- [ ] Integration tests

**Frontend Implementation Checklist:**
- [ ] TypeScript types for API responses
- [ ] API client functions with JWT
- [ ] React components (Server/Client)
- [ ] Authentication context/hooks
- [ ] Loading and error states
- [ ] Form validation
- [ ] Component tests

### Phase 5: Testing Strategy

**Backend Testing:**
```python
# Test authentication
def test_create_todo_requires_auth():
    response = client.post("/api/v1/todos/", json={"title": "Test"})
    assert response.status_code == 401

# Test ownership
def test_user_cannot_access_other_user_todo():
    # Create todo as user 1
    # Try to access as user 2
    # Assert 403 Forbidden

# Test CRUD operations
def test_complete_todo_lifecycle():
    # Create
    # Read
    # Update
    # Delete
```

**Frontend Testing:**
```typescript
// Test component rendering
test('TodoList renders todos', async () => {
  render(<TodoList />);
  await waitFor(() => {
    expect(screen.getByText('Test Todo')).toBeInTheDocument();
  });
});

// Test API integration
test('TodoList fetches from API', async () => {
  const mockFetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => [{ id: 1, title: 'Test' }]
  });
  global.fetch = mockFetch;

  render(<TodoList />);

  expect(mockFetch).toHaveBeenCalledWith(
    expect.stringContaining('/api/todos'),
    expect.objectContaining({
      headers: expect.objectContaining({
        'Authorization': expect.stringContaining('Bearer')
      })
    })
  );
});
```

**Integration Testing:**
```bash
# End-to-end flow
1. Start backend server
2. Start frontend dev server
3. Run Playwright/Cypress tests
   - Sign up new user
   - Create todo
   - Verify todo appears
   - Update todo
   - Delete todo
   - Verify isolation (other users can't see)
```

## Common Patterns

### Backend: Protected Endpoint Pattern
```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.database import get_session

router = APIRouter()

@router.get("/todos/")
async def get_todos(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Get all todos for authenticated user."""
    statement = select(Todo).where(Todo.user_id == current_user["id"])
    todos = session.exec(statement).all()
    return todos
```

### Frontend: API Client Pattern
```typescript
// lib/api/todos.ts
export async function getTodos(token: string): Promise<Todo[]> {
  const response = await fetch(`${API_URL}/api/v1/todos`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Unauthorized');
    }
    throw new Error('Failed to fetch todos');
  }

  return response.json();
}
```

### Frontend: Component with Auth Pattern
```typescript
'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth/useAuth';
import { getTodos } from '@/lib/api/todos';

export function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const { token, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) return;

    async function fetchTodos() {
      try {
        const data = await getTodos(token);
        setTodos(data);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchTodos();
  }, [token, isAuthenticated]);

  if (!isAuthenticated) return <div>Please log in</div>;
  if (loading) return <div>Loading...</div>;

  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
}
```

## Security Checklist

### Backend Security
- [ ] JWT verification on all protected endpoints
- [ ] Ownership checks before update/delete operations
- [ ] User ID extracted from JWT, never from request body
- [ ] All queries filtered by authenticated user_id
- [ ] Proper HTTP status codes (401, 403, 404)
- [ ] Input validation with Pydantic
- [ ] CORS configured for frontend origin only
- [ ] Environment variables for secrets
- [ ] No sensitive data in logs
- [ ] Rate limiting on endpoints

### Frontend Security
- [ ] JWT token stored securely (httpOnly cookies preferred)
- [ ] Token sent in Authorization header
- [ ] Handle 401 responses (redirect to login)
- [ ] Handle 403 responses (show error)
- [ ] Input sanitization
- [ ] No sensitive data in localStorage
- [ ] HTTPS in production
- [ ] CSP headers configured

## Documentation Requirements

### Prompt History Records (PHR)
**When to create:**
- After specification phase
- After planning phase
- After task breakdown
- After implementation milestones
- After debugging sessions

**Command:** `/sp.phr`

**Location:** `history/prompts/<feature-name>/`

### Architectural Decision Records (ADR)
**When to create:**
- Choosing authentication method
- Selecting database schema
- API design decisions
- Frontend architecture choices

**Command:** `/sp.adr <decision-title>`

**Location:** `history/adr/`

## Common Issues & Solutions

### Issue: CORS Errors
**Symptom:** Frontend can't call backend API
**Solution:**
```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: JWT Verification Fails
**Symptom:** 401 errors on all requests
**Solution:**
- Verify BETTER_AUTH_SECRET matches between frontend and backend
- Check JWT token format (should be `Bearer <token>`)
- Verify token hasn't expired
- Check JWT algorithm (usually HS256)

### Issue: User Can See Other Users' Data
**Symptom:** Cross-user data leakage
**Solution:**
- Always filter queries by `user_id == current_user["id"]`
- Add ownership checks before update/delete
- Never trust client-provided user_id
- Write tests for cross-user isolation

### Issue: Database Connection Errors
**Symptom:** Can't connect to Neon database
**Solution:**
- Verify DATABASE_URL in .env
- Check Neon project is active
- Verify connection string format
- Test connection with psql or database client

## Success Criteria

### Feature Complete When:
- [ ] All spec requirements implemented
- [ ] All tasks completed and tested
- [ ] Backend tests passing (>80% coverage)
- [ ] Frontend tests passing
- [ ] Integration tests passing
- [ ] Authentication flow works end-to-end
- [ ] Cross-user isolation verified
- [ ] API documentation complete
- [ ] PHRs created for major milestones
- [ ] ADRs created for significant decisions
- [ ] Code reviewed and committed
- [ ] Feature deployed and verified

### Quality Gates:
- [ ] No TypeScript errors
- [ ] No Python type errors (mypy)
- [ ] No linting errors (ESLint, Ruff)
- [ ] All tests passing
- [ ] No console errors in browser
- [ ] No security vulnerabilities
- [ ] Performance acceptable (< 200ms API response)
- [ ] Accessibility standards met (WCAG 2.1 AA)

## Next Steps After Implementation

1. **Code Review**
   - Review backend code for security issues
   - Review frontend code for best practices
   - Check test coverage

2. **Documentation**
   - Update API documentation
   - Create user documentation
   - Document deployment process

3. **Deployment**
   - Deploy backend to production
   - Deploy frontend to production
   - Verify production environment

4. **Monitoring**
   - Set up error tracking (Sentry)
   - Set up performance monitoring
   - Set up logging

5. **Iteration**
   - Gather user feedback
   - Plan next features
   - Refine based on usage

## Resources

### Backend Resources
- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLModel Documentation: https://sqlmodel.tiangolo.com
- Neon Documentation: https://neon.tech/docs

### Frontend Resources
- Next.js Documentation: https://nextjs.org/docs
- Better Auth Documentation: https://better-auth.com
- React Documentation: https://react.dev

### Spec-Driven Development
- SpecKit Documentation: `.specify/` directory
- Project Constitution: `.specify/memory/constitution.md`
- Templates: `.specify/templates/`

## Summary

This skill guides you through building a complete, production-ready Todo application using:
- **Spec-Driven Development** for structured implementation
- **JWT Authentication** for secure user sessions
- **Ownership-Based Authorization** for data isolation
- **Modern Tech Stack** (Next.js + FastAPI)
- **Comprehensive Testing** at all levels
- **Documentation** for maintainability

Follow the workflow: Specify → Plan → Tasks → Implement → Test → Document → Deploy
