# 📈 Stock Market Tracker

> Personal stock market tracker with AI-powered news summaries, sentiment analysis, and actionable insights — built for beginner investors.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Track your stock portfolio, stay informed with plain-English AI news digests for your holdings, and receive smart alerts — without needing Wall Street knowledge.

**AI Model:** `claude-sonnet-4-6` via LiteLLM for news summarisation and sentiment analysis.

## Features

- 📊 Portfolio tracker with real-time P&L
- 🔍 Watchlist for stocks you're monitoring
- 📰 AI-summarised news per holding (Bullish / Neutral / Bearish)
- 🔔 Price alerts via email and push notifications
- 📈 Historical charts with S&P 500 benchmark comparison
- 🧠 AI Insight Engine — "What should I know about AAPL this week?" *(V3)*
- 💡 Plain-English metric tooltips for beginners *(V3)*

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + TypeScript + Tailwind + shadcn/ui |
| Backend | FastAPI + SQLAlchemy + APScheduler |
| AI/NLP | LiteLLM → claude-sonnet-4-6 |
| Database | SQLite (MVP) → PostgreSQL (V2) |
| Cache | Redis |
| Alerts | SendGrid + Ntfy.sh |
| Deploy | Docker + GitHub Actions → VPS |

## Project Structure

```
stock-market-tracker/
├── backend/     FastAPI API + scheduler + AI services
├── frontend/    React + Vite dashboard
├── PLAN.md      Full project plan and roadmap
└── README.md
```

## Roadmap

See [`PLAN.md`](./PLAN.md) for the full architecture, feature tiers, API choices, database schema, and phased build roadmap.

| Phase | Scope | Status |
|---|---|---|
| 0 — Foundation | Auth + live quote | ✅ Done |
| 1 — MVP | Full portfolio tracker + news feed | ✅ Done |
| 2 — Intelligence | AI summaries + sentiment badges | 🔨 In Progress |
| 3 — Alerts | Price alerts + daily digest | 🔲 Planned |
| 4 — Insights | AI engine + risk score | 🔲 Planned |
| 5 — Production | Monitoring + performance | 🔲 Planned |

## Getting Started

```bash
# Clone
git clone https://github.com/Nokijai/stock-market-tracker
cd stock-market-tracker

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in API keys
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## License

MIT
