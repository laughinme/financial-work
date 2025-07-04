from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from .myfx_scheduler import myfx_job


def init_scheduler():
    """
    Add all jobs to scheduler
    """
    scheduler = AsyncIOScheduler()
    
    # scheduler.add_job(
    #     func=myfx_job,
    #     trigger="cron",
    #     minute="*/10",
    #     id="myfx_job",
    #     next_run_time=datetime.now() + timedelta(seconds=3),
    #     max_instances=1,
    #     coalesce=True,
    #     misfire_grace_time=60,
    # )
    scheduler.add_job(
        func=myfx_job,
        trigger="interval",
        seconds=60 * 1,
        id="myfx_job",
        next_run_time=datetime.now() + timedelta(seconds=3),
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
    )
    scheduler.start()

    return scheduler