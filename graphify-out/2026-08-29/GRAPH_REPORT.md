# Graph Report - finance buddy  (2026-08-29)

## Corpus Check
- 127 files · ~121,332 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 988 nodes · 2108 edges · 95 communities (67 shown, 28 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `13c6ce21`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- repositories.py
- User
- routers/auth.py
- application/health.py
- Text.tsx
- OnboardingService
- exceptions.py
- CategoryRepository
- Shared Types Package
- Backend Test Harness
- style.tsx
- GoalService
- expo
- dependencies.py
- scripts
- deps.py
- services/api.ts
- env.py
- types/api.ts
- login.tsx
- home.tsx
- orchestrator.py
- finance.ts
- FastAPI Server
- dependencies
- theme.ts
- .chat
- validators.ts
- mobile/package.json
- formatDate.ts
- Domain Layer (pure types, enums, deterministic rules)
- Backend Setup Procedure
- Upward Chevron / Ascending Peak Mark
- expo-router
- India-Specific Categories (Auto/Riksha, Kirana, EMI, Chai)
- Finance Buddy Android Adaptive Icon Foreground
- errors.py
- shared/package.json
- DDD Layering (core/domain/application/infrastructure/api)
- Icon Safe Zone Construction Guides
- Upward Chevron Brand Mark
- Mobile App Favicon (Expo web icon)
- get_settings
- tsconfig.json
- API Schemas as Sole HTTP Contract
- Splash Icon Asset (concentric rings on grid)
- App.tsx
- formatCurrency.ts
- Financial Health Score
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
- scripts
- schemas.py
- ChatService
- routers/goals.py
- chat.tsx
- app/database.py
- Finance Buddy
- e2e_smoke.py
- current_budget
- py.mjs

## God Nodes (most connected - your core abstractions)
1. `User` - 51 edges
2. `TransactionService` - 39 edges
3. `GoalService` - 34 edges
4. `ChatService` - 28 edges
5. `OnboardingService` - 27 edges
6. `CategoryRepository` - 25 edges
7. `BudgetService` - 24 edges
8. `Theme` - 22 edges
9. `AuthService` - 22 edges
10. `Base` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Domain Layer (pure types, enums, deterministic rules)` --semantically_similar_to--> `Financial Rules Engine (Deterministic, Testable, Auditable)`  [INFERRED] [semantically similar]
  PROGRESS.md → README.md
- `db service (postgres:16-alpine)` --implements--> `PostgreSQL 16`  [INFERRED]
  docker-compose.yml → README.md
- `Stateless Refresh Tokens Never Revoked` --conceptually_related_to--> `Redis 7 Cache`  [AMBIGUOUS]
  PROGRESS.md → README.md
- `Backend Setup Procedure` --references--> `Backend Environment Variables Contract`  [INFERRED]
  SETUP.md → README.md
- `api service (FastAPI container)` --implements--> `FastAPI Server`  [INFERRED]
  docker-compose.yml → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Android Adaptive Icon Authoring Constraints** — apps_mobile_assets_android_icon_foreground_icon, apps_mobile_assets_android_icon_foreground_adaptive_icon_layering, apps_mobile_assets_android_icon_foreground_safe_zone_padding [EXTRACTED 1.00]
- **DDD Layer Stack** — progress_ddd_layering, progress_domain_layer, progress_application_layer, progress_repositories_persistence_only, progress_api_schemas_contract [EXTRACTED 1.00]
- **India-First Localization System** — readme_india_first, readme_indian_numbering, readme_india_categories, readme_salary_cycle_awareness [EXTRACTED 1.00]
- **Local Dev Infrastructure Stack** — docker_compose_db_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_migrate_service, docker_compose_healthchecks [EXTRACTED 1.00]
- **Mobile App Visual Identity (mark + palette + tab-icon role)** — apps_mobile_assets_favicon_favicon, apps_mobile_assets_favicon_upward_chevron_mark, apps_mobile_assets_favicon_blue_on_pale_tint_palette, apps_mobile_assets_favicon_browser_tab_identity [INFERRED 0.75]
- **Android Adaptive Icon Background Composition** — apps_mobile_assets_android_icon_background, apps_mobile_assets_android_icon_background_adaptive_icon_background_layer, apps_mobile_assets_android_icon_background_safe_zone_construction_guides, apps_mobile_assets_android_icon_background_brand_pale_blue_fill [INFERRED 0.85]
- **Finance Buddy Android Launcher Identity System** — apps_mobile_assets_android_icon_monochrome_icon, apps_mobile_assets_android_icon_monochrome_chevron_mark, apps_mobile_assets_android_icon_monochrome_material_you_themed_icon_layer, apps_mobile_assets_android_icon_monochrome_rounded_geometry_treatment, apps_mobile_assets_android_icon_monochrome_upward_growth_motif [INFERRED 0.85]
- **Mobile Brand Identity System (mark, palette, adaptive-icon delivery)** — apps_mobile_assets_android_icon_foreground_icon, apps_mobile_assets_android_icon_foreground_upward_chevron_mark, apps_mobile_assets_android_icon_foreground_blue_gradient_palette, apps_mobile_assets_android_icon_foreground_growth_upward_trend_metaphor [INFERRED 0.85]
- **Icon Visual Design System (mark, grid, palette, stroke geometry)** — apps_mobile_assets_icon_upward_chevron_mark, apps_mobile_assets_icon_construction_grid, apps_mobile_assets_icon_blue_gradient_palette, apps_mobile_assets_icon_rounded_stroke_geometry [INFERRED 0.85]

## Communities (95 total, 28 thin omitted)

### Community 0 - "repositories.py"
Cohesion: 0.07
Nodes (54): AsyncSession, BudgetAllocationResponse, BudgetEnvelope, BudgetGenerateResponse, FinancialContextResponse, BudgetService, AsyncSession, User (+46 more)

### Community 1 - "User"
Cohesion: 0.24
Nodes (19): create_transaction(), delete_transaction(), get_transaction(), list_transactions(), monthly_summary(), date, delete, get (+11 more)

### Community 2 - "routers/auth.py"
Cohesion: 0.17
Nodes (18): login(), me(), get, post, User, refresh(), register(), LoginRequest (+10 more)

### Community 3 - "application/health.py"
Cohesion: 0.13
Nodes (27): BudgetInput, BudgetLine, generate_budget(), monthly_goal_contribution(), date, Decimal, Compute the monthly contribution needed to hit a goal by its target date. If no…, categorize_text() (+19 more)

### Community 4 - "Text.tsx"
Cohesion: 0.16
Nodes (12): styles, { width }, styles, styles, ButtonProps, styles, HealthRing(), HealthRingProps (+4 more)

### Community 5 - "OnboardingService"
Cohesion: 0.29
Nodes (14): complete(), expenses(), goals(), income(), post, User, spending_style(), ExpenseSetup (+6 more)

### Community 6 - "exceptions.py"
Cohesion: 0.10
Nodes (23): app_error_handler(), AppError, AuthenticationError, AuthorizationError, ConflictError, ExternalServiceError, NotFoundError, Any (+15 more)

### Community 7 - "CategoryRepository"
Cohesion: 0.07
Nodes (18): list_categories(), AsyncSession, get, User, AsyncSession, AsyncSession, CategoryRepository, AsyncSession (+10 more)

### Community 8 - "Shared Types Package"
Cohesion: 0.07
Nodes (27): AI_PERSONALITIES, AIPersonality, CURRENCY_SYMBOL, DEFAULT_CATEGORIES, DEFAULT_CURRENCY, GOAL_PRIORITIES, GoalPriority, INCOME_FREQUENCIES (+19 more)

### Community 9 - "Backend Test Harness"
Cohesion: 0.13
Nodes (23): auth_headers(), client(), engine(), event_loop_policy(), AsyncClient, register_user(), session_factory(), AsyncClient (+15 more)

### Community 10 - "style.tsx"
Cohesion: 0.11
Nodes (18): plugins, Index(), styles, queryClient, RootLayoutNav(), ProfileScreen(), HURDLE_CATEGORIES, HURDLES (+10 more)

### Community 11 - "GoalService"
Cohesion: 0.16
Nodes (17): contribute(), delete_goal(), get_goal(), list_goals(), delete, get, post, User (+9 more)

### Community 12 - "expo"
Cohesion: 0.09
Nodes (22): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, expo, android (+14 more)

### Community 13 - "dependencies.py"
Cohesion: 0.13
Nodes (22): get_ai_orchestrator(), get_auth_service(), get_budget_service(), get_current_user(), get_goal_service(), get_health_service(), get_onboarding_service(), get_optional_user() (+14 more)

### Community 14 - "scripts"
Cohesion: 0.10
Nodes (20): name, packageManager, private, scripts, build:web, dev:android, dev:backend, dev:web (+12 more)

### Community 15 - "deps.py"
Cohesion: 0.13
Nodes (23): auth_service(), budget_service(), chat_service(), current_user(), goal_service(), health_service(), onboarding_service(), AsyncSession (+15 more)

### Community 16 - "services/api.ts"
Cohesion: 0.17
Nodes (9): config, api, AuthResponse, authService, LoginPayload, RegisterPayload, Goal, GoalCreate (+1 more)

### Community 17 - "env.py"
Cohesion: 0.13
Nodes (16): do_run_migrations(), Alembic environment configuration for async migrations., Run migrations in 'offline' mode., Run migrations in 'online' mode with async engine., Run migrations in 'online' mode., run_async_migrations(), run_migrations_offline(), run_migrations_online() (+8 more)

### Community 18 - "types/api.ts"
Cohesion: 0.11
Nodes (16): ApiError, ApiResponse, AuthTokens, Budget, ChatMessage, DashboardData, FinancialGoal, LoginResponse (+8 more)

### Community 19 - "login.tsx"
Cohesion: 0.18
Nodes (12): LoginForm, loginSchema, LoginScreen(), styles, RegisterForm, registerSchema, RegisterScreen(), styles (+4 more)

### Community 20 - "home.tsx"
Cohesion: 0.18
Nodes (14): BudgetsScreen(), formatCurrency(), styles, formatCurrency(), HomeScreen(), styles, BudgetPlan, HealthScore (+6 more)

### Community 21 - "orchestrator.py"
Cohesion: 0.21
Nodes (13): assemble_context(), FinancialContext, format_context_for_prompt(), AsyncSession, UUID, Context assembler — builds a COMPLETE financial snapshot for AI prompts. This…, Format financial context as human-readable text for prompt injection., Pre-computed financial snapshot injected into AI prompts. Every field is… (+5 more)

### Community 22 - "finance.ts"
Cohesion: 0.10
Nodes (18): styles, COMMON_EXPENSES, Expense, styles, styles, Goal, GOAL_TEMPLATES, styles (+10 more)

### Community 23 - "FastAPI Server"
Cohesion: 0.18
Nodes (14): api service (FastAPI container), db service (postgres:16-alpine), Service Healthchecks, migrate service (tools profile), pgdata Persistent Volume, redis service (redis:7-alpine), Healthy-Dependency Startup Ordering, Stateless Refresh Tokens Never Revoked (+6 more)

### Community 24 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, axios, expo-font, expo-haptics, react-native, @tanstack/react-query, zod, axios (+5 more)

### Community 25 - "theme.ts"
Cohesion: 0.18
Nodes (8): Category, expenseCategories, borderRadius, colors, glassmorphism, shadows, spacing, typography

### Community 26 - ".chat"
Cohesion: 0.18
Nodes (9): generate_fallback_response(), AI fallbacks — graceful degradation when Gemini is unavailable. Uses random…, Return a helpful fallback response (stateless, random selection)., AIOrchestrator, ChatResponse, UUID, Main AI coordination — assembles context, calls Gemini, parses response., Process a user message and return AI response. (+1 more)

### Community 27 - "validators.ts"
Cohesion: 0.18
Nodes (10): GoalFormData, goalSchema, LoginFormData, loginSchema, OnboardingIncomeData, onboardingIncomeSchema, RegisterFormData, registerSchema (+2 more)

### Community 28 - "mobile/package.json"
Cohesion: 0.20
Nodes (9): devDependencies, @types/react, typescript, main, name, private, version, @types/react (+1 more)

### Community 29 - "formatDate.ts"
Cohesion: 0.28
Nodes (6): DAYS, formatDate(), getRelativeTime(), MONTHS, MONTHS_SHORT, pad()

### Community 30 - "Domain Layer (pure types, enums, deterministic rules)"
Cohesion: 0.29
Nodes (8): Budget Pacing Context for AI Chat, Date-Aware Goal Allocation, Domain Layer (pure types, enums, deterministic rules), Goal Contribution Overshoot Cap, Financial Rules Engine (Deterministic, Testable, Auditable), Google Gemini API, Core Principle: Trust (LLMs never compute balances), Optional Gemini Key with Feature Fallback

### Community 31 - "Backend Setup Procedure"
Cohesion: 0.29
Nodes (8): No Silent Catch on User Actions, React Query Owns Server State, Zustand Owns Session, Backend Environment Variables Contract, Expo Clients (Web + Android), Backend Setup Procedure, Expo Android Dev Target, Expo Web Dev Target, uv Python Package Manager

### Community 32 - "Upward Chevron / Ascending Peak Mark"
Cohesion: 0.43
Nodes (7): Finance Buddy Mobile App Icon, Blue Gradient Brand Palette, Circular Construction Grid and Symmetry Axes, Financial Growth / Upward Trend Metaphor, Mobile App Brand Identity Asset, Rounded-Cap Thick Stroke Geometry, Upward Chevron / Ascending Peak Mark

### Community 33 - "expo-router"
Cohesion: 0.17
Nodes (4): styles, TAB_ICONS, TAB_LABELS, expo-router

### Community 34 - "India-Specific Categories (Auto/Riksha, Kirana, EMI, Chai)"
Cohesion: 0.29
Nodes (7): Deterministic Category Seeding at Startup, Four-Step Onboarding Flow, Word-Boundary Transaction Categorization, Adaptive Budget Generation, India-Specific Categories (Auto/Riksha, Kirana, EMI, Chai), India-First Product Design, Salary Cycle Awareness

### Community 35 - "Finance Buddy Android Adaptive Icon Foreground"
Cohesion: 0.53
Nodes (6): Android Adaptive Icon Foreground/Background Layering, Blue Vertical Gradient Brand Palette, Upward Trend / Financial Growth Metaphor, Finance Buddy Android Adaptive Icon Foreground, Adaptive Icon Safe-Zone Padding, Upward Chevron Brand Mark

### Community 36 - "errors.py"
Cohesion: 0.12
Nodes (19): Transaction, TransactionResponse, transaction_response(), date, TransactionCreate, TransactionResponse, app_error_handler(), AppError (+11 more)

### Community 37 - "shared/package.json"
Cohesion: 0.33
Nodes (5): main, name, private, types, version

### Community 38 - "DDD Layering (core/domain/application/infrastructure/api)"
Cohesion: 0.40
Nodes (6): Application Layer (use cases, transaction boundaries), Chat Ownership Verification, Legacy Correctness Drift (phantom ORM columns), DDD Layering (core/domain/application/infrastructure/api), Repositories Own Only Persistence, SQL Aggregation for Monthly Summary

### Community 39 - "Icon Safe Zone Construction Guides"
Cohesion: 0.70
Nodes (5): Android Adaptive Icon Background Asset, Adaptive Icon Background Layer Pattern, Brand Pale Blue Fill, Optical Center Offset, Icon Safe Zone Construction Guides

### Community 40 - "Upward Chevron Brand Mark"
Cohesion: 0.60
Nodes (5): Upward Chevron Brand Mark, Android Monochrome App Icon (Finance Buddy), Material You Themed Icon Monochrome Layer, Rounded-Cap Geometric Glyph Treatment, Upward Growth / Rising Trend Visual Motif

### Community 41 - "Mobile App Favicon (Expo web icon)"
Cohesion: 0.60
Nodes (5): Blue-on-Pale-Tint Icon Palette, Browser Tab / PWA Identity Asset Role, Unbranded Expo Scaffold Default Artwork, Mobile App Favicon (Expo web icon), Upward Chevron Brand Mark

### Community 42 - "get_settings"
Cohesion: 0.17
Nodes (13): User, get_settings(), BaseSettings, field_validator, Settings, create_access_token(), create_refresh_token(), _create_token() (+5 more)

### Community 43 - "tsconfig.json"
Cohesion: 0.40
Nodes (4): compilerOptions, strict, extends, expo/tsconfig.base

### Community 44 - "API Schemas as Sole HTTP Contract"
Cohesion: 0.40
Nodes (5): API Schemas as Sole HTTP Contract, Decimal Money, Strings Over HTTP, Single Pagination Envelope, PUT/PATCH Client-Server Verb Mismatch, Indian Numbering System (INR formatting)

### Community 45 - "Splash Icon Asset (concentric rings on grid)"
Cohesion: 0.67
Nodes (4): Splash Icon Asset (concentric rings on grid), Centred Grid Alignment Guide Motif, Expo Splash Screen Launch Asset Slot, Unreplaced Expo Template Placeholder Branding

### Community 48 - "Financial Health Score"
Cohesion: 1.00
Nodes (3): Financial Health Score, Tiered Recommendations Engine, Month-Over-Month Spending Trend

### Community 85 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, android, ios, start, web

### Community 86 - "schemas.py"
Cohesion: 0.18
Nodes (17): BudgetPlanResponse, category_to_response(), CategoryResponse, CategorySummary, ChatMetadata, DailySpend, ErrorResponse, ExpenseItem (+9 more)

### Community 87 - "ChatService"
Cohesion: 0.27
Nodes (11): conversations(), messages(), get, post, User, send(), ChatRequest, ChatResponse (+3 more)

### Community 88 - "routers/goals.py"
Cohesion: 0.31
Nodes (8): create_goal(), GoalCreate, patch, put, replace_goal(), update_goal(), GoalCreate, GoalUpdate

### Community 89 - "chat.tsx"
Cohesion: 0.29
Nodes (7): ChatScreen(), INITIAL_MESSAGES, Message, renderWithAmounts(), styles, SUGGESTIONS, chatService

### Community 90 - "app/database.py"
Cohesion: 0.29
Nodes (6): create_tables(), get_db_session(), AsyncSession, Async SQLAlchemy engine, session factory, and FastAPI dependency. Supports…, FastAPI dependency — yields an async session with auto commit/rollback., Create all tables (SQLite dev mode — Alembic handles production).

### Community 91 - "Finance Buddy"
Cohesion: 0.33
Nodes (6): Hardcoded Dev JWT Secret, AI-Native Personal Finance Operating System, Finance Buddy, Custom JWT + Argon2 Auth, Psychological Spending Coaching, Turborepo Monorepo

### Community 92 - "e2e_smoke.py"
Cohesion: 0.47
Nodes (5): call(), main(), End-to-end smoke test: exercises every API route against a live server. Run…, Hit a route, record pass/fail, return the parsed body (or None)., report()

### Community 93 - "current_budget"
Cohesion: 0.40
Nodes (5): current_budget(), generate_budget(), get, post, User

### Community 94 - "py.mjs"
Cohesion: 0.40
Nodes (4): args, cwdIndex, repoRoot, result

## Ambiguous Edges - Review These
- `Redis 7 Cache` → `Stateless Refresh Tokens Never Revoked`  [AMBIGUOUS]
  PROGRESS.md · relation: conceptually_related_to
- `Upward Chevron Brand Mark` → `Android Adaptive Icon Foreground/Background Layering`  [AMBIGUOUS]
  apps/mobile/assets/android-icon-foreground.png · relation: shares_data_with
- `Optical Center Offset` → `Icon Safe Zone Construction Guides`  [AMBIGUOUS]
  apps/mobile/assets/android-icon-background.png · relation: rationale_for
- `Upward Chevron Brand Mark` → `Unbranded Expo Scaffold Default Artwork`  [AMBIGUOUS]
  apps/mobile/assets/favicon.png · relation: conceptually_related_to

## Knowledge Gaps
- **215 isolated node(s):** `styles`, `name`, `slug`, `version`, `orientation` (+210 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Redis 7 Cache` and `Stateless Refresh Tokens Never Revoked`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Upward Chevron Brand Mark` and `Android Adaptive Icon Foreground/Background Layering`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `Optical Center Offset` and `Icon Safe Zone Construction Guides`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
- **What is the exact relationship between `Upward Chevron Brand Mark` and `Unbranded Expo Scaffold Default Artwork`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `User` connect `User` to `repositories.py`, `routers/auth.py`, `OnboardingService`, `CategoryRepository`, `GoalService`, `deps.py`, `ChatService`, `routers/goals.py`, `current_budget`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `TransactionService` connect `User` to `repositories.py`, `application/health.py`, `errors.py`, `CategoryRepository`, `dependencies.py`, `deps.py`, `orchestrator.py`, `schemas.py`, `ChatService`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `CategoryRepository` connect `CategoryRepository` to `repositories.py`, `User`, `routers/auth.py`, `OnboardingService`, `Backend Test Harness`, `deps.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._