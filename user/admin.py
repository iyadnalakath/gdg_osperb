from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class UserAdmin(UserAdmin):
    list_display = (
        "pk",
        "username",
        "country",
        "date_joined",
        "last_login",
        "email",
        "is_admin",
        "is_active",
        "raw_password",
        "role",
    )
    search_fields = (
        "pk",
        "username",
    )
    readonly_fields = ("pk", "date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)

