from apscheduler.schedulers.background import BackgroundScheduler

def check_schedules():
    print("Checking upcoming classes and sending alerts...")

scheduler = BackgroundScheduler()
scheduler.add_job(check_schedules, "interval", minutes=5)
scheduler.start()