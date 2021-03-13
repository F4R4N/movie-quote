from rest_framework.views import APIView
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Quote, Show, Role
from .serializers import QuoteSerializer, UserLoginSerializer, AdminQuoteSerializer
from django.shortcuts import get_object_or_404
from .utils import IsAdminOrReadOnly
import random
from django.contrib.auth.models import User

class CreateQuote(APIView):
	permission_classes = (permissions.IsAdminUser, )

	def post(self, request, format=None):
		show = get_object_or_404(Show, slug=request.data['show'])
		role = get_object_or_404(Role, slug=request.data['role'])
		quote = Quote.objects.create(
			quote=request.data['quote'],
			show=show,
			role=role
		)
		quote.save()
		return Response(status=status.HTTP_201_CREATED, data={"detail": "created"})


class EditQuote(viewsets.ModelViewSet):
	queryset = Quote.objects.all()
	permission_classes = (permissions.IsAdminUser, )
	serializer_class = AdminQuoteSerializer
	lookup_field = "key"
	
class QuoteView(APIView):
	permission_classes = (IsAdminOrReadOnly, )

	def get(self, request, format=None):
		all_quotes = Quote.objects.all().values_list('pk', flat=True)
		quote_pk = random.choice(all_quotes)
		quote = get_object_or_404(Quote, pk=quote_pk)
		serializer = QuoteSerializer(instance=quote)
		return Response(status=status.HTTP_200_OK, data=serializer.data)

class MainPage(APIView):
	permission_classes = (permissions.AllowAny, )

	def get(self, request, format=None):
		all_shows = Show.objects.all().values_list('slug', flat=True)
		data = {
			"Developer": "Faran Taghavi",
			"Email": "farantgh@gmail.com",
			"Website": "movie-quote-api.herokuapp.com",
			"Github": "https://github.com/F4R4N",
			"Show-Slugs": all_shows,
			"Url": "https://movie-quote-api.herokuapp.com/v1/shows/<Show-Slugs>"
		}
		return Response(status=status.HTTP_200_OK, data=data)

class SpecificShowQuotes(APIView):
	permission_classes = (permissions.AllowAny, )

	def get(self, request, slug, format=None):
		requested_show = get_object_or_404(Show, slug=slug)
		if not requested_show.show.all():
			return Response(status=status.HTTP_204_NO_CONTENT, data={"detail": "no quote for this show yet."})
		all_requested_show_quotes = requested_show.show.all().values_list('pk', flat=True)
		quote_pk = random.choice(all_requested_show_quotes)
		quote = get_object_or_404(Quote, pk=quote_pk)
		serializer = QuoteSerializer(instance=quote)
		return Response(status=status.HTTP_200_OK, data=serializer.data)

