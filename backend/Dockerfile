# ─────────────────────────────────────────────────────────────────────────────
# Multi-stage build — compiler is dropped in the final image.
# Result: ~200MB instead of 1.2GB.
#
# Build for development:  docker build --target development .
# Build for production:   docker build --target production .  (default)
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: builder — has gcc to compile native extensions ──────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: development — hot-reload, mounts source as volume ───────────────
FROM python:3.11-slim AS development

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

ENV APP_ENV=development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ── Stage 3: production — lean final image, no compiler ──────────────────────
FROM python:3.11-slim AS production

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

ENV APP_ENV=production
# IMPORTANT: Run with 1 worker only.
# APScheduler (background scheduler) lives in the same process as uvicorn.
# With multiple workers, each worker spawns its own scheduler instance,
# causing duplicate cron jobs, double API calls, and double DB writes.
# To scale throughput, run multiple containers behind a load balancer instead.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
