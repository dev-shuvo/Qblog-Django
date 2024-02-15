from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "username",
        "user_type",
        "joined_at",
        "modified_at",
    )
    list_display_links = (
        "full_name",
        "email",
    )
    list_filter = ("user_type",)

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "username",
        "user_type",
    )
    readonly_fields = ("password",)


admin.site.register(User, UserAdmin)
