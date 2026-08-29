# Graph Report - finance buddy  (2026-08-22)

## Corpus Check
- Corpus is ~48,235 words - fits in a single context window. You may not need a graph.

## Summary
- 995 nodes · 2121 edges · 85 communities (57 shown, 28 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.93)
- Token cost: 244,905 input · 43,223 output

## Community Hubs (Navigation)
- API Dependency & ORM Core
- Transactions Feature Slice
- Auth & Error Handling
- Financial Health Scoring
- Mobile Screens & Tabs
- AI Chat Feature Slice
- Legacy Exception Hierarchy
- SQL Repository Aggregations
- Shared Types Package
- Backend Test Harness
- Mobile Routing & Auth Store
- Goals Feature Slice
- Expo App Icon Config
- Legacy DI Providers
- Monorepo Root Scripts
- Turborepo Pipeline Config
- Mobile API Service Layer
- Migrations & App Config
- Mobile API Type Definitions
- Mobile Auth Screens
- Dashboard & Transaction UI
- AI Context Assembly
- Budget UI Screens
- Local Dev Infrastructure
- Mobile Runtime Dependencies
- Mobile Theme & Categories
- AI Orchestration & Fallbacks
- Mobile Form Validation Schemas
- Mobile Package Scripts
- Date Formatting Utilities
- Deterministic AI Trust Boundary
- Dev Setup & State Rules
- App Icon Brand Design
- Async Database Session
- India-First Categorization
- Adaptive Icon Foreground
- Product Identity & Stack
- Shared Package Manifest
- DDD Layering Decisions
- Adaptive Icon Background
- Monochrome Themed Icon
- Favicon Scaffold Asset
- Mobile TypeScript DevDeps
- Mobile TypeScript Config
- API Contract Conventions
- Splash Screen Placeholder
- Legacy App Entry
- Indian Currency Formatting
- Health Score Metrics
- Expo SDK Dependency
- Expo Constants Dependency
- Anton Font Dependency
- Expo Linking Dependency
- Metro Runtime Dependency
- Expo Router Dependency
- Expo SecureStore Dependency
- Expo StatusBar Dependency
- Expo SystemUI Dependency
- Hookform Resolvers Dependency
- React Dependency
- React DOM Dependency
- React Hook Form Dependency
- Gesture Handler Dependency
- Safe Area Context Dependency
- React Native Screens Dependency
- React Native Web Dependency
- Zustand Dependency
- AI Package Init
- Application Package Init
- Core Package Init
- Domain Package Init
- Infrastructure Package Init
- ORM Package Init
- Backend Package Init
- Backend Project Manifest

