"""Structured error hierarchy for Finance Buddy.

Every business error is a subclass of AppError with a pre-defined HTTP
status code.  The global exception handler in main.py converts these into
consistent JSON envelopes — routers never need to guess status codes.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


# ── Base ────────────────────────────────────────────────────────────────────

class AppError(Exception):
    """Base application error.  All domain errors extend this."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_ERROR"

    def __init__(self, detail: str = "An unexpected error occurred", **extra: Any) -> None:
        self.detail = detail
        self.extra = extra
        super().__init__(detail)


# ── Auth ────────────────────────────────────────────────────────────────────

class AuthenticationError(AppError):
    """Invalid or missing credentials."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "AUTHENTICATION_ERROR"

    def __init__(self, detail: str = "Invalid or expired credentials") -> None:
        super().__init__(detail)


class AuthorizationError(AppError):
    """Authenticated but lacking permissions."""

    status_code = status.HTTP_403_FORBIDDEN
    error_code = "AUTHORIZATION_ERROR"

    def __init__(self, detail: str = "You do not have permission to perform this action") -> None:
        super().__init__(detail)


# ── CRUD ────────────────────────────────────────────────────────────────────

class NotFoundError(AppError):
    """Requested resource does not exist."""

    status_code = status.HTTP_404_NOT_FOUND
    error_code = "NOT_FOUND"

    def __init__(self, resource: str = "Resource", identifier: str | None = None) -> None:
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} '{identifier}' not found"
        super().__init__(detail, resource=resource, identifier=identifier)


class ConflictError(AppError):
    """Resource already exists or state conflict."""

    status_code = status.HTTP_409_CONFLICT
    error_code = "CONFLICT"

    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(detail)


class ValidationError(AppError):
    """Business-rule validation failure (not schema validation)."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "VALIDATION_ERROR"

    def __init__(self, detail: str = "Validation failed") -> None:
        super().__init__(detail)


# ── External ────────────────────────────────────────────────────────────────

class ExternalServiceError(AppError):
    """Third-party service (AI, payment gateway, etc.) failed."""

    status_code = status.HTTP_502_BAD_GATEWAY
    error_code = "EXTERNAL_SERVICE_ERROR"

    def __init__(self, service: str = "external service", detail: str | None = None) -> None:
        msg = f"{service} is temporarily unavailable"
        if detail:
            msg = f"{service}: {detail}"
        super().__init__(msg, service=service)


# ── Exception handlers (registered in main.py) ─────────────────────────────

async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    """Convert any AppError into a structured JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code,
        },
    )


async def unhandled_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unexpected errors — logs the traceback, returns a safe message."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal error occurred. Please try again.",
            "error_code": "INTERNAL_ERROR",
        },
    )
