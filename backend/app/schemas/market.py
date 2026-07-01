from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuoteOut(BaseModel):
    ticker: str
    price: Optional[float] = None
    day_change: Optional[float] = None
    day_change_pct: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    company_name: Optional[str] = None
    updated_at: Optional[datetime] = None

class HistoryPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class FundamentalsOut(BaseModel):
    ticker: str
    company_name: Optional[str] = None
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    dividend_yield: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    beta: Optional[float] = None
    market_cap: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

class MarketStatusOut(BaseModel):
    is_open: bool
    timezone: str = "US/Eastern"
    session: str  # "pre", "regular", "after", "closed"
