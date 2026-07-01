# ─────────────────────────────────────────────────────────────────────────────
# ARG must be declared BEFORE the first FROM to be usable in FROM instructions.
# Build for development (hot-reload):   docker build --build-arg ENV=development .
# Build for production (default):       docker build .
# ─────────────────────────────────────────────────────────────────────────────
ARG ENV=production

# ─────────────────────────────────────────────
# Base stage — shared setup for dev + production
# ─────────────────────────────────────────────
FROM python:3.11-slim AS base

WORKDIR /app

# System dependencies required by some Python packages (e.g. cryptography)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first — expensive pip layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# ─────────────────────────────────────────────
# Development stage — hot-reload, single worker
# ─────────────────────────────────────────────
FROM base AS development
ENV APP_ENV=development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ─────────────────────────────────────────────
# Production stage — no reload, multiple workers
# ─────────────────────────────────────────────
FROM base AS production
ENV APP_ENV=production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
