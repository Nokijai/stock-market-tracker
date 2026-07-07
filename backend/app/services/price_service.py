import yfinance as yf
from datetime import datetime, timezone
from typing import Optional, List, Dict
from app.utils.cache import cache_get, cache_set
import structlog

log = structlog.get_logger()

def fetch_quote(ticker: str) -> Optional[Dict]:
    cache_key = f"quote:{ticker}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    try:
        t = yf.Ticker(ticker)
        info = t.fast_info
        price = getattr(info, "last_price", None)
        prev_close = getattr(info, "previous_close", None)
        if price is None:
            return None
        day_change = (price - prev_close) if prev_close else 0
        day_change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0
        data = {
            "ticker": ticker.upper(),
            "price": round(price, 4),
            "day_change": round(day_change, 4),
            "day_change_pct": round(day_change_pct, 4),
            "volume": getattr(info, "three_month_average_volume", None),
            "market_cap": getattr(info, "market_cap", None),
            "company_name": ticker.upper(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        # Try to get company name from full info
        try:
            full_info = t.info
            data["company_name"] = full_info.get("longName", ticker.upper())
        except Exception:
            pass
        cache_set(cache_key, data, ttl=900)
        return data
    except Exception as e:
        log.error("fetch_quote_failed", ticker=ticker, error=str(e))
        return None

def fetch_quotes_bulk(tickers: List[str]) -> Dict[str, Dict]:
    results = {}
    uncached = []
    for t in tickers:
        cached = cache_get(f"quote:{t}")
        if cached:
            results[t] = cached
        else:
            uncached.append(t)
    if uncached:
        try:
            data = yf.download(uncached, period="2d", auto_adjust=True, progress=False, threads=True)
            if not data.empty:
                # yf.download returns a MultiIndex DataFrame with ticker columns
                for ticker in uncached:
                    try:
                        # Try to get close price for this ticker
                        close_series = data.get("Close", data.get("Adj Close"))
                        if close_series is not None and ticker in close_series.columns:
                            prices = close_series[ticker].dropna()
                            if len(prices) >= 2:
                                price = float(prices.iloc[-1])
                                prev_close = float(prices.iloc[-2])
                                day_change = price - prev_close
                                day_change_pct = (day_change / prev_close * 100) if prev_close else 0
                            elif len(prices) == 1:
                                price = float(prices.iloc[-1])
                                day_change = 0
                                day_change_pct = 0
                            else:
                                # Fallback to per-ticker fetch
                                q = fetch_quote(ticker)
                                if q:
                                    results[ticker] = q
                                continue

                            # Try to get volume and other info
                            volume = None
                            vol_series = data.get("Volume")
                            if vol_series is not None and ticker in vol_series.columns:
                                vols = vol_series[ticker].dropna()
                                if len(vols) > 0:
                                    volume = int(vols.iloc[-1])

                            results[ticker] = {
                                "ticker": ticker.upper(),
                                "price": round(price, 4),
                                "day_change": round(day_change, 4),
                                "day_change_pct": round(day_change_pct, 4),
                                "volume": volume,
                                "market_cap": None,
                                "company_name": ticker.upper(),
                                "updated_at": datetime.now(timezone.utc).isoformat(),
                            }
                        else:
                            # Fallback to per-ticker fetch
                            q = fetch_quote(ticker)
                            if q:
                                results[ticker] = q
                    except Exception:
                        q = fetch_quote(ticker)
                        if q:
                            results[ticker] = q
            else:
                # Empty download — fallback per ticker
                for ticker in uncached:
                    q = fetch_quote(ticker)
                    if q:
                        results[ticker] = q
        except Exception:
            for ticker in uncached:
                q = fetch_quote(ticker)
                if q:
                    results[ticker] = q
    return results

def fetch_history(ticker: str, period: str = "1mo") -> List[Dict]:
    cache_key = f"history:{ticker}:{period}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period, auto_adjust=True)
        if hist.empty:
            return []
        records = []
        for idx, row in hist.iterrows():
            records.append({
                "date": idx.strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 4),
                "high": round(float(row["High"]), 4),
                "low": round(float(row["Low"]), 4),
                "close": round(float(row["Close"]), 4),
                "volume": int(row["Volume"]),
            })
        ttl = 3600 if period in ("1y", "2y") else 900
        cache_set(cache_key, records, ttl=ttl)
        return records
    except Exception as e:
        log.error("fetch_history_failed", ticker=ticker, error=str(e))
        return []

def fetch_spy_history(period: str = "1y") -> List[Dict]:
    """Fetch SPY (S&P 500 ETF) price history in the same format as fetch_history."""
    return fetch_history("SPY", period=period)


def fetch_fundamentals(ticker: str) -> Optional[Dict]:
    cache_key = f"fundamentals:{ticker}"
    cached = cache_get(cache_key)
    if cached:
        return cached
    try:
        t = yf.Ticker(ticker)
        info = t.info
        data = {
            "ticker": ticker.upper(),
            "company_name": info.get("longName", ticker),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "dividend_yield": info.get("dividendYield"),
            "week_52_high": info.get("fiftyTwoWeekHigh"),
            "week_52_low": info.get("fiftyTwoWeekLow"),
            "beta": info.get("beta"),
            "market_cap": info.get("marketCap"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
        }
        cache_set(cache_key, data, ttl=86400)
        return data
    except Exception as e:
        log.error("fetch_fundamentals_failed", ticker=ticker, error=str(e))
        return None
