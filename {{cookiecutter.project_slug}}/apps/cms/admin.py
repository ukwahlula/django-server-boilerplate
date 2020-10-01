from django.contrib import admin

from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("content_type", "content")
    search_fields = ("content_type", "content")
