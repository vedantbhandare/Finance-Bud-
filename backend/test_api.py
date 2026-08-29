"""Comprehensive End-to-End QA, Security, and Regression Test Battery."""
from __future__ import annotations

import asyncio
import os
import sys
from decimal import Decimal
from httpx import AsyncClient, ASGITransport

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-with-enough-entropy-for-unit-tests"
os.environ["GEMINI_API_KEY"] = ""

from app.main import create_app
from app.infrastructure.orm.base import Base
from app.infrastructure.orm.repositories import CategoryRepository
from app.core.database import db_session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
        self.results = []

    def record(self, test_name: str, passed: bool, error: str = ""):
        self.tests_run += 1
        if passed:
            self.passed += 1
            self.results.append((test_name, "PASS", ""))
            print(f"  [PASS] {test_name}")
        else:
            self.failed += 1
            self.results.append((test_name, "FAIL", error))
            print(f"  [FAIL] {test_name}: {error}")

    def assert_eq(self, test_name: str, actual, expected, message: str = ""):
        passed = actual == expected
        err = f"{message} (expected {expected!r}, got {actual!r})" if not passed else ""
        self.record(test_name, passed, err)
        return passed

    def assert_true(self, test_name: str, condition: bool, message: str = ""):
        self.record(test_name, bool(condition), message if not condition else "")
        return bool(condition)


