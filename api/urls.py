from django.urls import path, re_path
from .views import (
	MainPage, SpecificShowQuotes, AdminQuoteView, AdminDeleteUserView,
	AdminEditAndDeleteQuoteView, AdminUserView, AdminEditUserView, UserQuoteView,
	AdminEditShowView, AdminEditRoleView, AllShowsView, AdminAllRolesView, )

app_name = 'api'

urlpatterns = [
	path('', MainPage.as_view(), name="main_page"),
	path("v1/quote/", UserQuoteView.as_view(), name="random_quote"),
	re_path(
		r"^v1/quote/(?P<censored>)/$", UserQuoteView.as_view(),
		name="random_censored_quote"),

	path(
		'v1/shows/<slug:slug>/', SpecificShowQuotes.as_view(), name="show_quote"),
	path('v1/shows/', AllShowsView.as_view(), name="all_shows"),

	path(
		"v1/admin/quote/", AdminQuoteView.as_view(), name="admin_create_list_quote"),
	path(
		"v1/admin/quote/<str:key>/",
		AdminEditAndDeleteQuoteView.as_view(), name="admin_edit_delete_quote"),

	path(
		"v1/admin/show/edit/<slug:slug>/",
		AdminEditShowView.as_view(), name="admin_edit_show"),
	path("v1/admin/shows/", AllShowsView.as_view(), name="admin_all_shows"),

	path(
		"v1/admin/role/edit/<slug:slug>/",
		AdminEditRoleView.as_view(), name="admin_edit_role"),
	path("v1/admin/roles/", AdminAllRolesView.as_view(), name="admin_all_roles"),

	path(
		"v1/admin/user/", AdminUserView.as_view(), name="admin_create_list_user"),
	path(
		"v1/admin/user/edit/<int:pk>/",
		AdminEditUserView.as_view(), name="admin_edit_user"),
	path(
		"v1/admin/user/delete/<int:pk>/",
		AdminDeleteUserView.as_view(), name="admin_delete_user"),

]
