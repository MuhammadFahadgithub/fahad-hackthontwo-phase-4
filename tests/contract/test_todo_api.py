import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.src.main import app
from backend.src.models import User, Todo


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_contract_get_todos(client):
    """Contract test for GET /api/v1/todos endpoint"""
    response = client.get("/api/v1/todos")
    # This should return 401 because authentication is required
    assert response.status_code == 401


def test_contract_post_todos(client):
    """Contract test for POST /api/v1/todos endpoint"""
    response = client.post("/api/v1/todos", json={
        "title": "Test todo",
        "description": "Test description"
    })
    # This should return 401 because authentication is required
    assert response.status_code == 401


def test_contract_get_todo_by_id(client):
    """Contract test for GET /api/v1/todos/{id} endpoint"""
    response = client.get("/api/v1/todos/123")
    # This should return 401 because authentication is required
    assert response.status_code == 401


def test_contract_put_todo_by_id(client):
    """Contract test for PUT /api/v1/todos/{id} endpoint"""
    response = client.put("/api/v1/todos/123", json={
        "title": "Updated title",
        "completed": True
    })
    # This should return 401 because authentication is required
    assert response.status_code == 401


def test_contract_delete_todo_by_id(client):
    """Contract test for DELETE /api/v1/todos/{id} endpoint"""
    response = client.delete("/api/v1/todos/123")
    # This should return 401 because authentication is required
    assert response.status_code == 401