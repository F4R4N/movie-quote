import datetime
import calendar
import time, os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()

from statistic.report import monthly_report

while True:
    cur_year, cur_month = datetime.datetime.now().year, datetime.datetime.now().month
    _, day_in_cur_month = calendar.monthrange(cur_year, cur_month)
    if datetime.datetime.now().strftime("%Y%m%d%H%M%S") == datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, 8, 23, 4, 59).strftime("%Y%m%d%H%M%S"):
        monthly_report()
        time.sleep(1)
    else:
        time.sleep(1)
