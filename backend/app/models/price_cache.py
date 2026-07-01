from sqlalchemy import Column, String, Float, Integer, DateTime
from datetime import datetime, timezone
from app.database import Base

class PriceCache(Base):
    __tablename__ = "price_cache"

    ticker = Column(String, primary_key=True, index=True)
    price = Column(Float)
    day_change = Column(Float)
    day_change_pct = Column(Float)
    volume = Column(Integer)
    market_cap = Column(Float)
    company_name = Column(String)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
