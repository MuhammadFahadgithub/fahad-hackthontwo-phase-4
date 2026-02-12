---
name: fullstack-testing-strategy
description: |
  Comprehensive testing guide for full-stack applications with Next.js frontend
  and FastAPI backend. Covers unit tests, integration tests, E2E tests, and
  authentication testing strategies.

proficiency_level: "B2"
category: "Testing"
use_when: |
  - Writing backend tests with pytest
  - Writing frontend tests with Jest and React Testing Library
  - Implementing integration tests
  - Setting up E2E tests with Playwright or Cypress
  - Testing authentication flows
  - Debugging test failures
---

# Full-Stack Testing Strategy

## Role
You are a testing specialist focused on building comprehensive test suites for full-stack applications with Next.js and FastAPI.

## Testing Philosophy

### Testing Pyramid
```
        /\
       /  \      E2E Tests (Few)
      /____\     - Critical user flows
     /      \    - Authentication flows
    /        \   Integration Tests (Some)
   /          \  - API + Database
  /____________\ Unit Tests (Many)
                 - Business logic
                 - Components
                 - Utilities
```

### Test Coverage Goals
- **Unit Tests**: 80%+ coverage
- **Integration Tests**: All API endpoints
- **E2E Tests**: Critical user journeys
- **Authentication Tests**: All auth flows

## Backend Testing (FastAPI + pytest)

### Setup

**Install Dependencies:**
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

**pytest Configuration:**
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts =
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --verbose
```

**Test Database Setup:**
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.core.auth import get_current_user

# Test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite://"

@pytest.fixture(name="engine")
def engine_fixture():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="session")
def session_fixture(engine):
    """Create test database session."""
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with overridden dependencies."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_current_user():
    """Mock authenticated user."""
    return {"id": 1, "email": "test@example.com"}

@pytest.fixture
def authenticated_client(client, mock_current_user):
    """Client with mocked authentication."""
    def get_current_user_override():
        return mock_current_user

    app.dependency_overrides[get_current_user] = get_current_user_override
    yield client
    app.dependency_overrides.clear()
```

### Unit Tests - Models

```python
# tests/test_models.py
import pytest
from datetime import datetime
from app.models.todo import Todo

def test_todo_model_creation():
    """Test Todo model can be created with required fields."""
    todo = Todo(
        title="Test Todo",
        description="Test Description",
        user_id=1
    )

    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.user_id == 1
    assert todo.completed is False
    assert isinstance(todo.created_at, datetime)
    assert isinstance(todo.updated_at, datetime)

def test_todo_model_defaults():
    """Test Todo model default values."""
    todo = Todo(title="Test", user_id=1)

    assert todo.completed is False
    assert todo.description is None
    assert todo.created_at is not None
    assert todo.updated_at is not None

def test_todo_model_validation():
    """Test Todo model validation."""
    with pytest.raises(ValueError):
        # Title too long
        Todo(title="x" * 256, user_id=1)
```

### Integration Tests - API Endpoints

