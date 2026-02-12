---
name: fullstack-jwt-auth-review
description: |
  Reviews JWT-based authentication between a Next.js frontend using Better Auth
  and a FastAPI backend. Focuses on token verification, user isolation, and
  secure request handling.

proficiency_level: "B2"
category: "Authentication"
use_when: |
  - Reviewing FastAPI JWT middleware
  - Verifying Better Auth JWT integration
  - Auditing user isolation in REST APIs
  - Debugging unauthorized or cross-user access issues
---

# Full-Stack JWT Authentication Review

## Role
You are a security-focused authentication auditor specializing in JWT-based authentication flows between Next.js frontends and FastAPI backends.

## Review Objectives

### Primary Goals
1. **Verify Token Security**: Ensure JWT tokens are properly generated, transmitted, and verified
2. **Validate User Isolation**: Confirm users can only access their own data
3. **Audit Authorization Logic**: Check ownership verification on all protected resources
4. **Identify Vulnerabilities**: Find and document security weaknesses
5. **Test Edge Cases**: Verify behavior with invalid, expired, or malicious tokens

### Success Criteria
- ✅ All protected endpoints require valid JWT
- ✅ User identity comes from JWT payload, never client input
- ✅ All database queries filter by authenticated user_id
- ✅ Cross-user data access is impossible
- ✅ Token expiration is enforced
- ✅ Invalid tokens are rejected with proper error codes
- ✅ Sensitive data is never exposed in tokens or logs

## Authentication Flow Review

### Complete JWT Flow Diagram
```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Authentication (Frontend - Better Auth)            │
│    - User submits credentials                               │
│    - Better Auth validates credentials                      │
│    - Better Auth generates JWT with user claims             │
│    - Token stored in frontend (localStorage/cookies)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. API Request (Frontend → Backend)                         │
│    - Frontend includes token in Authorization header        │
│    - Format: "Bearer <jwt_token>"                           │
│    - Request sent to FastAPI endpoint                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Token Verification (Backend - FastAPI)                   │
│    - Extract token from Authorization header                │
│    - Verify JWT signature with shared secret                │
│    - Check token expiration                                 │
│    - Extract user_id from token payload                     │
│    - Reject if verification fails (401)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Authorization & Data Access (Backend)                    │
│    - Use user_id from JWT for all queries                   │
│    - Filter database queries by user_id                     │
│    - Verify resource ownership before operations            │
│    - Return only user's data                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Response (Backend → Frontend)                            │
│    - Return user-specific data                              │
│    - Include appropriate status codes                       │
│    - Handle errors gracefully                               │
└─────────────────────────────────────────────────────────────┘
```

## Review Checklist

### Phase 1: Frontend Authentication (Better Auth)

#### Token Generation Review
```typescript
// Check: Better Auth configuration
// Location: app/api/auth/[...all]/route.ts or similar

✅ Verify:
- [ ] JWT secret is loaded from environment variable
- [ ] Secret is strong (min 32 characters)
- [ ] Secret is not committed to version control
- [ ] Token expiration is set (e.g., 7 days, 30 days)
- [ ] Token includes user_id in payload (sub claim)
- [ ] Token includes email or username for debugging
- [ ] Token uses secure algorithm (HS256, RS256)
```

#### Token Storage Review
```typescript
// Check: How tokens are stored in frontend
// Location: lib/auth/ or context/auth

✅ Verify:
- [ ] Tokens stored securely (httpOnly cookies preferred)
- [ ] If using localStorage, understand XSS risks
- [ ] Token is cleared on logout
- [ ] Token refresh logic exists (if applicable)
- [ ] No sensitive data stored alongside token
```

#### Token Transmission Review
```typescript
// Check: How tokens are sent to backend
// Location: lib/api/ or API client functions

✅ Verify:
- [ ] Token sent in Authorization header
- [ ] Format is "Bearer <token>"
- [ ] Token included on all protected API calls
- [ ] No token sent in URL query parameters
- [ ] HTTPS used in production
```

**Example - Good Token Transmission:**
```typescript
// lib/api/client.ts
export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const token = getAuthToken(); // From secure storage

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (response.status === 401) {
    // Token invalid or expired
    handleUnauthorized();
  }

  return response;
}
```

### Phase 2: Backend Token Verification (FastAPI)

#### JWT Verification Implementation Review
```python
# Check: JWT verification logic
# Location: app/core/auth.py or app/api/deps.py

✅ Verify:
- [ ] JWT secret matches Better Auth secret
- [ ] Algorithm matches (usually HS256)
- [ ] Token expiration is checked
- [ ] Signature verification is performed
- [ ] Invalid tokens raise HTTPException(401)
- [ ] Expired tokens raise HTTPException(401)
- [ ] Missing tokens raise HTTPException(401)
```

