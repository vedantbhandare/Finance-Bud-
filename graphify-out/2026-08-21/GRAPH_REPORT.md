# Graph Report - finance buddy  (2026-08-21)

## Corpus Check
- 122 files · ~46,930 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 928 nodes · 2004 edges · 74 communities (46 shown, 28 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 186 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `970e7bb1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- deps.py
- repositories.py
- schemas.py
- TransactionService
- Text.tsx
- application/health.py
- User
- exceptions.py
- types.ts
- conftest.py
- expo-router
- expo
- dependencies.py
- scripts
- tasks
- profile.tsx
- env.py
- types/api.ts
- login.tsx
- .__init__
- dashboard.tsx
- orchestrator.py
- budget.tsx
- dependencies
- Finance Buddy Rebuild Progress
- 💰 Finance Buddy
- Quick Start
- theme.ts
- .chat
- validators.ts
- mobile/package.json
- formatDate.ts
- app/database.py
- shared/package.json
- scripts
- tsconfig.json
- App.tsx
- formatCurrency.ts
- expo
- expo-constants
- @expo-google-fonts/anton
- expo-linking
- @expo/metro-runtime
- expo-router
- expo-secure-store
- expo-status-bar
- expo-system-ui
- @hookform/resolvers
- react
- react-dom
- react-hook-form
- react-native-gesture-handler
- react-native-safe-area-context
- react-native-screens
- react-native-web
- zustand
- app/ai/__init__.py
- application/__init__.py
- core/__init__.py
- domain/__init__.py
- infrastructure/__init__.py
- orm/__init__.py
- app/__init__.py
- finance-buddy-backend

## God Nodes (most connected - your core abstractions)
1. `User` - 51 edges
2. `TransactionService` - 39 edges
3. `GoalService` - 34 edges
4. `ChatService` - 27 edges
5. `OnboardingService` - 27 edges
6. `CategoryRepository` - 23 edges
7. `AuthService` - 22 edges
8. `Base` - 21 edges
9. `Theme` - 20 edges
10. `BudgetService` - 20 edges

## Surprising Connections (you probably didn't know these)
- `assemble_context()` --calls--> `GoalService`  [INFERRED]
  backend/app/ai/context.py → backend/app/application/goals.py
- `assemble_context()` --uses--> `HealthService`  [INFERRED]
  backend/app/ai/context.py → backend/app/application/health.py
- `assemble_context()` --calls--> `TransactionService`  [INFERRED]
  backend/app/ai/context.py → backend/app/application/transactions.py
- `current_user()` --uses--> `User`  [INFERRED]
  backend/app/api/deps.py → backend/app/infrastructure/orm/models.py
- `refresh()` --uses--> `RefreshRequest`  [INFERRED]
  backend/app/api/routers/auth.py → backend/app/api/schemas.py

## Import Cycles
- None detected.

## Communities (74 total, 28 thin omitted)

### Community 0 - "deps.py"
Cohesion: 0.05
Nodes (65): auth_service(), budget_service(), chat_service(), current_user(), goal_service(), health_service(), onboarding_service(), AsyncSession (+57 more)

### Community 1 - "repositories.py"
Cohesion: 0.07
Nodes (53): AsyncSession, current_budget(), generate_budget(), get, post, User, BudgetEnvelope, BudgetGenerateResponse (+45 more)

### Community 2 - "schemas.py"
Cohesion: 0.09
Nodes (44): conversations(), messages(), get, post, User, send(), complete(), expenses() (+36 more)

### Community 3 - "TransactionService"
Cohesion: 0.09
Nodes (34): create_transaction(), delete_transaction(), get_transaction(), list_transactions(), monthly_summary(), date, delete, get (+26 more)

### Community 4 - "Text.tsx"
Cohesion: 0.08
Nodes (28): styles, { width }, Message, QUICK_PROMPTS, styles, styles, TAB_EMOJIS, TAB_ICONS (+20 more)

### Community 5 - "application/health.py"
Cohesion: 0.10
Nodes (24): history(), get, User, score(), HealthScoreResponse, AsyncSession, HealthService, AsyncSession (+16 more)

### Community 6 - "User"
Cohesion: 0.14
Nodes (26): contribute(), create_goal(), delete_goal(), get_goal(), list_goals(), delete, get, GoalCreate (+18 more)

### Community 7 - "exceptions.py"
Cohesion: 0.10
Nodes (23): app_error_handler(), AppError, AuthenticationError, AuthorizationError, ConflictError, ExternalServiceError, NotFoundError, Any (+15 more)

### Community 8 - "types.ts"
Cohesion: 0.07
Nodes (27): AI_PERSONALITIES, AIPersonality, CURRENCY_SYMBOL, DEFAULT_CATEGORIES, DEFAULT_CURRENCY, GOAL_PRIORITIES, GoalPriority, INCOME_FREQUENCIES (+19 more)

### Community 9 - "conftest.py"
Cohesion: 0.13
Nodes (23): auth_headers(), client(), engine(), event_loop_policy(), AsyncClient, register_user(), session_factory(), AsyncClient (+15 more)

### Community 10 - "expo-router"
Cohesion: 0.10
Nodes (14): plugins, Index(), styles, queryClient, RootLayoutNav(), AuthState, useAuthStore, User (+6 more)

### Community 11 - "expo"
Cohesion: 0.09
Nodes (22): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, expo, android (+14 more)

### Community 12 - "dependencies.py"
Cohesion: 0.13
Nodes (22): get_ai_orchestrator(), get_auth_service(), get_budget_service(), get_current_user(), get_goal_service(), get_health_service(), get_onboarding_service(), get_optional_user() (+14 more)

### Community 13 - "scripts"
Cohesion: 0.10
Nodes (20): devDependencies, turbo, turbo, name, packageManager, private, scripts, build:web (+12 more)

### Community 14 - "tasks"
Cohesion: 0.11
Nodes (19): ^build, dist/**, **/.env.*local, ^lint, .next/**, !.next/cache/**, dependsOn, outputs (+11 more)

### Community 15 - "profile.tsx"
Cohesion: 0.16
Nodes (13): formatCurrency(), ProfileScreen(), styles, config, api, ChatMessage, ChatResponse, chatService (+5 more)

### Community 16 - "env.py"
Cohesion: 0.13
Nodes (16): do_run_migrations(), Alembic environment configuration for async migrations., Run migrations in 'offline' mode., Run migrations in 'online' mode with async engine., Run migrations in 'online' mode., run_async_migrations(), run_migrations_offline(), run_migrations_online() (+8 more)

### Community 17 - "types/api.ts"
Cohesion: 0.11
Nodes (16): ApiError, ApiResponse, AuthTokens, Budget, ChatMessage, DashboardData, FinancialGoal, LoginResponse (+8 more)

### Community 18 - "login.tsx"
Cohesion: 0.15
Nodes (13): LoginForm, loginSchema, LoginScreen(), styles, RegisterForm, registerSchema, RegisterScreen(), styles (+5 more)

### Community 19 - ".__init__"
Cohesion: 0.21
Nodes (3): AsyncSession, Repository, ModelT

### Community 20 - "dashboard.tsx"
Cohesion: 0.17
Nodes (13): DashboardScreen(), formatCurrency(), styles, CATEGORIES, FilterType, formatCurrency(), styles, TransactionsScreen() (+5 more)

### Community 21 - "orchestrator.py"
Cohesion: 0.21
Nodes (13): assemble_context(), FinancialContext, format_context_for_prompt(), AsyncSession, UUID, Context assembler — builds a COMPLETE financial snapshot for AI prompts. This…, Format financial context as human-readable text for prompt injection., Pre-computed financial snapshot injected into AI prompts. Every field is… (+5 more)

### Community 22 - "budget.tsx"
Cohesion: 0.18
Nodes (11): BudgetCategory, BudgetScreen(), CATEGORY_ICONS, formatCurrency(), styles, styles, Card(), CardProps (+3 more)

### Community 23 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, axios, expo-font, expo-haptics, react-native, @tanstack/react-query, zod, axios (+5 more)

### Community 24 - "Finance Buddy Rebuild Progress"
Cohesion: 0.15
Nodes (12): Backend Structure, Critique, Current State, Data Model, File Inventory Read, Finance Buddy Rebuild Progress, Mobile Structure, Module 0: Discovery/Critique/Redesign (+4 more)

### Community 25 - "💰 Finance Buddy"
Cohesion: 0.15
Nodes (12): 🏗️ Architecture, Core Principle: Trust, Environment Variables, 💰 Finance Buddy, 🚀 Getting Started, 🇮🇳 India-First, 📜 License, Prerequisites (+4 more)

### Community 26 - "Quick Start"
Cohesion: 0.15
Nodes (12): 1. Install dependencies, 1. Start databases, 2. Install Python dependencies, 2. Start Expo (web), 3. Create database tables, 3. Start Expo (Android), 4. Start API server, Environment Variables (+4 more)

### Community 27 - "theme.ts"
Cohesion: 0.18
Nodes (8): Category, expenseCategories, borderRadius, colors, glassmorphism, shadows, spacing, typography

### Community 28 - ".chat"
Cohesion: 0.18
Nodes (9): generate_fallback_response(), AI fallbacks — graceful degradation when Gemini is unavailable. Uses random…, Return a helpful fallback response (stateless, random selection)., AIOrchestrator, ChatResponse, UUID, Main AI coordination — assembles context, calls Gemini, parses response., Process a user message and return AI response. (+1 more)

### Community 29 - "validators.ts"
Cohesion: 0.18
Nodes (10): GoalFormData, goalSchema, LoginFormData, loginSchema, OnboardingIncomeData, onboardingIncomeSchema, RegisterFormData, registerSchema (+2 more)

### Community 30 - "mobile/package.json"
Cohesion: 0.20
Nodes (9): devDependencies, @types/react, typescript, main, name, private, version, @types/react (+1 more)

### Community 31 - "formatDate.ts"
Cohesion: 0.28
Nodes (6): DAYS, formatDate(), getRelativeTime(), MONTHS, MONTHS_SHORT, pad()

### Community 32 - "app/database.py"
Cohesion: 0.29
Nodes (6): create_tables(), get_db_session(), AsyncSession, Async SQLAlchemy engine, session factory, and FastAPI dependency. Supports…, FastAPI dependency — yields an async session with auto commit/rollback., Create all tables (SQLite dev mode — Alembic handles production).

### Community 33 - "shared/package.json"
Cohesion: 0.33
Nodes (5): main, name, private, types, version

### Community 34 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, android, ios, start, web

### Community 35 - "tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, strict, extends, expo/tsconfig.base

## Knowledge Gaps
- **229 isolated node(s):** `styles`, `name`, `slug`, `version`, `orientation` (+224 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `deps.py`, `repositories.py`, `schemas.py`, `TransactionService`, `application/health.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `TransactionService` connect `TransactionService` to `deps.py`, `repositories.py`, `schemas.py`, `application/health.py`, `dependencies.py`, `orchestrator.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `GoalService` connect `User` to `deps.py`, `repositories.py`, `schemas.py`, `TransactionService`, `application/health.py`, `dependencies.py`, `orchestrator.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `User` (e.g. with `current_user()` and `me()`) actually correct?**
  _`User` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `TransactionService` (e.g. with `assemble_context()` and `create_transaction()`) actually correct?**
  _`TransactionService` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `GoalService` (e.g. with `assemble_context()` and `contribute()`) actually correct?**
  _`GoalService` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `ChatService` (e.g. with `conversations()` and `messages()`) actually correct?**
  _`ChatService` has 18 INFERRED edges - model-reasoned connections that need verification._