from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from app.scheduler.jobs import refresh_prices, fetch_all_news, check_alerts
from app.scheduler.digest_job import run_daily_digest
import structlog

log = structlog.get_logger()
scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(refresh_prices, IntervalTrigger(minutes=15), id="refresh_prices", replace_existing=True)
    scheduler.add_job(fetch_all_news, IntervalTrigger(minutes=30), id="fetch_news", replace_existing=True)
    scheduler.add_job(check_alerts, IntervalTrigger(minutes=15), id="check_alerts", replace_existing=True)
    scheduler.add_job(run_daily_digest, CronTrigger(hour=8, minute=0, day_of_week='mon-fri'), id="daily_digest", replace_existing=True)
    scheduler.start()
    log.info("Scheduler started")

def stop_scheduler():
    scheduler.shutdown(wait=False)
    log.info("Scheduler stopped")
