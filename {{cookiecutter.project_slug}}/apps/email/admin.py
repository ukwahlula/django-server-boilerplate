from django.contrib import admin
from django.utils.translation import ugettext_lazy as _ul

from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("created_date", "sender", "recipients", "subject")
    search_fields = ("sender", "recipients", "subject", "body")
    exclude = ("raw", "body")
    readonly_fields = ("body_html",)
    fieldsets = (
        (_ul("Users"), {"classes": ("collapse", "close"), "fields": ("sender", "recipients",),},),
        (_ul("Body"), {"fields": ("subject", "body_html")}),
    )
