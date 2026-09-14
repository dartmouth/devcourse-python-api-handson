"""Database engine, session factory, and table creation.

Checkpoint 3 introduces SQLite persistence with SQLModel (which wraps
SQLAlchemy 2.x). We use a single file-based SQLite database so data survives
restarts. Tables are created with ``SQLModel.metadata.create_all`` to keep the
workshop focused (no migrations).
"""

import os
from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

# The database URL can be overridden (the test suite points it at a temporary
# database in Checkpoint 7).
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dartmouth_places.db")

# check_same_thread=False lets the SQLite connection be shared across the
# threads FastAPI's TestClient and Uvicorn workers use.
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """Create all tables. Safe to call repeatedly."""
    # Importing models registers them on SQLModel.metadata.
    from app import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """FastAPI dependency that yields a database session per request."""
    with Session(engine) as session:
        yield session
