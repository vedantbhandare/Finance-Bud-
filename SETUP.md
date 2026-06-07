# Finance Buddy — Backend Setup

## Prerequisites
- Python 3.12+ (with `uv` recommended)
- Docker + Docker Compose (for PostgreSQL + Redis)

## Quick Start

### 1. Start databases
```bash
docker compose up -d db redis
```

### 2. Install Python dependencies
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -e ".[dev]"
```

### 3. Create database tables
```bash
alembic upgrade head
```

### 4. Start API server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

---

# Frontend Setup

### 1. Install dependencies
```bash
cd apps/mobile
npm install
```

### 2. Start Expo (web)
```bash
npm run web
```

Opens at http://localhost:8081

### 3. Start Expo (Android)
```bash
npm run android
```

---

# Environment Variables

Copy `.env.example` to `.env` in the `backend/` directory:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/finance_buddy
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-here
GEMINI_API_KEY=your-gemini-api-key  # Optional: AI features fallback without it
DEBUG=true
```
