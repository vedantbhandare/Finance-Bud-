from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers

pytestmark = pytest.mark.asyncio


async def test_full_onboarding_flow(client: AsyncClient):
    headers = await auth_headers(client, "onboarding@example.com")

    income = await client.post(
        "/api/v1/onboarding/income",
        json={"amount": "75000.00", "frequency": "monthly", "pay_day": 5},
        headers=headers,
    )
    assert income.status_code == 200

    expenses = await client.post(
        "/api/v1/onboarding/expenses",
        json={
            "expenses": [
                {"description": "Rent", "amount": "25000.00", "category_name": "Rent/Housing"},
                {"description": "Internet", "amount": "1200.00", "category_name": "Phone/Internet"},
            ]
        },
        headers=headers,
    )
    assert expenses.status_code == 200

    goals = await client.post(
        "/api/v1/onboarding/goals",
        json={"goals": [{"name": "Emergency Fund", "target_amount": "120000.00"}]},
        headers=headers,
    )
    assert goals.status_code == 200

    style = await client.post(
        "/api/v1/onboarding/spending-style",
        json={"overspending_categories": ["Swiggy/Zomato"], "ai_personality": "balanced"},
        headers=headers,
    )
    assert style.status_code == 200

    complete = await client.post("/api/v1/onboarding/complete", headers=headers)
    assert complete.status_code == 200

    me = await client.get("/api/v1/auth/me", headers=headers)
    assert me.json()["is_onboarded"] is True
    assert me.json()["monthly_salary"] == "75000.00"

