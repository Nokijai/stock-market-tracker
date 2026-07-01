from fastapi import APIRouter, Query
from app.schemas.market import QuoteOut, HistoryPoint, FundamentalsOut, MarketStatusOut
from app.services.price_service import fetch_quote, fetch_history, fetch_fundamentals
from app.utils.market_hours import get_market_status
from typing import List

router = APIRouter(prefix="/api/market", tags=["market"])

@router.get("/status", response_model=MarketStatusOut)
def market_status():
    return get_market_status()

@router.get("/quote/{ticker}", response_model=QuoteOut)
def quote(ticker: str):
    data = fetch_quote(ticker.upper())
    if not data:
        return {"ticker": ticker.upper()}
    return data

@router.get("/history/{ticker}", response_model=List[HistoryPoint])
def history(ticker: str, period: str = Query("1mo", regex="^(1wk|1mo|3mo|1y|2y)$")):
    return fetch_history(ticker.upper(), period=period)

@router.get("/fundamentals/{ticker}", response_model=FundamentalsOut)
def fundamentals(ticker: str):
    data = fetch_fundamentals(ticker.upper())
    if not data:
        return {"ticker": ticker.upper()}
    return data
