from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
sched = BlockingScheduler()

# @sched.scheduled_job("cron", year="*", month='*', day="last", hour=23, minute=59)
@sched.scheduled_job("cron", minute=1)
def send_report():
    call_command("monthly_report")

sched.start()
