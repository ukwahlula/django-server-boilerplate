from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        (_("Profile info"), {"fields": ("first_name", "last_name", "avatar", "birthday",)},),
        (_("Important dates"), {"fields": ("created_date", "updated_date", "last_login")}),
        (
            _("Admin Django Access and Permissions"),
            {"fields": ("is_superuser", "is_staff", "is_active", "is_2fa_enabled", "groups", "user_permissions")},
        ),
        (
            _("Access codes"),
            {
                "fields": (
                    "email_verification_code",
                    "is_email_verified",
                    "phone_verification_code",
                    "is_phone_verified",
                    "reset_password_code",
                )
            },
        ),
    )
    add_fieldsets = (
        (_("Profile"), {"fields": ("email", "first_name", "last_name", "phone", "birthday",)}),
        (_("Passwords"), {"fields": ("password1", "password2")}),
    )
    list_display = ("email", "phone", "is_active", "is_superuser", "is_staff")
    list_filter = ("is_active", "is_superuser", "is_email_verified", "is_phone_verified")
    search_fields = ("email", "phone", "pk")
    readonly_fields = ("created_date", "updated_date")
