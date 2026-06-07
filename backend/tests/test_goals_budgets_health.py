"""Integration tests — Goals, Budgets, and Health APIs."""
from datetime import date

import pytest
from httpx import AsyncClient

from tests.conftest import register_user


async def _auth(client, email="user@example.com"):
    tokens = await register_user(client, email=email)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


# ══════════════════════════════════════════════════════════════════════════════
# Goals
# ══════════════════════════════════════════════════════════════════════════════

GOAL_PAYLOAD = {
    "name": "Emergency Fund",
    "target_amount": 100000,
    "target_date": "2027-12-31",
    "description": "6 months of expenses",
}


class TestCreateGoal:
    @pytest.mark.asyncio
    async def test_create_goal_success(self, client: AsyncClient):
        headers = await _auth(client, email="goalcreate@example.com")
        resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Emergency Fund"
        assert float(data["target_amount"]) == 100000
        assert float(data["current_amount"]) == 0
        assert data["status"] == "active"
        assert float(data["progress_pct"]) == 0

    @pytest.mark.asyncio
    async def test_create_goal_without_date(self, client: AsyncClient):
        headers = await _auth(client, email="goalnod@example.com")
        resp = await client.post("/api/v1/goals", json={
            "name": "Laptop", "target_amount": 80000
        }, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["target_date"] is None

    @pytest.mark.asyncio
    async def test_create_goal_requires_auth(self, client: AsyncClient):
        resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD)
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_create_goal_negative_amount_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="goalneg@example.com")
        resp = await client.post("/api/v1/goals", json={
            **GOAL_PAYLOAD, "target_amount": -1000
        }, headers=headers)
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_create_goal_empty_name_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="goalempty@example.com")
        resp = await client.post("/api/v1/goals", json={
            **GOAL_PAYLOAD, "name": ""
        }, headers=headers)
        assert resp.status_code == 422


