"""
Integration tests for user signup endpoint.

Tests POST /api/auth/signup endpoint functionality.
Constitution Principles II-V compliance verification.
"""
import pytest
from jose import jwt
from datetime import datetime, timedelta

from app.config import settings
from app.models.user import User
from app.core.security import verify_password


class TestSignupEndpoint:
    """
    Test POST /api/auth/signup endpoint.

    Constitution SR-001: Email/password signup required
    Constitution SR-003: JWT token generation with BETTER_AUTH_SECRET
    Constitution SR-018: Password hashing with bcrypt
    """

    def test_signup_success(self, client, session):
        """
        Test successful user signup with valid data.

        Verifies:
        - 201 Created status
        - User created in database
        - Password hashed (not plain text)
        - JWT token returned
        - Token contains user_id in 'sub' claim
        """
        signup_data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "securepassword123"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)

        # Verify response
        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "user" in data
        assert "token" in data
        assert "expires_at" in data

        # Verify user data
        user = data["user"]
        assert user["email"] == signup_data["email"]
        assert user["name"] == signup_data["name"]
        assert "id" in user
        assert user["email_verified"] is False

        # Verify user in database
        db_user = session.query(User).filter(User.email == signup_data["email"]).first()
        assert db_user is not None
        assert db_user.email == signup_data["email"]
        assert db_user.name == signup_data["name"]

        # Verify password is hashed (not plain text)
        assert db_user.hashed_password != signup_data["password"]
        assert db_user.hashed_password.startswith("$2b$")

        # Verify password can be verified
        assert verify_password(signup_data["password"], db_user.hashed_password) is True

        # Verify JWT token
        token = data["token"]
        decoded = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        assert decoded["sub"] == str(db_user.id)
        assert decoded["email"] == db_user.email
        assert "exp" in decoded

    def test_signup_duplicate_email(self, client, session):
        """
        Test signup fails with duplicate email.

        Constitution SR-001: Email must be unique
        Verifies 409 Conflict status
        """
        # Create first user
        signup_data = {
            "email": "duplicate@example.com",
            "name": "First User",
            "password": "password123"
        }
        response1 = client.post("/api/v1/auth/signup", json=signup_data)
        assert response1.status_code == 201

        # Try to create second user with same email
        signup_data2 = {
            "email": "duplicate@example.com",
            "name": "Second User",
            "password": "differentpassword"
        }
        response2 = client.post("/api/v1/auth/signup", json=signup_data2)

        # Verify conflict response
        assert response2.status_code == 409
        data = response2.json()
        assert "detail" in data
        assert "already exists" in data["detail"].lower() or "already registered" in data["detail"].lower()

    def test_signup_invalid_email_format(self, client):
        """
        Test signup fails with invalid email format.

        Verifies 422 Unprocessable Entity status
        """
        signup_data = {
            "email": "not-an-email",
            "name": "Test User",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_signup_password_too_short(self, client):
        """
        Test signup fails with password shorter than 8 characters.

        Constitution SR-001: Minimum password length 8
        Verifies 422 Unprocessable Entity status
        """
        signup_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "short"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_signup_missing_email(self, client):
        """Test signup fails when email is missing."""
        signup_data = {
            "name": "Test User",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422

    def test_signup_missing_name(self, client):
        """Test signup fails when name is missing."""
        signup_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422

    def test_signup_missing_password(self, client):
        """Test signup fails when password is missing."""
        signup_data = {
            "email": "test@example.com",
            "name": "Test User"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422

    def test_signup_empty_name(self, client):
        """Test signup fails with empty name."""
        signup_data = {
            "email": "test@example.com",
            "name": "",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422

    def test_signup_jwt_token_structure(self, client, session):
        """
        Test JWT token has correct structure and claims.

        Constitution SR-003: JWT must be signed with BETTER_AUTH_SECRET
        Constitution SR-006: JWT must contain user_id in 'sub' claim
        """
        signup_data = {
            "email": "jwttest@example.com",
            "name": "JWT Test User",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)
        assert response.status_code == 201

        data = response.json()
        token = data["token"]

        # Decode and verify token
        decoded = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])

        # Verify required claims
        assert "sub" in decoded  # User ID
        assert "email" in decoded  # Email
        assert "exp" in decoded  # Expiration

        # Verify sub is a valid user ID
        user_id = int(decoded["sub"])
        db_user = session.query(User).filter(User.id == user_id).first()
        assert db_user is not None
        assert db_user.email == signup_data["email"]

        # Verify expiration is in the future
        exp_timestamp = decoded["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        assert exp_datetime > datetime.utcnow()

    def test_signup_password_not_returned(self, client):
        """
        Test that password is never returned in response.

        Security: Passwords should never be exposed in API responses
        """
        signup_data = {
            "email": "security@example.com",
            "name": "Security Test",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/signup", json=signup_data)
        assert response.status_code == 201

        data = response.json()

        # Verify password not in user object
        assert "password" not in data["user"]
        assert "hashed_password" not in data["user"]

        # Verify password not anywhere in response
        response_str = str(data)
        assert "password123" not in response_str

    def test_signup_case_insensitive_email(self, client, session):
        """
        Test that email comparison is case-insensitive.

        user@example.com and USER@EXAMPLE.COM should be treated as same
        """
        # Create user with lowercase email
        signup_data1 = {
            "email": "user@example.com",
            "name": "User One",
            "password": "password123"
        }
        response1 = client.post("/api/v1/auth/signup", json=signup_data1)
        assert response1.status_code == 201

        # Try to create user with uppercase email
        signup_data2 = {
            "email": "USER@EXAMPLE.COM",
            "name": "User Two",
            "password": "password456"
        }
        response2 = client.post("/api/v1/auth/signup", json=signup_data2)

        # Should fail with conflict (email already exists)
        assert response2.status_code == 409

    def test_signup_timestamps_created(self, client, session):
        """Test that created_at and updated_at timestamps are set."""
        signup_data = {
            "email": "timestamps@example.com",
            "name": "Timestamp Test",
            "password": "password123"
        }

        before_signup = datetime.utcnow()
        response = client.post("/api/v1/auth/signup", json=signup_data)
        after_signup = datetime.utcnow()

        assert response.status_code == 201

        # Verify timestamps in database
        db_user = session.query(User).filter(User.email == signup_data["email"]).first()
        assert db_user is not None
        assert db_user.created_at is not None
        assert db_user.updated_at is not None

        # Verify timestamps are within expected range
        assert before_signup <= db_user.created_at <= after_signup
        assert before_signup <= db_user.updated_at <= after_signup
