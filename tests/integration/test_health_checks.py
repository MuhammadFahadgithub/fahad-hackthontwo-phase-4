import pytest
from fastapi.testclient import TestClient

from backend.src.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_readiness_probe():
    """Test for readiness probe"""
    with TestClient(app) as client:
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"


def test_liveness_probe():
    """Test for liveness probe"""
    with TestClient(app) as client:
        response = client.get("/api/v1/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"


def test_health_check():
    """Test for general health check"""
    with TestClient(app) as client:
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"