from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.configure(
    apscheduler_autostart=True,
    apscheduler_log_level=30,
    timezone="Asia/Shanghai")

if scheduler.running:
    scheduler.shutdown()
    print("scheduler shutdown")

if not scheduler.running:
    scheduler.start()
    print("scheduler start")
