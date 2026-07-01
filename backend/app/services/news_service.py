import finnhub
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from app.config import get_settings
from app.utils.cache import cache_get, cache_set
import structlog

log = structlog.get_logger()
settings = get_settings()

def _get_client():
    if not settings.FINNHUB_API_KEY:
        return None
    return finnhub.Client(api_key=settings.FINNHUB_API_KEY)

def fetch_ticker_news(ticker: str, limit: int = 10) -> List[Dict]:
    cache_key = f"news:{ticker}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    client = _get_client()
    if not client:
        return []

    try:
        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=7)
        articles = client.company_news(
            ticker.upper(),
            _from=from_date.strftime("%Y-%m-%d"),
            to=to_date.strftime("%Y-%m-%d"),
        )
        results = []
        seen_urls = set()
        for a in articles[:limit * 2]:
            url = a.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            # Normalise sentiment: Finnhub returns 0.0 if unavailable
            sentiment_raw = a.get("sentiment", 0.0)
            results.append({
                "ticker": ticker.upper(),
                "headline": a.get("headline", ""),
                "url": url,
                "source": a.get("source", ""),
                "sentiment": float(sentiment_raw) if sentiment_raw else None,
                "image": a.get("image", ""),
                "published_at": datetime.fromtimestamp(a.get("datetime", 0), tz=timezone.utc).isoformat()
                    if a.get("datetime") else None,
            })
            if len(results) >= limit:
                break
        cache_set(cache_key, results, ttl=1800)
        return results
    except Exception as e:
        log.error("fetch_news_failed", ticker=ticker, error=str(e))
        return []

def fetch_market_news(limit: int = 20) -> List[Dict]:
    cache_key = "news:market:general"
    cached = cache_get(cache_key)
    if cached:
        return cached

    client = _get_client()
    if not client:
        return []

    try:
        articles = client.general_news("general", min_id=0)
        results = []
        for a in articles[:limit]:
            results.append({
                "ticker": "MARKET",
                "headline": a.get("headline", ""),
                "url": a.get("url", ""),
                "source": a.get("source", ""),
                "sentiment": None,
                "image": a.get("image", ""),
                "published_at": datetime.fromtimestamp(a.get("datetime", 0), tz=timezone.utc).isoformat()
                    if a.get("datetime") else None,
            })
        cache_set(cache_key, results, ttl=1800)
        return results
    except Exception as e:
        log.error("fetch_market_news_failed", error=str(e))
        return []
