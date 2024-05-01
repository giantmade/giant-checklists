from django.contrib import admin

from .models import TemplateType, Template


@admin.register(TemplateType)
class TemplateTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "is_active",
        "type",
    ]
    list_filter = ["type", "is_active"]
    search_fields = ["title", "author"]

