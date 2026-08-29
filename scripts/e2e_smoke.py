"""End-to-end smoke test: exercises every API route against a live server.

Run with the backend already listening on :8000.
    ./.venv/Scripts/python.exe e2e_smoke.py
"""
from __future__ import annotations

import sys
import uuid
from datetime import date

import httpx

BASE = "http://localhost:8000"
API = f"{BASE}/api/v1"

results: list[tuple[str, str, int, bool, str]] = []
ctx: dict[str, str] = {}


def call(
    label: str,
    method: str,
    path: str,
    *,
    expect: int | tuple[int, ...] = 200,
    auth: bool = True,
    **kw,
):
    """Hit a route, record pass/fail, return the parsed body (or None)."""
    ok_codes = (expect,) if isinstance(expect, int) else expect
    headers = kw.pop("headers", {})
    if auth and "token" in ctx:
        headers["Authorization"] = f"Bearer {ctx['token']}"
    url = path if path.startswith("http") else f"{API}{path}"
    print(f"  -> {method:6} {path} ...", end="", flush=True)
    try:
        r = httpx.request(method, url, headers=headers, timeout=30.0, **kw)
    except Exception as exc:  # noqa: BLE001
        print(f" EXC {type(exc).__name__}", flush=True)
        results.append((label, f"{method} {path}", 0, False, f"EXC {type(exc).__name__}: {exc}"))
        return None
    passed = r.status_code in ok_codes
    detail = "" if passed else r.text[:200].replace("\n", " ")
    print(f" {r.status_code} {'PASS' if passed else 'FAIL'}", flush=True)
    results.append((label, f"{method} {path}", r.status_code, passed, detail))
    try:
        return r.json()
    except Exception:  # noqa: BLE001
        return None


