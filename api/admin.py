from django.contrib import admin
from .models import Quote, Role, Show

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
	list_display = ('key', 'quote', 'show', 'role')
admin.site.register(Show)
admin.site.register(Role)