```python
# tests/test_todos_api.py
import pytest
from fastapi.testclient import TestClient

def test_create_todo(authenticated_client: TestClient):
    """Test creating a new todo."""
    response = authenticated_client.post(
        "/api/v1/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "completed": False
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert data["user_id"] == 1
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_todo_requires_auth(client: TestClient):
    """Test that creating todo requires authentication."""
    response = client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo"}
    )

    assert response.status_code == 401

def test_create_todo_validation(authenticated_client: TestClient):
    """Test todo creation validation."""
    # Missing required field
    response = authenticated_client.post(
        "/api/v1/todos/",
        json={"description": "No title"}
    )

    assert response.status_code == 422

def test_get_todos(authenticated_client: TestClient):
    """Test getting all todos for user."""
    # Create test todos
    authenticated_client.post(
        "/api/v1/todos/",
        json={"title": "Todo 1"}
    )
    authenticated_client.post(
        "/api/v1/todos/",
        json={"title": "Todo 2"}
    )

    # Get todos
    response = authenticated_client.get("/api/v1/todos/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"

def test_get_todos_requires_auth(client: TestClient):
    """Test that getting todos requires authentication."""
    response = client.get("/api/v1/todos/")
    assert response.status_code == 401

def test_get_todo_by_id(authenticated_client: TestClient):
    """Test getting a specific todo by ID."""
    # Create todo
    create_response = authenticated_client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo"}
    )
    todo_id = create_response.json()["id"]

    # Get todo
    response = authenticated_client.get(f"/api/v1/todos/{todo_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo"

def test_get_nonexistent_todo(authenticated_client: TestClient):
    """Test getting a todo that doesn't exist."""
    response = authenticated_client.get("/api/v1/todos/99999")
    assert response.status_code == 404

def test_update_todo(authenticated_client: TestClient):
    """Test updating a todo."""
    # Create todo
    create_response = authenticated_client.post(
        "/api/v1/todos/",
        json={"title": "Original Title", "completed": False}
    )
    todo_id = create_response.json()["id"]

    # Update todo
    response = authenticated_client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Updated Title", "completed": True}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] is True

def test_update_todo_partial(authenticated_client: TestClient):
    """Test partial update of todo."""
    # Create todo
    create_response = authenticated_client.post(
        "/api/v1/todos/",
        json={"title": "Original", "description": "Original Desc"}
    )
    todo_id = create_response.json()["id"]

    # Update only title
    response = authenticated_client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Updated"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["description"] == "Original Desc"  # Unchanged

def test_delete_todo(authenticated_client: TestClient):
    """Test deleting a todo."""
    # Create todo
    create_response = authenticated_client.post(
        "/api/v1/todos/",
        json={"title": "To Delete"}
    )
    todo_id = create_response.json()["id"]

    # Delete todo
    response = authenticated_client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = authenticated_client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_todo(authenticated_client: TestClient):
    """Test deleting a todo that doesn't exist."""
    response = authenticated_client.delete("/api/v1/todos/99999")
    assert response.status_code == 404
```

### Authorization Tests - User Isolation

```python
# tests/test_authorization.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import get_current_user

@pytest.fixture
def user1_client(client):
    """Client authenticated as user 1."""
    def get_user1():
        return {"id": 1, "email": "user1@example.com"}

    app.dependency_overrides[get_current_user] = get_user1
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def user2_client(client):
    """Client authenticated as user 2."""
    def get_user2():
        return {"id": 2, "email": "user2@example.com"}

    app.dependency_overrides[get_current_user] = get_user2
    yield client
    app.dependency_overrides.clear()

def test_user_cannot_see_other_user_todos(user1_client, user2_client):
    """Test that users can only see their own todos."""
    # User 1 creates a todo
    user1_client.post(
        "/api/v1/todos/",
        json={"title": "User 1 Todo"}
    )

    # User 2 creates a todo
    user2_client.post(
        "/api/v1/todos/",
        json={"title": "User 2 Todo"}
    )

    # User 1 gets todos
    response1 = user1_client.get("/api/v1/todos/")
    todos1 = response1.json()

    # User 2 gets todos
    response2 = user2_client.get("/api/v1/todos/")
    todos2 = response2.json()

    # Each user should only see their own todo
    assert len(todos1) == 1
    assert todos1[0]["title"] == "User 1 Todo"

    assert len(todos2) == 1
    assert todos2[0]["title"] == "User 2 Todo"

def test_user_cannot_access_other_user_todo(user1_client, user2_client):
    """Test that users cannot access other users' todos by ID."""
    # User 1 creates a todo
    response = user1_client.post(
        "/api/v1/todos/",
        json={"title": "User 1 Todo"}
    )
    todo_id = response.json()["id"]

    # User 2 tries to access User 1's todo
    response = user2_client.get(f"/api/v1/todos/{todo_id}")

    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]

def test_user_cannot_update_other_user_todo(user1_client, user2_client):
    """Test that users cannot update other users' todos."""
    # User 1 creates a todo
    response = user1_client.post(
        "/api/v1/todos/",
        json={"title": "User 1 Todo"}
    )
    todo_id = response.json()["id"]

    # User 2 tries to update User 1's todo
    response = user2_client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Hacked"}
    )

    assert response.status_code == 403

def test_user_cannot_delete_other_user_todo(user1_client, user2_client):
    """Test that users cannot delete other users' todos."""
    # User 1 creates a todo
    response = user1_client.post(
        "/api/v1/todos/",
        json={"title": "User 1 Todo"}
    )
    todo_id = response.json()["id"]

    # User 2 tries to delete User 1's todo
    response = user2_client.delete(f"/api/v1/todos/{todo_id}")

    assert response.status_code == 403
```

### Running Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_todos_api.py

# Run specific test
pytest tests/test_todos_api.py::test_create_todo

# Run tests matching pattern
pytest -k "authorization"

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

