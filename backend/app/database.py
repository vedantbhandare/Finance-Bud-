"""Async SQLAlchemy engine, session factory, and FastAPI dependency.

Supports SQLite (local dev, zero setup) and PostgreSQL (production).
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

_settings = get_settings()

_is_sqlite = _settings.database_url.startswith("sqlite")

_engine_kwargs: dict = {
    "echo": _settings.database_echo,
}

if _is_sqlite:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    _engine_kwargs["pool_size"] = 20
    _engine_kwargs["max_overflow"] = 10
    _engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(_settings.database_url, **_engine_kwargs)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields an async session with auto commit/rollback."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables() -> None:
    """Create all tables (SQLite dev mode — Alembic handles production)."""
    from app.models.base import Base

    # Import all model modules so they register with Base.metadata
    import app.models.user  # noqa: F401
    import app.models.transaction  # noqa: F401
    import app.models.goal  # noqa: F401
    import app.models.budget  # noqa: F401
    import app.models.conversation  # noqa: F401
    import app.models.health  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
