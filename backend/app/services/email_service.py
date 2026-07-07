"""Email service for sending daily digest emails via SMTP (or fallback to logging)."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional

import aiosmtplib
import jinja2
import structlog

from app.config import get_settings

log = structlog.get_logger()

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_jinja_env: Optional[jinja2.Environment] = None


def _get_jinja_env() -> jinja2.Environment:
    """Lazy-init the Jinja2 environment pointing at app/templates/."""
    global _jinja_env
    if _jinja_env is None:
        _jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=True,
        )
    return _jinja_env


async def send_daily_digest(
    user_email: str,
    user_name: str,
    holdings_data: List[Dict],
    summary: Dict,
    watchlist_data: Optional[List[Dict]] = None,
) -> bool:
    """
    Render the daily digest template and send via SMTP.

    Falls back to logging the digest if SMTP is not configured.

    Returns True on success, False on failure.
    """
    settings = get_settings()
    smtp_configured = bool(settings.SMTP_HOST and settings.SMTP_USERNAME)

    try:
        env = _get_jinja_env()
        template = env.get_template("daily_digest.html")
        html_body = template.render(
            user_name=user_name,
            holdings=holdings_data,
            summary=summary,
            watchlist=watchlist_data or [],
        )
    except Exception as exc:
        log.error("Failed to render digest template", error=str(exc))
        return False

    if not smtp_configured:
        # Fallback: log the digest
        log.info(
            "Daily digest (SMTP not configured — logged instead)",
            user_email=user_email,
            user_name=user_name,
            summary=summary,
        )
        return True

    # Build MIME message
    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM
    msg["To"] = user_email
    msg["Subject"] = f"Stock Tracker Daily Digest — {user_name}"
    msg.attach(MIMEText(html_body, "html"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        log.info("Daily digest sent", user_email=user_email, user_name=user_name)
        return True
    except Exception as exc:
        log.error(
            "Failed to send daily digest email",
            user_email=user_email,
            error=str(exc),
        )
        return False