from django.urls import path, include
from .views import MainPage, SpecificShowQuotes, AdminQuoteView, AdminDeleteUserView, AdminEditQuoteView, AdminUserView, AdminEditUserView, UserQuoteView
from rest_framework import permissions, routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('user', AdminUserView)
# router.register("quote", AdminQuoteView)
urlpatterns = [
	path('', MainPage.as_view()),
	# path('v1/', QuoteView.as_view()),
	path('v1/shows/<slug:slug>/', SpecificShowQuotes.as_view()),
	path("v1/quote/", UserQuoteView.as_view()),
	path("v1/admin/quote/", AdminQuoteView.as_view()),
	path("v1/admin/quote/<str:key>/", AdminEditQuoteView.as_view()),
	path("v1/admin/", include(router.urls)),
	path("v1/admin/user/edit/<int:pk>/", AdminEditUserView.as_view()),
	path("v1/admin/user/delete/<int:pk>/", AdminDeleteUserView.as_view()),
]