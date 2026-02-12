"""
Security utilities for password hashing and verification.

Uses bcrypt for secure password hashing with cost factor 12.
Constitution Principle II: Authentication & JWT Security
"""
from passlib.context import CryptContext

# Create password context with bcrypt
# Constitution SR-018: Use bcrypt with cost factor 12
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Note:
        - Uses bcrypt with cost factor 12 (secure but performant)
        - Never store plain text passwords
        - Constitution SR-018: Passwords MUST be hashed with bcrypt
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise

    Note:
        - Uses constant-time comparison to prevent timing attacks
        - Constitution SR-018: Password verification with bcrypt
    """
    return pwd_context.verify(plain_password, hashed_password)