## Frontend Testing (Next.js + Jest + React Testing Library)

### Setup

**Install Dependencies:**
```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

**Jest Configuration:**
```javascript
// jest.config.js
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
  collectCoverageFrom: [
    'app/**/*.{js,jsx,ts,tsx}',
    'components/**/*.{js,jsx,ts,tsx}',
    'lib/**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
  ],
}

module.exports = createJestConfig(customJestConfig)
```

**Jest Setup:**
```javascript
// jest.setup.js
import '@testing-library/jest-dom'

// Mock fetch
global.fetch = jest.fn()

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000'
```

### Unit Tests - Utilities

```typescript
// lib/api/__tests__/todos.test.ts
import { getTodos, createTodo, updateTodo, deleteTodo } from '../todos'

describe('Todo API Client', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('getTodos', () => {
    it('should fetch todos with auth token', async () => {
      const mockTodos = [
        { id: 1, title: 'Test Todo', completed: false }
      ]

      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => mockTodos,
      })

      const result = await getTodos('test-token')

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/todos',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-token',
          }),
        })
      )
      expect(result).toEqual(mockTodos)
    })

    it('should throw error on 401', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 401,
      })

      await expect(getTodos('invalid-token')).rejects.toThrow('Unauthorized')
    })

    it('should throw error on network failure', async () => {
      global.fetch = jest.fn().mockRejectedValue(new Error('Network error'))

      await expect(getTodos('test-token')).rejects.toThrow('Network error')
    })
  })

  describe('createTodo', () => {
    it('should create todo with auth token', async () => {
      const newTodo = { title: 'New Todo', description: 'Description' }
      const createdTodo = { id: 1, ...newTodo, completed: false }

      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        status: 201,
        json: async () => createdTodo,
      })

      const result = await createTodo(newTodo, 'test-token')

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/todos',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-token',
            'Content-Type': 'application/json',
          }),
          body: JSON.stringify(newTodo),
        })
      )
      expect(result).toEqual(createdTodo)
    })
  })
})
```

### Component Tests

```typescript
// components/__tests__/TodoList.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { TodoList } from '../TodoList'
import * as todoApi from '@/lib/api/todos'

// Mock the API module
jest.mock('@/lib/api/todos')

// Mock auth hook
jest.mock('@/lib/auth/useAuth', () => ({
  useAuth: () => ({
    token: 'test-token',
    isAuthenticated: true,
  }),
}))

describe('TodoList', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('should render loading state initially', () => {
    jest.spyOn(todoApi, 'getTodos').mockImplementation(
      () => new Promise(() => {}) // Never resolves
    )

    render(<TodoList />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('should render todos after loading', async () => {
    const mockTodos = [
      { id: 1, title: 'Todo 1', completed: false },
      { id: 2, title: 'Todo 2', completed: true },
    ]

    jest.spyOn(todoApi, 'getTodos').mockResolvedValue(mockTodos)

    render(<TodoList />)

    await waitFor(() => {
      expect(screen.getByText('Todo 1')).toBeInTheDocument()
      expect(screen.getByText('Todo 2')).toBeInTheDocument()
    })
  })

  it('should render error message on fetch failure', async () => {
    jest.spyOn(todoApi, 'getTodos').mockRejectedValue(
      new Error('Failed to fetch')
    )

    render(<TodoList />)

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })
  })

  it('should show login prompt when not authenticated', () => {
    jest.mock('@/lib/auth/useAuth', () => ({
      useAuth: () => ({
        token: null,
        isAuthenticated: false,
      }),
    }))

    render(<TodoList />)
    expect(screen.getByText(/please log in/i)).toBeInTheDocument()
  })
})
```

### Running Frontend Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test file
npm test TodoList.test.tsx

# Update snapshots
npm test -- -u
```

## Integration Testing

### End-to-End Flow Tests

```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient

def test_complete_todo_lifecycle(authenticated_client: TestClient):
    """Test complete CRUD lifecycle for a todo."""
    # Create
    create_response = authenticated_client.post(
        "/api/v1/todos/",
        json={"title": "Integration Test Todo", "completed": False}
    )
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    # Read (list)
    list_response = authenticated_client.get("/api/v1/todos/")
    assert list_response.status_code == 200
    todos = list_response.json()
    assert any(t["id"] == todo_id for t in todos)

    # Read (single)
    get_response = authenticated_client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Integration Test Todo"

    # Update
    update_response = authenticated_client.put(
        f"/api/v1/todos/{todo_id}",
        json={"completed": True}
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    # Delete
    delete_response = authenticated_client.delete(f"/api/v1/todos/{todo_id}")
    assert delete_response.status_code == 204

    # Verify deleted
    get_after_delete = authenticated_client.get(f"/api/v1/todos/{todo_id}")
    assert get_after_delete.status_code == 404
```

