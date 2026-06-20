from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    path("v1/auth/", include("auth.urls")),
    path("v1/", include("statistic.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path("docs/", include("swagger_urls")),
]
