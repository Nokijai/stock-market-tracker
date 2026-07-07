"""
Alert notification service.

Sends alert notifications via ntfy.sh (primary) with optional SMTP/email fallback.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

import httpx
import structlog

from app.config import get_settings

log = structlog.get_logger()

NOTIFICATION_TEMPLATE = (
    "{emoji} {alert_type} alert triggered for {ticker}\n"
    "Threshold: {threshold}\n"
    "Current price: ${price}\n"
    "Time: {timestamp}"
)

ALERT_TYPE_EMOJI = {
    "price_above": "📈",
    "price_below": "📉",
    "pct_change": "📊",
}


async def send_alert_notification(
    ticker: str,
    alert_type: str,
    threshold: float,
    price: float,
    timestamp: datetime | None = None,
) -> bool:
    """Send alert notification, trying ntfy.sh first, then email fallback.

    Returns True if at least one delivery method succeeded.
    """
    settings = get_settings()

    ts = (timestamp or datetime.utcnow()).isoformat()
    emoji = ALERT_TYPE_EMOJI.get(alert_type, "🚨")

    message = NOTIFICATION_TEMPLATE.format(
        emoji=emoji,
        alert_type=alert_type.replace("_", " ").title(),
        ticker=ticker,
        threshold=threshold,
        price=f"{price:.2f}",
        timestamp=ts,
    )

    sent = False

    # --- ntfy.sh (primary) ---
    if settings.NTFY_TOPIC:
        try:
            await _send_ntfy(settings.NTFY_TOPIC, ticker, message)
            sent = True
        except Exception as exc:
            log.warning("ntfy.sh notification failed, trying email fallback",
                        ticker=ticker, error=str(exc))

    # --- Email fallback ---
    if not sent:
        # Check if SMTP settings are configured (we use commented-out defaults,
        # so try to use settings directly — they'll be empty strings if unset).
        smtp_host = getattr(settings, "SMTP_HOST", None)
        if smtp_host:
            try:
                await _send_email(
                    to=getattr(settings, "NOTIFY_EMAIL", ""),
                    subject=f"🚨 Alert: {ticker}",
                    body=message,
                )
                sent = True
            except Exception as exc:
                log.error("Email notification also failed",
                          ticker=ticker, error=str(exc))

    if not sent:
        log.info("No notification method configured; alert logged only",
                 ticker=ticker, alert_type=alert_type)

    return sent


async def _send_ntfy(topic: str, ticker: str, message: str) -> None:
    """Send push notification via ntfy.sh."""
    url = f"https://ntfy.sh/{topic}"
    payload = message.encode("utf-8")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            content=payload,
            headers={
                "Title": f"🚨 Alert: {ticker}",
                "Priority": "high",
                "Tags": "warning,chart_with_upwards_trend",
            },
            timeout=10.0,
        )
        resp.raise_for_status()

    log.info("ntfy.sh notification sent", ticker=ticker, topic=topic)


async def _send_email(to: str, subject: str, body: str) -> None:
    """Send email notification via SMTP using aiosmtplib."""
    import aiosmtplib
    from email.mime.text import MIMEText

    settings = get_settings()

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = getattr(settings, "SMTP_FROM", "alerts@stock-tracker")
    msg["To"] = to

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=getattr(settings, "SMTP_PORT", 587),
        username=getattr(settings, "SMTP_USERNAME", None),
        password=getattr(settings, "SMTP_PASSWORD", None),
        start_tls=True,
        timeout=15,
    )

    log.info("Email notification sent", to=to, subject=subject)