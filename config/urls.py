from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
	openapi.Info(
		title="Movie Quote Api Documentation",
		default_version='v1',
		description="auto created documentation by drf_yasg.",
		contact=openapi.Contact(email="farantgh@gmail.com"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('api.urls')),
	path("v1/auth/", include("auth.urls")),
	path("v1/", include("statistic.urls")),
	path('doc/', schema_view.with_ui(
		'swagger', cache_timeout=0), name='schema_swagger_ui')

]
