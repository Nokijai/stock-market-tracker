from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime, timezone
from app.database import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False, index=True)
    headline = Column(Text, nullable=False)
    url = Column(String, unique=True)
    source = Column(String)
    sentiment = Column(Float)  # -1.0 to +1.0
    image = Column(String)
    published_at = Column(DateTime)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
