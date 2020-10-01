from django.contrib import admin

from .models import File, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "pk", "image")
    search_fields = ("name", "pk")
    autocomplete_fields = ("creator",)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "pk", "file")
    search_fields = ("name", "pk")
    autocomplete_fields = ("creator",)
