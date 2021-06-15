from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "description",
        "first_name",
        "last_name",
    )
    search_fields = ("username", "email")
    empty_value_display = "-пусто-"
