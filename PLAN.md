# 📈 Stock Market Tracker — Full Project Plan

> **Target User:** Beginner investor | **Developer:** Solo | **Stack:** FastAPI + React + openai SDK → yuanyuaicloud.cn (glm-5.2) | **Deploy:** VPS (178.128.223.228) via Docker + GitHub Actions

---

## Table of Contents

1. [Project Vision](#1-project-vision)
2. [Architecture](#2-architecture)
3. [Feature Tiers](#3-feature-tiers)
4. [Data APIs](#4-data-apis)
5. [Tech Stack](#5-tech-stack)
6. [Key Service Components](#6-key-service-components)
7. [Database Schema](#7-database-schema)
8. [Phased Roadmap](#8-phased-roadmap)
9. [Cost Estimate](#9-cost-estimate)
10. [Risk Register](#10-risk-register)
11. [Beginner UX Principles](#11-beginner-ux-principles)
12. [File Structure](#12-file-structure)

---

## 1. Project Vision

Build a **personal stock market tracker** that helps a beginner investor:

- Understand what they own and how it's performing
- Stay informed via plain-English AI news summaries for their holdings
- Receive actionable guidance — not Wall Street jargon

**AI Model:** `glm-5.2` via yuanyuaicloud.cn (OpenAI-compatible API).
- glm-5.2 is the right call: news summarisation + sentiment classification are structured extraction tasks, not deep reasoning. Fast, cost-effective.
- Only upgrade to a reasoning model for V3 AI Insight Engine if deeper portfolio analysis is needed.

**Out of scope:** Automated trading, real-time tick data, options/derivatives, institutional data.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                      │
│  Dashboard │ Portfolio │ Watchlist │ News Feed │ Alerts │ Advice │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST + WebSocket
┌────────────────────────────▼────────────────────────────────────┐
│                   BACKEND API (FastAPI / Python)                 │
│  Auth · Portfolio CRUD · News Fetch · Advice Engine · Alerts    │
└──────┬─────────────┬──────────────┬──────────────┬─────────────┘
       │             │              │              │
┌──────▼──────┐ ┌────▼────┐ ┌──────▼──────┐ ┌────▼────────────┐
│  Scheduler  │ │  Cache  │ │  Database   │ │  AI/NLP Layer   │
│ (APScheduler│ │ (Redis) │ │ (SQLite →   │ │ openai SDK →   │
│  or cron)   │ │         │ │  PostgreSQL) │ │ glm-5.2        │
└──────┬──────┘ └─────────┘ └─────────────┘ └─────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────────┐
│                   EXTERNAL DATA SOURCES                         │
│  yfinance · Finnhub · Alpha Vantage · Marketaux                 │
│  Financial Modeling Prep (fundamentals) · LiteLLM (NLP)        │
└─────────────────────────────────────────────────────────────────┘
```

### Ports on VPS
| Service | Port | Notes |
|---|---|---|
| Frontend (Next.js/Vite) | 4002 | nginx proxy → stock.worldofnoki.com |
| Backend API (FastAPI) | 4003 | nginx proxy → stock.worldofnoki.com/api |
| Redis | 6380 | Internal only (non-standard port to avoid clash) |

---

## 3. Feature Tiers

### 🟢 MVP — Build First (Weeks 1–8)

| # | Feature | Description |
|---|---|---|
| M1 | User auth | JWT register/login |
| M2 | Portfolio CRUD | Add/edit/delete holdings (ticker, shares, avg cost) |
| M3 | Watchlist | Track tickers without owning them |
| M4 | Live price display | Current price, day change %, market cap |
| M5 | Portfolio P&L | Total value, gain/loss per holding and overall |
| M6 | Basic news feed | Latest 5 headlines per ticker (Finnhub free) |
| M7 | Market status indicator | Open/closed indicator |
| M8 | Sector tagging | Auto-tag holdings by sector via yfinance |
| M9 | Dashboard | Pie chart allocation, total value card, top movers |
| M10 | Manual refresh | Button to pull fresh quotes on demand |

### 🟡 V2 — Intelligence Layer (Weeks 9–16)

| # | Feature | Description |
|---|---|---|
| V2-1 | **AI news summary** | Per-ticker 3-bullet plain-English digest via Sonnet 4.6 |
| V2-2 | **Sentiment badge** | Bullish / Neutral / Bearish per ticker from news analysis |
| V2-3 | Price alerts | Email/push when price crosses user-set threshold |
| V2-4 | Daily digest email | Morning briefing: portfolio + key news summary |
| V2-5 | Historical price chart | 1W / 1M / 3M / 1Y chart |
| V2-6 | Fundamentals panel | P/E, EPS, dividend yield, 52wk range, beta |
| V2-7 | Portfolio vs S&P 500 | Time-series benchmark comparison |
| V2-8 | Scheduled refresh | Auto-refresh prices every 15 min during market hours |
| V2-9 | News deduplication | Cross-provider article dedup via URL hash |
| V2-10 | CSV import | Bulk-import holdings from brokerage CSV export |

### 🔵 V3 — Power Features (Weeks 17–28)

| # | Feature | Description |
|---|---|---|
| V3-1 | **AI Insight Engine** | "What should I know about AAPL this week?" (Sonnet/Opus) |
| V3-2 | **"Explain this" tooltips** | Hover any metric for plain-English definition |
| V3-3 | Risk score | Concentration warning, beta, volatility score |
| V3-4 | Earnings calendar | Upcoming earnings dates for holdings |
| V3-5 | Dividend tracker | Expected dividends, yield on cost, payout calendar |
| V3-6 | Scenario calculator | "What if NVDA drops 20%?" portfolio impact |
| V3-7 | Smart alerts | Unusual volume, negative news burst, earnings proximity |
| V3-8 | Similar stock suggestions | "You own AAPL — you might watch MSFT?" |
| V3-9 | Mobile PWA | Installable Progressive Web App |
| V3-10 | PDF/CSV export | Portfolio report for tax season |

---

## 4. Data APIs

### Stock Prices

| Provider | Free Tier | Use Case | Notes |
|---|---|---|---|
| **yfinance** | Unlimited (unofficial) | MVP prototyping | Can break; use as primary for MVP |
| **Finnhub** | 60 req/min, WebSocket | Free near-real-time quotes | Best free tier for streaming |
| **Alpha Vantage** | 25 req/day | Fundamentals | Restrictive but good quality |
| **Polygon.io** | 15-min delayed | Production upgrade | $29/mo for real-time |
| **FMP** | 250 req/day | Deep fundamentals | Full financial statements |

**Recommended:**
- **MVP:** `yfinance` + **Finnhub** (free news + basic quotes)
- **V2:** Add **Alpha Vantage** for fundamentals
- **V3/Production:** **Polygon.io Starter ($29/mo)** for reliable real-time

### News + Sentiment

| Provider | Free Tier | Sentiment | Best For |
|---|---|---|---|
| **Finnhub** | 60 req/min | Basic score | MVP — company-specific, ticker-tagged |
| **Marketaux** | 100 req/day | ✅ Confidence-weighted | V2 — best free-tier sentiment |
| **Alpha Vantage News** | 25 req/day (bundled) | ✅ Score | Combined with AV fundamentals |

### AI / NLP

| Option | Cost | Notes |
|---|---|---|
| **openai SDK → yuanyuaicloud.cn/glm-5.2** | Existing setup | ✅ Use this — fast, structured extraction, great for summaries |
| **openai SDK → deep-reasoning model** | Existing setup | Reserve for V3 deep insights if needed |
| **sumy (extractive)** | Free | Fallback if LiteLLM unavailable; lower quality |

**Per-summary cost:** ~$0.001–0.003 at personal scale (~1000 summaries/mo ≈ $1–3/mo)

---

## 5. Tech Stack

### Full Stack

```
Frontend:  React 18 + Vite + TypeScript + Tailwind CSS + shadcn/ui
           Recharts (charts) · React Query (TanStack) · Zustand · Axios

Backend:   Python 3.11 · FastAPI · Uvicorn · SQLAlchemy 2.0
           Alembic (migrations) · Pydantic v2 · python-jose (JWT)
           httpx / aiohttp · APScheduler 3.x

AI/NLP:    openai Python SDK → pointed at yuanyuaicloud.cn/v1
           Model: glm-5.2 (via yuanyuaicloud.cn/v1)

Database:  SQLite (MVP) → PostgreSQL 16 (V2+)
Cache:     Redis 7

Alerts:    aiosmtplib / SendGrid free (email) · Ntfy.sh (push)

DevOps:    Docker + docker-compose · GitHub Actions → GHCR → SSH deploy
           nginx (existing, manual management) · port 4002/4003
```

### Why These Choices

| Choice | Reason |
|---|---|
| **FastAPI** | Async-native, auto OpenAPI docs, Pythonic, great for solo dev |
| **React + Vite** | Fastest dev startup, shadcn makes UI beautiful quickly |
| **SQLite → PostgreSQL** | Zero-config start; migrate when user data grows |
| **APScheduler** | In-process cron, no Redis broker needed for MVP |
| **Redis** | Rate-limit buffer, 15-min price cache, prevents API hammering |
| **LiteLLM (sonnet-4-6)** | Existing setup, no new API key needed |
| **Ntfy.sh** | Free push notifications, zero infra |

---

## 6. Key Service Components

### 6.1 Data Ingestion Scheduler

| Job | Frequency | Source | Notes |
|---|---|---|---|
| Price refresh | Every 15 min (market hours) | yfinance / Finnhub | Skip weekends + after-hours |
| News fetch | Every 30 min | Finnhub + Marketaux | Deduplicate by URL hash |
| Fundamentals sync | Weekly (Sunday 2am) | yfinance / FMP | Low-change data |
| Alert evaluation | Every 15 min | Internal DB | Compare price vs. thresholds |
| Daily digest | 8:00am weekdays | Internal | Compose + send email |
| AI summary generation | Every 6h | LiteLLM | Batch news → summaries |

### 6.2 NLP Summarisation Pipeline

```
[Raw Headlines + Snippets for ticker]
         ↓
[Deduplicate by URL hash + title similarity]
         ↓
[Concatenate top 5 articles into context]
         ↓
[yuanyuaicloud.cn/v1 → glm-5.2 prompt]
 "You are a financial assistant for a beginner investor.
  Summarise the following news about {ticker} in 3 bullet points.
  Use plain English. Highlight any risks or opportunities.
  End with: Sentiment: [Bullish/Neutral/Bearish]"
         ↓
[Parse response → extract summary + sentiment label]
         ↓
[Cache in DB with 6h TTL → serve via /api/news/{ticker}/summary]
```

**Prompt variants:**
- **Daily digest:** Morning briefing tone, portfolio-wide
- **On-demand:** Concise paragraph per ticker
- **Insight mode (V3):** Structured analysis with recommendation bullets

### 6.3 Alert Engine

**Alert Types:**

| Alert | Tier | Trigger |
|---|---|---|
| Price above threshold | MVP | `current_price > user_target` |
| Price below threshold | MVP | `current_price < user_stop` |
| Day change % spike | V2 | `abs(day_change_pct) > 5%` |
| Unusual volume | V2 | `volume > 2× 30-day avg` |
| Negative news burst | V2 | ≥3 negative articles in 1hr |
| Earnings proximity | V3 | Earnings within 3 days |
| Portfolio drawdown | V3 | Total loss exceeds threshold % |

### 6.4 Portfolio Analytics

```python
# Per-holding
unrealized_gain = (current_price - avg_cost) * shares
unrealized_gain_pct = (current_price / avg_cost - 1) * 100
weight = current_value / total_portfolio_value * 100

# Portfolio-level
total_return_pct = (total_market_value / total_cost_basis - 1) * 100

# V2: Benchmark
alpha = total_return_pct - fetch_spy_return(portfolio_start_date)
```

### 6.5 REST API Map

```
/api/auth/         POST /register, /login, /refresh-token
/api/portfolio/    GET / · POST / · PUT /{id} · DELETE /{id} · GET /summary
/api/watchlist/    GET / · POST / · DELETE /{ticker}
/api/market/       GET /quote/{ticker} · /history/{ticker} · /fundamentals/{ticker}
/api/news/         GET /{ticker} · /{ticker}/summary · /feed
/api/alerts/       GET / · POST / · DELETE /{id}
/api/insights/     GET /{ticker} · /portfolio          [V3]
```

---

## 7. Database Schema

```sql
CREATE TABLE users (
    id           INTEGER PRIMARY KEY,
    email        TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE holdings (
    id        INTEGER PRIMARY KEY,
    user_id   INTEGER REFERENCES users(id),
    ticker    TEXT NOT NULL,
    shares    REAL NOT NULL,
    avg_cost  REAL NOT NULL,
    currency  TEXT DEFAULT 'USD',
    added_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, ticker)
);

CREATE TABLE watchlist (
    id       INTEGER PRIMARY KEY,
    user_id  INTEGER REFERENCES users(id),
    ticker   TEXT NOT NULL,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, ticker)
);

CREATE TABLE price_cache (
    ticker          TEXT PRIMARY KEY,
    price           REAL NOT NULL,
    day_change      REAL,
    day_change_pct  REAL,
    volume          INTEGER,
    market_cap      REAL,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE news_articles (
    id           INTEGER PRIMARY KEY,
    ticker       TEXT NOT NULL,
    headline     TEXT NOT NULL,
    url          TEXT UNIQUE,
    source       TEXT,
    sentiment    REAL,          -- -1.0 to +1.0
    published_at DATETIME,
    fetched_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE news_summaries (
    id              INTEGER PRIMARY KEY,
    ticker          TEXT NOT NULL,
    summary_text    TEXT NOT NULL,    -- AI 3-bullet digest
    sentiment_label TEXT,             -- bullish / neutral / bearish
    generated_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts (
    id           INTEGER PRIMARY KEY,
    user_id      INTEGER REFERENCES users(id),
    ticker       TEXT NOT NULL,
    alert_type   TEXT NOT NULL,       -- price_above / price_below / pct_change
    threshold    REAL NOT NULL,
    is_active    BOOLEAN DEFAULT TRUE,
    triggered_at DATETIME,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fundamentals_cache (
    ticker        TEXT PRIMARY KEY,
    pe_ratio      REAL,
    eps           REAL,
    dividend_yield REAL,
    week_52_high  REAL,
    week_52_low   REAL,
    beta          REAL,
    market_cap    REAL,
    sector        TEXT,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 8. Phased Roadmap

### Phase 0 — Foundation (Week 1–2)
**Goal:** Working skeleton — auth + one ticker showing a price

| Task | Est |
|---|---|
| Repo + monorepo structure (`/backend`, `/frontend`) | 2h |
| FastAPI scaffold + Uvicorn + SQLite + SQLAlchemy | 3h |
| Alembic migrations | 2h |
| JWT auth endpoints (register/login/me) | 4h |
| React + Vite + Tailwind + shadcn/ui setup | 3h |
| Login/register UI + Zustand auth store | 4h |
| `GET /api/market/quote/{ticker}` via yfinance | 2h |
| Show one live quote in frontend | 2h |
| docker-compose for local dev | 2h |

### Phase 1 — MVP Core (Week 3–6)
**Goal:** Usable portfolio tracker (M1–M10)

| Task | Est |
|---|---|
| Holdings CRUD endpoints + DB | 4h |
| Watchlist CRUD | 2h |
| Portfolio P&L calculation service | 4h |
| Portfolio table UI (gain/loss colours) | 4h |
| Price cache + Redis layer | 3h |
| APScheduler: 15-min price refresh | 3h |
| Finnhub news fetch + store in DB | 3h |
| Basic news feed UI per ticker | 3h |
| Dashboard: value card + allocation pie | 5h |
| Market open/closed indicator | 1h |

### Phase 2 — News Intelligence (Week 7–10)
**Goal:** AI summaries + sentiment (V2-1 to V2-8)

| Task | Est |
|---|---|
| LiteLLM client setup (sonnet-4-6) | 2h |
| News deduplication (URL hash) | 2h |
| Summariser service: headlines → 3-bullet digest | 4h |
| Sentiment label extraction from AI response | 2h |
| Scheduled summary generation (every 6h) | 2h |
| SummaryCard UI + sentiment badge | 3h |
| Marketaux integration (second news source) | 3h |
| Alpha Vantage fundamentals panel | 4h |
| Historical chart (Recharts, 1W/1M/3M/1Y) | 5h |
| Portfolio vs S&P 500 chart | 4h |

### Phase 3 — Alerts & Notifications (Week 11–13)
**Goal:** Users get alerted when something important happens

| Task | Est |
|---|---|
| Alert CRUD endpoints | 3h |
| Alert evaluation job (APScheduler, 15-min) | 4h |
| Email delivery via SendGrid / aiosmtplib | 3h |
| Alerts management UI | 3h |
| Daily digest email (Jinja2 template) | 3h |
| Ntfy.sh push notifications | 2h |
| CSV holdings import | 3h |

### Phase 4 — Insights & Polish (Week 14–20)
**Goal:** V3 features — AI insights, risk, earnings

| Task | Est |
|---|---|
| AI Insight Engine endpoint + prompt | 5h |
| Portfolio-level AI advice | 5h |
| "Explain this" metric tooltips | 3h |
| Scenario calculator | 3h |
| Risk score (concentration + beta) | 4h |
| Earnings calendar (Finnhub) | 3h |
| Dividend tracker | 4h |
| PWA (manifest + service worker) | 3h |
| PDF/CSV export | 3h |
| Migrate SQLite → PostgreSQL | 2h |

### Phase 5 — Production Hardening (Week 21–24)
**Goal:** Live, monitored, auto-deployed on VPS

| Task | Est |
|---|---|
| GitHub Actions CI/CD → GHCR → SSH deploy | 4h |
| nginx config (port 4002/4003) | 2h |
| Rate limiting (slowapi) | 2h |
| Sentry error monitoring (free tier) | 2h |
| Structured logging (structlog) | 2h |
| Uptime monitoring (UptimeRobot) | 1h |
| Load test key flows (locust) | 2h |

---

## 9. Cost Estimate

| Service | MVP | V2 | V3 |
|---|---|---|---|
| yfinance | Free | Free | Free |
| Finnhub | Free | Free | Free |
| Marketaux | — | $9/mo | $9/mo |
| LiteLLM | ~$1–2/mo | ~$2–5/mo | ~$5–10/mo |
| SendGrid | Free (100/day) | Free | Free |
| Polygon.io | — | — | $29/mo |
| VPS (existing) | Shared | Shared | Shared |
| **Total** | **~$1–3/mo** | **~$12–15/mo** | **~$45–55/mo** |

---

## 10. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| yfinance breaks | High | Dual-source: Finnhub fallback; alert on fetch failure |
| LiteLLM cost spike | Medium | Cache summaries 6h TTL; daily token budget cap |
| Free API rate limits | Medium | Redis cache; exponential backoff; queue-based fetching |
| News hallucination | Medium | Cite sources in UI; extractive fallback (sumy) |
| Port conflict on VPS | Medium | Use non-standard ports (4002/4003); check before deploy |
| DB corruption (SQLite) | Medium | Daily backup; migrate to PostgreSQL at V2 |
| API keys in env | High | `.env` never committed; Docker secrets / env_file |

---

## 11. Beginner UX Principles

1. **Plain English first** — every metric has a one-sentence tooltip (P/E, beta, EPS, etc.)
2. **Traffic-light colours** — green = good, red = bad, never make users decode arrows
3. **"So what?" endings** — every insight ends with a dollar/action implication: *"AAPL is up 3% — your position gained HK$370"*
4. **No danger zones** — no margin, leverage, or short-selling exposed in UI
5. **Progress over perfection** — show time-in-market alongside gain/loss to reinforce long-term thinking
6. **Transparent freshness** — always show "Last updated: 14 min ago"
7. **Never show unexplained data** — if no tooltip exists for a metric, hide it until V3

---

## 12. File Structure

```
stock-market-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app factory
│   │   ├── config.py                # Settings (pydantic-settings)
│   │   ├── database.py              # SQLAlchemy engine + session
│   │   ├── models/                  # ORM models
│   │   ├── schemas/                 # Pydantic request/response models
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── portfolio.py
│   │   │   ├── watchlist.py
│   │   │   ├── market.py
│   │   │   ├── news.py
│   │   │   └── alerts.py
│   │   ├── services/
│   │   │   ├── price_service.py
│   │   │   ├── news_service.py
│   │   │   ├── summariser.py        # LiteLLM → sonnet-4.6
│   │   │   ├── analytics.py
│   │   │   └── alert_engine.py
│   │   ├── scheduler/
│   │   │   ├── scheduler_config.py
│   │   │   ├── price_ingester.py
│   │   │   ├── news_ingester.py
│   │   │   └── digest_sender.py
│   │   └── utils/
│   │       ├── cache.py             # Redis helpers
│   │       └── email.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Portfolio.tsx
│   │   │   ├── Watchlist.tsx
│   │   │   ├── StockDetail.tsx
│   │   │   ├── Alerts.tsx
│   │   │   └── Settings.tsx
│   │   ├── components/
│   │   │   ├── PortfolioPieChart.tsx
│   │   │   ├── PriceChart.tsx
│   │   │   ├── NewsCard.tsx
│   │   │   ├── SummaryCard.tsx
│   │   │   ├── HoldingRow.tsx
│   │   │   └── MetricTooltip.tsx
│   │   ├── hooks/
│   │   │   ├── usePortfolio.ts
│   │   │   ├── useQuote.ts
│   │   │   └── useNews.ts
│   │   └── store/
│   │       └── authStore.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
├── .github/workflows/
│   └── deploy.yml
├── PLAN.md                          # ← this file
└── README.md
```

---

## Quick-Start Checklist

### Day 1 Setup
- [ ] Clone repo: `git clone https://github.com/Nokijai/stock-market-tracker`
- [ ] `cd backend && python -m venv .venv && source .venv/bin/activate`
- [ ] `pip install fastapi uvicorn sqlalchemy alembic pydantic-settings python-jose passlib yfinance httpx apscheduler openai redis`
- [ ] `cd ../frontend && npm create vite@latest . -- --template react-ts`
- [ ] `npm install tailwindcss shadcn-ui recharts @tanstack/react-query zustand axios`
- [ ] Copy `.env.example` → `.env`, fill in API keys
- [ ] `docker-compose up -d` (Redis)
- [ ] `uvicorn app.main:app --reload` → visit `http://localhost:8000/docs`

### API Keys to Get (All Free Tier)
- [ ] **Finnhub:** https://finnhub.io — free, 60 req/min
- [ ] **Alpha Vantage:** https://alphavantage.co — free, 25 req/day
- [ ] **Marketaux:** https://marketaux.com — free, 100 req/day
- [ ] **SendGrid:** https://sendgrid.com — free, 100 emails/day
- [ ] **yuanyuaicloud.cn:** Already configured — uses glm-5.2 via yuanyuaicloud.cn/v1
|- [ ] **yuanyuaicloud.cn:** OpenAI-compatible API, uses glm-5.2 — set `LITELLM_BASE_URL` in `.env`|
|### LLM Config (`.env`)
|```
|LITELLM_API_KEY=<your-api-key>
|LITELLM_BASE_URL=https://yuanyuaicloud.cn/v1
|LITELLM_MODEL=glm-5.2
|```
