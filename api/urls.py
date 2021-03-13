from django.urls import path, include
from .views import QuoteView, MainPage, SpecificShowQuotes, CreateQuote, EditQuote
from rest_framework import permissions, routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('quote', EditQuote)
urlpatterns = [
	path('', MainPage.as_view()),
	path('v1/', QuoteView.as_view()),
	path('v1/shows/<slug:slug>/', SpecificShowQuotes.as_view()),
	path("v1/quote/add/", CreateQuote.as_view()),
	path("v1/", include(router.urls))
]