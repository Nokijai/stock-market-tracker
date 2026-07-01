from sqlalchemy import Column, String, Float, DateTime, Text
from datetime import datetime, timezone
from app.database import Base

class FundamentalsCache(Base):
    __tablename__ = "fundamentals_cache"

    ticker = Column(String, primary_key=True, index=True)
    company_name = Column(String)
    pe_ratio = Column(Float)
    eps = Column(Float)
    dividend_yield = Column(Float)
    week_52_high = Column(Float)
    week_52_low = Column(Float)
    beta = Column(Float)
    market_cap = Column(Float)
    sector = Column(String)
    industry = Column(String)
    description = Column(Text)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
