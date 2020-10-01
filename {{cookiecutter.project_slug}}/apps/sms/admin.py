from django.contrib import admin

from .models import Sms


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ("created_date", "phone", "sms")
    search_fields = ("phone", "sms")
