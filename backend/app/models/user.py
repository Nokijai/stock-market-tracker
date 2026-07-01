from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    holdings = relationship("Holding", back_populates="user", cascade="all, delete")
    watchlist = relationship("WatchlistItem", back_populates="user", cascade="all, delete")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete")
