"""Daily digest job — renders and sends a portfolio digest email to every user."""

import asyncio
from datetime import datetime, timezone
from typing import Dict, List

import structlog
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models.holding import Holding
from app.models.user import User
from app.models.watchlist import WatchlistItem
from app.services.analytics import compute_portfolio_summary, enrich_holding
from app.services.email_service import send_daily_digest
from app.services.price_service import fetch_quote

log = structlog.get_logger()


def run_daily_digest() -> None:
    """
    Run the daily digest job.

    For each user in the DB:
    1. Fetch their holdings and enrich with current prices
    2. Compute portfolio summary via analytics
    3. Render the HTML template
    4. Send via email_service (or log if SMTP not configured)

    Intended to run every weekday at 8:00 AM via APScheduler.
    """
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        if not users:
            log.info("Daily digest: no users found")
            return

        settings = get_settings()
        smtp_ready = bool(settings.SMTP_HOST and settings.SMTP_USERNAME)
        log.info(
            "Daily digest starting",
            user_count=len(users),
            smtp_configured=smtp_ready,
        )

        success_count = 0
        fail_count = 0

        async def _process_user(user):
            nonlocal success_count, fail_count
            try:
                # --- Holdings ---
                holdings = (
                    db.query(Holding)
                    .filter(Holding.user_id == user.id)
                    .all()
                )

                holdings_data: List[Dict] = []
                for h in holdings:
                    quote = fetch_quote(h.ticker)
                    h_dict = {
                        "ticker": h.ticker,
                        "shares": h.shares,
                        "avg_cost": h.avg_cost,
                        "currency": h.currency,
                    }
                    enriched = enrich_holding(h_dict, quote)
                    holdings_data.append(enriched)

                summary = compute_portfolio_summary(holdings_data)

                watchlist_items = (
                    db.query(WatchlistItem)
                    .filter(WatchlistItem.user_id == user.id)
                    .all()
                )
                watchlist_data: List[Dict] = []
                for w in watchlist_items:
                    quote = fetch_quote(w.ticker)
                    watchlist_data.append({
                        "ticker": w.ticker,
                        "price": quote["price"] if quote else None,
                        "day_change_pct": quote.get("day_change_pct") if quote else None,
                    })

                user_name = user.email.split("@")[0] if "@" in user.email else user.email

                sent = await send_daily_digest(
                    user_email=user.email,
                    user_name=user_name,
                    holdings_data=holdings_data,
                    summary=summary,
                    watchlist_data=watchlist_data,
                )

                if sent:
                    success_count += 1
                else:
                    fail_count += 1

            except Exception as exc:
                log.error(
                    "Daily digest failed for user",
                    user_id=user.id,
                    user_email=user.email,
                    error=str(exc),
                )
                fail_count += 1

        async def _process_all():
            for user in users:
                await _process_user(user)

        asyncio.run(_process_all())

        log.info(
            "Daily digest complete",
            success=success_count,
            failed=fail_count,
        )

    except Exception as exc:
        log.error("Daily digest job failed", error=str(exc))
    finally:
        db.close()