class TestListGoals:
    @pytest.mark.asyncio
    async def test_list_goals_empty(self, client: AsyncClient):
        headers = await _auth(client, email="goallist@example.com")
        resp = await client.get("/api/v1/goals", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []

    @pytest.mark.asyncio
    async def test_list_goals_returns_created_items(self, client: AsyncClient):
        headers = await _auth(client, email="goallistfull@example.com")
        await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        await client.post("/api/v1/goals", json={
            "name": "Car", "target_amount": 500000
        }, headers=headers)

        resp = await client.get("/api/v1/goals", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    @pytest.mark.asyncio
    async def test_goals_isolated_per_user(self, client: AsyncClient):
        headers_a = await _auth(client, email="goalA@example.com")
        headers_b = await _auth(client, email="goalB@example.com")
        await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers_a)

        resp = await client.get("/api/v1/goals", headers=headers_b)
        assert resp.json() == []


class TestGetGoal:
    @pytest.mark.asyncio
    async def test_get_goal_by_id(self, client: AsyncClient):
        headers = await _auth(client, email="goalget@example.com")
        create_resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        goal_id = create_resp.json()["id"]

        resp = await client.get(f"/api/v1/goals/{goal_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == goal_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_goal_returns_404(self, client: AsyncClient):
        headers = await _auth(client, email="goalmiss@example.com")
        resp = await client.get(
            "/api/v1/goals/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert resp.status_code == 404


class TestUpdateGoal:
    @pytest.mark.asyncio
    async def test_update_goal_name(self, client: AsyncClient):
        headers = await _auth(client, email="goalupdate@example.com")
        create_resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        goal_id = create_resp.json()["id"]

        resp = await client.put(f"/api/v1/goals/{goal_id}",
                                json={"name": "Big Emergency Fund"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Big Emergency Fund"

    @pytest.mark.asyncio
    async def test_update_goal_target_amount(self, client: AsyncClient):
        headers = await _auth(client, email="goalamt@example.com")
        create_resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        goal_id = create_resp.json()["id"]

        resp = await client.put(f"/api/v1/goals/{goal_id}",
                                json={"target_amount": 200000}, headers=headers)
        assert resp.status_code == 200
        assert float(resp.json()["target_amount"]) == 200000

    @pytest.mark.asyncio
    async def test_update_nonexistent_goal_returns_404(self, client: AsyncClient):
        headers = await _auth(client, email="goalupdatemiss@example.com")
        resp = await client.put(
            "/api/v1/goals/00000000-0000-0000-0000-000000000000",
            json={"name": "Ghost"},
            headers=headers,
        )
        assert resp.status_code == 404


class TestDeleteGoal:
    @pytest.mark.asyncio
    async def test_delete_goal_success(self, client: AsyncClient):
        headers = await _auth(client, email="goaldelete@example.com")
        create_resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        goal_id = create_resp.json()["id"]

        resp = await client.delete(f"/api/v1/goals/{goal_id}", headers=headers)
        assert resp.status_code == 204

        get_resp = await client.get(f"/api/v1/goals/{goal_id}", headers=headers)
        assert get_resp.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_nonexistent_goal_returns_404(self, client: AsyncClient):
        headers = await _auth(client, email="goaldelmiss@example.com")
        resp = await client.delete(
            "/api/v1/goals/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert resp.status_code == 404


class TestContributeToGoal:
    @pytest.mark.asyncio
    async def test_contribute_updates_current_amount(self, client: AsyncClient):
        headers = await _auth(client, email="goalcontrib@example.com")
        create_resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        goal_id = create_resp.json()["id"]

        resp = await client.post(f"/api/v1/goals/{goal_id}/contribute", json={
            "amount": 10000,
            "contribution_date": str(date.today()),
        }, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert float(data["current_amount"]) == 10000
        assert float(data["progress_pct"]) == pytest.approx(10.0, rel=0.01)

    @pytest.mark.asyncio
    async def test_contribute_marks_goal_completed_when_target_reached(self, client: AsyncClient):
        headers = await _auth(client, email="goalcomplete@example.com")
        create_resp = await client.post("/api/v1/goals", json={
            "name": "Small Goal", "target_amount": 5000
        }, headers=headers)
        goal_id = create_resp.json()["id"]

        resp = await client.post(f"/api/v1/goals/{goal_id}/contribute", json={
            "amount": 5000, "contribution_date": str(date.today()),
        }, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "completed"

    @pytest.mark.asyncio
    async def test_multiple_contributions_accumulate(self, client: AsyncClient):
        headers = await _auth(client, email="goalaccum@example.com")
        create_resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        goal_id = create_resp.json()["id"]

        for _ in range(3):
            await client.post(f"/api/v1/goals/{goal_id}/contribute", json={
                "amount": 5000, "contribution_date": str(date.today()),
            }, headers=headers)

        resp = await client.get(f"/api/v1/goals/{goal_id}", headers=headers)
        assert float(resp.json()["current_amount"]) == 15000

    @pytest.mark.asyncio
    async def test_contribute_to_nonexistent_goal_returns_400(self, client: AsyncClient):
        headers = await _auth(client, email="goalcontribmiss@example.com")
        resp = await client.post(
            "/api/v1/goals/00000000-0000-0000-0000-000000000000/contribute",
            json={"amount": 1000, "contribution_date": str(date.today())},
            headers=headers,
        )
        assert resp.status_code in (400, 404)

    @pytest.mark.asyncio
    async def test_contribute_negative_amount_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="goalcontribneg@example.com")
        create_resp = await client.post("/api/v1/goals", json=GOAL_PAYLOAD, headers=headers)
        goal_id = create_resp.json()["id"]

        resp = await client.post(f"/api/v1/goals/{goal_id}/contribute", json={
            "amount": -500, "contribution_date": str(date.today()),
        }, headers=headers)
        assert resp.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# Budgets
# ══════════════════════════════════════════════════════════════════════════════

class TestBudgets:
    @pytest.mark.asyncio
    async def test_get_current_budget_when_none_exists(self, client: AsyncClient):
        headers = await _auth(client, email="budgetnone@example.com")
        resp = await client.get("/api/v1/budgets/current", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["budget"] is None
        assert "generate" in data["message"].lower() or "no active" in data["message"].lower()

    @pytest.mark.asyncio
    async def test_generate_budget_success(self, client: AsyncClient):
        headers = await _auth(client, email="budgetgen@example.com")
        # Set up income first
        await client.post("/api/v1/onboarding/income",
                          json={"amount": 80000, "pay_day": 1}, headers=headers)

        resp = await client.post("/api/v1/budgets/generate", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "budget_plan" in data
        plan = data["budget_plan"]
        assert len(plan) > 0

    @pytest.mark.asyncio
    async def test_generate_budget_requires_auth(self, client: AsyncClient):
        resp = await client.post("/api/v1/budgets/generate")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_get_current_budget_requires_auth(self, client: AsyncClient):
        resp = await client.get("/api/v1/budgets/current")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_generate_budget_with_no_income_uses_default(self, client: AsyncClient):
        """Budget generation falls back to 50000 default if no income set."""
        headers = await _auth(client, email="budgetdef@example.com")
        resp = await client.post("/api/v1/budgets/generate", headers=headers)
        assert resp.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
# Health Score
# ══════════════════════════════════════════════════════════════════════════════

class TestHealthScore:
    @pytest.mark.asyncio
    async def test_health_score_returns_structure(self, client: AsyncClient):
        headers = await _auth(client, email="health@example.com")
        resp = await client.get("/api/v1/health/score", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "overall_score" in data
        assert "label" in data
        assert "savings_rate" in data
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    @pytest.mark.asyncio
    async def test_health_score_is_bounded(self, client: AsyncClient):
        headers = await _auth(client, email="healthbound@example.com")
        resp = await client.get("/api/v1/health/score", headers=headers)
        score = resp.json()["overall_score"]
        assert 0 <= score <= 100

    @pytest.mark.asyncio
    async def test_health_label_is_valid(self, client: AsyncClient):
        headers = await _auth(client, email="healthlabel@example.com")
        resp = await client.get("/api/v1/health/score", headers=headers)
        label = resp.json()["label"]
        valid_labels = {"Excellent", "Good", "Fair", "Needs Attention", "Critical"}
        assert label in valid_labels

    @pytest.mark.asyncio
    async def test_health_score_requires_auth(self, client: AsyncClient):
        resp = await client.get("/api/v1/health/score")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_health_history_returns_empty_snapshots(self, client: AsyncClient):
        headers = await _auth(client, email="healthhist@example.com")
        resp = await client.get("/api/v1/health/history", headers=headers)
        assert resp.status_code == 200
        assert "snapshots" in resp.json()

    @pytest.mark.asyncio
    async def test_health_score_after_income_and_expenses(self, client: AsyncClient):
        """Score should reflect actual transaction data."""
        headers = await _auth(client, email="healthreal@example.com")
        today = date.today()
        # Add income
        await client.post("/api/v1/transactions", json={
            "amount": 80000, "type": "income",
            "description": "Salary", "transaction_date": str(today),
        }, headers=headers)
        # Add expenses (only 30% of income — good savings rate)
        await client.post("/api/v1/transactions", json={
            "amount": 24000, "type": "expense",
            "description": "Monthly expenses", "transaction_date": str(today),
        }, headers=headers)

        resp = await client.get("/api/v1/health/score", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        # Savings rate should be positive (income > expenses)
        assert data["savings_rate"] > 0
        assert data["spending_trend"] == "stable"


# ══════════════════════════════════════════════════════════════════════════════
# System Health Endpoint
# ══════════════════════════════════════════════════════════════════════════════

class TestSystemHealth:
    @pytest.mark.asyncio
    async def test_system_health_check(self, client: AsyncClient):
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "version" in data
