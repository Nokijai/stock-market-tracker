from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import re

_TICKER_RE = re.compile(r'^[A-Z0-9.\-\^]{1,10}$')


def _validate_ticker_field(v: str) -> str:
    t = v.upper().strip()
    if not _TICKER_RE.match(t):
        raise ValueError(
            "Invalid ticker symbol. Must be 1-10 characters: letters, digits, '.', '-', '^'."
        )
    return t


class HoldingCreate(BaseModel):
    ticker: str
    shares: float
    avg_cost: float
    currency: str = "USD"

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        return _validate_ticker_field(v)

    @field_validator("shares")
    @classmethod
    def validate_shares(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("shares must be positive")
        return v

    @field_validator("avg_cost")
    @classmethod
    def validate_avg_cost(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("avg_cost must be positive")
        return v


class HoldingUpdate(BaseModel):
    shares: Optional[float] = None
    avg_cost: Optional[float] = None

    @field_validator("shares")
    @classmethod
    def validate_shares(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("shares must be positive")
        return v

    @field_validator("avg_cost")
    @classmethod
    def validate_avg_cost(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("avg_cost must be positive")
        return v


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

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        return _validate_ticker_field(v)


class WatchlistItemOut(BaseModel):
    id: int
    ticker: str
    added_at: datetime
    current_price: Optional[float] = None
    day_change_pct: Optional[float] = None
    company_name: Optional[str] = None
    model_config = {"from_attributes": True}
