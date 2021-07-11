from rest_framework import serializers
from .models import Visit


class VisitByMonthSerializer(serializers.ModelSerializer):
	"""Used in VisitorsViewByMonth view"""
	class Meta:
		model = Visit
		fields = ("date", "visitors", )
