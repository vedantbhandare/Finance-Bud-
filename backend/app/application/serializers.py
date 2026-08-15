from __future__ import annotations

from decimal import Decimal

from app.api.schemas import (
    BudgetAllocationResponse,
    BudgetPlanResponse,
    GoalResponse,
    TransactionResponse,
)
from app.domain.categories import color_for_category
from app.infrastructure.orm.models import BudgetAllocation, BudgetPlan, Goal, Transaction


def transaction_response(transaction: Transaction) -> TransactionResponse:
    category = transaction.category
    return TransactionResponse(
        id=transaction.id,
        category_id=transaction.category_id,
        category_name=category.name if category else None,
        category_icon=category.icon if category else None,
        category_color=color_for_category(category.name if category else None),
        amount=transaction.amount,
        type=transaction.transaction_type,
        description=transaction.description,
        merchant=transaction.merchant,
        transaction_date=transaction.transaction_date,
        notes=transaction.notes,
        is_recurring=transaction.is_recurring,
        source=transaction.source or "manual",
        created_at=transaction.created_at,
    )


def goal_response(goal: Goal) -> GoalResponse:
    target = goal.target_amount or Decimal("0.00")
    current = goal.current_amount or Decimal("0.00")
    progress = float(min(Decimal("100.00"), (current / target * 100) if target > 0 else Decimal("0.00")))
    remaining = max(Decimal("0.00"), target - current)
    status = "abandoned" if goal.status == "cancelled" else goal.status
    return GoalResponse(
        id=goal.id,
        name=goal.name,
        description=goal.description,
        target_amount=target,
        current_amount=current,
        target_date=goal.target_date,
        icon=goal.icon,
        status=status,
        progress_pct=round(progress, 2),
        remaining_amount=remaining,
        created_at=goal.created_at,
    )


def budget_allocation_response(allocation: BudgetAllocation) -> BudgetAllocationResponse:
    allocated = allocation.allocated_amount or Decimal("0.00")
    spent = allocation.spent_amount or Decimal("0.00")
    remaining = allocated - spent
    pct = float((spent / allocated * 100) if allocated > 0 else Decimal("0.00"))
    category = allocation.category
    category_name = category.name if category else "Uncategorized"
    return BudgetAllocationResponse(
        id=allocation.id,
        category_id=allocation.category_id,
        category_name=category_name,
        category_icon=category.icon if category else None,
        category_color=color_for_category(category_name),
        allocated_amount=allocated,
        spent_amount=spent,
        remaining=remaining,
        utilization_pct=round(pct, 2),
    )


def budget_response(plan: BudgetPlan) -> BudgetPlanResponse:
    allocations = [budget_allocation_response(allocation) for allocation in plan.allocations]
    return BudgetPlanResponse(
        id=plan.id,
        period_start=plan.month_start,
        period_end=plan.month_end,
        total_income=plan.total_income,
        total_allocated=sum((a.allocated_amount for a in plan.allocations), Decimal("0.00")),
        needs_pct=plan.needs_pct,
        wants_pct=plan.wants_pct,
        savings_pct=plan.savings_pct,
        is_ai_generated=plan.is_ai_generated,
        ai_reasoning=plan.ai_reasoning,
        status=plan.status,
        allocations=allocations,
    )

