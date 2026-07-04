from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from contextlib import asynccontextmanager
from app.database import init_db
from app.scheduler.setup import start_scheduler, stop_scheduler
from app.routers import auth, portfolio, watchlist, market, news, alerts
from app.config import get_settings
import structlog
import os

log = structlog.get_logger()
settings = get_settings()

# Determine allowed CORS origins from env or safe default
_CORS_ORIGINS_RAW = os.environ.get(
    "CORS_ORIGINS",
    "https://stock.worldofnoki.com"
)
CORS_ORIGINS = [o.strip() for o in _CORS_ORIGINS_RAW.split(",") if o.strip()]


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add basic security headers to every response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up stock-tracker API")
    init_db()
    start_scheduler()
    yield
    stop_scheduler()
    log.info("Shutdown complete")

app = FastAPI(
    title="Stock Market Tracker API",
    version="1.0.0",
    description="Personal stock tracker with AI news summaries",
    lifespan=lifespan,
    # Hide internal detail from 500 error responses
    openapi_url="/openapi.json" if settings.ENV != "production" else None,
)

# --- Security headers on every response ---
app.add_middleware(SecurityHeadersMiddleware)

# --- CORS: explicit origins only; credentials require explicit origin list ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(watchlist.router)
app.include_router(market.router)
app.include_router(news.router)
app.include_router(alerts.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "stock-tracker"}
