from django.core.management.base import BaseCommand, CommandError
from statistic.report import monthly_report

class Command(BaseCommand):
    help = "Send month's report to admin's email address"

    def handle(self, *args, **options):
        monthly_report()