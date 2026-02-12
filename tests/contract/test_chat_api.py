import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from backend.src.main import app
from backend.src.database import Base
from backend.src.models import User, Todo


# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_contract_for_post_chat_message(client):
    """Contract test for POST /api/v1/chat/message endpoint"""
    # Mock the chat service to avoid actual processing
    with patch('backend.src.services.chat_service.ChatService.process_message') as mock_process:
        mock_process.return_value = ("Test response", [])
        
        response = client.post("/api/v1/chat/message", json={
            "message": "Add a todo: Test task"
        })
        
        assert response.status_code == 200
        assert "response" in response.json()
        assert "conversation_id" in response.json()
        assert response.json()["response"] == "Test response"


def test_chat_message_missing_required_field(client):
    """Test that chat message endpoint returns error when required field is missing"""
    response = client.post("/api/v1/chat/message", json={})
    assert response.status_code == 422  # Unprocessable Entity