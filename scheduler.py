from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

def schedule(sync_job, send_job, week_job, url, tz, bot):
    scheduler = AsyncIOScheduler(timezone=timezone(tz))
    scheduler.add_job(sync_job, 'interval', hours=2, args=[url])
    scheduler.add_job(send_job, 'cron', hour=0, minute=0, args=[bot])
    scheduler.add_job(week_job, 'cron', day_of_week='sun', hour=0, minute=15, args=[bot])
    scheduler.start()