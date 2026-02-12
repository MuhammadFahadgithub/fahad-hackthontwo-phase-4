"""
Database connection and session management.

Provides SQLModel engine with connection pooling for Neon PostgreSQL.
"""
from sqlmodel import Session, create_engine
from app.config import settings

# Create engine with Neon-optimized settings
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before using
    pool_size=5,          # Connection pool size
    max_overflow=10,      # Max connections beyond pool_size
    pool_recycle=3600,    # Recycle connections after 1 hour
    connect_args={
        "sslmode": "require",  # Require SSL for Neon
        "connect_timeout": 10,  # Connection timeout
    }
)


def get_session():
    """
    Dependency for database session.

    Yields a SQLModel session that automatically commits on success
    and rolls back on error.
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Initialize database (create tables).

    This is called on application startup to ensure all tables exist.
    In production, use Alembic migrations instead.
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
