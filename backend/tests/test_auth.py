from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.conftest import register_user

pytestmark = pytest.mark.asyncio


async def test_register_returns_tokens_and_user(client: AsyncClient):
    data = await register_user(client, "register@example.com")
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["user"]["email"] == "register@example.com"
    assert data["user"]["is_onboarded"] is False


async def test_register_rejects_duplicate_email(client: AsyncClient):
    await register_user(client, "duplicate@example.com")
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123", "full_name": "User"},
    )
    assert response.status_code == 409


async def test_login_refresh_and_me(client: AsyncClient):
    auth = await register_user(client, "login@example.com", "password123")

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["email"] == "login@example.com"

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": auth["refresh_token"]},
    )
    assert refresh.status_code == 200
    assert refresh.json()["user"]["email"] == "login@example.com"

    me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {auth['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == "login@example.com"


async def test_login_rejects_bad_password(client: AsyncClient):
    await register_user(client, "bad-password@example.com", "password123")
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "bad-password@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401

