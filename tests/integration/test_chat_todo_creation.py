import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.src.main import app
from backend.src.models import User, Todo
from backend.src.database import Base, get_db
from backend.src.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_integration_chat_todo_creation(client):
    """Integration test for chat-based todo creation"""
    # Mock the chat service to return a specific response
    with patch('backend.src.services.chat_service.ChatService.process_message') as mock_process:
        mock_process.return_value = ("I've added 'Test task' to your todos.", [{"type": "create_todo", "params": {"title": "Test task"}}])
        
        # Send a request to create a todo via chat
        response = client.post("/api/v1/chat/message", json={
            "message": "Add a todo: Test task"
        })
        
        # Check that the response is successful
        assert response.status_code == 200
        assert "response" in response.json()
        assert "Test task" in response.json()["response"]
        
        # Verify the action was recorded
        assert len(response.json()["actions"]) > 0
        assert response.json()["actions"][0]["type"] == "create_todo"
        assert response.json()["actions"][0]["params"]["title"] == "Test task"