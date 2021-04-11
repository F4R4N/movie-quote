from django.utils import timezone
from .models import Visit


def add_or_create_visit(ip):
	try:
		visit = Visit.objects.get(date=timezone.now().date())
		visit.visits += 1
		if ip in visit.ips:
			visit.ips[ip] += 1
		else:
			visit.ips[ip] = 1
		visit.save()
	except Visit.DoesNotExist:
		visit = Visit.objects.create(visits=1, ips={ip: 1})
		visit.save()


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
