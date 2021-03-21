from django.shortcuts import render
from django.utils import timezone
from .models import Visit
from .serializers import VisitSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets, generics

class VisitsYearView(APIView):
	permissin_classes = (permissions.IsAdminUser)

	def get(self, request, year, format=None):
		cur_year = timezone.now().year
		if year == cur_year:
			months = timezone.now().month
		elif year < cur_year:
			months = 12
		elif year > cur_year:
			return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "given year not reached yet."})
		cur_month_visits = {}
		for month in range(1, months+1):
			if not month in cur_month_visits.keys():
				cur_month_visits[month] = 0
			year_visit = list(Visit.objects.filter(date__year=year, date__month=month).values_list("visits", flat=True))
			# for i in year_visit:
			cur_month_visits[month] += sum(year_visit)

		return Response(status=status.HTTP_200_OK, data=cur_month_visits)


class VisitsMonthView(APIView):
	permissin_classes = (permissions.IsAdminUser)

	def get(self, request, year, month, foramt=None):
		month_visit = Visit.objects.filter(date__year=year, date__month=month)
		serializer = VisitSerializer(instance=month_visit, many=True)
		return Response(status=status.HTTP_200_OK, data=serializer.data)