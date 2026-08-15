from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-with-enough-entropy-for-unit-tests"
os.environ["GEMINI_API_KEY"] = ""

from app.core.database import db_session
from app.infrastructure.orm.base import Base
import app.infrastructure.orm.models  # noqa: F401
from app.main import create_app


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def client(session_factory) -> AsyncGenerator[AsyncClient, None]:
    async def override_db():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app = create_app()
    app.dependency_overrides[db_session] = override_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as api:
        yield api
    app.dependency_overrides.clear()


async def register_user(
    client: AsyncClient,
    email: str = "user@example.com",
    password: str = "password123",
    full_name: str = "Test User",
) -> dict:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": full_name},
    )
    assert response.status_code == 201, response.text
    return response.json()


async def auth_headers(client: AsyncClient, email: str = "user@example.com") -> dict[str, str]:
    auth = await register_user(client, email=email)
    return {"Authorization": f"Bearer {auth['access_token']}"}

