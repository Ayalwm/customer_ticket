import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from database import Base
from app import models  # Ensure models are imported to register metadata

# Alembic Config
config = context.config

# Set the database URL from the environment variable
database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ticket_db")
config.set_main_option("sqlalchemy.url", database_url)

# Setup Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata from Models
target_metadata = Base.metadata  # Ensure this has tables

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
