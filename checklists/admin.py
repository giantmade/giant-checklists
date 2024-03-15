from django.contrib import admin

from .models import Category


@admin.register(Category)
class ChecklistCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
