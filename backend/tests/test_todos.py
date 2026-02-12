"""
Integration tests for todo CRUD endpoints.

Tests all todo operations with authentication and ownership enforcement.
Constitution Principles III-V compliance verification.
"""
import pytest
from datetime import datetime

from app.models.todo import Todo
from app.models.user import User
from app.core.security import hash_password


class TestTodoCreate:
    """
    Test POST /api/v1/todos endpoint.

    Constitution SR-002: JWT authentication required
    Constitution SR-006: User identity from JWT only
    """

    def test_create_todo_success(self, authenticated_client, session, mock_current_user):
        """Test successful todo creation."""
        todo_data = {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": False
        }

        response = authenticated_client.post("/api/v1/todos", json=todo_data)

        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert data["title"] == todo_data["title"]
        assert data["description"] == todo_data["description"]
        assert data["completed"] is False
        assert data["user_id"] == mock_current_user["id"]
        assert "created_at" in data
        assert "updated_at" in data

        # Verify in database
        db_todo = session.query(Todo).filter(Todo.id == data["id"]).first()
        assert db_todo is not None
        assert db_todo.user_id == mock_current_user["id"]

    def test_create_todo_without_auth(self, client):
        """
        Test that creating todo without authentication fails.

        Constitution SR-004: Missing tokens MUST return 401
        """
        todo_data = {
            "title": "Test todo",
            "description": "Should fail"
        }

        response = client.post("/api/v1/todos", json=todo_data)

        assert response.status_code == 401

    def test_create_todo_minimal(self, authenticated_client, mock_current_user):
        """Test creating todo with only required fields."""
        todo_data = {
            "title": "Minimal todo"
        }

        response = authenticated_client.post("/api/v1/todos", json=todo_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal todo"
        assert data["description"] is None
        assert data["completed"] is False

    def test_create_todo_missing_title(self, authenticated_client):
        """Test that creating todo without title fails."""
        todo_data = {
            "description": "No title"
        }

        response = authenticated_client.post("/api/v1/todos", json=todo_data)

        assert response.status_code == 422


class TestTodoList:
    """
    Test GET /api/v1/todos endpoint.

    Constitution Principle IV: Query-level authorization with user_id filtering
    Constitution Principle V: Zero cross-user data access
    """

    def test_list_todos_success(self, authenticated_client, session, mock_current_user):
        """Test listing user's todos."""
        # Create todos for current user
        todo1 = Todo(
            title="Todo 1",
            description="First todo",
            completed=False,
            user_id=mock_current_user["id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        todo2 = Todo(
            title="Todo 2",
            description="Second todo",
            completed=True,
            user_id=mock_current_user["id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(todo1)
        session.add(todo2)
        session.commit()

        response = authenticated_client.get("/api/v1/todos")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(todo["user_id"] == mock_current_user["id"] for todo in data)

    def test_list_todos_empty(self, authenticated_client):
        """Test listing todos when user has none."""
        response = authenticated_client.get("/api/v1/todos")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_todos_cross_user_isolation(self, authenticated_client, session, mock_current_user):
        """
        Test that users only see their own todos.

        Constitution Principle V: Zero cross-user data access
        """
        # Create todo for current user
        user_todo = Todo(
            title="My todo",
            user_id=mock_current_user["id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user_todo)

        # Create todo for another user
        other_user_todo = Todo(
            title="Other user's todo",
            user_id=999,  # Different user
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(other_user_todo)
        session.commit()

        response = authenticated_client.get("/api/v1/todos")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "My todo"
        assert data[0]["user_id"] == mock_current_user["id"]

    def test_list_todos_without_auth(self, client):
        """Test that listing todos without authentication fails."""
        response = client.get("/api/v1/todos")

        assert response.status_code == 401


class TestTodoGet:
    """
    Test GET /api/v1/todos/{id} endpoint.

    Constitution Principle V: Ownership verification required
    """

    def test_get_todo_success(self, authenticated_client, session, mock_current_user):
        """Test getting a specific todo."""
        todo = Todo(
            title="Test todo",
            description="Test description",
            completed=False,
            user_id=mock_current_user["id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)

        response = authenticated_client.get(f"/api/v1/todos/{todo.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo.id
        assert data["title"] == "Test todo"
        assert data["user_id"] == mock_current_user["id"]

    def test_get_todo_not_found(self, authenticated_client):
        """Test getting non-existent todo."""
        response = authenticated_client.get("/api/v1/todos/99999")

        assert response.status_code == 404

    def test_get_todo_wrong_owner(self, authenticated_client, session, mock_current_user):
        """
        Test that user cannot access another user's todo.

        Constitution Principle V: Zero cross-user data access
        """
        # Create todo for another user
        other_todo = Todo(
            title="Other user's todo",
            user_id=999,  # Different user
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(other_todo)
        session.commit()
        session.refresh(other_todo)

        response = authenticated_client.get(f"/api/v1/todos/{other_todo.id}")

        assert response.status_code == 403
        data = response.json()
        assert "not authorized" in data["detail"].lower() or "forbidden" in data["detail"].lower()


class TestTodoUpdate:
    """
    Test PUT /api/v1/todos/{id} endpoint.

    Constitution Principle V: Ownership verification required
    """

    def test_update_todo_success(self, authenticated_client, session, mock_current_user):
        """Test updating a todo."""
        todo = Todo(
            title="Original title",
            description="Original description",
            completed=False,
            user_id=mock_current_user["id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)

        update_data = {
            "title": "Updated title",
            "description": "Updated description",
            "completed": True
        }

        response = authenticated_client.put(f"/api/v1/todos/{todo.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["description"] == "Updated description"
        assert data["completed"] is True

        # Verify in database
        session.refresh(todo)
        assert todo.title == "Updated title"
        assert todo.completed is True

    def test_update_todo_partial(self, authenticated_client, session, mock_current_user):
        """Test partial update of todo."""
        todo = Todo(
            title="Original title",
            description="Original description",
            completed=False,
            user_id=mock_current_user["id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)

        update_data = {
            "completed": True
        }

        response = authenticated_client.put(f"/api/v1/todos/{todo.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original title"  # Unchanged
        assert data["completed"] is True  # Changed

    def test_update_todo_not_found(self, authenticated_client):
        """Test updating non-existent todo."""
        update_data = {"title": "Updated"}

        response = authenticated_client.put("/api/v1/todos/99999", json=update_data)

        assert response.status_code == 404

    def test_update_todo_wrong_owner(self, authenticated_client, session, mock_current_user):
        """
        Test that user cannot update another user's todo.

        Constitution Principle V: Zero cross-user data access
        """
        other_todo = Todo(
            title="Other user's todo",
            user_id=999,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(other_todo)
        session.commit()
        session.refresh(other_todo)

        update_data = {"title": "Hacked"}

        response = authenticated_client.put(f"/api/v1/todos/{other_todo.id}", json=update_data)

        assert response.status_code == 403


class TestTodoDelete:
    """
    Test DELETE /api/v1/todos/{id} endpoint.

    Constitution Principle V: Ownership verification required
    """

    def test_delete_todo_success(self, authenticated_client, session, mock_current_user):
        """Test deleting a todo."""
        todo = Todo(
            title="To be deleted",
            user_id=mock_current_user["id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        todo_id = todo.id

        response = authenticated_client.delete(f"/api/v1/todos/{todo_id}")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data

        # Verify deleted from database
        deleted_todo = session.query(Todo).filter(Todo.id == todo_id).first()
        assert deleted_todo is None

    def test_delete_todo_not_found(self, authenticated_client):
        """Test deleting non-existent todo."""
        response = authenticated_client.delete("/api/v1/todos/99999")

        assert response.status_code == 404

    def test_delete_todo_wrong_owner(self, authenticated_client, session, mock_current_user):
        """
        Test that user cannot delete another user's todo.

        Constitution Principle V: Zero cross-user data access
        """
        other_todo = Todo(
            title="Other user's todo",
            user_id=999,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(other_todo)
        session.commit()
        session.refresh(other_todo)

        response = authenticated_client.delete(f"/api/v1/todos/{other_todo.id}")

        assert response.status_code == 403

        # Verify not deleted
        session.refresh(other_todo)
        assert other_todo is not None
