from django.contrib import admin

from .models import Category, Checklist


@admin.register(Category)
class ChecklistCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = [
        "template",
        "title",
        "created_on",
        "completed",
        "archived",
        "author",
        "category",
    ]
