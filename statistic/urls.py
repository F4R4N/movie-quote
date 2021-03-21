from django.urls import path
from .views import VisitsYearView, VisitsMonthView

app_name = "statistic"

urlpatterns = [
	path("admin/statistic/visits/<int:year>/", VisitsYearView.as_view()),
	path("admin/statistic/visits/<int:year>/<int:month>/", VisitsMonthView.as_view()),
]