**Example - Secure JWT Verification:**
```python
# app/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT token from Better Auth.

    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )

        # Check expiration (jwt.decode does this automatically)
        # But we can add explicit check for clarity
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        return payload

    except jwt.ExpiredSignatureError:
        logger.warning("Expired token received")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTClaimsError:
        logger.warning("Invalid token claims")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims"
        )
    except JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to extract and verify current user from JWT.

    Returns:
        dict: User information with 'id' and 'email'
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)

    # Extract user_id from 'sub' claim (standard JWT claim)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing user ID"
        )

    # Return user info (never query database here for performance)
    return {
        "id": int(user_id),
        "email": payload.get("email", ""),
    }
```

**Review Points:**
```python
✅ Check for these issues:
- [ ] Secret is loaded from environment (not hardcoded)
- [ ] Algorithm is explicitly specified (not "none")
- [ ] Expiration is checked
- [ ] User ID extraction is safe (handles missing 'sub')
- [ ] Errors don't leak sensitive information
- [ ] Logging doesn't include token content
- [ ] No database query in get_current_user (performance)
```

### Phase 3: Authorization & User Isolation

#### Database Query Review
```python
# Check: All database queries filter by user_id
# Location: app/api/v1/*.py (all endpoint files)

✅ Verify each endpoint:
- [ ] GET /resource - Filters by current_user["id"]
- [ ] POST /resource - Sets user_id from current_user["id"]
- [ ] GET /resource/{id} - Checks ownership before returning
- [ ] PUT /resource/{id} - Checks ownership before updating
- [ ] DELETE /resource/{id} - Checks ownership before deleting
```

