import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool

from src.main import create_app
from src.database import get_session
from src.models.task import Task


# Create a test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app = create_app()
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_check(client: TestClient):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_chat_endpoint_exists(client: TestClient):
    """Test that the chat endpoint exists"""
    # This will fail because we don't have auth implemented, but should return 401 or 422, not 404
    response = client.post("/api/v1/chat", json={"message": "test"})
    # Should not return 404 (not found)
    assert response.status_code != 404


def test_nlp_processor():
    """Test the NLP processor directly"""
    from src.nlp.processor import NaturalLanguageProcessor
    
    processor = NaturalLanguageProcessor()
    
    # Test add task
    result = processor.process_input("Add a task to buy groceries")
    assert result["operation"] == "add_task"
    assert result["params"]["description"] == "buy groceries"
    
    # Test list tasks
    result = processor.process_input("Show me my tasks")
    assert result["operation"] == "list_tasks"
    
    # Test complete task
    result = processor.process_input("Complete task 1")
    assert result["operation"] == "complete_task"
    assert result["params"]["task_id"] == "1"
    
    # Test delete task
    result = processor.process_input("Delete task 2")
    assert result["operation"] == "delete_task"
    assert result["params"]["task_id"] == "2"


def test_mcp_tools_validation():
    """Test MCP tools validation"""
    from src.mcp.tools import MCPTaskTools
    from sqlmodel import Session
    
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    tools = MCPTaskTools(mock_session)
    
    # Test add_task with empty description
    result = tools.add_task("user123", "")
    assert result["status"] == "error"
    assert "cannot be empty" in result["message"]
    
    # Test add_task with valid input
    with patch.object(tools.task_service, 'create_task') as mock_create:
        mock_task = MagicMock()
        mock_task.id = "task123"
        mock_task.description = "test task"
        mock_create.return_value = mock_task
        
        result = tools.add_task("user123", "test task")
        assert result["status"] == "success"
        assert result["task_id"] == "task123"