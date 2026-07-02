"""
V2 AI Service — news summarisation + sentiment via LiteLLM (claude-sonnet-4-6).
"""
import json
from typing import List, Dict, Optional
from openai import OpenAI
from app.config import get_settings
from app.utils.cache import cache_get, cache_set
import structlog

log = structlog.get_logger()
settings = get_settings()

_SYSTEM_PROMPT = """You are a concise financial news analyst for beginner investors.
Given a list of news headlines and snippets about a stock, return a JSON object with:
- "bullets": exactly 3 plain-English bullet points (≤15 words each) summarising the key themes
- "sentiment": one of "Bullish", "Neutral", or "Bearish" reflecting the overall tone
- "reason": one short sentence (≤20 words) explaining the sentiment

Respond ONLY with valid JSON. No markdown, no extra text."""

_USER_TEMPLATE = """Stock: {ticker}

News headlines (last 7 days):
{headlines}

Return JSON only."""


def _get_client() -> Optional[OpenAI]:
    if not settings.LITELLM_BASE_URL:
        return None
    return OpenAI(
        api_key=settings.LITELLM_API_KEY or "dummy",
        base_url=settings.LITELLM_BASE_URL,
    )


def summarise_news(ticker: str, articles: List[Dict]) -> Optional[Dict]:
    """
    Summarise news articles for a ticker.
    Returns: {"bullets": [...], "sentiment": "Bullish"|"Neutral"|"Bearish", "reason": "..."}
    Returns None if AI is unavailable or fails.
    """
    if not articles:
        return None

    cache_key = f"ai:summary:{ticker}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    client = _get_client()
    if not client:
        log.warning("ai_service_unavailable", reason="LITELLM_BASE_URL not set")
        return None

    headlines = "\n".join(
        f"- {a['headline']}" for a in articles[:10] if a.get("headline")
    )
    if not headlines:
        return None

    try:
        response = client.chat.completions.create(
            model=settings.LITELLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": _USER_TEMPLATE.format(
                    ticker=ticker.upper(),
                    headlines=headlines,
                )},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if model wraps in ```json
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        result = json.loads(raw)

        # Validate shape
        if not all(k in result for k in ("bullets", "sentiment", "reason")):
            raise ValueError(f"Missing keys in AI response: {result}")
        if result["sentiment"] not in ("Bullish", "Neutral", "Bearish"):
            result["sentiment"] = "Neutral"
        if not isinstance(result["bullets"], list):
            result["bullets"] = [str(result["bullets"])]

        cache_set(cache_key, result, ttl=3600)  # cache 1 hour
        log.info("ai_summary_ok", ticker=ticker, sentiment=result["sentiment"])
        return result

    except json.JSONDecodeError as e:
        log.error("ai_summary_json_error", ticker=ticker, error=str(e), raw=raw[:200])
        return None
    except Exception as e:
        log.error("ai_summary_failed", ticker=ticker, error=str(e))
        return None
