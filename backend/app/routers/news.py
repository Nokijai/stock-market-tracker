from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.holding import Holding
from app.models.news import NewsArticle
from app.schemas.news import NewsArticleOut
from app.utils.auth import get_current_user
from app.services.news_service import fetch_ticker_news
from app.services.ai_service import summarise_news

router = APIRouter(prefix="/api/news", tags=["news"])


class AISummary(BaseModel):
    ticker: str
    bullets: List[str]
    sentiment: str   # "Bullish" | "Neutral" | "Bearish"
    reason: str
    cached: bool = False


@router.get("/feed", response_model=List[NewsArticleOut])
def news_feed(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = Query(20, le=50)):
    holdings = db.query(Holding.ticker).filter(Holding.user_id == current_user.id).distinct().all()
    tickers = [h.ticker for h in holdings]
    if not tickers:
        return []
    articles = (db.query(NewsArticle)
                .filter(NewsArticle.ticker.in_(tickers))
                .order_by(NewsArticle.published_at.desc())
                .limit(limit).all())
    return articles


@router.get("/{ticker}", response_model=List[NewsArticleOut])
def ticker_news(ticker: str, db: Session = Depends(get_db), limit: int = Query(10, le=30)):
    t = ticker.upper()
    live = fetch_ticker_news(t, limit=limit)
    if live:
        from datetime import datetime, timezone
        for a in live:
            existing = db.query(NewsArticle).filter(NewsArticle.url == a.get("url")).first()
            if existing or not a.get("url"):
                continue
            pub_at = None
            if a.get("published_at"):
                try:
                    pub_at = datetime.fromisoformat(a["published_at"].replace("Z", "+00:00"))
                except Exception:
                    pass
            db.add(NewsArticle(
                ticker=t, headline=a["headline"], url=a.get("url"),
                source=a.get("source"), sentiment=a.get("sentiment"),
                image=a.get("image"), published_at=pub_at,
            ))
        try:
            db.commit()
        except Exception:
            db.rollback()
    articles = (db.query(NewsArticle)
                .filter(NewsArticle.ticker == t)
                .order_by(NewsArticle.published_at.desc())
                .limit(limit).all())
    return articles


@router.get("/{ticker}/summary", response_model=AISummary)
def ticker_ai_summary(ticker: str, db: Session = Depends(get_db)):
    """V2: AI-generated 3-bullet summary + sentiment for a ticker's recent news."""
    t = ticker.upper()
    # Use cached articles or fetch fresh
    articles = fetch_ticker_news(t, limit=10)
    if not articles:
        # Fall back to DB
        rows = (db.query(NewsArticle)
                .filter(NewsArticle.ticker == t)
                .order_by(NewsArticle.published_at.desc())
                .limit(10).all())
        articles = [{"headline": r.headline} for r in rows]

    result = summarise_news(t, articles)
    if not result:
        raise HTTPException(
            status_code=503,
            detail="AI summary unavailable — check LITELLM_BASE_URL config",
        )
    return AISummary(ticker=t, **result)

