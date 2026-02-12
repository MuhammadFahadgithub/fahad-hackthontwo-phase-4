from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from contextlib import contextmanager


# Get database URL from environment, with a default for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Create database tables based on SQLModel models
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    with Session(engine) as session:
        yield session


# Additional utility functions
def get_session_direct():
    """
    Get a direct session (not as a generator) - useful for scripts
    """
    return Session(engine)