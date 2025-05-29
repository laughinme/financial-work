from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .myfx_scheduler import myfx_job

scheduler = AsyncIOScheduler()

def init_scheduler():
    """
    Add all jobs to scheduler
    """
    
    scheduler.add_job(
        func=myfx_job,
        trigger='interval',
        seconds=3
    )
    scheduler.start()
