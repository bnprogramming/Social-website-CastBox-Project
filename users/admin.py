from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "username", "email", "phone", "is_superuser", "is_staff", "is_active", "date_joined"]
    list_display_links = ["id", "first_name", "last_name", "username"]
    list_filter = ["is_superuser", "is_staff", "is_active"]
    search_fields = ["first_name", "last_name", "username", "email", "phone"]
