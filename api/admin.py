from django.contrib import admin
from .models import Quote, Role, Show


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
	list_display = ('key', "contain_adult_lang", 'quote', 'show', 'role', "id", )
	list_editable_link = ("quote", )
	list_editable = ("contain_adult_lang", )


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
	list_display = ("name", "slug", "id")
	prepopulated_fields = {"slug": ("name", )}


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', "id")
	prepopulated_fields = {"slug": ("name", )}
