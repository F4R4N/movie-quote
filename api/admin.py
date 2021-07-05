from django.contrib import admin
from .models import Quote, Role, Show


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
	list_display = ('key', 'quote', 'show', 'role', "id", "contain_adult_lang", )
	list_editable_link = ("quote", "contain_adult_lang", )


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
	list_display = ("name", "slug", "id")
	prepopulated_fields = {"slug": ("name", )}


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', "id")
	prepopulated_fields = {"slug": ("name", )}
