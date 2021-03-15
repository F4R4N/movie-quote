from django.urls import path
from .views import LogoutView, UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
app_name = "auth"
urlpatterns = [
	path('login/', UserLoginView.as_view(), name='auth_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]
