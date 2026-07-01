from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsArticleOut(BaseModel):
    id: int
    ticker: str
    headline: str
    url: Optional[str] = None
    source: Optional[str] = None
    sentiment: Optional[float] = None
    image: Optional[str] = None
    published_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
