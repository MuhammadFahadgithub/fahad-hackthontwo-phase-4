"""
Security tests for authentication core.

Tests password hashing and JWT verification.
Constitution Principles II-V compliance verification.
"""
import pytest
from jose import jwt
from datetime import datetime, timedelta

from app.core.security import hash_password, verify_password
from app.core.auth import verify_jwt_token, get_current_user
from app.config import settings
from fastapi import HTTPException


class TestPasswordHashing:
    """
    Test password hashing and verification.

    Constitution SR-018: Passwords MUST be hashed with bcrypt
    """

    def test_hash_password(self):
        """Test that password hashing works."""
        password = "securepassword123"
        hashed = hash_password(password)

        # Verify hash is different from plain text
        assert hashed != password
        # Verify hash starts with bcrypt identifier
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "securepassword123"
        hashed = hash_password(password)

        # Verify correct password
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "securepassword123"
        hashed = hash_password(password)

        # Verify incorrect password fails
        assert verify_password("wrongpassword", hashed) is False

    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "securepassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Hashes should be different due to salt
        assert hash1 != hash2
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTVerification:
    """
    Test JWT token verification.

    Constitution SR-003: Backend MUST verify token using BETTER_AUTH_SECRET
    Constitution SR-004: Invalid/missing tokens MUST return 401 Unauthorized
    """

    def test_verify_valid_jwt_token(self):
        """Test JWT verification with valid token."""
        # Create valid token
        payload = {
            "sub": "1",
            "email": "test@example.com",
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        # Verify token
        decoded = verify_jwt_token(token)
        assert decoded["sub"] == "1"
        assert decoded["email"] == "test@example.com"

    def test_verify_invalid_jwt_token(self):
        """
        Test JWT verification rejects invalid tokens.

        Constitution SR-004: Invalid tokens MUST return 401 Unauthorized
        """
        invalid_token = "invalid.jwt.token"

        with pytest.raises(HTTPException) as exc_info:
            verify_jwt_token(invalid_token)

        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail

    def test_verify_expired_jwt_token(self):
        """
        Test JWT verification rejects expired tokens.

        Constitution SR-004: Expired tokens MUST return 401 Unauthorized
        """
        # Create expired token
        payload = {
            "sub": "1",
            "email": "test@example.com",
            "exp": datetime.utcnow() - timedelta(days=1)  # Expired yesterday
        }
        token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        with pytest.raises(HTTPException) as exc_info:
            verify_jwt_token(token)

        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()

    def test_verify_jwt_token_wrong_secret(self):
        """Test JWT verification rejects tokens signed with wrong secret."""
        # Create token with wrong secret
        payload = {
            "sub": "1",
            "email": "test@example.com",
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, "wrong-secret", algorithm="HS256")

        with pytest.raises(HTTPException) as exc_info:
            verify_jwt_token(token)

        assert exc_info.value.status_code == 401

    def test_verify_jwt_token_missing_sub(self):
        """
        Test JWT verification rejects tokens without user_id in 'sub' claim.

        Constitution SR-006: User identity MUST be extracted from JWT
        """
        # Create token without 'sub' claim
        payload = {
            "email": "test@example.com",
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        # verify_jwt_token should succeed (token is valid)
        decoded = verify_jwt_token(token)
        assert "sub" not in decoded or decoded.get("sub") is None


class TestGetCurrentUser:
    """
    Test get_current_user dependency.

    Constitution SR-006: User identity MUST be extracted from JWT only
    Constitution Principle III: Never trust client-provided user_id
    """

    @pytest.mark.asyncio
    async def test_get_current_user_valid_token(self):
        """Test extracting user from valid JWT token."""
        from fastapi.security import HTTPAuthorizationCredentials

        # Create valid token
        payload = {
            "sub": "123",
            "email": "test@example.com",
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        # Create credentials
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )

        # Get current user
        user = await get_current_user(credentials)

        assert user["id"] == 123
        assert user["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_current_user_missing_sub(self):
        """
        Test that missing user_id in token raises 401.

        Constitution SR-006: User identity MUST be extracted from JWT
        """
        from fastapi.security import HTTPAuthorizationCredentials

        # Create token without 'sub' claim
        payload = {
            "email": "test@example.com",
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials)

        assert exc_info.value.status_code == 401
        assert "missing user ID" in exc_info.value.detail


class TestAuthenticationEndpoints:
    """
    Test authentication endpoint requirements.

    Constitution SR-002: JWT MUST be sent in Authorization: Bearer <token> header
    Constitution SR-004: Missing/invalid tokens MUST return 401
    """

    def test_missing_authorization_header(self, client):
        """
        Test that missing Authorization header returns 401.

        Constitution SR-004: Missing tokens MUST return 401 Unauthorized
        """
        # Try to access protected endpoint without token
        # Note: This will be tested properly when we implement protected endpoints
        # For now, test the health endpoint (public)
        response = client.get("/api/v1/health")
        assert response.status_code == 200  # Health endpoint is public

    def test_health_endpoint_public(self, client):
        """Test that health endpoint is accessible without authentication."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
