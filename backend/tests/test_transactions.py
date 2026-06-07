"""Integration tests — Transactions API (/api/v1/transactions/*)."""
from datetime import date

import pytest
from httpx import AsyncClient

from tests.conftest import register_user


async def _auth(client, email="txn@example.com"):
    tokens = await register_user(client, email=email)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


EXPENSE_PAYLOAD = {
    "amount": 500.00,
    "type": "expense",
    "description": "Swiggy dinner",
    "merchant": "Swiggy",
    "transaction_date": str(date.today()),
}

INCOME_PAYLOAD = {
    "amount": 80000.00,
    "type": "income",
    "description": "Monthly salary",
    "merchant": "Employer",
    "transaction_date": str(date.today()),
}


class TestCreateTransaction:
    @pytest.mark.asyncio
    async def test_create_expense_success(self, client: AsyncClient):
        headers = await _auth(client)
        resp = await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["type"] == "expense"
        assert float(data["amount"]) == 500.00
        assert data["description"] == "Swiggy dinner"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_income_success(self, client: AsyncClient):
        headers = await _auth(client, email="income@example.com")
        resp = await client.post("/api/v1/transactions", json=INCOME_PAYLOAD, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["type"] == "income"

    @pytest.mark.asyncio
    async def test_create_transaction_requires_auth(self, client: AsyncClient):
        resp = await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD)
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_create_transaction_negative_amount_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="neg@example.com")
        resp = await client.post("/api/v1/transactions", json={
            **EXPENSE_PAYLOAD, "amount": -100
        }, headers=headers)
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_create_transaction_invalid_type_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="badtype@example.com")
        resp = await client.post("/api/v1/transactions", json={
            **EXPENSE_PAYLOAD, "type": "investment"
        }, headers=headers)
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_create_transaction_zero_amount_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="zero@example.com")
        resp = await client.post("/api/v1/transactions", json={
            **EXPENSE_PAYLOAD, "amount": 0
        }, headers=headers)
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_create_transaction_no_date_defaults_to_today(self, client: AsyncClient):
        headers = await _auth(client, email="nodate@example.com")
        payload = {k: v for k, v in EXPENSE_PAYLOAD.items() if k != "transaction_date"}
        resp = await client.post("/api/v1/transactions", json=payload, headers=headers)
        assert resp.status_code == 201
        assert resp.json()["transaction_date"] == str(date.today())


class TestListTransactions:
    @pytest.mark.asyncio
    async def test_list_transactions_empty(self, client: AsyncClient):
        headers = await _auth(client, email="list@example.com")
        resp = await client.get("/api/v1/transactions", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    @pytest.mark.asyncio
    async def test_list_transactions_returns_created_items(self, client: AsyncClient):
        headers = await _auth(client, email="listfull@example.com")
        await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers)
        await client.post("/api/v1/transactions", json=INCOME_PAYLOAD, headers=headers)

        resp = await client.get("/api/v1/transactions", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["total"] == 2

    @pytest.mark.asyncio
    async def test_list_transactions_pagination(self, client: AsyncClient):
        headers = await _auth(client, email="page@example.com")
        for i in range(5):
            await client.post("/api/v1/transactions", json={
                **EXPENSE_PAYLOAD, "amount": 100 + i
            }, headers=headers)

        resp = await client.get("/api/v1/transactions?page=1&limit=2", headers=headers)
        data = resp.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["pages"] == 3

    @pytest.mark.asyncio
    async def test_list_transactions_filter_by_type(self, client: AsyncClient):
        headers = await _auth(client, email="filtertype@example.com")
        await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers)
        await client.post("/api/v1/transactions", json=INCOME_PAYLOAD, headers=headers)

        resp = await client.get("/api/v1/transactions?type=expense", headers=headers)
        data = resp.json()
        assert all(t["type"] == "expense" for t in data["items"])

    @pytest.mark.asyncio
    async def test_list_transactions_isolated_per_user(self, client: AsyncClient):
        """User A cannot see User B's transactions."""
        headers_a = await _auth(client, email="usera@example.com")
        headers_b = await _auth(client, email="userb@example.com")
        await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers_a)

        resp = await client.get("/api/v1/transactions", headers=headers_b)
        assert resp.json()["total"] == 0

    @pytest.mark.asyncio
    async def test_list_transactions_requires_auth(self, client: AsyncClient):
        resp = await client.get("/api/v1/transactions")
        assert resp.status_code in (401, 403)