async def run_all_qa_tests():
    runner = TestRunner()
    
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    session_maker = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    
    # Seed system categories
    async with session_maker() as session:
        await CategoryRepository(session).ensure_system_categories()
        await session.commit()

    async def override_db():
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app = create_app()
    app.dependency_overrides[db_session] = override_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        
        print("\n=======================================================")
        print("1. AUTHENTICATION & AUTHORIZATION LIFECYCLE & SECURITY")
        print("=======================================================")
        
        # Test 1.1: Valid Registration
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={"email": "alice@example.com", "password": "Password123!", "full_name": "Alice Sharma"},
        )
        runner.assert_eq("1.1 Register valid user", reg_res.status_code, 201)
        alice_data = reg_res.json()
        alice_token = alice_data.get("access_token")
        alice_refresh = alice_data.get("refresh_token")
        alice_headers = {"Authorization": f"Bearer {alice_token}"}
        runner.assert_true("1.1 Token response structure", bool(alice_token and alice_refresh))

        # Test 1.2: Email normalization (spaces, case)
        reg_norm = await client.post(
            "/api/v1/auth/register",
            json={"email": "  ALICE2@EXAMPLE.COM  ", "password": "Password123!", "full_name": "Alice Two"},
        )
        runner.assert_eq("1.2 Register with uppercase & whitespace email", reg_norm.status_code, 201)
        runner.assert_eq("1.2 Normalized email", reg_norm.json()["user"]["email"], "alice2@example.com")

        # Test 1.3: Duplicate email rejection
        dup_res = await client.post(
            "/api/v1/auth/register",
            json={"email": "alice@example.com", "password": "AnotherPassword123!", "full_name": "Alice Clone"},
        )
        runner.assert_eq("1.3 Reject duplicate email (409 Conflict)", dup_res.status_code, 409)

        # Test 1.4: Invalid password length (< 8)
        short_pw = await client.post(
            "/api/v1/auth/register",
            json={"email": "short@example.com", "password": "short", "full_name": "Short Pw"},
        )
        runner.assert_eq("1.4 Reject short password (<8 chars, 422)", short_pw.status_code, 422)

        # Test 1.5: Invalid email format
        bad_email = await client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "Password123!", "full_name": "Bad Email"},
        )
        runner.assert_eq("1.5 Reject malformed email (422)", bad_email.status_code, 422)

        # Test 1.6: Valid Login
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": "alice@example.com", "password": "Password123!"},
        )
        runner.assert_eq("1.6 Login with valid credentials", login_res.status_code, 200)

        # Test 1.7: Login with wrong password
        bad_login = await client.post(
            "/api/v1/auth/login",
            json={"email": "alice@example.com", "password": "WrongPassword!"},
        )
        runner.assert_eq("1.7 Login with wrong password (401)", bad_login.status_code, 401)

        # Test 1.8: Login with non-existent user
        no_user_login = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@example.com", "password": "Password123!"},
        )
        runner.assert_eq("1.8 Login with non-existent user (401)", no_user_login.status_code, 401)

        # Test 1.9: Token Refresh with valid token
        ref_res = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": alice_refresh},
        )
        runner.assert_eq("1.9 Refresh token valid (200)", ref_res.status_code, 200)

        # Test 1.10: Token Refresh with invalid/tampered token
        bad_ref = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"},
        )
        runner.assert_eq("1.10 Refresh token invalid (401)", bad_ref.status_code, 401)

        # Test 1.11: Token Refresh using an Access Token instead of Refresh Token
        wrong_token_type = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": alice_token},
        )
        runner.assert_eq("1.11 Reject access token as refresh token (401)", wrong_token_type.status_code, 401)

        # Test 1.12: Protected endpoint without auth
        no_auth = await client.get("/api/v1/auth/me")
        runner.assert_true("1.12 Protected route without token returns 401/403", no_auth.status_code in [401, 403])

        # Test 1.13: Protected endpoint with valid auth
        me_res = await client.get("/api/v1/auth/me", headers=alice_headers)
        runner.assert_eq("1.13 Protected route /auth/me with valid token", me_res.status_code, 200)
        runner.assert_eq("1.13 User email in /auth/me", me_res.json()["email"], "alice@example.com")


        print("\n=======================================================")
        print("2. ONBOARDING WORKFLOW & CONFIGURATION")
        print("=======================================================")

        # Test 2.1: Income Setup
        inc_res = await client.post(
            "/api/v1/onboarding/income",
            json={"amount": "125000.00", "source_name": "Tech Salary", "frequency": "monthly", "pay_day": 1},
            headers=alice_headers,
        )
        runner.assert_eq("2.1 Setup income valid", inc_res.status_code, 200)

        # Test 2.2: Income Setup with invalid pay_day (> 28)
        bad_pay_day = await client.post(
            "/api/v1/onboarding/income",
            json={"amount": "125000.00", "pay_day": 31},
            headers=alice_headers,
        )
        runner.assert_eq("2.2 Reject invalid pay_day > 28 (422)", bad_pay_day.status_code, 422)

        # Test 2.3: Income Setup with negative amount
        neg_inc = await client.post(
            "/api/v1/onboarding/income",
            json={"amount": "-5000.00", "pay_day": 1},
            headers=alice_headers,
        )
        runner.assert_eq("2.3 Reject negative income amount (422)", neg_inc.status_code, 422)

        # Test 2.4: Expenses Setup
        exp_res = await client.post(
            "/api/v1/onboarding/expenses",
            json={
                "expenses": [
                    {"description": "House Rent", "amount": "30000.00", "frequency": "monthly", "category_name": "Rent"},
                    {"description": "Internet & Wifi", "amount": "1200.00", "frequency": "monthly", "category_name": "Utilities"},
                ]
            },
            headers=alice_headers,
        )
        runner.assert_eq("2.4 Setup recurring expenses", exp_res.status_code, 200)

        # Test 2.5: Goals Setup
        goals_setup = await client.post(
            "/api/v1/onboarding/goals",
            json={
                "goals": [
                    {"name": "Emergency Reserve", "target_amount": "300000.00", "target_date": "2027-12-31", "priority": 1},
                    {"name": "Goa Trip", "target_amount": "50000.00", "target_date": "2027-02-15", "priority": 2},
                ]
            },
            headers=alice_headers,
        )
        runner.assert_eq("2.5 Setup initial goals", goals_setup.status_code, 200)

        # Test 2.6: Spending Style Setup
        style_res = await client.post(
            "/api/v1/onboarding/spending-style",
            json={
                "overspending_categories": ["food", "shopping"],
                "ai_personality": "analytical",
            },
            headers=alice_headers,
        )
        runner.assert_eq("2.6 Setup spending style", style_res.status_code, 200)

        # Test 2.7: Complete Onboarding
        comp_res = await client.post("/api/v1/onboarding/complete", headers=alice_headers)
        runner.assert_eq("2.7 Complete onboarding", comp_res.status_code, 200)

        # Verify is_onboarded is now True
        me_updated = await client.get("/api/v1/auth/me", headers=alice_headers)
        runner.assert_eq("2.8 User is_onboarded state updated to True", me_updated.json()["is_onboarded"], True)
        runner.assert_eq("2.8 User monthly_salary persisted", Decimal(me_updated.json()["monthly_salary"]), Decimal("125000.00"))


        print("\n=======================================================")
        print("3. CATEGORIES")
        print("=======================================================")

        # Test 3.1: List Categories
        cat_res = await client.get("/api/v1/categories", headers=alice_headers)
        runner.assert_eq("3.1 List categories status", cat_res.status_code, 200)
        categories = cat_res.json()
        runner.assert_true("3.1 Returns at least 20 India-specific categories", len(categories) >= 20)
        cat_names = [c["name"] for c in categories]
        runner.assert_true("3.1 Contains Swiggy/Zomato", "Swiggy/Zomato" in cat_names or "Eating Out" in cat_names)
        runner.assert_true("3.1 Contains Rent/Housing", "Rent/Housing" in cat_names or "Rent" in cat_names)


        print("\n=======================================================")
        print("4. TRANSACTIONS CRUD, CATEGORIZATION & SUMMARY")
        print("=======================================================")

        # Test 4.1: Create expense with auto keyword categorization (Swiggy)
        tx1 = await client.post(
            "/api/v1/transactions",
            json={"amount": "850.00", "type": "expense", "description": "Swiggy Biryani Order", "transaction_date": "2026-08-05"},
            headers=alice_headers,
        )
        runner.assert_eq("4.1 Create expense with Swiggy description", tx1.status_code, 201)
        tx1_data = tx1.json()
        runner.assert_eq("4.1 Auto categorization to Swiggy/Zomato", tx1_data["category_name"], "Swiggy/Zomato")

        # Test 4.2: Create expense with Uber auto categorization
        tx2 = await client.post(
            "/api/v1/transactions",
            json={"amount": "420.00", "type": "expense", "description": "Uber ride to office", "transaction_date": "2026-08-06"},
            headers=alice_headers,
        )
        runner.assert_eq("4.2 Create expense with Uber description", tx2.status_code, 201)
        runner.assert_eq("4.2 Auto categorization to Cab/Uber/Ola", tx2.json()["category_name"], "Cab/Uber/Ola")

        # Test 4.3: Create salary income
        tx3 = await client.post(
            "/api/v1/transactions",
            json={"amount": "125000.00", "type": "income", "description": "Monthly Salary Credit", "transaction_date": "2026-08-01"},
            headers=alice_headers,
        )
        runner.assert_eq("4.3 Create income transaction", tx3.status_code, 201)
        runner.assert_eq("4.3 Auto categorization to Salary", tx3.json()["category_name"], "Salary")

        # Test 4.4: Reject zero amount transaction
        zero_tx = await client.post(
            "/api/v1/transactions",
            json={"amount": "0.00", "type": "expense", "description": "Zero test"},
            headers=alice_headers,
        )
        runner.assert_eq("4.4 Reject 0 amount transaction (422)", zero_tx.status_code, 422)

        # Test 4.5: Reject negative amount transaction
        neg_tx = await client.post(
            "/api/v1/transactions",
            json={"amount": "-100.00", "type": "expense", "description": "Negative test"},
            headers=alice_headers,
        )
        runner.assert_eq("4.5 Reject negative amount transaction (422)", neg_tx.status_code, 422)

        # Test 4.6: Reject invalid transaction type
        bad_type_tx = await client.post(
            "/api/v1/transactions",
            json={"amount": "500.00", "type": "bitcoin", "description": "Invalid type test"},
            headers=alice_headers,
        )
        runner.assert_eq("4.6 Reject invalid transaction type (422)", bad_type_tx.status_code, 422)

        # Test 4.7: List transactions with pagination & filter
        list_tx = await client.get("/api/v1/transactions?page=1&limit=10&type=expense", headers=alice_headers)
        runner.assert_eq("4.7 List transactions status", list_tx.status_code, 200)
        runner.assert_eq("4.7 Expense count matches", list_tx.json()["total"], 2)

        # Test 4.8: Get single transaction
        get_tx1 = await client.get(f"/api/v1/transactions/{tx1_data['id']}", headers=alice_headers)
        runner.assert_eq("4.8 Get single transaction", get_tx1.status_code, 200)
        runner.assert_eq("4.8 Get single transaction ID", get_tx1.json()["id"], tx1_data["id"])

        # Test 4.9: Update transaction
        upd_tx = await client.patch(
            f"/api/v1/transactions/{tx1_data['id']}",
            json={"amount": "920.00", "notes": "Added drinks"},
            headers=alice_headers,
        )
        runner.assert_eq("4.9 Update transaction status", upd_tx.status_code, 200)
        runner.assert_eq("4.9 Updated amount persisted", upd_tx.json()["amount"], "920.00")
        runner.assert_eq("4.9 Updated notes persisted", upd_tx.json()["notes"], "Added drinks")

        # Test 4.10: Monthly Summary computation
        summary_res = await client.get("/api/v1/transactions/summary/monthly?year=2026&month=8", headers=alice_headers)
        runner.assert_eq("4.10 Monthly summary status", summary_res.status_code, 200)
        summary_data = summary_res.json()
        runner.assert_eq("4.10 Total income in summary", summary_data["total_income"], "125000.00")
        runner.assert_eq("4.10 Total expenses in summary", summary_data["total_expenses"], "1340.00") # 920 + 420
        runner.assert_eq("4.10 Net savings in summary", summary_data["net"], "123660.00")
        runner.assert_true("4.10 Category breakdown exists", len(summary_data["by_category"]) >= 2)

        # Test 4.11: Delete transaction
        del_tx = await client.delete(f"/api/v1/transactions/{tx2.json()['id']}", headers=alice_headers)
        runner.assert_eq("4.11 Delete transaction (204)", del_tx.status_code, 204)

        # Test 4.12: Verify deleted transaction returns 404
        get_del_tx = await client.get(f"/api/v1/transactions/{tx2.json()['id']}", headers=alice_headers)
        runner.assert_eq("4.12 Deleted transaction is 404", get_del_tx.status_code, 404)


        print("\n=======================================================")
        print("5. BUDGET GENERATION & PACING")
        print("=======================================================")

        # Test 5.1: Generate Budget for Alice
        gen_budget = await client.post("/api/v1/budgets/generate", headers=alice_headers)
        runner.assert_eq("5.1 Generate budget status", gen_budget.status_code, 200)
        budget_plan = gen_budget.json()["budget_plan"]
        runner.assert_eq("5.1 Budget total income matches salary", budget_plan["total_income"], "125000.00")
        runner.assert_true("5.1 Allocations generated", len(budget_plan["allocations"]) > 0)

        # Test 5.2: Get current active budget
        curr_budget = await client.get("/api/v1/budgets/current", headers=alice_headers)
        runner.assert_eq("5.2 Get current budget status", curr_budget.status_code, 200)
        runner.assert_eq("5.2 Current budget plan ID matches generated", curr_budget.json()["budget"]["id"], budget_plan["id"])


        print("\n=======================================================")
        print("6. GOALS & ESCROWS (CRUD & CONTRIBUTIONS)")
        print("=======================================================")

        # Test 6.1: Create New Goal
        new_goal = await client.post(
            "/api/v1/goals",
            json={"name": "MacBook Pro M4", "target_amount": "200000.00", "target_date": "2027-06-30", "priority": 3},
            headers=alice_headers,
        )
        runner.assert_eq("6.1 Create goal status", new_goal.status_code, 201)
        goal_data = new_goal.json()
        runner.assert_eq("6.1 Initial goal current_amount", goal_data["current_amount"], "0.00")
        runner.assert_eq("6.1 Initial goal progress", goal_data["progress_pct"], 0.0)

        # Test 6.2: Contribute to Goal
        contrib_res = await client.post(
            f"/api/v1/goals/{goal_data['id']}/contribute",
            json={"amount": "50000.00", "notes": "First bonus contribution"},
            headers=alice_headers,
        )
        runner.assert_eq("6.2 Contribute to goal status", contrib_res.status_code, 200)
        contrib_data = contrib_res.json()
        runner.assert_eq("6.2 Goal current_amount after contribution", contrib_data["current_amount"], "50000.00")
        runner.assert_eq("6.2 Goal progress_pct after contribution", contrib_data["progress_pct"], 25.0)

        # Test 6.3: Contribute to complete the goal
        contrib_finish = await client.post(
            f"/api/v1/goals/{goal_data['id']}/contribute",
            json={"amount": "150000.00", "notes": "Final payment"},
            headers=alice_headers,
        )
        runner.assert_eq("6.3 Goal complete contribution status", contrib_finish.status_code, 200)
        runner.assert_eq("6.3 Goal status changes to completed", contrib_finish.json()["status"], "completed")
        runner.assert_eq("6.3 Goal progress_pct is 100%", contrib_finish.json()["progress_pct"], 100.0)

        # Test 6.4: Contribute to already completed goal (must reject)
        over_contrib = await client.post(
            f"/api/v1/goals/{goal_data['id']}/contribute",
            json={"amount": "1000.00"},
            headers=alice_headers,
        )
        runner.assert_eq("6.4 Reject contribution to completed goal (422/400)", over_contrib.status_code in [400, 422], True)

        # Test 6.5: List active goals filter
        list_goals = await client.get("/api/v1/goals?status_filter=active", headers=alice_headers)
        runner.assert_eq("6.5 List active goals status", list_goals.status_code, 200)
        active_names = [g["name"] for g in list_goals.json()]
        runner.assert_true("6.5 Completed goal excluded from active filter", "MacBook Pro M4" not in active_names)


        print("\n=======================================================")
        print("7. HEALTH SCORE & DIAGNOSTICS")
        print("=======================================================")

        # Test 7.1: Compute Health Score
        health_res = await client.get("/api/v1/health/score", headers=alice_headers)
        runner.assert_eq("7.1 Health score status", health_res.status_code, 200)
        h_data = health_res.json()
        runner.assert_true("7.1 Overall score between 0 and 100", 0 <= h_data["overall_score"] <= 100)
        runner.assert_true("7.1 Recommendations generated", len(h_data["recommendations"]) > 0)
        runner.assert_true("7.1 Spending trend generated", bool(h_data["spending_trend"]))


        print("\n=======================================================")
        print("8. AI FINANCIAL ADVISOR CHAT")
        print("=======================================================")

        # Test 8.1: Send Chat Message (New Conversation)
        chat1 = await client.post(
            "/api/v1/chat/message",
            json={"message": "Can I afford dinner at a luxury restaurant for Rs 5,000?"},
            headers=alice_headers,
        )
        runner.assert_eq("8.1 Send chat message status", chat1.status_code, 200)
        chat1_data = chat1.json()
        conv_id = chat1_data["conversation_id"]
        runner.assert_true("8.1 Reply non-empty", bool(chat1_data["reply"]))
        runner.assert_true("8.1 Conversation ID generated", bool(conv_id))

        # Test 8.2: Send follow-up in same conversation
        chat2 = await client.post(
            "/api/v1/chat/message",
            json={"message": "What is my current savings rate?", "conversation_id": conv_id},
            headers=alice_headers,
        )
        runner.assert_eq("8.2 Follow-up message in same conversation", chat2.status_code, 200)
        runner.assert_eq("8.2 Conversation ID persisted", chat2.json()["conversation_id"], conv_id)

        # Test 8.3: List user conversations
        convs_res = await client.get("/api/v1/chat/conversations", headers=alice_headers)
        runner.assert_eq("8.3 List conversations status", convs_res.status_code, 200)
        runner.assert_true("8.3 Found conversation in list", any(c["id"] == conv_id for c in convs_res.json()))

        # Test 8.4: Get messages for conversation
        msgs_res = await client.get(f"/api/v1/chat/conversations/{conv_id}/messages", headers=alice_headers)
        runner.assert_eq("8.4 Get conversation messages status", msgs_res.status_code, 200)
        runner.assert_eq("8.4 Message count in conversation is 4 (2 user, 2 assistant)", len(msgs_res.json()), 4)


        print("\n=======================================================")
        print("9. MULTI-TENANCY & IDOR SECURITY TESTING")
        print("=======================================================")

        # Create User Bob (Attacker / Separate Tenant)
        reg_bob = await client.post(
            "/api/v1/auth/register",
            json={"email": "bob@attacker.com", "password": "BobPassword123!", "full_name": "Bob Attacker"},
        )
        bob_token = reg_bob.json()["access_token"]
        bob_headers = {"Authorization": f"Bearer {bob_token}"}

        # Test 9.1: Bob tries to GET Alice's transaction
        idor_get_tx = await client.get(f"/api/v1/transactions/{tx1_data['id']}", headers=bob_headers)
        runner.assert_eq("9.1 IDOR Prevention: Bob cannot GET Alice's transaction (404)", idor_get_tx.status_code, 404)

        # Test 9.2: Bob tries to UPDATE Alice's transaction
        idor_patch_tx = await client.patch(
            f"/api/v1/transactions/{tx1_data['id']}",
            json={"amount": "1.00"},
            headers=bob_headers,
        )
        runner.assert_eq("9.2 IDOR Prevention: Bob cannot UPDATE Alice's transaction (404)", idor_patch_tx.status_code, 404)

        # Test 9.3: Bob tries to DELETE Alice's transaction
        idor_del_tx = await client.delete(f"/api/v1/transactions/{tx1_data['id']}", headers=bob_headers)
        runner.assert_eq("9.3 IDOR Prevention: Bob cannot DELETE Alice's transaction (404)", idor_del_tx.status_code, 404)

        # Test 9.4: Bob tries to GET Alice's goal
        idor_get_goal = await client.get(f"/api/v1/goals/{goal_data['id']}", headers=bob_headers)
        runner.assert_eq("9.4 IDOR Prevention: Bob cannot GET Alice's goal (404)", idor_get_goal.status_code, 404)

        # Test 9.5: Bob tries to UPDATE Alice's goal
        idor_upd_goal = await client.patch(
            f"/api/v1/goals/{goal_data['id']}",
            json={"name": "Hacked Goal"},
            headers=bob_headers,
        )
        runner.assert_eq("9.5 IDOR Prevention: Bob cannot UPDATE Alice's goal (404)", idor_upd_goal.status_code, 404)

        # Test 9.6: Bob tries to CONTRIBUTE to Alice's goal
        idor_contrib_goal = await client.post(
            f"/api/v1/goals/{goal_data['id']}/contribute",
            json={"amount": "100.00"},
            headers=bob_headers,
        )
        runner.assert_eq("9.6 IDOR Prevention: Bob cannot CONTRIBUTE to Alice's goal (404)", idor_contrib_goal.status_code, 404)

        # Test 9.7: Bob tries to access Alice's chat messages
        idor_chat_msgs = await client.get(
            f"/api/v1/chat/conversations/{conv_id}/messages",
            headers=bob_headers,
        )
        runner.assert_eq("9.7 IDOR Prevention: Bob cannot read Alice's chat messages (404)", idor_chat_msgs.status_code, 404)

        # Test 9.8: Data Segregation in Monthly Summary
        bob_summary = await client.get("/api/v1/transactions/summary/monthly?year=2026&month=8", headers=bob_headers)
        runner.assert_eq("9.8 Data Segregation: Bob's monthly summary is clean", bob_summary.json()["total_expenses"], "0.00")

    print("\n=======================================================")
    print(f"QA TEST SUMMARY: {runner.passed}/{runner.tests_run} PASSED ({runner.failed} FAILED)")
    print("=======================================================\n")
    return runner.failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_qa_tests())
    sys.exit(0 if success else 1)