## E2E Testing (Playwright)

### Setup

```bash
npm install --save-dev @playwright/test
npx playwright install
```

**Playwright Configuration:**
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  webServer: [
    {
      command: 'npm run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'cd backend && uvicorn app.main:app --reload',
      url: 'http://localhost:8000',
      reuseExistingServer: !process.env.CI,
    },
  ],
})
```

### E2E Tests

```typescript
// e2e/todos.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Todo Application', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/dashboard')
  })

  test('should create a new todo', async ({ page }) => {
    await page.goto('/todos')

    // Fill form
    await page.fill('[name="title"]', 'E2E Test Todo')
    await page.fill('[name="description"]', 'Created by E2E test')
    await page.click('button:has-text("Add Todo")')

    // Verify todo appears
    await expect(page.locator('text=E2E Test Todo')).toBeVisible()
  })

  test('should mark todo as complete', async ({ page }) => {
    await page.goto('/todos')

    // Create todo
    await page.fill('[name="title"]', 'Todo to Complete')
    await page.click('button:has-text("Add Todo")')

    // Mark as complete
    await page.click('[data-testid="todo-checkbox"]')

    // Verify completed state
    await expect(page.locator('[data-testid="todo-checkbox"]')).toBeChecked()
  })

  test('should delete todo', async ({ page }) => {
    await page.goto('/todos')

    // Create todo
    await page.fill('[name="title"]', 'Todo to Delete')
    await page.click('button:has-text("Add Todo")')

    // Delete todo
    await page.click('[data-testid="delete-button"]')
    await page.click('button:has-text("Confirm")')

    // Verify deleted
    await expect(page.locator('text=Todo to Delete')).not.toBeVisible()
  })

  test('should not show other users todos', async ({ page, context }) => {
    // User 1 creates a todo
    await page.goto('/todos')
    await page.fill('[name="title"]', 'User 1 Todo')
    await page.click('button:has-text("Add Todo")')

    // Logout
    await page.click('[data-testid="logout-button"]')

    // Login as User 2
    await page.goto('/login')
    await page.fill('[name="email"]', 'user2@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    // Verify User 2 doesn't see User 1's todo
    await page.goto('/todos')
    await expect(page.locator('text=User 1 Todo')).not.toBeVisible()
  })
})
```

### Running E2E Tests

```bash
# Run all E2E tests
npx playwright test

# Run in UI mode
npx playwright test --ui

# Run specific test
npx playwright test todos.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Debug test
npx playwright test --debug
```

## Test Coverage Analysis

### Backend Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

**Coverage Goals:**
- Models: 100%
- API endpoints: 90%+
- Business logic: 85%+
- Overall: 80%+

### Frontend Coverage

```bash
# Generate coverage report
npm test -- --coverage

# View coverage report
open coverage/lcov-report/index.html
```

**Coverage Goals:**
- Components: 80%+
- Utilities: 90%+
- API clients: 85%+
- Overall: 75%+

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps
      - name: Run E2E tests
        run: npx playwright test
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

## Best Practices

### ✅ DO:
- Write tests before or alongside code (TDD)
- Test behavior, not implementation
- Use descriptive test names
- Keep tests independent and isolated
- Mock external dependencies
- Test edge cases and error conditions
- Maintain high test coverage
- Run tests in CI/CD pipeline
- Use fixtures for common setup
- Clean up test data after tests

### ❌ DON'T:
- Test implementation details
- Write flaky tests
- Share state between tests
- Skip error case testing
- Hardcode test data
- Ignore failing tests
- Test third-party libraries
- Write tests that depend on execution order
- Leave commented-out tests
- Commit failing tests

## Summary

A comprehensive testing strategy includes:
1. **Unit Tests**: Fast, isolated tests for individual functions
2. **Integration Tests**: Test API endpoints with database
3. **E2E Tests**: Test complete user flows
4. **Authorization Tests**: Verify user isolation
5. **Coverage Analysis**: Ensure adequate test coverage
6. **CI/CD Integration**: Automated testing on every commit

Follow this guide to build a robust, well-tested full-stack application.
