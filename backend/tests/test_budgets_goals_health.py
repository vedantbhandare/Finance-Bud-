from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers

pytestmark = pytest.mark.asyncio


async def test_goal_crud_and_contribution(client: AsyncClient):
    headers = await auth_headers(client, "goals@example.com")

    created = await client.post(
        "/api/v1/goals",
        json={"name": "Emergency", "target_amount": "10000.00"},
        headers=headers,
    )
    assert created.status_code == 201
    goal_id = created.json()["id"]

    contributed = await client.post(
        f"/api/v1/goals/{goal_id}/contribute",
        json={"amount": "2500.00", "notes": "First deposit"},
        headers=headers,
    )
    assert contributed.status_code == 200
    assert contributed.json()["current_amount"] == "2500.00"
    assert contributed.json()["progress_pct"] == 25.0

    listed = await client.get("/api/v1/goals?status_filter=active", headers=headers)
    assert len(listed.json()) == 1

    updated = await client.patch(f"/api/v1/goals/{goal_id}", json={"status": "paused"}, headers=headers)
    assert updated.json()["status"] == "paused"

    deleted = await client.delete(f"/api/v1/goals/{goal_id}", headers=headers)
    assert deleted.status_code == 204


async def test_budget_generation_and_health_score(client: AsyncClient):
    headers = await auth_headers(client, "budget@example.com")
    await client.post("/api/v1/onboarding/income", json={"amount": "90000.00"}, headers=headers)
    await client.post(
        "/api/v1/onboarding/expenses",
        json={"expenses": [{"description": "Rent", "amount": "25000.00", "category_name": "Rent/Housing"}]},
        headers=headers,
    )

    empty = await client.get("/api/v1/budgets/current", headers=headers)
    assert empty.status_code == 200
    assert empty.json()["budget"] is None

    generated = await client.post("/api/v1/budgets/generate", headers=headers)
    assert generated.status_code == 200, generated.text
    budget = generated.json()["budget_plan"]
    assert budget["total_income"] == "90000.00"
    assert len(budget["allocations"]) > 0

    current = await client.get("/api/v1/budgets/current", headers=headers)
    assert current.json()["budget"]["id"] == budget["id"]

    health = await client.get("/api/v1/health/score", headers=headers)
    assert health.status_code == 200
    assert 0 <= health.json()["overall_score"] <= 100
    assert "recommendations" in health.json()

