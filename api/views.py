from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from .models import Quote, Show, Role
from .serializers import (
	QuoteSerializer, AdminQuoteSerializer,
	AdminAddUserSerializer, ShowSerializer, RoleSerializer)
from django.shortcuts import get_object_or_404
from statistic.utils import get_client_ip
from django.conf import settings
import random
from django.contrib.auth.models import User
from statistic.utils import add_or_create_visit


class MainPage(APIView):
	"""Show developers info instead of 404 at the main page"""
	permission_classes = (permissions.AllowAny, )

	def get(self, request, format=None):
		all_shows = list(set(Show.objects.all().values_list('slug', flat=True)))
		data = {
			"Developer": "Faran Taghavi",
			"Email": "farantgh@gmail.com",
			"Website": "https://movie-quote-api.herokuapp.com/",
			"Github": "https://github.com/F4R4N",
			"Show-Slugs": all_shows,
			"Paths": [
				"v1/quote/",
				"v1/shows/<Show-Slugs>",
				"v1/quote/censored/"
			]
		}
		return Response(status=status.HTTP_200_OK, data=data)


class UserQuoteView(APIView):
	"""Show a random quote to the user"""
	permission_classes = (permissions.AllowAny, )

	def get(self, request, format=None):
		ip = get_client_ip(request)
		add_or_create_visit(ip)
		if "censored" in request.query_params:

			all_quotes = Quote.objects.filter(
				contain_adult_lang=False).values_list('pk', flat=True)
		else:
			all_quotes = Quote.objects.all().values_list('pk', flat=True)

		try:
			quote_pk = random.choice(all_quotes)
		except IndexError:
			return Response(
				status=status.HTTP_200_OK,
				data={
					"detail": "No quote available please try again later.",
					"status": "no-quote"
				}
			)

		quote = get_object_or_404(Quote, pk=quote_pk)
		serializer = QuoteSerializer(instance=quote)
		return Response(status=status.HTTP_200_OK, data=serializer.data)


class SpecificShowQuotes(APIView):
	"""Show a random quote from the given slug show (shows slug are listed in
	the mainpage)"""
	permission_classes = (permissions.AllowAny, )

	def get(self, request, slug, format=None):
		requested_show = get_object_or_404(Show, slug=slug)
		if not requested_show.show.all().exists():
			return Response(
				status=status.HTTP_204_NO_CONTENT,
				data={
					"detail": "no quote for this show yet.",
					"status": "no-quote-for-show"
				}
			)

		all_requested_show_quotes = requested_show.show.all().values_list(
			'pk', flat=True)

		quote_pk = random.choice(all_requested_show_quotes)
		quote = get_object_or_404(Quote, pk=quote_pk)
		serializer = QuoteSerializer(instance=quote)
		return Response(status=status.HTTP_200_OK, data=serializer.data)


class AdminQuoteView(generics.ListCreateAPIView):
	"""
	GET show all quotes at once (admin only).
	POST add new quote (included quote, show, role) (admins only).

	"""

	queryset = Quote.objects.all()
	permission_classes = (permissions.IsAdminUser, )
	serializer_class = AdminQuoteSerializer


class AdminEditQuoteView(APIView):
	"""
	edit quotes get field 'quote', 'role', 'show'.
	should include quote key in the url.

	"""

	permission_classes = (permissions.IsAdminUser, )

	def put(self, request, key, format=None):
		if not "quote" and "show" and "role" in request.data:
			return Response(
				status=status.HTTP_400_BAD_REQUEST,
				data={"detail": "no new data provided"})

		quote = get_object_or_404(Quote, key=key)

		if "show" in request.data:
			show = get_object_or_404(Show, name=request.data["show"].title())
			quote.show = show
		if "role" in request.data:
			role = get_object_or_404(Role, name=request.data["role"].title())
			quote.role = role
		if "quote" in request.data:
			quote.quote = request.data["quote"]
		quote.save()
		return Response(status=status.HTTP_200_OK, data={"detail": "updated"})

	def delete(self, request, key, format=None):
		quote = get_object_or_404(Quote, key=key)
		quote.delete()
		return Response(status=status.HTTP_200_OK, data={"detail": "deleted"})


class AdminEditShowView(APIView):
	""" edit show get field 'name' should include show slug in url. """
	permission_classes = (permissions.IsAdminUser, )

	def put(self, request, slug, format=None):
		if "name" not in request.data:
			return Response(
				status=status.HTTP_400_BAD_REQUEST,
				data={
					"detail": "no new data provided.",
					"name": "this field is required."
				}
			)

		show = get_object_or_404(Show, slug=slug)
		show.name = request.data["name"]
		show.save()
		return Response(status=status.HTTP_200_OK, data={"detail": "show updated"})


