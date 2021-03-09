from django.urls import path
from .views import QuoteView, MainPage
app_name = 'api'

urlpatterns = [
	path('v1/', QuoteView.as_view()),
	path('', MainPage.as_view())
]