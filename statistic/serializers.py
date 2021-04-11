from rest_framework import serializers
from .models import Visit


class VisitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Visit
		fields = ("visits", "date")
