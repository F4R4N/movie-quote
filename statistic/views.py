from django.utils import timezone
from .models import Visit
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
import calendar


class VisitsYearView(APIView):
	permissin_classes = (permissions.IsAdminUser, )

	def get(self, request, year, format=None):
		cur_year = timezone.now().year
		if year == cur_year:
			months = timezone.now().month
		elif year < cur_year:
			months = 12
		elif year > cur_year:
			return Response(
				status=status.HTTP_400_BAD_REQUEST,
				data={"detail": "given year not reached yet."})

		cur_month_visits = {}
		for month in range(1, months+1):
			if month not in cur_month_visits.keys():
				cur_month_visits[calendar.month_name[month]] = 0
			year_visit = list(Visit.objects.filter(date__year=year, date__month=month).values_list("visits", flat=True))
			cur_month_visits[calendar.month_name[month]] += sum(year_visit)

		return Response(status=status.HTTP_200_OK, data=cur_month_visits)


class VisitsMonthView(APIView):
	permissin_classes = (permissions.IsAdminUser, )

	def get(self, request, year, month, foramt=None):
		cur_year = timezone.now().year
		cur_month = timezone.now().month
		cur_day = timezone.now().day
		mnt = month
		if year == cur_year:
			if month > cur_month:
				return Response(
					status=status.HTTP_400_BAD_REQUEST,
					data={"detail": "requested month not reached yet."})

		elif year > cur_year:
			return Response(
				status=status.HTTP_400_BAD_REQUEST,
				data={"detail": "requested year not reached yet."})
		n, day_in_cur_month = calendar.monthrange(year, mnt)
		visits_in_month = {}
		if month == cur_month:
			day_in_cur_month = cur_day
		for day in range(1, day_in_cur_month+1):
			visits_in_month["{0}-{1}-{2}".format(year, month, day)] = 0
			try:
				month_visit = Visit.objects.get(date__year=year, date__month=mnt, date__day=day)
				visits_in_month["{0}-{1}-{2}".format(year, month, day)] = month_visit.visits
			except Visit.DoesNotExist:
				pass

		return Response(status=status.HTTP_200_OK, data=visits_in_month)


class VisitorsView(APIView):
	permissin_classes = (permissions.IsAdminUser, )

	def get(self, request, year, month, day, format=None):
		visit = get_object_or_404(Visit, date__year=year, date__month=month, date__day=day)
		return Response(status=status.HTTP_200_OK, data=visit.ips)
