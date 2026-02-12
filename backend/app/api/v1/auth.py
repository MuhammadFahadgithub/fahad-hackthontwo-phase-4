"""
Authentication endpoints.

Handles user signup, login, logout, and password reset.
Constitution Principles II-V compliance.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from jose import jwt
from datetime import datetime, timedelta

from app.database import get_session
from app.models.user import User
from app.schemas.auth import SignUpRequest, LoginRequest, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password
from app.config import settings


router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignUpRequest,
    session: Session = Depends(get_session)
):
    """
    Create a new user account.

    Constitution SR-001: Email/password signup
    Constitution SR-003: JWT token generation with BETTER_AUTH_SECRET
    Constitution SR-018: Password hashing with bcrypt

    Args:
        signup_data: User signup information (email, name, password)
        session: Database session

    Returns:
        TokenResponse with user data, JWT token, and expiration

    Raises:
        HTTPException 409: Email already registered
        HTTPException 422: Invalid input data
    """
    # Normalize email to lowercase for case-insensitive comparison
    email_lower = signup_data.email.lower()

    # Check if user already exists (case-insensitive)
    statement = select(User).where(User.email == email_lower)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(signup_data.password)

    # Create new user
    new_user = User(
        email=email_lower,
        name=signup_data.name,
        hashed_password=hashed_password,
        email_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Save to database
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token
    # Constitution SR-003: Use BETTER_AUTH_SECRET
    # Constitution SR-006: Include user_id in 'sub' claim
    token_expiration = datetime.utcnow() + timedelta(days=7)
    token_payload = {
        "sub": str(new_user.id),
        "email": new_user.email,
        "exp": token_expiration
    }
    token = jwt.encode(token_payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

    # Return response
    return TokenResponse(
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            email_verified=new_user.email_verified,
            created_at=new_user.created_at
        ),
        token=token,
        expires_at=token_expiration
    )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token.

    Constitution SR-001: Email/password authentication
    Constitution SR-003: JWT token generation with BETTER_AUTH_SECRET
    Constitution SR-004: Invalid credentials return 401 Unauthorized

    Args:
        login_data: User login credentials (email, password)
        session: Database session

    Returns:
        TokenResponse with user data, JWT token, and expiration

    Raises:
        HTTPException 401: Invalid email or password
        HTTPException 422: Invalid input data
    """
    # Normalize email to lowercase for case-insensitive comparison
    email_lower = login_data.email.lower()

    # Find user by email (case-insensitive)
    statement = select(User).where(User.email == email_lower)
    user = session.exec(statement).first()

    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    # Constitution SR-003: Use BETTER_AUTH_SECRET
    # Constitution SR-006: Include user_id in 'sub' claim
    token_expiration = datetime.utcnow() + timedelta(days=7)
    token_payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": token_expiration
    }
    token = jwt.encode(token_payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

    # Return response
    return TokenResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            email_verified=user.email_verified,
            created_at=user.created_at
        ),
        token=token,
        expires_at=token_expiration
    )

@router.post("/logout", response_model=dict, status_code=status.HTTP_200_OK)
async def logout():
    """
    Logout user (client-side token removal).

    Since we use stateless JWT tokens, logout is primarily handled client-side
    by removing the token from storage. This endpoint exists for API consistency
    and potential future token blacklisting implementation.

    Constitution SR-002: JWT tokens are stateless

    Returns:
        Success message

    Note:
        - Client must remove token from localStorage
        - Token remains valid until expiration (7 days)
        - Future: Implement token blacklist for immediate invalidation
    """
    return {
        "message": "Logout successful. Please remove token from client storage."
    }
