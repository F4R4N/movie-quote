from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

sched = BlockingScheduler()


# @sched.scheduled_job("cron", year="*", month='*', day="*", hour=23, minute=2)
@sched.scheduled_job("interval", minutes=1)
def send_report():
    call_command("monthly_report")


sched.start()
