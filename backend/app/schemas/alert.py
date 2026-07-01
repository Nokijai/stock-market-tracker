from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertCreate(BaseModel):
    ticker: str
    alert_type: str  # price_above, price_below, pct_change
    threshold: float

class AlertOut(BaseModel):
    id: int
    ticker: str
    alert_type: str
    threshold: float
    is_active: bool
    triggered_at: Optional[datetime] = None
    created_at: datetime
    model_config = {"from_attributes": True}
