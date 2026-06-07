"""Shared test fixtures for Finance Buddy backend tests."""
import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# ── Force SQLite for all tests (no Postgres/Redis needed) ──────────────────
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_finance_buddy.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/99")   # unused – won't connect
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-at-least-32-characters-long")
os.environ.setdefault("GEMINI_API_KEY", "fake-key-for-tests")

from app.models.base import Base
from app.database import get_db_session
from app.main import create_app

TEST_DB_URL = "sqlite+aiosqlite:///./test_finance_buddy.db"


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """Create a fresh SQLite engine for each test function."""
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a clean AsyncSession per test."""
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_engine) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client wired to a fresh in-memory DB."""
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with async_session() as session:
            async with session.begin():
                yield session

    app = create_app()
    app.dependency_overrides[get_db_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


# ── Helpers ────────────────────────────────────────────────────────────────

async def register_user(client: AsyncClient, email: str = "test@example.com",
                         password: str = "password123", name: str = "Test User") -> dict:
    resp = await client.post("/api/v1/auth/register", json={
        "email": email, "password": password, "full_name": name
    })
    assert resp.status_code == 201, resp.text
    return resp.json()


async def auth_headers(client: AsyncClient, email: str = "test@example.com",
                        password: str = "password123") -> dict:
    """Register (if needed) then login and return bearer headers."""
    # Try login first
    resp = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    if resp.status_code != 200:
        await register_user(client, email, password)
        resp = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
