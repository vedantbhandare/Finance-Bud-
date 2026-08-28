# Finance Buddy Rebuild Progress

Single source of truth for continuation. Always read this file before editing code in a new session or after a context/model switch.

## Current State

- Phase: Discovery, critique, and redesign complete. Backend rebuild is next.
- In progress: Backend module 1, core/domain foundation.
- Next: Replace the current backend layering with a clean `app/core`, `app/domain`, `app/application`, `app/infrastructure`, `app/api` structure, then update tests.
- Verification status: Existing tests could not run because the checked-in `.venv` points to a missing Python 3.10 interpreter and the default Python environment has no `pytest`.

## File Inventory Read

First-party text files were read in full:

- Root: `.gitignore`, `README.md`, `SETUP.md`, `PROGRESS.md`, `package.json`, `package-lock.json`, `turbo.json`, `docker-compose.yml`.
- Shared package: `packages/shared/*`.
- Backend: config, database, dependencies, exceptions, main app, Alembic config/template/env, models, schemas, repositories, services, rules, AI layer, routers, tests, setup scripts.
- Mobile: Expo config, route files, auth/onboarding/main tab screens, UI components, constants, hooks, store, services, types, utilities, and `redesign.py`.

Generated/vendor/build/cache files were catalogued but not semantically reviewed: root `node_modules`, `apps/mobile/node_modules`, `apps/mobile/dist`, `apps/mobile/.expo`, `backend/.venv`, `backend/.pytest_cache`, and Python `__pycache__`.

Binary artifacts were inspected by metadata/schema:

- App image assets: `android-icon-background.png`, `android-icon-foreground.png`, `android-icon-monochrome.png`, `favicon.png`, `icon.png`, `splash-icon.png`.
- SQLite DB: `backend/finance_buddy.db`, 184320 bytes. Tables: `users`, `categories`, `transactions`, `recurring_rules`, `budget_plans`, `budget_allocations`, `goals`, `goal_contributions`, `conversations`, `messages`, `health_snapshots`, `user_preferences`.

## What The App Does

Finance Buddy is an India-first personal finance app with a FastAPI backend and Expo React Native frontend. It provides:

- Registration, login, JWT access and refresh tokens, current-user profile.
- Authenticated route gating in the mobile app.
- Four-step onboarding: monthly income/pay day, recurring fixed expenses, goals, overspending categories/AI personality.
- First-budget generation after onboarding.
- Transaction creation, listing, filtering by type, pagination, deletion, monthly summary.
- Dashboard with monthly income, expenses, net available amount, financial health score, recent transactions, quick-add modal, and quick navigation.
- Budget screen with active/generated budget, monthly spending pace, category spending breakdown, and regeneration.
- Goal CRUD plus goal contributions and profile goal preview.
- Health score with savings rate, budget adherence, goal progress, trend label, and recommendations.
- AI chat using deterministic financial context plus Gemini when configured, with fallback responses otherwise.
- Chat conversation and message persistence.
- India-specific categories, rupee formatting, Indian date/number formatting, UPI/EMI/salary-cycle prompt language.
- Cross-platform token storage: SecureStore on native, localStorage on web.

## Data Model

Current domain entities:

- User: email, password hash, full name, active flag, onboarded flag, monthly salary, pay cycle day.
- Category: optional user ownership, name, icon, category type, system flag.
- Transaction: user, optional category, optional recurring rule, amount, transaction type, description, merchant, date, notes, recurring flag, source.
- RecurringRule: user, optional category, amount, description, frequency, start/end/next due dates, active flag, transaction type.
- BudgetPlan: user, month start/end, total income, need/want/saving percentages, status, AI generated flag, reasoning.
- BudgetAllocation: budget plan, category, allocated amount, spent amount.
- Goal: user, name, description, target/current amounts, target date, icon, status.
- GoalContribution: goal, amount, contribution date, notes.
- Conversation and Message: user conversations and chat messages with role/content/token count.
- HealthSnapshot: point-in-time score breakdown.
- UserPreference: spending style, top categories, goals text, savings target, budget strategy.

## Critique

The current code is not fit for incremental cleanup. It has severe correctness drift:

- Repository queries reference non-existent ORM columns: `Transaction.type`, `Transaction.date`, `RecurringRule.next_run_date`, `GoalStatus.IN_PROGRESS`, `GoalContribution.date`.
- Frontend services call `PUT` for update endpoints while backend exposes `PATCH`.
- Auth service returns token responses without `user`, while frontend expects `response.user`; login/register can break the client.
- Budget responses are inconsistent: `/budgets/current` returns `{ budget, message }` only when empty, but a raw `BudgetPlanResponse` when present. The mobile service assumes one shape.
- Budget generation returns raw ORM objects nested in JSON; FastAPI cannot reliably serialize lazy SQLAlchemy relations.
- Category selection in the mobile transaction form sets only description, never sends a real `category_id`; backend has no category lookup endpoint exposed.
- Category seeding exists but is not called at startup or registration, so budgets cannot allocate to categories in a fresh DB.
- Tests expect legacy payload fields (`category`, `date`) that schemas do not accept; the suite is not a trustworthy parity contract.
- Services call `commit()` inside request-scoped sessions that already auto-commit, creating inconsistent transaction boundaries.
- AI context suppresses all exceptions and formats keys that do not match actual goal summary keys.
- Chat message/conversation endpoints do not verify conversation ownership for reads.
- JWT refresh tokens are stateless and never persisted, rotated, revoked, or invalidated on logout.
- The local `.env` exists with secrets and the repo has a checked-in SQLite DB, broken `.venv`, generated `dist`, and caches.
- The mobile app has multiple parallel type systems (`src/types`, service interfaces, shared package) that do not match backend schemas.
- UI state is mostly local component state with duplicated loading/error handling and silent catches.
- Feature flags/settings in profile are fake toggles, not persisted preferences.
- The shared package is almost unused and already out of sync with the backend.
- Alembic has no real migration revision files, while runtime creates SQLite tables automatically.
- Error handling is inconsistent: backend has structured errors, frontend mostly ignores them.

