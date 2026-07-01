from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HoldingCreate(BaseModel):
    ticker: str
    shares: float
    avg_cost: float
    currency: str = "USD"

class HoldingUpdate(BaseModel):
    shares: Optional[float] = None
    avg_cost: Optional[float] = None

class HoldingOut(BaseModel):
    id: int
    ticker: str
    shares: float
    avg_cost: float
    currency: str
    added_at: datetime
    # Enriched fields (added at runtime)
    current_price: Optional[float] = None
    day_change_pct: Optional[float] = None
    current_value: Optional[float] = None
    unrealized_gain: Optional[float] = None
    unrealized_gain_pct: Optional[float] = None
    weight: Optional[float] = None
    company_name: Optional[str] = None
    sector: Optional[str] = None
    model_config = {"from_attributes": True}

class PortfolioSummary(BaseModel):
    total_cost_basis: float
    total_market_value: float
    total_unrealized_pnl: float
    total_return_pct: float
    holdings_count: int
    last_updated: Optional[datetime] = None

class WatchlistItemCreate(BaseModel):
    ticker: str

class WatchlistItemOut(BaseModel):
    id: int
    ticker: str
    added_at: datetime
    current_price: Optional[float] = None
    day_change_pct: Optional[float] = None
    company_name: Optional[str] = None
    model_config = {"from_attributes": True}
