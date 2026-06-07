"""Integration tests — Onboarding API (/api/v1/onboarding/*)."""
import pytest
from httpx import AsyncClient

from tests.conftest import register_user


async def _auth(client, email="onboard@example.com"):
    tokens = await register_user(client, email=email)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


class TestIncomeSetup:
    @pytest.mark.asyncio
    async def test_setup_income_success(self, client: AsyncClient):
        headers = await _auth(client)
        resp = await client.post("/api/v1/onboarding/income", json={
            "amount": 75000,
            "pay_day": 1,
        }, headers=headers)
        assert resp.status_code == 200
        assert "saved" in resp.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_setup_income_requires_auth(self, client: AsyncClient):
        resp = await client.post("/api/v1/onboarding/income", json={"amount": 50000, "pay_day": 1})
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_setup_income_missing_body_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="income2@example.com")
        resp = await client.post("/api/v1/onboarding/income", json={}, headers=headers)
        assert resp.status_code == 422


class TestExpensesSetup:
    @pytest.mark.asyncio
    async def test_setup_expenses_success(self, client: AsyncClient):
        headers = await _auth(client, email="exp@example.com")
        resp = await client.post("/api/v1/onboarding/expenses", json={
            "expenses": [
                {"description": "Rent", "amount": 15000, "frequency": "monthly",
                 "start_date": "2026-01-01"},
                {"description": "Gym", "amount": 2000, "frequency": "monthly",
                 "start_date": "2026-01-01"},
            ]
        }, headers=headers)
        assert resp.status_code == 200
        assert "2" in resp.json()["message"]

    @pytest.mark.asyncio
    async def test_setup_expenses_empty_list(self, client: AsyncClient):
        headers = await _auth(client, email="noexp@example.com")
        resp = await client.post("/api/v1/onboarding/expenses", json={"expenses": []}, headers=headers)
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_setup_expenses_requires_auth(self, client: AsyncClient):
        resp = await client.post("/api/v1/onboarding/expenses", json={"expenses": []})
        assert resp.status_code in (401, 403)


class TestGoalsSetup:
    @pytest.mark.asyncio
    async def test_setup_goals_success(self, client: AsyncClient):
        headers = await _auth(client, email="goals@example.com")
        resp = await client.post("/api/v1/onboarding/goals", json={
            "goals": [
                {"name": "Emergency Fund", "target_amount": 100000, "target_date": "2027-01-01"},
                {"name": "Laptop", "target_amount": 80000},
            ]
        }, headers=headers)
        assert resp.status_code == 200
        assert "2" in resp.json()["message"]

    @pytest.mark.asyncio
    async def test_setup_goals_empty_list(self, client: AsyncClient):
        headers = await _auth(client, email="nogoals@example.com")
        resp = await client.post("/api/v1/onboarding/goals", json={"goals": []}, headers=headers)
        assert resp.status_code == 200


class TestSpendingStyleSetup:
    @pytest.mark.asyncio
    async def test_setup_spending_style_success(self, client: AsyncClient):
        headers = await _auth(client, email="style@example.com")
        resp = await client.post("/api/v1/onboarding/spending-style", json={
            "overspending_categories": ["Eating Out", "Shopping"]
        }, headers=headers)
        assert resp.status_code == 200
        assert "saved" in resp.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_setup_spending_style_empty_categories(self, client: AsyncClient):
        headers = await _auth(client, email="nostyle@example.com")
        resp = await client.post("/api/v1/onboarding/spending-style", json={
            "overspending_categories": []
        }, headers=headers)
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_setup_spending_style_upsert(self, client: AsyncClient):
        """Second call should update, not create a duplicate."""
        headers = await _auth(client, email="upsert@example.com")
        await client.post("/api/v1/onboarding/spending-style", json={
            "overspending_categories": ["Eating Out"]
        }, headers=headers)
        resp = await client.post("/api/v1/onboarding/spending-style", json={
            "overspending_categories": ["Shopping"]
        }, headers=headers)
        assert resp.status_code == 200


class TestCompleteOnboarding:
    @pytest.mark.asyncio
    async def test_complete_onboarding(self, client: AsyncClient):
        headers = await _auth(client, email="complete@example.com")
        resp = await client.post("/api/v1/onboarding/complete", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["onboarding_completed"] is True
        assert "Welcome" in data["message"]

    @pytest.mark.asyncio
    async def test_complete_onboarding_requires_auth(self, client: AsyncClient):
        resp = await client.post("/api/v1/onboarding/complete")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_full_onboarding_flow(self, client: AsyncClient):
        """End-to-end: register → income → expenses → goals → style → complete."""
        headers = await _auth(client, email="fullflow@example.com")

        # Step 1: Income
        r = await client.post("/api/v1/onboarding/income",
                              json={"amount": 80000, "pay_day": 1}, headers=headers)
        assert r.status_code == 200

        # Step 2: Expenses
        r = await client.post("/api/v1/onboarding/expenses", json={
            "expenses": [{"description": "Rent", "amount": 20000,
                          "frequency": "monthly", "start_date": "2026-01-01"}]
        }, headers=headers)
        assert r.status_code == 200

        # Step 3: Goals
        r = await client.post("/api/v1/onboarding/goals", json={
            "goals": [{"name": "Vacation", "target_amount": 50000}]
        }, headers=headers)
        assert r.status_code == 200

        # Step 4: Spending style
        r = await client.post("/api/v1/onboarding/spending-style", json={
            "overspending_categories": ["Eating Out"]
        }, headers=headers)
        assert r.status_code == 200

        # Step 5: Complete
        r = await client.post("/api/v1/onboarding/complete", headers=headers)
        assert r.status_code == 200
        assert r.json()["onboarding_completed"] is True
