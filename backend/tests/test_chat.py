from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers

pytestmark = pytest.mark.asyncio


async def test_chat_fallback_persists_conversation_and_messages(client: AsyncClient):
    headers = await auth_headers(client, "chat@example.com")

    response = await client.post(
        "/api/v1/chat/message",
        json={"message": "How am I doing this month?"},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["conversation_id"]
    assert body["metadata"]["model"] == "fallback"

    conversations = await client.get("/api/v1/chat/conversations", headers=headers)
    assert len(conversations.json()) == 1

    messages = await client.get(
        f"/api/v1/chat/conversations/{body['conversation_id']}/messages",
        headers=headers,
    )
    assert [message["role"] for message in messages.json()] == ["user", "assistant"]

