from django.db import models


class Visit(models.Model):
	visits = models.PositiveIntegerField(default=0)
	date = models.DateField(auto_now=True, unique=True)  # deployment
	ips = models.JSONField(blank=True, null=True)
	# date = models.DateField(unique=True) # development

	def __str__(self):
		return "visits: '{0}', date: '{1}'".format(str(self.visits), str(self.date))
