# 💰 Finance Buddy

**AI-Native Personal Finance Operating System**

Finance Buddy is an intelligent financial assistant that helps you understand, manage, and improve your relationship with money. It combines deterministic financial computation with conversational AI to deliver trustworthy insights and actionable advice.

## ✨ What Makes This Different

This is NOT a simple expense tracker. Finance Buddy:

- **Understands your financial behavior** — spending patterns, salary cycles, recurring habits
- **Generates adaptive budgets** — AI-powered recommendations based on your actual lifestyle
- **Coaches you psychologically** — understands emotional spending and helps you build better habits
- **Answers your real questions** — "Can I afford this?", "Why am I overspending?", "How do I reach my goals faster?"

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│                 Clients                      │
│    Web App (Expo Web)  •  Android (Expo)    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              FastAPI Server                  │
├─────────────────────────────────────────────┤
│  Auth  │ Transactions │ Budget │ Goals │ AI │
├─────────────────────────────────────────────┤
│         Financial Rules Engine              │
│    (Deterministic • Testable • Auditable)   │
├─────────────────────────────────────────────┤
│      PostgreSQL      │      Redis           │
└─────────────────────────────────────────────┘
```

### Core Principle: Trust

> **LLMs never compute balances or make financial assertions.**
> Deterministic services compute financial truth. AI interprets, explains, and coaches.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Expo (React Native) + TypeScript — Android & Web |
| **Backend** | FastAPI + Python 3.13 |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |
| **AI** | Google Gemini API (free tier) |
| **Auth** | Custom JWT + Argon2 |
| **Monorepo** | Turborepo |

## 📁 Project Structure

```
finance-buddy/
├── apps/mobile/          # Expo app (Android + Web)
├── backend/              # FastAPI server
├── packages/shared/      # Shared types & constants
├── docker-compose.yml    # PostgreSQL + Redis
├── turbo.json           # Monorepo config
└── package.json         # Workspace root
```

## 🚀 Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- Android Studio (for Android dev) or web browser

### Setup

```bash
# 1. Clone & install
git clone <repo-url> && cd finance-buddy
npm install

# 2. Start databases
docker compose up -d db redis

# 3. Backend
cd backend
pip install uv
uv venv && .venv\Scripts\activate   # Windows
uv pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload

# 4. Frontend (new terminal)
npm run dev:web     # Web browser
# OR
npm run dev:android # Android device/emulator
```

### Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/financebuddy
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-secret-key-change-this
GEMINI_API_KEY=your-gemini-api-key
```

## 🇮🇳 India-First

- Currency: INR (₹)
- Indian numbering system (₹1,00,000)
- India-specific categories (Auto/Riksha, Kirana, EMI, Chai/Coffee)
- Salary cycle awareness (1st/last of month)

## 📜 License

Private — All rights reserved.
