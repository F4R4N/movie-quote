from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Quote
from .serializers import QuoteSerializer
import random
class QuoteView(APIView):
	permission_classes = (permissions.AllowAny, )

	def get(self, request, format=None):
		all_quotes = Quote.objects.all().values_list('pk', flat=True)
		quote_pk = random.choice(all_quotes)
		quote = Quote.objects.get(pk=quote_pk)
		serializer = QuoteSerializer(instance=quote)
		return Response(status=status.HTTP_200_OK, data=serializer.data)

class MainPage(APIView):
	permission_classes = (permissions.AllowAny, )

	def get(self, request, format=None):
		data = {
			"Developer": "Faran Taghavi",
			"Email": "farantgh@gmail.com",
			"Website": "movie-quote-api.herokuapp.com",
			"Github": "https://github.com/F4R4N",
			"Paths": ["v1/"]
		}
		return Response(status=status.HTTP_200_OK, data=data)