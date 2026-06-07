// ============================================================
// Shared Constants — Used by both Frontend and Backend
// ============================================================

/** Default expense categories for India-first MVP */
export const DEFAULT_CATEGORIES = [
  // Essentials
  { name: 'Rent/Housing', icon: '🏠', color: '#6366F1', group: 'essentials' },
  { name: 'Groceries/Kirana', icon: '🛒', color: '#22C55E', group: 'essentials' },
  { name: 'Utilities', icon: '💡', color: '#EAB308', group: 'essentials' },
  { name: 'Phone/Internet', icon: '📱', color: '#3B82F6', group: 'essentials' },
  { name: 'Insurance', icon: '🛡️', color: '#8B5CF6', group: 'essentials' },
  { name: 'EMI/Loan', icon: '🏦', color: '#EF4444', group: 'essentials' },

  // Transport
  { name: 'Auto/Riksha', icon: '🛺', color: '#F59E0B', group: 'transport' },
  { name: 'Fuel/Petrol', icon: '⛽', color: '#F97316', group: 'transport' },
  { name: 'Metro/Bus', icon: '🚇', color: '#06B6D4', group: 'transport' },
  { name: 'Cab/Uber/Ola', icon: '🚗', color: '#14B8A6', group: 'transport' },

  // Food
  { name: 'Eating Out', icon: '🍽️', color: '#EC4899', group: 'food' },
  { name: 'Chai/Coffee', icon: '☕', color: '#92400E', group: 'food' },
  { name: 'Swiggy/Zomato', icon: '📦', color: '#F43F5E', group: 'food' },

  // Lifestyle
  { name: 'Shopping', icon: '🛍️', color: '#A855F7', group: 'lifestyle' },
  { name: 'Entertainment', icon: '🎬', color: '#D946EF', group: 'lifestyle' },
  { name: 'Health/Medical', icon: '🏥', color: '#10B981', group: 'lifestyle' },
  { name: 'Gym/Fitness', icon: '💪', color: '#84CC16', group: 'lifestyle' },
  { name: 'Personal Care', icon: '💇', color: '#FB923C', group: 'lifestyle' },
  { name: 'Education', icon: '📚', color: '#0EA5E9', group: 'lifestyle' },

  // Subscriptions
  { name: 'Subscriptions', icon: '📺', color: '#7C3AED', group: 'subscriptions' },

  // Other
  { name: 'Gifts/Donations', icon: '🎁', color: '#F472B6', group: 'other' },
  { name: 'Travel/Vacation', icon: '✈️', color: '#38BDF8', group: 'other' },
  { name: 'Other', icon: '📌', color: '#6B7280', group: 'other' },
] as const;

/** Income frequency options */
export const INCOME_FREQUENCIES = ['monthly', 'biweekly', 'weekly'] as const;
export type IncomeFrequency = typeof INCOME_FREQUENCIES[number];

/** Goal priority levels */
export const GOAL_PRIORITIES = [1, 2, 3, 4, 5] as const;
export type GoalPriority = typeof GOAL_PRIORITIES[number];

/** AI personality options */
export const AI_PERSONALITIES = ['supportive', 'direct', 'analytical', 'balanced'] as const;
export type AIPersonality = typeof AI_PERSONALITIES[number];

/** Spending style categories (for onboarding) */
export const OVERSPENDING_CATEGORIES = [
  'Eating Out',
  'Shopping',
  'Entertainment',
  'Cab/Uber/Ola',
  'Swiggy/Zomato',
  'Chai/Coffee',
  'Subscriptions',
  'Impulse Purchases',
] as const;

/** Currency */
export const DEFAULT_CURRENCY = 'INR';
export const CURRENCY_SYMBOL = '₹';
