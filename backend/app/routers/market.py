import re
from fastapi import APIRouter, Query, HTTPException
from app.schemas.market import QuoteOut, HistoryPoint, FundamentalsOut, MarketStatusOut
from app.services.price_service import fetch_quote, fetch_history, fetch_fundamentals, fetch_spy_history
from app.utils.market_hours import get_market_status
from typing import List

router = APIRouter(prefix="/api/market", tags=["market"])

_TICKER_RE = re.compile(r'^[A-Z0-9.\-\^]{1,10}$')


def _validate_ticker(ticker: str) -> str:
    """Normalise and validate a ticker symbol. Raises 422 on invalid input."""
    t = ticker.upper().strip()
    if not _TICKER_RE.match(t):
        raise HTTPException(
            status_code=422,
            detail="Invalid ticker symbol. Must be 1-10 characters: letters, digits, '.', '-', '^'.",
        )
    return t


@router.get("/status", response_model=MarketStatusOut)
def market_status():
    return get_market_status()


@router.get("/quote/{ticker}", response_model=QuoteOut)
def quote(ticker: str):
    t = _validate_ticker(ticker)
    data = fetch_quote(t)
    if not data:
        return {"ticker": t}
    return data


@router.get("/history/{ticker}", response_model=List[HistoryPoint])
def history(ticker: str, period: str = Query("1mo", pattern="^(1wk|1mo|3mo|1y|2y)$")):
    t = _validate_ticker(ticker)
    return fetch_history(t, period=period)


@router.get("/fundamentals/{ticker}", response_model=FundamentalsOut)
def fundamentals(ticker: str):
    t = _validate_ticker(ticker)
    data = fetch_fundamentals(t)
    if not data:
        return {"ticker": t}
    return data


@router.get("/benchmark/{ticker}")
def benchmark(ticker: str, period: str = Query("1mo", pattern="^(1wk|1mo|3mo|1y|5y)$")):
    t = _validate_ticker(ticker)
    ticker_data = fetch_history(t, period=period)
    spy_data = fetch_spy_history(period=period)
    return {
        "ticker": t,
        "period": period,
        "benchmark": "SPY",
        "ticker_data": ticker_data,
        "spy_data": spy_data,
    }
