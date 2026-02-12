"""
JWT authentication and verification.

Implements JWT token verification for FastAPI endpoints.
Constitution Principle II: Authentication & JWT Security
Constitution Principle III: User Identity & Isolation
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime
import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)


def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT token from Better Auth.

    Args:
        token: JWT token string

    Returns:
        dict: Token payload with user information

    Raises:
        HTTPException: 401 if token is invalid, expired, or malformed

    Note:
        - Constitution SR-003: Backend MUST verify token using BETTER_AUTH_SECRET
        - Constitution SR-004: Invalid/missing tokens MUST return 401 Unauthorized
        - Constitution SR-005: JWT secrets MUST NEVER be logged
    """
    try:
        # Decode and verify token signature
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )

        # Check expiration (jwt.decode does this automatically, but explicit check for clarity)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            logger.warning("Expired token received")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except jwt.ExpiredSignatureError:
        logger.warning("Expired token received")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTClaimsError:
        logger.warning("Invalid token claims")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.error(f"JWT verification failed: {type(e).__name__}")
        # Constitution SR-005: Never log token content
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> dict:
    """
    Dependency to extract and verify current user from JWT.

    Args:
        credentials: HTTP Authorization credentials from request header

    Returns:
        dict: User information with 'id' and 'email'

    Raises:
        HTTPException: 401 if token is invalid or missing user_id

    Note:
        - Constitution SR-002: JWT MUST be sent in Authorization: Bearer <token> header
        - Constitution SR-006: User identity MUST be extracted from JWT only
        - Constitution Principle III: Never trust client-provided user_id
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = verify_jwt_token(token)

    # Extract user_id from 'sub' claim (standard JWT claim)
    user_id = payload.get("sub")
    if user_id is None:
        logger.warning("Token missing user ID in 'sub' claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return user info (never query database here for performance)
    # Constitution SR-006: User identity extracted from JWT only
    return {
        "id": int(user_id),
        "email": payload.get("email", ""),
    }
