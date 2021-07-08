from django.utils import timezone
from .models import Visit
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
import calendar
from .utils import views_in_month


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
		status, data, total_views = views_in_month(year, month)
		return Response(status=status, data=data)


class VisitorsView(APIView):
	permissin_classes = (permissions.IsAdminUser, )

	def get(self, request, year, month, day, format=None):
		visit = get_object_or_404(Visit, date__year=year, date__month=month, date__day=day)
		return Response(status=status.HTTP_200_OK, data=visit.ips)
