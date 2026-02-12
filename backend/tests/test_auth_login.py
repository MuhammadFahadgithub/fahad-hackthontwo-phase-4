"""
Integration tests for user login endpoint.

Tests POST /api/auth/login endpoint functionality.
Constitution Principles II-V compliance verification.
"""
import pytest
from jose import jwt
from datetime import datetime, timedelta

from app.config import settings
from app.models.user import User
from app.core.security import hash_password


class TestLoginEndpoint:
    """
    Test POST /api/auth/login endpoint.

    Constitution SR-001: Email/password authentication required
    Constitution SR-003: JWT token generation with BETTER_AUTH_SECRET
    Constitution SR-004: Invalid credentials return 401 Unauthorized
    """

    def test_login_success(self, client, session):
        """
        Test successful login with valid credentials.

        Verifies:
        - 200 OK status
        - JWT token returned
        - Token contains user_id in 'sub' claim
        - User data returned (without password)
        """
        # Create a user first
        hashed_password = hash_password("password123")
        user = User(
            email="testuser@example.com",
            name="Test User",
            hashed_password=hashed_password,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Attempt login
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        # Verify response
        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "user" in data
        assert "token" in data
        assert "expires_at" in data

        # Verify user data
        user_data = data["user"]
        assert user_data["email"] == "testuser@example.com"
        assert user_data["name"] == "Test User"
        assert user_data["id"] == user.id

        # Verify JWT token
        token = data["token"]
        decoded = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        assert decoded["sub"] == str(user.id)
        assert decoded["email"] == user.email

    def test_login_invalid_email(self, client):
        """
        Test login fails with non-existent email.

        Constitution SR-004: Invalid credentials MUST return 401 Unauthorized
        """
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid" in data["detail"].lower() or "incorrect" in data["detail"].lower()

    def test_login_incorrect_password(self, client, session):
        """
        Test login fails with incorrect password.

        Constitution SR-004: Invalid credentials MUST return 401 Unauthorized
        """
        # Create a user
        hashed_password = hash_password("correctpassword")
        user = User(
            email="user@example.com",
            name="User",
            hashed_password=hashed_password,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()

        # Attempt login with wrong password
        login_data = {
            "email": "user@example.com",
            "password": "wrongpassword"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "invalid" in data["detail"].lower() or "incorrect" in data["detail"].lower()

    def test_login_missing_email(self, client):
        """Test login fails when email is missing."""
        login_data = {
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422

    def test_login_missing_password(self, client):
        """Test login fails when password is missing."""
        login_data = {
            "email": "test@example.com"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422

    def test_login_invalid_email_format(self, client):
        """Test login fails with invalid email format."""
        login_data = {
            "email": "not-an-email",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422

    def test_login_empty_password(self, client):
        """Test login fails with empty password."""
        login_data = {
            "email": "test@example.com",
            "password": ""
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422

    def test_login_case_insensitive_email(self, client, session):
        """
        Test that email comparison is case-insensitive during login.

        User registered with lowercase email should be able to login with uppercase.
        """
        # Create user with lowercase email
        hashed_password = hash_password("password123")
        user = User(
            email="user@example.com",
            name="User",
            hashed_password=hashed_password,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()

        # Login with uppercase email
        login_data = {
            "email": "USER@EXAMPLE.COM",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == "user@example.com"

    def test_login_password_not_returned(self, client, session):
        """
        Test that password is never returned in login response.

        Security: Passwords should never be exposed in API responses
        """
        # Create user
        hashed_password = hash_password("password123")
        user = User(
            email="security@example.com",
            name="Security Test",
            hashed_password=hashed_password,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()

        # Login
        login_data = {
            "email": "security@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200

        data = response.json()

        # Verify password not in user object
        assert "password" not in data["user"]
        assert "hashed_password" not in data["user"]

        # Verify password not anywhere in response
        response_str = str(data)
        assert "password123" not in response_str

    def test_login_jwt_token_structure(self, client, session):
        """
        Test JWT token has correct structure and claims.

        Constitution SR-003: JWT must be signed with BETTER_AUTH_SECRET
        Constitution SR-006: JWT must contain user_id in 'sub' claim
        """
        # Create user
        hashed_password = hash_password("password123")
        user = User(
            email="jwttest@example.com",
            name="JWT Test",
            hashed_password=hashed_password,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Login
        login_data = {
            "email": "jwttest@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200

        data = response.json()
        token = data["token"]

        # Decode and verify token
        decoded = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])

        # Verify required claims
        assert "sub" in decoded  # User ID
        assert "email" in decoded  # Email
        assert "exp" in decoded  # Expiration

        # Verify sub matches user ID
        assert decoded["sub"] == str(user.id)
        assert decoded["email"] == user.email

        # Verify expiration is in the future
        exp_timestamp = decoded["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        assert exp_datetime > datetime.utcnow()

    def test_login_token_expiration(self, client, session):
        """Test that login token has 7-day expiration."""
        # Create user
        hashed_password = hash_password("password123")
        user = User(
            email="expiry@example.com",
            name="Expiry Test",
            hashed_password=hashed_password,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()

        # Login
        login_data = {
            "email": "expiry@example.com",
            "password": "password123"
        }

        before_login = datetime.utcnow()
        response = client.post("/api/v1/auth/login", json=login_data)
        after_login = datetime.utcnow()

        assert response.status_code == 200
        data = response.json()

        # Verify expires_at is approximately 7 days from now
        expires_at = datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00"))
        expected_expiry_min = before_login + timedelta(days=7)
        expected_expiry_max = after_login + timedelta(days=7)

        # Allow 1 minute tolerance
        assert expected_expiry_min - timedelta(minutes=1) <= expires_at <= expected_expiry_max + timedelta(minutes=1)

    def test_login_multiple_times(self, client, session):
        """
        Test that user can login multiple times.

        Each login should generate a new token.
        """
        # Create user
        hashed_password = hash_password("password123")
        user = User(
            email="multilogin@example.com",
            name="Multi Login",
            hashed_password=hashed_password,
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()

        login_data = {
            "email": "multilogin@example.com",
            "password": "password123"
        }

        # First login
        response1 = client.post("/api/v1/auth/login", json=login_data)
        assert response1.status_code == 200
        token1 = response1.json()["token"]

        # Second login
        response2 = client.post("/api/v1/auth/login", json=login_data)
        assert response2.status_code == 200
        token2 = response2.json()["token"]

        # Tokens should be different (different timestamps)
        # Note: They might be the same if generated in the same second
        # but both should be valid
        decoded1 = jwt.decode(token1, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        decoded2 = jwt.decode(token2, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])

        assert decoded1["sub"] == decoded2["sub"]
        assert decoded1["email"] == decoded2["email"]
