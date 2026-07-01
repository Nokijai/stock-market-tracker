from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.holding import Holding
from app.models.news import NewsArticle
from app.schemas.news import NewsArticleOut
from app.utils.auth import get_current_user
from app.services.news_service import fetch_ticker_news

router = APIRouter(prefix="/api/news", tags=["news"])

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
    # Try live fetch first, store to DB
    live = fetch_ticker_news(t, limit=limit)
    if live:
        from datetime import datetime, timezone
        from app.models.news import NewsArticle
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
    # Return from DB
    articles = (db.query(NewsArticle)
                .filter(NewsArticle.ticker == t)
                .order_by(NewsArticle.published_at.desc())
                .limit(limit).all())
    return articles
