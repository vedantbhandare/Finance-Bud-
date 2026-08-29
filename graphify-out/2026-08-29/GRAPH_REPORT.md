# Graph Report - finance buddy  (2026-08-29)

## Corpus Check
- 125 files · ~116,680 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 989 nodes · 2094 edges · 86 communities (58 shown, 28 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `13c6ce21`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User
- schemas.py
- deps.py
- application/health.py
- Text.tsx
- OnboardingService
- exceptions.py
- TransactionRepository
- Shared Types Package
- Backend Test Harness
- useAuthStore
- GoalService
- expo
- dependencies.py
- scripts
- tasks
- services/api.ts
- get_settings
- types/api.ts
- login.tsx
- home.tsx
- orchestrator.py
- goals.tsx
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
- Finance Buddy
- Finance Buddy Android Adaptive Icon Foreground
- expenses.tsx
- shared/package.json
- DDD Layering (core/domain/application/infrastructure/api)
- Icon Safe Zone Construction Guides
- Upward Chevron Brand Mark
- Mobile App Favicon (Expo web icon)
- env.py
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

## God Nodes (most connected - your core abstractions)
1. `User` - 51 edges
2. `TransactionService` - 39 edges
3. `GoalService` - 34 edges
4. `ChatService` - 28 edges
5. `OnboardingService` - 27 edges
6. `CategoryRepository` - 25 edges
7. `BudgetService` - 24 edges
8. `AuthService` - 22 edges
9. `Theme` - 21 edges
10. `Base` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Domain Layer (pure types, enums, deterministic rules)` --semantically_similar_to--> `Financial Rules Engine (Deterministic, Testable, Auditable)`  [INFERRED] [semantically similar]
  PROGRESS.md → README.md
- `db service (postgres:16-alpine)` --implements--> `PostgreSQL 16`  [INFERRED]
  docker-compose.yml → README.md
- `Uvicorn ASGI Dev Server` --implements--> `FastAPI Server`  [INFERRED]
  SETUP.md → README.md
- `Stateless Refresh Tokens Never Revoked` --conceptually_related_to--> `Redis 7 Cache`  [AMBIGUOUS]
  PROGRESS.md → README.md
- `Backend Setup Procedure` --references--> `Backend Environment Variables Contract`  [INFERRED]
  SETUP.md → README.md

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

## Communities (86 total, 28 thin omitted)

### Community 0 - "User"
Cohesion: 0.08
Nodes (54): AsyncSession, budget_service(), current_budget(), generate_budget(), get, post, User, conversations() (+46 more)

### Community 1 - "schemas.py"
Cohesion: 0.07
Nodes (54): transaction_service(), create_transaction(), delete_transaction(), get_transaction(), list_transactions(), monthly_summary(), date, delete (+46 more)

### Community 2 - "deps.py"
Cohesion: 0.06
Nodes (58): auth_service(), chat_service(), current_user(), AsyncSession, HTTPAuthorizationCredentials, User, login(), me() (+50 more)

### Community 3 - "application/health.py"
Cohesion: 0.07
Nodes (39): health_service(), history(), get, User, score(), HealthScoreResponse, AsyncSession, User (+31 more)

### Community 4 - "Text.tsx"
Cohesion: 0.11
Nodes (17): styles, { width }, styles, styles, styles, HURDLES, styles, Button() (+9 more)

### Community 5 - "OnboardingService"
Cohesion: 0.24
Nodes (16): onboarding_service(), complete(), expenses(), goals(), income(), post, User, spending_style() (+8 more)

### Community 6 - "exceptions.py"
Cohesion: 0.10
Nodes (23): app_error_handler(), AppError, AuthenticationError, AuthorizationError, ConflictError, ExternalServiceError, NotFoundError, Any (+15 more)

### Community 7 - "TransactionRepository"
Cohesion: 0.10
Nodes (11): AsyncSession, AsyncSession, date, Transaction, Single SQL query for income, expenses, and net., SQL GROUP BY for expense breakdown per category., SQL GROUP BY for daily expense totals., Repository (+3 more)

### Community 8 - "Shared Types Package"
Cohesion: 0.07
Nodes (27): AI_PERSONALITIES, AIPersonality, CURRENCY_SYMBOL, DEFAULT_CATEGORIES, DEFAULT_CURRENCY, GOAL_PRIORITIES, GoalPriority, INCOME_FREQUENCIES (+19 more)

### Community 9 - "Backend Test Harness"
Cohesion: 0.13
Nodes (23): auth_headers(), client(), engine(), event_loop_policy(), AsyncClient, register_user(), session_factory(), AsyncClient (+15 more)

### Community 10 - "useAuthStore"
Cohesion: 0.14
Nodes (14): plugins, Index(), styles, queryClient, RootLayoutNav(), ProfileScreen(), AuthState, useAuthStore (+6 more)

### Community 11 - "GoalService"
Cohesion: 0.11
Nodes (30): goal_service(), contribute(), create_goal(), delete_goal(), get_goal(), list_goals(), delete, get (+22 more)

### Community 12 - "expo"
Cohesion: 0.09
Nodes (22): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, expo, android (+14 more)

### Community 13 - "dependencies.py"
Cohesion: 0.13
Nodes (22): get_ai_orchestrator(), get_auth_service(), get_budget_service(), get_current_user(), get_goal_service(), get_health_service(), get_onboarding_service(), get_optional_user() (+14 more)

### Community 14 - "scripts"
Cohesion: 0.10
Nodes (20): devDependencies, turbo, turbo, name, packageManager, private, scripts, build:web (+12 more)

### Community 15 - "tasks"
Cohesion: 0.11
Nodes (19): ^build, dist/**, **/.env.*local, ^lint, .next/**, !.next/cache/**, dependsOn, outputs (+11 more)

### Community 16 - "services/api.ts"
Cohesion: 0.19
Nodes (8): config, api, AuthResponse, LoginPayload, RegisterPayload, Goal, GoalCreate, goalService

### Community 17 - "get_settings"
Cohesion: 0.13
Nodes (14): get_settings(), BaseSettings, field_validator, Application configuration loaded from environment variables. Validates critical…, Centralised application settings backed by .env / env vars., Log a loud warning if the JWT secret is a known insecure default. In production…, Return a cached Settings instance (loaded once per process)., Settings (+6 more)

### Community 18 - "types/api.ts"
Cohesion: 0.11
Nodes (16): ApiError, ApiResponse, AuthTokens, Budget, ChatMessage, DashboardData, FinancialGoal, LoginResponse (+8 more)

### Community 19 - "login.tsx"
Cohesion: 0.21
Nodes (10): LoginForm, loginSchema, LoginScreen(), styles, RegisterForm, registerSchema, RegisterScreen(), styles (+2 more)

### Community 20 - "home.tsx"
Cohesion: 0.13
Nodes (17): styles, formatCurrency(), HomeScreen(), styles, styles, BudgetPlan, budgetService, ChatMessage (+9 more)

### Community 21 - "orchestrator.py"
Cohesion: 0.21
Nodes (13): assemble_context(), FinancialContext, format_context_for_prompt(), AsyncSession, UUID, Context assembler — builds a COMPLETE financial snapshot for AI prompts. This…, Format financial context as human-readable text for prompt injection., Pre-computed financial snapshot injected into AI prompts. Every field is… (+5 more)

### Community 22 - "goals.tsx"
Cohesion: 0.22
Nodes (7): styles, Goal, GOAL_TEMPLATES, styles, Card(), CardProps, styles

### Community 23 - "FastAPI Server"
Cohesion: 0.19
Nodes (14): api service (FastAPI container), db service (postgres:16-alpine), Hardcoded Dev JWT Secret, Service Healthchecks, migrate service (tools profile), pgdata Persistent Volume, redis service (redis:7-alpine), Healthy-Dependency Startup Ordering (+6 more)

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
Cohesion: 0.22
Nodes (10): No Silent Catch on User Actions, React Query Owns Server State, Zustand Owns Session, Backend Environment Variables Contract, Expo Clients (Web + Android), OpenAPI Docs Endpoint, Backend Setup Procedure, Expo Android Dev Target, Expo Web Dev Target (+2 more)

### Community 32 - "Upward Chevron / Ascending Peak Mark"
Cohesion: 0.43
Nodes (7): Finance Buddy Mobile App Icon, Blue Gradient Brand Palette, Circular Construction Grid and Symmetry Axes, Financial Growth / Upward Trend Metaphor, Mobile App Brand Identity Asset, Rounded-Cap Thick Stroke Geometry, Upward Chevron / Ascending Peak Mark

### Community 33 - "expo-router"
Cohesion: 0.17
Nodes (4): styles, TAB_ICONS, TAB_LABELS, expo-router

### Community 34 - "Finance Buddy"
Cohesion: 0.18
Nodes (11): Deterministic Category Seeding at Startup, Four-Step Onboarding Flow, Word-Boundary Transaction Categorization, Adaptive Budget Generation, AI-Native Personal Finance Operating System, Finance Buddy, India-Specific Categories (Auto/Riksha, Kirana, EMI, Chai), India-First Product Design (+3 more)

### Community 35 - "Finance Buddy Android Adaptive Icon Foreground"
Cohesion: 0.53
Nodes (6): Android Adaptive Icon Foreground/Background Layering, Blue Vertical Gradient Brand Palette, Upward Trend / Financial Growth Metaphor, Finance Buddy Android Adaptive Icon Foreground, Adaptive Icon Safe-Zone Padding, Upward Chevron Brand Mark

### Community 36 - "expenses.tsx"
Cohesion: 0.20
Nodes (7): COMMON_EXPENSES, Expense, styles, styles, Input(), InputProps, styles

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

### Community 42 - "env.py"
Cohesion: 0.28
Nodes (8): do_run_migrations(), Alembic environment configuration for async migrations., Run migrations in 'offline' mode., Run migrations in 'online' mode with async engine., Run migrations in 'online' mode., run_async_migrations(), run_migrations_offline(), run_migrations_online()

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
- **212 isolated node(s):** `styles`, `name`, `slug`, `version`, `orientation` (+207 more)
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
- **Why does `User` connect `User` to `schemas.py`, `deps.py`, `application/health.py`, `OnboardingService`, `GoalService`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `TransactionService` connect `schemas.py` to `User`, `deps.py`, `application/health.py`, `TransactionRepository`, `GoalService`, `dependencies.py`, `orchestrator.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `CategoryRepository` connect `deps.py` to `User`, `schemas.py`, `application/health.py`, `OnboardingService`, `TransactionRepository`, `Backend Test Harness`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._