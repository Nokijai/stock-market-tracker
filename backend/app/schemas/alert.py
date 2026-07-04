from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import re

_TICKER_RE = re.compile(r'^[A-Z0-9.\-\^]{1,10}$')


class AlertCreate(BaseModel):
    ticker: str
    alert_type: str  # price_above, price_below, pct_change
    threshold: float

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        t = v.upper().strip()
        if not _TICKER_RE.match(t):
            raise ValueError(
                "Invalid ticker symbol. Must be 1-10 characters: letters, digits, '.', '-', '^'."
            )
        return t

    @field_validator("alert_type")
    @classmethod
    def validate_alert_type(cls, v: str) -> str:
        valid = {"price_above", "price_below", "pct_change"}
        if v not in valid:
            raise ValueError(f"alert_type must be one of: {valid}")
        return v


class AlertOut(BaseModel):
    id: int
    ticker: str
    alert_type: str
    threshold: float
    is_active: bool
    triggered_at: Optional[datetime] = None
    created_at: datetime
    model_config = {"from_attributes": True}
