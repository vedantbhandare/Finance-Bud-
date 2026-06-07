// ============================================================
// Shared API Types — Used by both Frontend and Backend
// ============================================================

// --- Auth ---
export interface UserResponse {
  id: string;
  email: string;
  display_name: string | null;
  currency: string;
  onboarding_completed: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
  user: UserResponse;
}

// --- Transactions ---
export type TransactionType = 'expense' | 'income';

export interface TransactionResponse {
  id: string;
  category_id: string | null;
  category_name: string | null;
  amount: string; // Decimal as string for precision
  type: TransactionType;
  description: string | null;
  merchant: string | null;
  transaction_date: string;
  is_recurring: boolean;
  source: string;
  created_at: string;
}

export interface MonthlySummary {
  total_income: string;
  total_expenses: string;
  net: string;
  by_category: CategorySummary[];
  daily_trend: DailySpend[];
}

export interface CategorySummary {
  category_id: string;
  category_name: string;
  total: string;
  percentage: number;
  color: string;
}

export interface DailySpend {
  date: string;
  amount: string;
}

// --- Budget ---
export interface BudgetPlanResponse {
  id: string;
  period_start: string;
  period_end: string;
  total_income: string;
  total_allocated: string;
  is_ai_generated: boolean;
  ai_reasoning: string | null;
  status: 'draft' | 'active' | 'expired';
  allocations: BudgetAllocationResponse[];
}

export interface BudgetAllocationResponse {
  id: string;
  category_id: string;
  category_name: string;
  allocated_amount: string;
  spent_amount: string;
  remaining: string;
  utilization_pct: number;
}

// --- Goals ---
export type GoalStatus = 'active' | 'paused' | 'completed' | 'abandoned';

export interface GoalResponse {
  id: string;
  name: string;
  target_amount: string;
  current_amount: string;
  target_date: string | null;
  priority: number;
  status: GoalStatus;
  progress_pct: number;
  created_at: string;
}

// --- Health ---
export interface HealthScoreResponse {
  overall_score: number;
  savings_rate: number;
  budget_adherence: number;
  goal_progress: number;
  spending_trend: 'improving' | 'stable' | 'declining';
  breakdown: Record<string, number>;
}

// --- Chat ---
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  metadata?: {
    tokens_used?: number;
    model?: string;
    latency_ms?: number;
  };
}

export interface ChatResponse {
  reply: string;
  conversation_id: string;
  metadata: {
    tokens_used: number;
    model: string;
    latency_ms: number;
  };
}

// --- Categories ---
export interface CategoryResponse {
  id: string;
  name: string;
  icon: string;
  color: string;
  is_system: boolean;
  parent_category_id: string | null;
}

// --- Pagination ---
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

// --- Error ---
export interface ErrorResponse {
  detail: string;
  code?: string;
}
