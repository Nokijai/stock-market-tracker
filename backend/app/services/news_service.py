"""
News service — Marketaux API (100 req/day free, no CC required).
Fallback: returns empty list gracefully if key missing or quota hit.
"""
import httpx
from datetime import datetime, timezone
from typing import List, Dict, Optional
from app.config import get_settings
from app.utils.cache import cache_get, cache_set
import structlog

log = structlog.get_logger()
settings = get_settings()

_MARKETAUX_URL = "https://api.marketaux.com/v1/news/all"


def _parse_article(a: dict, ticker: str) -> Optional[Dict]:
    headline = a.get("title", "").strip()
    url = a.get("url", "").strip()
    if not headline or not url:
        return None

    # Marketaux sentiment: positive/negative/neutral float per entity
    sentiment = None
    for entity in a.get("entities", []):
        if entity.get("symbol", "").upper() == ticker.upper():
            s = entity.get("sentiment_score")
            if s is not None:
                sentiment = float(s)
            break

    published_raw = a.get("published_at") or a.get("publishedAt")
    published_at = None
    if published_raw:
        try:
            published_at = datetime.fromisoformat(
                published_raw.replace("Z", "+00:00")
            ).isoformat()
        except Exception:
            pass

    return {
        "ticker": ticker.upper(),
        "headline": headline,
        "url": url,
        "source": a.get("source", ""),
        "sentiment": sentiment,
        "image": a.get("image_url", ""),
        "published_at": published_at,
    }


def fetch_ticker_news(ticker: str, limit: int = 10) -> List[Dict]:
    cache_key = f"news:{ticker}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    if not settings.MARKETAUX_API_KEY:
        log.warning("news_service_unavailable", reason="MARKETAUX_API_KEY not set")
        return []

    try:
        resp = httpx.get(
            _MARKETAUX_URL,
            params={
                "symbols": ticker.upper(),
                "filter_entities": "true",
                "language": "en",
                "limit": min(limit * 2, 50),  # fetch extra to dedupe
                "api_token": settings.MARKETAUX_API_KEY,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPStatusError as e:
        log.error("fetch_news_failed", ticker=ticker,
                  status=e.response.status_code, error=str(e))
        return []
    except Exception as e:
        log.error("fetch_news_failed", ticker=ticker, error=str(e))
        return []

    results = []
    seen_urls: set = set()
    for a in data.get("data", []):
        article = _parse_article(a, ticker)
        if not article or article["url"] in seen_urls:
            continue
        seen_urls.add(article["url"])
        results.append(article)
        if len(results) >= limit:
            break

    cache_set(cache_key, results, ttl=1800)
    log.info("fetch_news_ok", ticker=ticker, count=len(results))
    return results


def fetch_market_news(limit: int = 20) -> List[Dict]:
    cache_key = "news:market:general"
    cached = cache_get(cache_key)
    if cached:
        return cached

    if not settings.MARKETAUX_API_KEY:
        return []

    try:
        resp = httpx.get(
            _MARKETAUX_URL,
            params={
                "filter_entities": "true",
                "language": "en",
                "limit": limit,
                "api_token": settings.MARKETAUX_API_KEY,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        log.error("fetch_market_news_failed", error=str(e))
        return []

    results = []
    for a in data.get("data", []):
        headline = a.get("title", "").strip()
        url = a.get("url", "").strip()
        if not headline or not url:
            continue
        published_raw = a.get("published_at") or a.get("publishedAt")
        published_at = None
        if published_raw:
            try:
                published_at = datetime.fromisoformat(
                    published_raw.replace("Z", "+00:00")
                ).isoformat()
            except Exception:
                pass
        results.append({
            "ticker": "MARKET",
            "headline": headline,
            "url": url,
            "source": a.get("source", ""),
            "sentiment": None,
            "image": a.get("image_url", ""),
            "published_at": published_at,
        })

    cache_set(cache_key, results, ttl=1800)
    return results
