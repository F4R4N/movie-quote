from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def send_report():
    call_command("monthly_report")


sched = BlockingScheduler()

sched.add_job(send_report, "cron", year="*", month="*", day="*")

sched.start()