def main() -> int:
    today = date.today()
    email = f"e2e_{uuid.uuid4().hex[:10]}@example.com"
    pwd = "SecurePass123!"

    # ---- infra ----
    call("health", "GET", f"{BASE}/api/health", auth=False)

    # ---- auth ----
    reg = call(
        "auth.register", "POST", "/auth/register",
        expect=(200, 201), auth=False,
        json={"email": email, "password": pwd, "full_name": "E2E Tester"},
    )
    if not reg or "access_token" not in reg:
        print("FATAL: registration did not return tokens; cannot continue.")
        report()
        return 1
    ctx["token"] = reg["access_token"]
    ctx["refresh"] = reg.get("refresh_token", "")

    login = call(
        "auth.login", "POST", "/auth/login", auth=False,
        json={"email": email, "password": pwd},
    )
    if login and login.get("access_token"):
        ctx["token"] = login["access_token"]
        ctx["refresh"] = login.get("refresh_token", ctx["refresh"])

    call("auth.me", "GET", "/auth/me")
    call(
        "auth.refresh", "POST", "/auth/refresh", auth=False,
        json={"refresh_token": ctx["refresh"]},
    )

    # ---- reference data ----
    cats = call("categories.list", "GET", "/categories")
    cat_id = None
    if isinstance(cats, list) and cats:
        cat_id = cats[0].get("id")
    elif isinstance(cats, dict):
        items = cats.get("items") or cats.get("categories") or []
        if items:
            cat_id = items[0].get("id")

    # ---- onboarding ----
    call(
        "onboarding.income", "POST", "/onboarding/income",
        expect=(200, 201),
        json={"amount": 85000, "source_name": "Salary", "frequency": "monthly", "pay_day": 1},
    )
    call(
        "onboarding.expenses", "POST", "/onboarding/expenses",
        expect=(200, 201),
        json={"expenses": [
            {"description": "Rent", "amount": 22000, "frequency": "monthly", "category_name": "rent"},
            {"description": "Internet", "amount": 999, "frequency": "monthly", "category_name": "bills"},
        ]},
    )
    call(
        "onboarding.goals", "POST", "/onboarding/goals",
        expect=(200, 201),
        json={"goals": [
            {"name": "Emergency Fund", "target_amount": 300000,
             "target_date": str(today.replace(year=today.year + 1)), "priority": 1},
        ]},
    )
    call(
        "onboarding.spending_style", "POST", "/onboarding/spending-style",
        expect=(200, 201),
        json={"overspending_categories": ["food", "shopping"], "ai_personality": "supportive"},
    )
    call("onboarding.complete", "POST", "/onboarding/complete", expect=(200, 201))

    # ---- transactions ----
    tx_body = {
        "amount": 1250.50,
        "type": "expense",
        "description": "Groceries at BigBasket",
        "merchant": "BigBasket",
        "transaction_date": str(today),  # API field is a `date`, not a datetime
        "notes": "weekly run",
        "is_recurring": False,
    }
    if cat_id:
        tx_body["category_id"] = cat_id
    else:
        tx_body["category_name"] = "groceries"

    tx = call("tx.create", "POST", "/transactions", expect=(200, 201), json=tx_body)
    tx_id = (tx or {}).get("id")

    call("tx.list", "GET", "/transactions")
    if tx_id:
        call("tx.get", "GET", f"/transactions/{tx_id}")
        call("tx.patch", "PATCH", f"/transactions/{tx_id}",
             json={"amount": 1300.75, "notes": "corrected amount"})
        call("tx.put", "PUT", f"/transactions/{tx_id}",
             json={"amount": 1400.00, "type": "expense", "description": "Groceries (revised)"})
    else:
        for lbl, m, p in [("tx.get", "GET", "/transactions/{id}"),
                          ("tx.patch", "PATCH", "/transactions/{id}"),
                          ("tx.put", "PUT", "/transactions/{id}")]:
            results.append((lbl, f"{m} {p}", 0, False, "SKIPPED: no transaction id from create"))

    call("tx.summary_monthly", "GET", "/transactions/summary/monthly",
         params={"year": today.year, "month": today.month})

    # ---- budgets ----
    call("budgets.generate", "POST", "/budgets/generate", expect=(200, 201))
    call("budgets.current", "GET", "/budgets/current")

    # ---- health ----
    call("health.score", "GET", "/health/score")
    call("health.history", "GET", "/health/history")

    # ---- goals ----
    goal = call("goals.create", "POST", "/goals", expect=(200, 201), json={
        "name": "Trip to Japan",
        "description": "2 weeks",
        "target_amount": 250000,
        "target_date": str(today.replace(year=today.year + 2)),
        "icon": "airplane",
        "priority": 2,
    })
    goal_id = (goal or {}).get("id")
    call("goals.list", "GET", "/goals")
    if goal_id:
        call("goals.get", "GET", f"/goals/{goal_id}")
        call("goals.patch", "PATCH", f"/goals/{goal_id}", json={"name": "Trip to Japan (spring)"})
        call("goals.put", "PUT", f"/goals/{goal_id}", json={"target_amount": 275000})
        call("goals.contribute", "POST", f"/goals/{goal_id}/contribute",
             expect=(200, 201), json={"amount": 5000, "notes": "first deposit"})
        call("goals.delete", "DELETE", f"/goals/{goal_id}", expect=(200, 204))
    else:
        for lbl, m in [("goals.get", "GET"), ("goals.patch", "PATCH"), ("goals.put", "PUT"),
                       ("goals.contribute", "POST"), ("goals.delete", "DELETE")]:
            results.append((lbl, f"{m} /goals/{{id}}", 0, False, "SKIPPED: no goal id from create"))

    # ---- chat ----
    msg = call("chat.message", "POST", "/chat/message", expect=(200, 201),
               json={"message": "How much did I spend on groceries this month?"})
    conv_id = (msg or {}).get("conversation_id") or (msg or {}).get("id")
    call("chat.conversations", "GET", "/chat/conversations")
    if conv_id:
        call("chat.messages", "GET", f"/chat/conversations/{conv_id}/messages")
    else:
        results.append(("chat.messages", "GET", 0, False,
                        "SKIPPED: no conversation_id from chat.message"))

    # ---- destructive last ----
    if tx_id:
        call("tx.delete", "DELETE", f"/transactions/{tx_id}", expect=(200, 204))
    else:
        results.append(("tx.delete", "DELETE /transactions/{id}", 0, False, "SKIPPED"))

    # ---- negative / authz checks ----
    call("authz.me_no_token", "GET", "/auth/me", expect=(401, 403), auth=False)
    call("authz.bad_token", "GET", "/auth/me", expect=(401, 403), auth=False,
         headers={"Authorization": "Bearer not-a-real-token"})
    call("validation.bad_register", "POST", "/auth/register", expect=(422,), auth=False,
         json={"email": "not-an-email", "password": "x", "full_name": ""})
    call("notfound.tx", "GET", f"/transactions/{uuid.uuid4()}", expect=(404,))
    call("dup.register", "POST", "/auth/register", expect=(400, 409), auth=False,
         json={"email": email, "password": pwd, "full_name": "Dupe"})
    call("wrongpw.login", "POST", "/auth/login", expect=(400, 401), auth=False,
         json={"email": email, "password": "WrongPassword1!"})

    return report()


def report() -> int:
    passed = sum(1 for *_, ok, _ in results if ok)
    failed = len(results) - passed
    print("\n" + "=" * 88)
    print(f"{'RESULT':6} {'CODE':5} {'LABEL':26} {'ROUTE'}")
    print("-" * 88)
    for label, route, code, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL':6} {code or '---':<5} {label:26} {route}")
        if detail:
            print(f"         {detail}")
    print("=" * 88)
    print(f"TOTAL {len(results)}  |  PASSED {passed}  |  FAILED {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
