"""
Database configuration module for the FastAPI project.

Supports PostgreSQL and SQLite. Adjust the DATABASE_URL as needed.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =============================================================================
# Database Connection Configuration
# =============================================================================

# Example:
# For PostgreSQL: 'postgresql://user:password@localhost/dbname'
# For SQLite: 'sqlite:///./db.sqlite3'
DATABASE_URL = 'sqlite:///./db.sqlite3'

# Additional arguments for SQLite to prevent threading issues
SQLITE_CONNECT_ARGS = {'check_same_thread': False}
connect_args = SQLITE_CONNECT_ARGS if DATABASE_URL.startswith('sqlite') else {}

# =============================================================================
# SQLAlchemy Engine and Session
# =============================================================================

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create a configured session class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =============================================================================
# Base Model Declaration
# =============================================================================

# Base class for all SQLAlchemy models
Base = declarative_base()