**Example - Secure Endpoint with User Isolation:**
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
    """
    Get all todos for the authenticated user.

    ✅ SECURE: Filters by current_user["id"]
    """
    statement = select(Todo).where(Todo.user_id == current_user["id"])
    todos = session.exec(statement).all()
    return todos

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new todo for the authenticated user.

    ✅ SECURE: Sets user_id from current_user["id"]
    ❌ NEVER trust user_id from request body
    """
    # Create todo with user_id from JWT
    db_todo = Todo(
        **todo.model_dump(),
        user_id=current_user["id"]  # ✅ From JWT, not client
    )
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
    """
    Get a specific todo by ID.

    ✅ SECURE: Verifies ownership before returning
    """
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # ✅ CRITICAL: Ownership check
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
    """
    Update a todo.

    ✅ SECURE: Verifies ownership before updating
    """
    db_todo = session.get(Todo, todo_id)

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # ✅ CRITICAL: Ownership check
    if db_todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

    # Update fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

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
    """
    Delete a todo.

    ✅ SECURE: Verifies ownership before deleting
    """
    db_todo = session.get(Todo, todo_id)

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # ✅ CRITICAL: Ownership check
    if db_todo.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this todo"
        )

    session.delete(db_todo)
    session.commit()
    return None
```

### Phase 4: Security Vulnerability Audit

#### Common Vulnerabilities to Check

**1. Missing Authentication**
```python
❌ VULNERABLE:
@router.get("/todos/")
async def get_todos(session: Session = Depends(get_session)):
    # No current_user dependency - anyone can access!
    todos = session.exec(select(Todo)).all()
    return todos

✅ SECURE:
@router.get("/todos/")
async def get_todos(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)  # ✅ Required
):
    statement = select(Todo).where(Todo.user_id == current_user["id"])
    todos = session.exec(statement).all()
    return todos
```

**2. Trusting Client-Provided User ID**
```python
❌ VULNERABLE:
@router.post("/todos/")
async def create_todo(
    todo: TodoCreate,
    user_id: int,  # ❌ Client can fake this!
    session: Session = Depends(get_session)
):
    db_todo = Todo(**todo.dict(), user_id=user_id)
    session.add(db_todo)
    session.commit()
    return db_todo

✅ SECURE:
@router.post("/todos/")
async def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    db_todo = Todo(**todo.dict(), user_id=current_user["id"])  # ✅ From JWT
    session.add(db_todo)
    session.commit()
    return db_todo
```

**3. Missing Ownership Checks**
```python
❌ VULNERABLE:
@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    session.delete(todo)  # ❌ No ownership check - any user can delete any todo!
    session.commit()

✅ SECURE:
@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if todo.user_id != current_user["id"]:  # ✅ Ownership check
        raise HTTPException(status_code=403, detail="Not authorized")
    session.delete(todo)
    session.commit()
```

**4. Weak JWT Secret**
```python
❌ VULNERABLE:
BETTER_AUTH_SECRET = "secret"  # ❌ Too weak, hardcoded

✅ SECURE:
# .env file
BETTER_AUTH_SECRET=<long-random-string-min-32-chars>

# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BETTER_AUTH_SECRET: str  # ✅ From environment

    class Config:
        env_file = ".env"
```

**5. Token in URL Parameters**
```typescript
❌ VULNERABLE:
fetch(`/api/todos?token=${token}`)  // ❌ Token in URL (logged, cached)

✅ SECURE:
fetch('/api/todos', {
  headers: {
    'Authorization': `Bearer ${token}`  // ✅ In header
  }
})
```

**6. Exposing Sensitive Data in Errors**
```python
❌ VULNERABLE:
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))  # ❌ Leaks internals

✅ SECURE:
except Exception as e:
    logger.error(f"Error: {e}")  # ✅ Log internally
    raise HTTPException(status_code=500, detail="Internal server error")
```

## Testing Authentication

### Manual Testing Checklist

**Test 1: Valid Token Access**
```bash
# Get valid token from Better Auth
TOKEN="<valid-jwt-token>"

# Test protected endpoint
curl -X GET "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer $TOKEN"

✅ Expected: 200 OK with user's todos
```

**Test 2: Missing Token**
```bash
# No Authorization header
curl -X GET "http://localhost:8000/api/v1/todos"

✅ Expected: 401 Unauthorized
```

**Test 3: Invalid Token**
```bash
# Malformed token
curl -X GET "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer invalid-token"

✅ Expected: 401 Unauthorized
```

**Test 4: Expired Token**
```bash
# Use expired token
TOKEN="<expired-jwt-token>"

curl -X GET "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer $TOKEN"

✅ Expected: 401 Unauthorized with "Token has expired"
```

**Test 5: Cross-User Access**
```bash
# User 1 creates a todo
TOKEN_USER1="<user1-token>"
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer $TOKEN_USER1" \
  -H "Content-Type: application/json" \
  -d '{"title": "User 1 Todo"}'

# Get todo ID from response (e.g., id: 123)

# User 2 tries to access User 1's todo
TOKEN_USER2="<user2-token>"
curl -X GET "http://localhost:8000/api/v1/todos/123" \
  -H "Authorization: Bearer $TOKEN_USER2"

✅ Expected: 403 Forbidden
```

**Test 6: Token Tampering**
```bash
# Modify token payload (change user_id)
# Use JWT debugger to create tampered token

curl -X GET "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer <tampered-token>"

✅ Expected: 401 Unauthorized (signature verification fails)
```

### Automated Testing

**Backend Integration Tests:**
```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_protected_endpoint_requires_auth():
    """Test that protected endpoints require authentication."""
    response = client.get("/api/v1/todos")
    assert response.status_code == 401

def test_invalid_token_rejected():
    """Test that invalid tokens are rejected."""
    response = client.get(
        "/api/v1/todos",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401

def test_user_isolation():
    """Test that users can only access their own data."""
    # Create todo as user 1
    response1 = client.post(
        "/api/v1/todos",
        headers={"Authorization": f"Bearer {USER1_TOKEN}"},
        json={"title": "User 1 Todo"}
    )
    todo_id = response1.json()["id"]

    # Try to access as user 2
    response2 = client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {USER2_TOKEN}"}
    )
    assert response2.status_code == 403

def test_ownership_check_on_update():
    """Test that users cannot update other users' todos."""
    # Create todo as user 1
    response1 = client.post(
        "/api/v1/todos",
        headers={"Authorization": f"Bearer {USER1_TOKEN}"},
        json={"title": "User 1 Todo"}
    )
    todo_id = response1.json()["id"]

    # Try to update as user 2
    response2 = client.put(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {USER2_TOKEN}"},
        json={"title": "Hacked"}
    )
    assert response2.status_code == 403

def test_ownership_check_on_delete():
    """Test that users cannot delete other users' todos."""
    # Create todo as user 1
    response1 = client.post(
        "/api/v1/todos",
        headers={"Authorization": f"Bearer {USER1_TOKEN}"},
        json={"title": "User 1 Todo"}
    )
    todo_id = response1.json()["id"]

    # Try to delete as user 2
    response2 = client.delete(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {USER2_TOKEN}"}
    )
    assert response2.status_code == 403
```

## Debugging Common Issues

### Issue 1: 401 Unauthorized on All Requests

**Symptoms:**
- All API requests return 401
- Frontend shows "Unauthorized" errors

**Debugging Steps:**
1. Check JWT secret matches between frontend and backend
2. Verify token format in Authorization header
3. Check token expiration
4. Verify algorithm matches (HS256)
5. Check for typos in environment variables

**Debug Script:**
```python
# debug_jwt.py
from jose import jwt
import os

