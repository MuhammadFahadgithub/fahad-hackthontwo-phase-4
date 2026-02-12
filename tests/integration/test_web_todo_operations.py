import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.src.main import app
from backend.src.models import User, Todo
from backend.src.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_web_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_integration_web_todo_operations(client):
    """Integration test for web-based todo operations"""
    # Mock the authentication to bypass it for testing
    with patch('backend.src.auth.get_current_user') as mock_auth:
        # Create a mock user
        mock_user = User(id="test-user-id", email="test@example.com", hashed_password="fake-hash")
        mock_auth.return_value = mock_user
        
        # Test creating a todo
        create_response = client.post("/api/v1/todos", json={
            "title": "Test todo",
            "description": "Test description",
            "priority": "high"
        })
        
        assert create_response.status_code == 201
        created_todo = create_response.json()
        assert created_todo["title"] == "Test todo"
        assert created_todo["description"] == "Test description"
        assert created_todo["priority"] == "high"
        
        # Store the created todo ID for later use
        todo_id = created_todo["id"]
        
        # Test getting all todos
        get_all_response = client.get("/api/v1/todos")
        assert get_all_response.status_code == 200
        todos = get_all_response.json()
        assert len(todos) >= 1
        
        # Test getting a specific todo
        get_one_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_one_response.status_code == 200
        retrieved_todo = get_one_response.json()
        assert retrieved_todo["id"] == todo_id
        assert retrieved_todo["title"] == "Test todo"
        
        # Test updating a todo
        update_response = client.put(f"/api/v1/todos/{todo_id}", json={
            "title": "Updated todo",
            "completed": True
        })
        assert update_response.status_code == 200
        updated_todo = update_response.json()
        assert updated_todo["id"] == todo_id
        assert updated_todo["title"] == "Updated todo"
        assert updated_todo["completed"] is True
        
        # Test deleting a todo
        delete_response = client.delete(f"/api/v1/todos/{todo_id}")
        assert delete_response.status_code == 204
        
        # Verify the todo was deleted
        get_deleted_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_deleted_response.status_code == 404