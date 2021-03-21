from django.urls import path, include
from .views import (MainPage, SpecificShowQuotes, 
	AdminQuoteView, AdminDeleteUserView, AdminEditQuoteView, 
	AdminUserView, AdminEditUserView, UserQuoteView, 
	AdminEditShowView, AdminEditRoleView, AdminAllShowsView, AdminAllRolesView)


app_name = 'api'
urlpatterns = [
	path('', MainPage.as_view()),
	path("v1/quote/", UserQuoteView.as_view()),
	path('v1/shows/<slug:slug>/', SpecificShowQuotes.as_view()),

	path("v1/admin/quote/", AdminQuoteView.as_view()),
	path("v1/admin/quote/<str:key>/", AdminEditQuoteView.as_view()),

	path("v1/admin/show/edit/<slug:slug>/", AdminEditShowView.as_view()),
	path("v1/admin/shows/", AdminAllShowsView.as_view()),

	path("v1/admin/role/edit/<slug:slug>/", AdminEditRoleView.as_view()),
	path("v1/admin/roles/", AdminAllRolesView.as_view()),

	path("v1/admin/user/", AdminUserView.as_view()),
	path("v1/admin/user/edit/<int:pk>/", AdminEditUserView.as_view()),
	path("v1/admin/user/delete/<int:pk>/", AdminDeleteUserView.as_view()),

]