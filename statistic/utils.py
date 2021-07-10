from django.utils import timezone
from rest_framework import status
from .models import Visit
import requests
from django.conf import settings
import calendar


def add_or_create_visit(ip):
	try:
		visit = Visit.objects.get(date=timezone.now().date())
		visit.visits += 1
		if ip in visit.visitors:
			visit.visitors[ip]["views"] += 1
		else:
			visit.visitors[ip] = {"views": 1}
			visit.visitors[ip]["location"] = get_user_country_by_ip(ip)
		visit.save()
	except Visit.DoesNotExist:
		visit = Visit.objects.create(
			visits=1, visitors={
				ip: {"views": 1, "location": get_user_country_by_ip(ip), }
			}
		)


def get_client_ip(request) -> str:
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def get_user_country_by_ip(ip: str) -> str:
	api_key = settings.IPSTACK_ACCESS_KEY
	print(api_key)
	url = f"http://api.ipstack.com/{ip}?access_key={api_key}"
	response = requests.get(url).json()
	return "{0} {1}, {2}".format(
		response["country_name"], response["region_name"], response["city"])


def views_in_month(year, month):
	cur_year = timezone.now().year
	cur_month = timezone.now().month
	cur_day = timezone.now().day
	total_visits = 0
	if year == cur_year:
		if month > cur_month:
			return (
				status.HTTP_400_BAD_REQUEST,
				{"detail": "requested month not reached yet."})

	elif year > cur_year:
		return (
			status.HTTP_400_BAD_REQUEST,
			{"detail": "requested year not reached yet."})

	n, day_in_cur_month = calendar.monthrange(year, month)
	visits_in_month = {}
	if month == cur_month:
		day_in_cur_month = cur_day
	for day in range(1, day_in_cur_month + 1):
		visits_in_month["{0}-{1}-{2}".format(year, month, day)] = 0
		try:
			month_visit = Visit.objects.get(
				date__year=year, date__month=month, date__day=day)

			visits_in_month["{0}-{1}-{2}".format(year, month, day)] = month_visit.visits
			total_visits += month_visit.visits
		except Visit.DoesNotExist:
			pass
	return (status.HTTP_200_OK, visits_in_month, total_visits)
