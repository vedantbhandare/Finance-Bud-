"""Integration tests — Auth API (/api/v1/auth/*)."""
import pytest
from httpx import AsyncClient

from tests.conftest import register_user


class TestRegister:
    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "securepassword",
            "full_name": "New User",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["full_name"] == "New User"
        assert data["user"]["is_active"] is True
        assert data["user"]["is_onboarded"] is False

    @pytest.mark.asyncio
    async def test_register_duplicate_email_returns_409(self, client: AsyncClient):
        await register_user(client)
        resp = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "anotherpassword",
            "full_name": "Another User",
        })
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_register_short_password_returns_422(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "short@example.com",
            "password": "123",
            "full_name": "Short",
        })
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email_returns_422(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "validpassword",
            "full_name": "Test",
        })
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_empty_name_returns_422(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "emptyname@example.com",
            "password": "validpassword",
            "full_name": "",
        })
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_returns_uuid_for_user_id(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "uuid@example.com",
            "password": "password123",
            "full_name": "UUID Test",
        })
        assert resp.status_code == 201
        import uuid
        user_id = resp.json()["user"]["id"]
        uuid.UUID(user_id)  # raises if invalid


class TestLogin:
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient):
        await register_user(client)
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data

    @pytest.mark.asyncio
    async def test_login_wrong_password_returns_401(self, client: AsyncClient):
        await register_user(client)
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_login_unknown_email_returns_401(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/login", json={
            "email": "ghost@example.com",
            "password": "password123",
        })
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_login_missing_fields_returns_422(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/login", json={"email": "test@example.com"})
        assert resp.status_code == 422


class TestRefreshToken:
    @pytest.mark.asyncio
    async def test_refresh_returns_new_access_token(self, client: AsyncClient):
        tokens = await register_user(client)
        resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": tokens["refresh_token"]
        })
        assert resp.status_code == 200
        data = resp.json()
        # Just check a valid token is returned (JWT is deterministic within the same second)
        assert "access_token" in data
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 20

    @pytest.mark.asyncio
    async def test_refresh_with_invalid_token_returns_401(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": "totally.invalid.token"
        })
        assert resp.status_code == 401


class TestGetMe:
    @pytest.mark.asyncio
    async def test_get_me_returns_user(self, client: AsyncClient):
        tokens = await register_user(client, email="me@example.com", name="Me User")
        resp = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "me@example.com"
        assert data["full_name"] == "Me User"

    @pytest.mark.asyncio
    async def test_get_me_without_token_returns_403_or_401(self, client: AsyncClient):
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_get_me_with_invalid_token_returns_401_or_403(self, client: AsyncClient):
        resp = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer bad.token.here"},
        )
        assert resp.status_code in (401, 403)