class AdminAllShowsView(generics.ListAPIView):
	""" show all shows to admin user """
	permission_classes = (permissions.IsAdminUser, )
	serializer_class = ShowSerializer
	queryset = Show.objects.all()


class AdminEditRoleView(APIView):
	""" edit role get field 'name' should include role slug in url. """
	permission_classes = (permissions.IsAdminUser, )

	def put(self, request, slug, format=None):
		if "name" not in request.data:
			return Response(
				status=status.HTTP_400_BAD_REQUEST,
				data={
					"detail": "no new data provided.",
					"name": "this field is required."
				}
			)

		role = get_object_or_404(Role, slug=slug)
		role.name = request.data["name"]
		role.save()
		return Response(status=status.HTTP_200_OK, data={"detail": "role updated."})


class AdminAllRolesView(generics.ListAPIView):
	""" show all roles to admin user """
	permission_classes = (permissions.IsAdminUser, )
	serializer_class = RoleSerializer
	queryset = Role.objects.all()


class AdminUserView(generics.ListCreateAPIView):
	"""
	GET return all users (admin only).
	POST add new user (admin only) [username, first_name, last_name, email,
	password1, password2](only main superuser can make user)

	"""

	queryset = User.objects.all()
	permission_classes = (permissions.IsAdminUser, )
	serializer_class = AdminAddUserSerializer


class AdminEditUserView(APIView):
	"""
	edit user credentials (every user can edit itselves profile.
	also mainsuperuser (default faran) can edit every users profile.).
	it should include at least one of : [first_name, last_name, username, email,
	(together [password1,password2]), (only main superuser can modify this
	[is_superuser, is_active, is_staff]) ]"""

	permission_classes = (permissions.IsAuthenticated, )

	def put(self, request, pk, format=None):
		user = request.user
		if user != User.objects.get(pk=pk):
			if not user.is_superuser and user.username != settings.MAINSUPERUSER:
				return Response(
					status=status.HTTP_401_UNAUTHORIZED,
					data={"detail": "you don't have permission for this user"})

		instance = get_object_or_404(User, pk=pk)

		if "first_name" in request.data:
			instance.first_name = request.data['first_name']
		if "last_name" in request.data:
			instance.last_name = request.data['last_name']
		if "username" in request.data:
			if User.objects.filter(username=request.data['username']).exists():
				return Response(
					status=status.HTTP_400_BAD_REQUEST,
					data={"detail": "username already exist"})

			instance.username = request.data['username']
		if "email" in request.data:
			try:
				validate_email(request.data["email"])
			except ValidationError as eex:
				return Response(
					status=status.HTTP_400_BAD_REQUEST, data={"detail": {"email": eex}})

			instance.email = request.data['email']

		if "password1" in request.data:
			if "password2" not in request.data:
				return Response(
					status=status.HTTP_400_BAD_REQUEST,
					data={"detail": "password2 field not provided"})

			if request.data['password1'] != request.data["password2"]:
				return Response(
					status=status.HTTP_400_BAD_REQUEST,
					data={"detail": "password fields don't match"})

			try:
				validate_password(request.data['password1'], user)
				instance.set_password(request.data['password1'])
			except ValidationError as ex:
				return Response(
					status=status.HTTP_400_BAD_REQUEST, data={"detail": {"password": ex}})

		if "is_superuser" or "is_active" or "is_staff" in request.data:
			if user.username != settings.MAINSUPERUSER:
				return Response(
					status=status.HTTP_401_UNAUTHORIZED,
					data={
						"detail": "you don't have permission to perform \
						this action, contact the admin user"
					}
				)

		if "is_superuser" in request.data:
			instance.is_superuser = request.data["is_superuser"]
		if "is_active" in request.data:
			instance.is_active = request.data['is_active']
		if "is_staff" in request.data:
			instance.is_staff = request.data['is_staff']
		instance.save()
		return Response(status=status.HTTP_200_OK, data={"detail": "user updated"})


class AdminDeleteUserView(APIView):
	"""
	main super user can delete anyone and anyone can delete itself. put pk in url

	"""

	permission_classes = (permissions.IsAdminUser, )

	def delete(self, request, pk, format=None):
		user = request.user
		deletable_user = get_object_or_404(User, pk=pk)
		if user.username != settings.MAINSUPERUSER:
			if user != deletable_user:
				return Response(
					status=status.HTTP_400_BAD_REQUEST,
					data={"detail": "you don't have permission for this user."})

		deletable_user.is_active = False
		deletable_user.save()
		return Response(
			status=status.HTTP_200_OK,
			data={"detail": "user '{0}' deleted".format(deletable_user.username)})