## God Nodes (most connected - your core abstractions)
1. `User` - 51 edges
2. `TransactionService` - 39 edges
3. `GoalService` - 34 edges
4. `ChatService` - 28 edges
5. `OnboardingService` - 27 edges
6. `CategoryRepository` - 25 edges
7. `BudgetService` - 24 edges
8. `AuthService` - 22 edges
9. `Base` - 21 edges
10. `Theme` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Domain Layer (pure types, enums, deterministic rules)` --semantically_similar_to--> `Financial Rules Engine (Deterministic, Testable, Auditable)`  [INFERRED] [semantically similar]
  PROGRESS.md → README.md
- `db service (postgres:16-alpine)` --implements--> `PostgreSQL 16`  [INFERRED]
  docker-compose.yml → README.md
- `Stateless Refresh Tokens Never Revoked` --conceptually_related_to--> `Redis 7 Cache`  [AMBIGUOUS]
  PROGRESS.md → README.md
- `Backend Setup Procedure` --references--> `Backend Environment Variables Contract`  [INFERRED]
  SETUP.md → README.md
- `Budget Pacing Context for AI Chat` --implements--> `Core Principle: Trust (LLMs never compute balances)`  [INFERRED]
  PROGRESS.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **DDD Layer Stack** — progress_ddd_layering, progress_domain_layer, progress_application_layer, progress_repositories_persistence_only, progress_api_schemas_contract [EXTRACTED 1.00]
- **India-First Localization System** — readme_india_first, readme_indian_numbering, readme_india_categories, readme_salary_cycle_awareness [EXTRACTED 1.00]
- **Local Dev Infrastructure Stack** — docker_compose_db_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_migrate_service, docker_compose_healthchecks [EXTRACTED 1.00]
- **Android Adaptive Icon Background Composition** — apps_mobile_assets_android_icon_background, apps_mobile_assets_android_icon_background_adaptive_icon_background_layer, apps_mobile_assets_android_icon_background_safe_zone_construction_guides, apps_mobile_assets_android_icon_background_brand_pale_blue_fill [INFERRED 0.85]
- **Mobile Brand Identity System (mark, palette, adaptive-icon delivery)** — apps_mobile_assets_android_icon_foreground_icon, apps_mobile_assets_android_icon_foreground_upward_chevron_mark, apps_mobile_assets_android_icon_foreground_blue_gradient_palette, apps_mobile_assets_android_icon_foreground_growth_upward_trend_metaphor [INFERRED 0.85]
- **Android Adaptive Icon Authoring Constraints** — apps_mobile_assets_android_icon_foreground_icon, apps_mobile_assets_android_icon_foreground_adaptive_icon_layering, apps_mobile_assets_android_icon_foreground_safe_zone_padding [EXTRACTED 1.00]
- **Finance Buddy Android Launcher Identity System** — apps_mobile_assets_android_icon_monochrome_icon, apps_mobile_assets_android_icon_monochrome_chevron_mark, apps_mobile_assets_android_icon_monochrome_material_you_themed_icon_layer, apps_mobile_assets_android_icon_monochrome_rounded_geometry_treatment, apps_mobile_assets_android_icon_monochrome_upward_growth_motif [INFERRED 0.85]
- **Mobile App Visual Identity (mark + palette + tab-icon role)** — apps_mobile_assets_favicon_favicon, apps_mobile_assets_favicon_upward_chevron_mark, apps_mobile_assets_favicon_blue_on_pale_tint_palette, apps_mobile_assets_favicon_browser_tab_identity [INFERRED 0.75]
- **Icon Visual Design System (mark, grid, palette, stroke geometry)** — apps_mobile_assets_icon_upward_chevron_mark, apps_mobile_assets_icon_construction_grid, apps_mobile_assets_icon_blue_gradient_palette, apps_mobile_assets_icon_rounded_stroke_geometry [INFERRED 0.85]

## Communities (85 total, 28 thin omitted)

### Community 0 - "API Dependency & ORM Core"
Cohesion: 0.06
Nodes (78): budget_service(), current_user(), goal_service(), onboarding_service(), AsyncSession, HTTPAuthorizationCredentials, User, current_budget() (+70 more)

### Community 1 - "Transactions Feature Slice"
Cohesion: 0.08
Nodes (53): transaction_service(), create_transaction(), delete_transaction(), get_transaction(), list_transactions(), monthly_summary(), date, delete (+45 more)

### Community 2 - "Auth & Error Handling"
Cohesion: 0.08
Nodes (42): auth_service(), login(), me(), get, post, User, refresh(), register() (+34 more)

### Community 3 - "Financial Health Scoring"
Cohesion: 0.08
Nodes (39): health_service(), history(), get, User, score(), HealthScoreResponse, HealthService, AsyncSession (+31 more)

### Community 4 - "Mobile Screens & Tabs"
Cohesion: 0.08
Nodes (28): styles, { width }, Message, QUICK_PROMPTS, styles, styles, TAB_EMOJIS, TAB_ICONS (+20 more)

### Community 5 - "AI Chat Feature Slice"
Cohesion: 0.11
Nodes (25): AsyncSession, chat_service(), conversations(), messages(), get, post, User, send() (+17 more)

### Community 6 - "Legacy Exception Hierarchy"
Cohesion: 0.10
Nodes (23): app_error_handler(), AppError, AuthenticationError, AuthorizationError, ConflictError, ExternalServiceError, NotFoundError, Any (+15 more)

### Community 7 - "SQL Repository Aggregations"
Cohesion: 0.11
Nodes (10): AsyncSession, date, Transaction, Single SQL query for income, expenses, and net., SQL GROUP BY for expense breakdown per category., SQL GROUP BY for daily expense totals., Repository, TransactionRepository (+2 more)

### Community 8 - "Shared Types Package"
Cohesion: 0.07
Nodes (27): AI_PERSONALITIES, AIPersonality, CURRENCY_SYMBOL, DEFAULT_CATEGORIES, DEFAULT_CURRENCY, GOAL_PRIORITIES, GoalPriority, INCOME_FREQUENCIES (+19 more)

### Community 9 - "Backend Test Harness"
Cohesion: 0.13
Nodes (23): auth_headers(), client(), engine(), event_loop_policy(), AsyncClient, register_user(), session_factory(), AsyncClient (+15 more)

### Community 10 - "Mobile Routing & Auth Store"
Cohesion: 0.10
Nodes (14): plugins, Index(), styles, queryClient, RootLayoutNav(), AuthState, useAuthStore, User (+6 more)

### Community 11 - "Goals Feature Slice"
Cohesion: 0.16
Nodes (16): ContributionCreate, GoalCreate, GoalResponse, GoalUpdate, GoalService, AsyncSession, Goal, GoalCreate (+8 more)

### Community 12 - "Expo App Icon Config"
Cohesion: 0.09
Nodes (22): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, expo, android (+14 more)

### Community 13 - "Legacy DI Providers"
Cohesion: 0.13
Nodes (22): get_ai_orchestrator(), get_auth_service(), get_budget_service(), get_current_user(), get_goal_service(), get_health_service(), get_onboarding_service(), get_optional_user() (+14 more)

### Community 14 - "Monorepo Root Scripts"
Cohesion: 0.10
Nodes (20): devDependencies, turbo, turbo, name, packageManager, private, scripts, build:web (+12 more)

### Community 15 - "Turborepo Pipeline Config"
Cohesion: 0.11
Nodes (19): ^build, dist/**, **/.env.*local, ^lint, .next/**, !.next/cache/**, dependsOn, outputs (+11 more)

### Community 16 - "Mobile API Service Layer"
Cohesion: 0.16
Nodes (13): formatCurrency(), ProfileScreen(), styles, config, api, ChatMessage, ChatResponse, chatService (+5 more)

### Community 17 - "Migrations & App Config"
Cohesion: 0.13
Nodes (16): do_run_migrations(), Alembic environment configuration for async migrations., Run migrations in 'offline' mode., Run migrations in 'online' mode with async engine., Run migrations in 'online' mode., run_async_migrations(), run_migrations_offline(), run_migrations_online() (+8 more)

### Community 18 - "Mobile API Type Definitions"
Cohesion: 0.11
Nodes (16): ApiError, ApiResponse, AuthTokens, Budget, ChatMessage, DashboardData, FinancialGoal, LoginResponse (+8 more)

### Community 19 - "Mobile Auth Screens"
Cohesion: 0.15
Nodes (13): LoginForm, loginSchema, LoginScreen(), styles, RegisterForm, registerSchema, RegisterScreen(), styles (+5 more)

### Community 20 - "Dashboard & Transaction UI"
Cohesion: 0.17
Nodes (13): DashboardScreen(), formatCurrency(), styles, CATEGORIES, FilterType, formatCurrency(), styles, TransactionsScreen() (+5 more)

### Community 21 - "AI Context Assembly"
Cohesion: 0.21
Nodes (13): assemble_context(), FinancialContext, format_context_for_prompt(), AsyncSession, UUID, Context assembler — builds a COMPLETE financial snapshot for AI prompts. This…, Format financial context as human-readable text for prompt injection., Pre-computed financial snapshot injected into AI prompts. Every field is… (+5 more)

### Community 22 - "Budget UI Screens"
Cohesion: 0.18
Nodes (11): BudgetCategory, BudgetScreen(), CATEGORY_ICONS, formatCurrency(), styles, styles, Card(), CardProps (+3 more)

### Community 23 - "Local Dev Infrastructure"
Cohesion: 0.18
Nodes (14): api service (FastAPI container), db service (postgres:16-alpine), Service Healthchecks, migrate service (tools profile), pgdata Persistent Volume, redis service (redis:7-alpine), Healthy-Dependency Startup Ordering, Stateless Refresh Tokens Never Revoked (+6 more)

### Community 24 - "Mobile Runtime Dependencies"
Cohesion: 0.15
Nodes (13): dependencies, axios, expo-font, expo-haptics, react-native, @tanstack/react-query, zod, axios (+5 more)

### Community 25 - "Mobile Theme & Categories"
Cohesion: 0.18
Nodes (8): Category, expenseCategories, borderRadius, colors, glassmorphism, shadows, spacing, typography

### Community 26 - "AI Orchestration & Fallbacks"
Cohesion: 0.18
Nodes (9): generate_fallback_response(), AI fallbacks — graceful degradation when Gemini is unavailable. Uses random…, Return a helpful fallback response (stateless, random selection)., AIOrchestrator, ChatResponse, UUID, Main AI coordination — assembles context, calls Gemini, parses response., Process a user message and return AI response. (+1 more)

### Community 27 - "Mobile Form Validation Schemas"
Cohesion: 0.18
Nodes (10): GoalFormData, goalSchema, LoginFormData, loginSchema, OnboardingIncomeData, onboardingIncomeSchema, RegisterFormData, registerSchema (+2 more)

### Community 28 - "Mobile Package Scripts"
Cohesion: 0.20
Nodes (9): main, name, private, scripts, android, ios, start, web (+1 more)

### Community 29 - "Date Formatting Utilities"
Cohesion: 0.28
Nodes (6): DAYS, formatDate(), getRelativeTime(), MONTHS, MONTHS_SHORT, pad()

### Community 30 - "Deterministic AI Trust Boundary"
Cohesion: 0.29
Nodes (8): Budget Pacing Context for AI Chat, Date-Aware Goal Allocation, Domain Layer (pure types, enums, deterministic rules), Goal Contribution Overshoot Cap, Financial Rules Engine (Deterministic, Testable, Auditable), Google Gemini API, Core Principle: Trust (LLMs never compute balances), Optional Gemini Key with Feature Fallback

### Community 31 - "Dev Setup & State Rules"
Cohesion: 0.29
Nodes (8): No Silent Catch on User Actions, React Query Owns Server State, Zustand Owns Session, Backend Environment Variables Contract, Expo Clients (Web + Android), Backend Setup Procedure, Expo Android Dev Target, Expo Web Dev Target, uv Python Package Manager

### Community 32 - "App Icon Brand Design"
Cohesion: 0.43
Nodes (7): Finance Buddy Mobile App Icon, Blue Gradient Brand Palette, Circular Construction Grid and Symmetry Axes, Financial Growth / Upward Trend Metaphor, Mobile App Brand Identity Asset, Rounded-Cap Thick Stroke Geometry, Upward Chevron / Ascending Peak Mark

### Community 33 - "Async Database Session"
Cohesion: 0.29
Nodes (6): create_tables(), get_db_session(), AsyncSession, Async SQLAlchemy engine, session factory, and FastAPI dependency. Supports…, FastAPI dependency — yields an async session with auto commit/rollback., Create all tables (SQLite dev mode — Alembic handles production).

### Community 34 - "India-First Categorization"
Cohesion: 0.29
Nodes (7): Deterministic Category Seeding at Startup, Four-Step Onboarding Flow, Word-Boundary Transaction Categorization, Adaptive Budget Generation, India-Specific Categories (Auto/Riksha, Kirana, EMI, Chai), India-First Product Design, Salary Cycle Awareness

### Community 35 - "Adaptive Icon Foreground"
Cohesion: 0.53
Nodes (6): Android Adaptive Icon Foreground/Background Layering, Blue Vertical Gradient Brand Palette, Upward Trend / Financial Growth Metaphor, Finance Buddy Android Adaptive Icon Foreground, Adaptive Icon Safe-Zone Padding, Upward Chevron Brand Mark

### Community 36 - "Product Identity & Stack"
Cohesion: 0.33
Nodes (6): Hardcoded Dev JWT Secret, AI-Native Personal Finance Operating System, Finance Buddy, Custom JWT + Argon2 Auth, Psychological Spending Coaching, Turborepo Monorepo

### Community 37 - "Shared Package Manifest"
Cohesion: 0.33
Nodes (5): main, name, private, types, version

### Community 38 - "DDD Layering Decisions"
Cohesion: 0.40
Nodes (6): Application Layer (use cases, transaction boundaries), Chat Ownership Verification, Legacy Correctness Drift (phantom ORM columns), DDD Layering (core/domain/application/infrastructure/api), Repositories Own Only Persistence, SQL Aggregation for Monthly Summary

### Community 39 - "Adaptive Icon Background"
Cohesion: 0.70
Nodes (5): Android Adaptive Icon Background Asset, Adaptive Icon Background Layer Pattern, Brand Pale Blue Fill, Optical Center Offset, Icon Safe Zone Construction Guides

### Community 40 - "Monochrome Themed Icon"
Cohesion: 0.60
Nodes (5): Upward Chevron Brand Mark, Android Monochrome App Icon (Finance Buddy), Material You Themed Icon Monochrome Layer, Rounded-Cap Geometric Glyph Treatment, Upward Growth / Rising Trend Visual Motif

### Community 41 - "Favicon Scaffold Asset"
Cohesion: 0.60
Nodes (5): Blue-on-Pale-Tint Icon Palette, Browser Tab / PWA Identity Asset Role, Unbranded Expo Scaffold Default Artwork, Mobile App Favicon (Expo web icon), Upward Chevron Brand Mark

### Community 42 - "Mobile TypeScript DevDeps"
Cohesion: 0.40
Nodes (5): devDependencies, @types/react, typescript, @types/react, typescript

### Community 43 - "Mobile TypeScript Config"
Cohesion: 0.40
Nodes (4): compilerOptions, strict, extends, expo/tsconfig.base

### Community 44 - "API Contract Conventions"
Cohesion: 0.40
Nodes (5): API Schemas as Sole HTTP Contract, Decimal Money, Strings Over HTTP, Single Pagination Envelope, PUT/PATCH Client-Server Verb Mismatch, Indian Numbering System (INR formatting)

### Community 45 - "Splash Screen Placeholder"
Cohesion: 0.67
Nodes (4): Splash Icon Asset (concentric rings on grid), Centred Grid Alignment Guide Motif, Expo Splash Screen Launch Asset Slot, Unreplaced Expo Template Placeholder Branding

### Community 48 - "Health Score Metrics"
Cohesion: 1.00
Nodes (3): Financial Health Score, Tiered Recommendations Engine, Month-Over-Month Spending Trend

## Ambiguous Edges - Review These
- `Redis 7 Cache` → `Stateless Refresh Tokens Never Revoked`  [AMBIGUOUS]
  PROGRESS.md · relation: conceptually_related_to
- `Icon Safe Zone Construction Guides` → `Optical Center Offset`  [AMBIGUOUS]
  apps/mobile/assets/android-icon-background.png · relation: rationale_for
- `Upward Chevron Brand Mark` → `Android Adaptive Icon Foreground/Background Layering`  [AMBIGUOUS]
  apps/mobile/assets/android-icon-foreground.png · relation: shares_data_with
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
- **What is the exact relationship between `Icon Safe Zone Construction Guides` and `Optical Center Offset`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
- **What is the exact relationship between `Upward Chevron Brand Mark` and `Android Adaptive Icon Foreground/Background Layering`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `Upward Chevron Brand Mark` and `Unbranded Expo Scaffold Default Artwork`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `User` connect `API Dependency & ORM Core` to `Transactions Feature Slice`, `Auth & Error Handling`, `Financial Health Scoring`, `AI Chat Feature Slice`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `TransactionService` connect `Transactions Feature Slice` to `API Dependency & ORM Core`, `Financial Health Scoring`, `AI Chat Feature Slice`, `SQL Repository Aggregations`, `Goals Feature Slice`, `Legacy DI Providers`, `AI Context Assembly`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `CategoryRepository` connect `API Dependency & ORM Core` to `Transactions Feature Slice`, `Auth & Error Handling`, `Backend Test Harness`, `SQL Repository Aggregations`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._