import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import requests
import time

BASE_URL = "http://localhost:8000/api/v1"
s = requests.Session()

def test():
    print("1. Register")
    email = f"test_{int(time.time())}@test.com"
    r = s.post(f"{BASE_URL}/auth/register", json={"email": email, "password": "password123", "full_name": "Test User"})
    if r.status_code != 201:
        print("Register failed", r.text)
        return
    token = r.json()["access_token"]
    s.headers.update({"Authorization": f"Bearer {token}"})

    print("2. Setup Income")
    r = s.post(f"{BASE_URL}/onboarding/income", json={"amount": 50000, "pay_day": 1})
    print(r.status_code, r.text)

    print("3. Setup Expenses")
    r = s.post(f"{BASE_URL}/onboarding/expenses", json={"expenses": [{"description": "Rent", "amount": 15000, "frequency": "monthly"}]})
    print(r.status_code, r.text)

    print("4. Setup Goals")
    r = s.post(f"{BASE_URL}/onboarding/goals", json={"goals": [{"name": "Emergency", "target_amount": 100000, "priority": 1}]})
    print(r.status_code, r.text)

    print("5. Setup Spending Style")
    r = s.post(f"{BASE_URL}/onboarding/spending-style", json={"overspending_categories": ["Food"], "ai_personality": "balanced"})
    print(r.status_code, r.text)

    print("6. Complete Onboarding")
    r = s.post(f"{BASE_URL}/onboarding/complete")
    print(r.status_code, r.text)

    print("7. Dashboard - Transactions")
    r = s.get(f"{BASE_URL}/transactions?limit=5")
    print(r.status_code, r.text[:200])

    print("8. Dashboard - Monthly Summary")
    r = s.get(f"{BASE_URL}/transactions/summary/monthly?year=2026&month=5")
    print(r.status_code, r.text)

    print("9. Dashboard - Health Score")
    r = s.get(f"{BASE_URL}/health/score")
    print(r.status_code, r.text)

    print("10. Budget - Generate")
    r = s.post(f"{BASE_URL}/budgets/generate")
    print(r.status_code, r.text[:200])

test()
