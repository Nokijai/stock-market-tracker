from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.scheduler.setup import start_scheduler, stop_scheduler
from app.routers import auth, portfolio, watchlist, market, news, alerts
import structlog

log = structlog.get_logger()

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
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