## New Architecture

Keep the best-fit technologies: FastAPI, SQLAlchemy async, Pydantic, Expo Router, React Query, Zustand, and Zod. Replace the organization and contracts.

### Backend Structure

```text
backend/
  app/
    main.py
    core/
      config.py
      database.py
      errors.py
      security.py
      time.py
    domain/
      money.py
      categories.py
      users.py
      transactions.py
      recurring.py
      budgets.py
      goals.py
      health.py
      chat.py
    infrastructure/
      orm/
        base.py
        models.py
        repositories.py
      ai/
        gateway.py
        prompts.py
    application/
      auth.py
      onboarding.py
      transactions.py
      budgets.py
      goals.py
      health.py
      chat.py
    api/
      deps.py
      schemas.py
      routers/
        auth.py
        onboarding.py
        transactions.py
        categories.py
        budgets.py
        goals.py
        health.py
        chat.py
  tests/
    conftest.py
    test_auth.py
    test_onboarding.py
    test_transactions.py
    test_budgets_goals_health.py
    test_chat.py
    test_rules.py
```

Backend design rules:

- Domain modules own pure types, enums, constants, and deterministic rules.
- Application services own use cases and transaction boundaries.
- Repositories own only persistence.
- API schemas are the only HTTP contract and mirror the mobile client contract.
- Money is represented as `Decimal` in Python and strings over HTTP.
- List responses use one pagination envelope.
- Auth responses always include `user`.
- Budget endpoints always return stable envelope shapes.
- Categories are seeded deterministically at startup and exposed read-only for the MVP.
- Chat read/write always checks ownership.

### Mobile Structure

```text
apps/mobile/
  app/
    _layout.tsx
    index.tsx
    (auth)/
    (onboarding)/
    (main)/(tabs)/
  src/
    api/
      client.ts
      contracts.ts
      errors.ts
    domain/
      money.ts
      dates.ts
      categories.ts
    features/
      auth/
      onboarding/
      dashboard/
      transactions/
      budgets/
      goals/
      chat/
      profile/
    state/
      auth-store.ts
    ui/
      Button.tsx
      Card.tsx
      Field.tsx
      Screen.tsx
      Text.tsx
      EmptyState.tsx
      SegmentedControl.tsx
```

Mobile design rules:

- Screens compose feature components and hooks; they do not own API contract details.
- React Query owns server state; Zustand owns only session/auth.
- API contract types are centralized and match backend response shapes exactly.
- No silent catch for user actions; show actionable error text.
- Transaction/category/budget/goal models use the same naming as API responses.
- Existing screens are rebuilt to preserve flows, not copied.

## Module Log

### Module 0: Discovery/Critique/Redesign

- Completed file inventory and semantic read.
- Identified generated/vendor artifacts and binary artifacts.
- Captured current features, data model, failure points, and new architecture.
- Existing verification blocked by broken `.venv` and missing `pytest` in default Python.

### Module 1: Backend Core/Domain Foundation

- Status: COMPLETE.
- Replaced fragile backend internals with clean DDD layering: core/, domain/, application/, infrastructure/, api/.
- All 13 tests passing.

### Module 2: Logic Rewrite (10 Critical Fixes)

- Status: COMPLETE.
- Changes made:
  1. **SQL aggregation** — `monthly_summary` now uses 3 SQL queries (SUM/CASE, GROUP BY category, GROUP BY date) instead of Python loops over 10K rows.
  2. **Real spending trend** — `spending_trend()` compares current vs. previous month expenses (15% threshold). No longer hardcoded to "stable".
  3. **Richer recommendations** — Expanded from 3 to 10+ possible recommendations with tiered savings advice, spending trend awareness, overspent category callouts, and end-of-month urgency alerts.
  4. **Date-aware goal allocation** — `monthly_goal_contribution()` computes per-goal monthly need based on actual target dates. A goal due in 2 months gets 6x the allocation of one due in 12 months.
  5. **Word-boundary categorization** — `categorize_text()` now uses precompiled regex with `\b` word boundaries. "auto" no longer false-matches "automatic payment".
  6. **AI chat gets budget context** — `FinancialContextResponse` now includes `budget_allocations` (spent vs. allocated per category) and `spending_trend`. Prompt template shows pacing data.
  7. **Goal contribution cap** — Contributions are capped at the remaining amount needed. No more ₹1L contributions to a ₹50K goal.
  8. **Removed ensure_system_categories spam** — Calls removed from auth/register, transaction/create, budget/generate, onboarding/expenses. Only runs once at app startup.
  9. **Fixed assert in budget generation** — Replaced `assert reloaded is not None` with proper `AppError` that works under `python -O`.
  10. **Enhanced AI prompt** — Budget pacing section added to system prompt showing spent/allocated per category.
