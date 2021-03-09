from rest_framework import serializers
from .models import Quote, Role
class QuoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Quote
		fields = ("quote", 'role')
	role = serializers.CharField(source="role.name")
