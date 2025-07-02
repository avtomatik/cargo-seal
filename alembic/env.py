from logging.config import fileConfig
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, pool

from alembic import context
from app.database import Base  # declarative_base()

# =============================================================================
# Project path setup
# =============================================================================

# Base directory: /your-project-root/
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / '.env'

# Load environment variables from .env
load_dotenv(dotenv_path=ENV_PATH)

# =============================================================================
# Application-specific imports
# Make sure 'app' is a proper Python module with __init__.py
# =============================================================================

# =============================================================================
# Alembic Config
# =============================================================================
config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

# Use dotenv-loaded variable directly
DATABASE_URL = getenv('DATABASE_URL')
if DATABASE_URL:
    config.set_main_option('sqlalchemy.url', DATABASE_URL)

target_metadata = Base.metadata

# =============================================================================
# Migration logic
# =============================================================================


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


# =============================================================================
# Entrypoint
# =============================================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
