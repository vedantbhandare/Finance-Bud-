from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Generic, Literal, TypeVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.categories import color_for_category

T = TypeVar("T")


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int
    pages: int


class RegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)

    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if "@" not in cleaned or "." not in cleaned.rsplit("@", 1)[-1]:
            raise ValueError("Enter a valid email address")
        return cleaned


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    is_active: bool
    is_onboarded: bool
    monthly_salary: Decimal | None = None
    pay_cycle_day: int = 1
    currency: Literal["INR"] = "INR"
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"
    user: UserResponse


class CategoryResponse(BaseModel):
    id: str
    name: str
    icon: str | None
    color: str
    category_type: str
    is_system: bool


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    type: Literal["expense", "income"]
    description: str | None = Field(default=None, max_length=500)
    merchant: str | None = Field(default=None, max_length=200)
    category_id: str | None = None
    category_name: str | None = Field(default=None, validation_alias=AliasChoices("category_name", "category"))
    transaction_date: date | None = Field(default=None, validation_alias=AliasChoices("transaction_date", "date"))
    notes: str | None = None
    is_recurring: bool = False


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, max_digits=14, decimal_places=2)
    type: Literal["expense", "income"] | None = None
    description: str | None = Field(default=None, max_length=500)
    merchant: str | None = Field(default=None, max_length=200)
    category_id: str | None = None
    category_name: str | None = Field(default=None, validation_alias=AliasChoices("category_name", "category"))
    transaction_date: date | None = Field(default=None, validation_alias=AliasChoices("transaction_date", "date"))
    notes: str | None = None
    is_recurring: bool | None = None


class TransactionResponse(BaseModel):
    id: str
    category_id: str | None
    category_name: str | None
    category_icon: str | None
    category_color: str
    amount: Decimal
    type: Literal["expense", "income"]
    description: str | None
    merchant: str | None
    transaction_date: date
    notes: str | None = None
    is_recurring: bool
    source: str
    created_at: datetime


class CategorySummary(BaseModel):
    category_id: str | None
    category_name: str
    total: Decimal
    percentage: float
    color: str


class DailySpend(BaseModel):
    date: date
    amount: Decimal


class MonthlySummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net: Decimal
    by_category: list[CategorySummary]
    daily_trend: list[DailySpend]


class IncomeSetup(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    source_name: str | None = Field(default="Primary", max_length=100)
    frequency: Literal["monthly", "biweekly", "weekly"] = "monthly"
    pay_day: int = Field(default=1, ge=1, le=28)


class ExpenseItem(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    frequency: Literal["monthly", "weekly", "yearly"] = "monthly"
    start_date: date | None = None
    category_name: str | None = None


class ExpenseSetup(BaseModel):
    expenses: list[ExpenseItem] = Field(default_factory=list)


class GoalItem(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    target_amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    target_date: date | None = None
    priority: int = Field(default=1, ge=1, le=10)


class GoalSetup(BaseModel):
    goals: list[GoalItem] = Field(default_factory=list)


class SpendingStyleSetup(BaseModel):
    overspending_categories: list[str] = Field(default_factory=list)
    ai_personality: Literal["supportive", "direct", "analytical", "balanced"] = "balanced"


class StatusResponse(BaseModel):
    status: Literal["success"] = "success"
    message: str


class BudgetAllocationResponse(BaseModel):
    id: str
    category_id: str | None
    category_name: str
    category_icon: str | None
    category_color: str
    allocated_amount: Decimal
    spent_amount: Decimal
    remaining: Decimal
    utilization_pct: float


class BudgetPlanResponse(BaseModel):
    id: str
    period_start: date
    period_end: date
    total_income: Decimal
    total_allocated: Decimal
    needs_pct: Decimal
    wants_pct: Decimal
    savings_pct: Decimal
    is_ai_generated: bool
    ai_reasoning: str | None
    status: str
    allocations: list[BudgetAllocationResponse]


class BudgetEnvelope(BaseModel):
    budget: BudgetPlanResponse | None
    message: str | None = None


class BudgetGenerateResponse(BaseModel):
    budget_plan: BudgetPlanResponse
    message: str


class GoalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    target_amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    target_date: date | None = None
    icon: str | None = None
    priority: int = Field(default=1, ge=1, le=10)


class GoalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    target_amount: Decimal | None = Field(default=None, gt=0, max_digits=14, decimal_places=2)
    target_date: date | None = None
    icon: str | None = None
    status: Literal["active", "paused", "completed", "abandoned"] | None = None


class ContributionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    notes: str | None = Field(default=None, validation_alias=AliasChoices("notes", "note"))


class GoalResponse(BaseModel):
    id: str
    name: str
    description: str | None
    target_amount: Decimal
    current_amount: Decimal
    target_date: date | None
    priority: int = 1
    icon: str | None
    status: Literal["active", "paused", "completed", "abandoned"]
    progress_pct: float
    remaining_amount: Decimal
    created_at: datetime


class HealthScoreResponse(BaseModel):
    overall_score: int
    label: str
    savings_rate: float
    budget_adherence: float
    goal_progress: float
    spending_trend: str
    recommendations: list[str]


class FinancialContextResponse(BaseModel):
    monthly_income: Decimal
    total_spent_this_month: Decimal
    remaining_budget: Decimal
    savings_rate: float
    health_score: int
    days_until_payday: int
    spending_trend: str = "stable"
    top_spending_categories: list[CategorySummary]
    recent_transactions: list[TransactionResponse]
    active_goals: list[GoalResponse]
    budget_allocations: list[BudgetAllocationResponse] = Field(default_factory=list)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: str | None = None


class ChatMetadata(BaseModel):
    tokens_used: int = 0
    model: str = "fallback"
    latency_ms: int = 0


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    suggestions: list[str] = Field(default_factory=list)
    metadata: ChatMetadata = Field(default_factory=ChatMetadata)


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime


def category_to_response(category: Any) -> CategoryResponse:
    return CategoryResponse(
        id=category.id,
        name=category.name,
        icon=category.icon,
        color=color_for_category(category.name),
        category_type=category.category_type,
        is_system=category.is_system,
    )