token = "<paste-token-here>"
secret = os.getenv("BETTER_AUTH_SECRET")

try:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    print("✅ Token valid!")
    print(f"User ID: {payload.get('sub')}")
    print(f"Email: {payload.get('email')}")
    print(f"Expires: {payload.get('exp')}")
except Exception as e:
    print(f"❌ Token invalid: {e}")
```

### Issue 2: Cross-User Data Leakage

**Symptoms:**
- Users can see other users' data
- User A can modify User B's resources

**Debugging Steps:**
1. Check all endpoints have `current_user` dependency
2. Verify queries filter by `user_id`
3. Check ownership verification before update/delete
4. Review database queries for missing WHERE clauses

**Audit Script:**
```python
# audit_endpoints.py
import ast
import os

def audit_endpoint_file(filepath):
    """Check if endpoint has proper auth and user filtering."""
    with open(filepath) as f:
        content = f.read()

    issues = []

    # Check for current_user dependency
    if "current_user" not in content:
        issues.append("Missing current_user dependency")

    # Check for user_id filtering
    if "user_id ==" not in content and "user_id =" not in content:
        issues.append("Missing user_id filtering")

    # Check for ownership checks
    if "403" not in content and "FORBIDDEN" not in content:
        issues.append("Missing ownership checks (403)")

    return issues

# Run on all endpoint files
for file in os.listdir("app/api/v1"):
    if file.endswith(".py"):
        issues = audit_endpoint_file(f"app/api/v1/{file}")
        if issues:
            print(f"⚠️  {file}: {', '.join(issues)}")
```

### Issue 3: Token Not Being Sent

**Symptoms:**
- Frontend has token but backend receives 401
- Authorization header missing

**Debugging Steps:**
1. Check token storage (localStorage, cookies)
2. Verify API client includes Authorization header
3. Check for CORS issues
4. Verify token retrieval logic

**Frontend Debug:**
```typescript
// Debug API calls
async function debugApiCall() {
  const token = localStorage.getItem('auth_token');
  console.log('Token:', token ? 'Present' : 'Missing');

  const response = await fetch('/api/todos', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  console.log('Status:', response.status);
  console.log('Headers sent:', response.headers);
}
```

## Security Best Practices Summary

### ✅ DO:
- Use strong JWT secrets (min 32 characters)
- Store secrets in environment variables
- Verify JWT signature on every request
- Check token expiration
- Extract user_id from JWT payload
- Filter all queries by authenticated user_id
- Verify ownership before update/delete
- Return appropriate status codes (401, 403, 404)
- Use HTTPS in production
- Log security events (failed auth attempts)
- Implement rate limiting
- Use httpOnly cookies for token storage (preferred)

### ❌ DON'T:
- Hardcode JWT secrets
- Trust client-provided user_id
- Skip ownership checks
- Expose sensitive data in errors
- Send tokens in URL parameters
- Store tokens in localStorage without understanding XSS risks
- Use weak secrets
- Skip token expiration checks
- Allow algorithm "none"
- Log token contents

## Review Report Template

After completing the review, document findings:

```markdown
# JWT Authentication Review Report

**Date:** YYYY-MM-DD
**Reviewer:** [Name]
**System:** Next.js + Better Auth + FastAPI

## Executive Summary
[Brief overview of findings]

## Findings

### Critical Issues (Fix Immediately)
- [ ] Issue 1: [Description]
  - **Impact:** [Security impact]
  - **Location:** [File:line]
  - **Fix:** [Recommended fix]

### High Priority
- [ ] Issue 2: [Description]

### Medium Priority
- [ ] Issue 3: [Description]

### Low Priority / Recommendations
- [ ] Issue 4: [Description]

## Test Results
- [ ] Valid token access: PASS/FAIL
- [ ] Missing token rejection: PASS/FAIL
- [ ] Invalid token rejection: PASS/FAIL
- [ ] Expired token rejection: PASS/FAIL
- [ ] Cross-user isolation: PASS/FAIL
- [ ] Ownership checks: PASS/FAIL

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

## Sign-off
- [ ] All critical issues resolved
- [ ] All tests passing
- [ ] Documentation updated
```

## Conclusion

A secure JWT authentication system requires:
1. **Proper token generation** (Better Auth)
2. **Secure token transmission** (Authorization header)
3. **Rigorous token verification** (FastAPI)
4. **Strict user isolation** (database queries)
5. **Ownership verification** (before operations)
6. **Comprehensive testing** (all scenarios)

Follow this review process to ensure your authentication system is secure and robust.
