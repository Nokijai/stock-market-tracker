from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.holding import Holding
from app.models.watchlist import WatchlistItem
from app.models.price_cache import PriceCache
from app.models.news import NewsArticle
from app.services.price_service import fetch_quote
from app.services.news_service import fetch_ticker_news
from app.utils.market_hours import is_market_open
from datetime import datetime, timezone
import structlog

log = structlog.get_logger()

def refresh_prices():
    """Refresh prices for all tracked tickers. Runs every 15 min."""
    if not is_market_open():
        log.info("Market closed, skipping price refresh")
        return
    db: Session = SessionLocal()
    try:
        tickers = set()
        for h in db.query(Holding.ticker).distinct().all():
            tickers.add(h.ticker)
        for w in db.query(WatchlistItem.ticker).distinct().all():
            tickers.add(w.ticker)
        log.info("Refreshing prices", count=len(tickers))
        for ticker in tickers:
            quote = fetch_quote(ticker)
            if quote:
                cached = db.query(PriceCache).filter(PriceCache.ticker == ticker).first()
                if cached:
                    cached.price = quote["price"]
                    cached.day_change = quote.get("day_change")
                    cached.day_change_pct = quote.get("day_change_pct")
                    cached.volume = quote.get("volume")
                    cached.market_cap = quote.get("market_cap")
                    cached.company_name = quote.get("company_name")
                    cached.updated_at = datetime.now(timezone.utc)
                else:
                    db.add(PriceCache(
                        ticker=ticker,
                        price=quote["price"],
                        day_change=quote.get("day_change"),
                        day_change_pct=quote.get("day_change_pct"),
                        volume=quote.get("volume"),
                        market_cap=quote.get("market_cap"),
                        company_name=quote.get("company_name"),
                        updated_at=datetime.now(timezone.utc),
                    ))
        db.commit()
        log.info("Price refresh done", count=len(tickers))
    except Exception as e:
        log.error("Price refresh failed", error=str(e))
        db.rollback()
    finally:
        db.close()

def fetch_all_news():
    """Fetch news for all tracked tickers. Runs every 30 min."""
    db: Session = SessionLocal()
    try:
        tickers = set()
        for h in db.query(Holding.ticker).distinct().all():
            tickers.add(h.ticker)
        log.info("Fetching news", count=len(tickers))
        for ticker in tickers:
            articles = fetch_ticker_news(ticker, limit=10)
            for a in articles:
                existing = db.query(NewsArticle).filter(NewsArticle.url == a["url"]).first()
                if existing or not a.get("url"):
                    continue
                pub_at = None
                if a.get("published_at"):
                    try:
                        from datetime import datetime
                        pub_at = datetime.fromisoformat(a["published_at"].replace("Z", "+00:00"))
                    except Exception:
                        pass
                db.add(NewsArticle(
                    ticker=ticker,
                    headline=a["headline"],
                    url=a.get("url"),
                    source=a.get("source"),
                    sentiment=a.get("sentiment"),
                    image=a.get("image"),
                    published_at=pub_at,
                ))
        db.commit()
    except Exception as e:
        log.error("News fetch failed", error=str(e))
        db.rollback()
    finally:
        db.close()

def check_alerts():
    """Evaluate price alerts for all users. Runs every 15 min."""
    if not is_market_open():
        return
    db: Session = SessionLocal()
    try:
        from app.models.alert import Alert
        alerts = db.query(Alert).filter(Alert.is_active == True).all()  # noqa
        for alert in alerts:
            quote = fetch_quote(alert.ticker)
            if not quote or not quote.get("price"):
                continue
            price = quote["price"]
            triggered = False
            if alert.alert_type == "price_above" and price >= alert.threshold:
                triggered = True
            elif alert.alert_type == "price_below" and price <= alert.threshold:
                triggered = True
            elif alert.alert_type == "pct_change":
                if abs(quote.get("day_change_pct", 0)) >= abs(alert.threshold):
                    triggered = True
            if triggered:
                alert.is_active = False
                alert.triggered_at = datetime.now(timezone.utc)
                log.info("Alert triggered", ticker=alert.ticker, type=alert.alert_type, threshold=alert.threshold, price=price)
        db.commit()
    except Exception as e:
        log.error("Alert check failed", error=str(e))
        db.rollback()
    finally:
        db.close()
