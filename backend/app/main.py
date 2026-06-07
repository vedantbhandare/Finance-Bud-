"""Finance Buddy — FastAPI Application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle — startup and shutdown."""
    settings = get_settings()

    # Auto-create tables for SQLite dev mode
    if settings.database_url.startswith("sqlite"):
        from app.database import create_tables
        await create_tables()
        print("[OK] SQLite tables created")

    # Initialize Redis connection pool (optional — skip if unavailable)
    try:
        import redis.asyncio as aioredis
        pool = aioredis.ConnectionPool.from_url(
            settings.redis_url,
            max_connections=50,
            decode_responses=True,
        )
        app.state.redis = aioredis.Redis(connection_pool=pool)
        # Test connection
        await app.state.redis.ping()
        print("[OK] Redis connected")
    except Exception:
        app.state.redis = None
        print("[WARN] Redis not available - running without cache")

    yield

    # Cleanup
    if hasattr(app.state, 'redis') and app.state.redis:
        try:
            await app.state.redis.connection_pool.disconnect()
        except Exception:
            pass


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="AI-native personal finance operating system",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS — allow frontend origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8081",   # Expo web
            "http://localhost:19006",  # Expo web alt
            "http://localhost:3000",   # Next.js (future)
            "http://localhost:5173",   # Vite (future)
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register global exception handler
    from app.middleware.error_handler import global_exception_handler
    app.add_exception_handler(Exception, global_exception_handler)

    # Register routers
    from app.routers import auth, budgets, chat, goals, health, onboarding, transactions

    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(onboarding.router, prefix="/api/v1/onboarding", tags=["Onboarding"])
    app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
    app.include_router(budgets.router, prefix="/api/v1/budgets", tags=["Budgets"])
    app.include_router(goals.router, prefix="/api/v1/goals", tags=["Goals"])
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
    app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])

    @app.get("/api/health", tags=["System"])
    async def health_check():
        return {"status": "healthy", "version": "0.1.0"}

    return app


app = create_app()
