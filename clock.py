from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

sched = BlockingScheduler()

# @sched.scheduled_job("cron", year="*", month='*', day="last", hour=23, minutes=59)
@sched.scheduled_job("interval", minutes=1)
def send_report():
    call_command("migrate")

sched.start()
