from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers

pytestmark = pytest.mark.asyncio


async def test_create_list_update_delete_transaction(client: AsyncClient):
    headers = await auth_headers(client, "transactions@example.com")

    created = await client.post(
        "/api/v1/transactions",
        json={
            "amount": "450.50",
            "type": "expense",
            "description": "Swiggy dinner",
            "transaction_date": "2026-08-10",
        },
        headers=headers,
    )
    assert created.status_code == 201, created.text
    transaction = created.json()
    assert transaction["type"] == "expense"
    assert transaction["category_name"] == "Swiggy/Zomato"

    listed = await client.get("/api/v1/transactions?type=expense", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    updated = await client.patch(
        f"/api/v1/transactions/{transaction['id']}",
        json={"amount": "500.00", "category_name": "Eating Out"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["amount"] == "500.00"
    assert updated.json()["category_name"] == "Eating Out"

    deleted = await client.delete(f"/api/v1/transactions/{transaction['id']}", headers=headers)
    assert deleted.status_code == 204

    missing = await client.get(f"/api/v1/transactions/{transaction['id']}", headers=headers)
    assert missing.status_code == 404


async def test_monthly_summary_and_user_isolation(client: AsyncClient):
    headers_a = await auth_headers(client, "summary-a@example.com")
    headers_b = await auth_headers(client, "summary-b@example.com")

    await client.post(
        "/api/v1/transactions",
        json={"amount": "2000", "type": "income", "description": "Salary", "transaction_date": "2026-08-01"},
        headers=headers_a,
    )
    await client.post(
        "/api/v1/transactions",
        json={"amount": "300", "type": "expense", "description": "Uber ride", "transaction_date": "2026-08-02"},
        headers=headers_a,
    )

    summary_a = await client.get("/api/v1/transactions/summary/monthly?year=2026&month=8", headers=headers_a)
    assert summary_a.status_code == 200
    assert summary_a.json()["total_income"] == "2000.00"
    assert summary_a.json()["total_expenses"] == "300.00"
    assert summary_a.json()["by_category"][0]["category_name"] == "Cab/Uber/Ola"

    summary_b = await client.get("/api/v1/transactions/summary/monthly?year=2026&month=8", headers=headers_b)
    assert summary_b.json()["total_income"] == "0.00"
    assert summary_b.json()["total_expenses"] == "0.00"

