from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, budgets, categories, chat, goals, health, onboarding, transactions
from app.core.config import get_settings
from app.core.database import SessionFactory, create_schema
from app.core.errors import AppError, app_error_handler, unhandled_error_handler
from app.infrastructure.orm.repositories import CategoryRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    if settings.database_url.startswith("sqlite"):
        await create_schema()
        async with SessionFactory() as session:
            await CategoryRepository(session).ensure_system_categories()
            await session.commit()

    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-native personal finance operating system",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)

    api_prefix = "/api/v1"
    app.include_router(auth.router, prefix=api_prefix)
    app.include_router(categories.router, prefix=api_prefix)
    app.include_router(onboarding.router, prefix=api_prefix)
    app.include_router(transactions.router, prefix=api_prefix)
    app.include_router(budgets.router, prefix=api_prefix)
    app.include_router(goals.router, prefix=api_prefix)
    app.include_router(health.router, prefix=api_prefix)
    app.include_router(chat.router, prefix=api_prefix)

    @app.get("/api/health", tags=["System"])
    async def health_check():
        return {"status": "healthy", "version": settings.app_version}

    return app


app = create_app()