class TestGetTransaction:
    @pytest.mark.asyncio
    async def test_get_transaction_by_id(self, client: AsyncClient):
        headers = await _auth(client, email="getone@example.com")
        create_resp = await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers)
        txn_id = create_resp.json()["id"]

        resp = await client.get(f"/api/v1/transactions/{txn_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == txn_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_transaction_returns_404(self, client: AsyncClient):
        headers = await _auth(client, email="getmissing@example.com")
        resp = await client.get(
            "/api/v1/transactions/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_cannot_get_another_users_transaction(self, client: AsyncClient):
        headers_a = await _auth(client, email="owner@example.com")
        headers_b = await _auth(client, email="thief@example.com")
        create_resp = await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers_a)
        txn_id = create_resp.json()["id"]

        resp = await client.get(f"/api/v1/transactions/{txn_id}", headers=headers_b)
        assert resp.status_code == 404


class TestUpdateTransaction:
    @pytest.mark.asyncio
    async def test_update_transaction_amount(self, client: AsyncClient):
        headers = await _auth(client, email="update@example.com")
        create_resp = await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers)
        txn_id = create_resp.json()["id"]

        resp = await client.put(f"/api/v1/transactions/{txn_id}", json={"amount": 999.00}, headers=headers)
        assert resp.status_code == 200
        assert float(resp.json()["amount"]) == 999.00

    @pytest.mark.asyncio
    async def test_update_transaction_description(self, client: AsyncClient):
        headers = await _auth(client, email="updatedesc@example.com")
        create_resp = await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers)
        txn_id = create_resp.json()["id"]

        resp = await client.put(f"/api/v1/transactions/{txn_id}",
                                json={"description": "Updated"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["description"] == "Updated"

    @pytest.mark.asyncio
    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        headers = await _auth(client, email="updatemiss@example.com")
        resp = await client.put(
            "/api/v1/transactions/00000000-0000-0000-0000-000000000000",
            json={"amount": 100},
            headers=headers,
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_update_type_income_to_expense(self, client: AsyncClient):
        headers = await _auth(client, email="updatetype@example.com")
        create_resp = await client.post("/api/v1/transactions", json=INCOME_PAYLOAD, headers=headers)
        txn_id = create_resp.json()["id"]

        resp = await client.put(f"/api/v1/transactions/{txn_id}",
                                json={"type": "expense"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["type"] == "expense"


class TestDeleteTransaction:
    @pytest.mark.asyncio
    async def test_delete_transaction_success(self, client: AsyncClient):
        headers = await _auth(client, email="delete@example.com")
        create_resp = await client.post("/api/v1/transactions", json=EXPENSE_PAYLOAD, headers=headers)
        txn_id = create_resp.json()["id"]

        resp = await client.delete(f"/api/v1/transactions/{txn_id}", headers=headers)
        assert resp.status_code == 204

        # Verify it's gone
        get_resp = await client.get(f"/api/v1/transactions/{txn_id}", headers=headers)
        assert get_resp.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_nonexistent_returns_404(self, client: AsyncClient):
        headers = await _auth(client, email="deletemiss@example.com")
        resp = await client.delete(
            "/api/v1/transactions/00000000-0000-0000-0000-000000000000",
            headers=headers,
        )
        assert resp.status_code == 404


class TestMonthlySummary:
    @pytest.mark.asyncio
    async def test_monthly_summary_empty(self, client: AsyncClient):
        headers = await _auth(client, email="summary@example.com")
        resp = await client.get("/api/v1/transactions/summary/monthly?year=2026&month=6",
                                headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_income"] == 0
        assert data["total_expenses"] == 0
        assert data["net"] == 0

    @pytest.mark.asyncio
    async def test_monthly_summary_with_transactions(self, client: AsyncClient):
        headers = await _auth(client, email="sumfull@example.com")
        today = date.today()
        await client.post("/api/v1/transactions", json={
            "amount": 80000, "type": "income",
            "description": "Salary", "transaction_date": str(today),
        }, headers=headers)
        await client.post("/api/v1/transactions", json={
            "amount": 5000, "type": "expense",
            "description": "Rent", "transaction_date": str(today),
        }, headers=headers)

        resp = await client.get(
            f"/api/v1/transactions/summary/monthly?year={today.year}&month={today.month}",
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert float(data["total_income"]) == pytest.approx(80000)
        assert float(data["total_expenses"]) == pytest.approx(5000)
        assert float(data["net"]) == pytest.approx(75000)

    @pytest.mark.asyncio
    async def test_monthly_summary_requires_year_and_month(self, client: AsyncClient):
        headers = await _auth(client, email="sumparams@example.com")
        resp = await client.get("/api/v1/transactions/summary/monthly", headers=headers)
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_monthly_summary_invalid_month_returns_422(self, client: AsyncClient):
        headers = await _auth(client, email="summonth@example.com")
        resp = await client.get("/api/v1/transactions/summary/monthly?year=2026&month=13",
                                headers=headers)
        assert resp.status_code == 422
