from django.urls import path
from .views import VisitsYearView, VisitsMonthView, VisitorsView

app_name = "statistic"

urlpatterns = [
	path("admin/statistic/visits/<int:year>/", VisitsYearView.as_view()),
	path("admin/statistic/visits/<int:year>/<int:month>/", VisitsMonthView.as_view()),
	path("admin/statistic/visitors/<int:year>/<int:month>/<int:day>/", VisitorsView.as_view()),
]