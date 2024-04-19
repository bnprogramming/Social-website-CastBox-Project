from django.contrib import admin

from home_module.models import Country
from utils.admin_class import ClassBaseAdmin


# Register your models here.
@admin.register(Country)
class CountryAdmin(ClassBaseAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'nickname', 'slug', 'query', 'is_active']
    list_display_links = ['id', 'name', 'nickname', 'slug']
    list_filter = ['is_active']
    search_fields = ['name', 'nickname']
