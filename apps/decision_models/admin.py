from django.contrib import admin

from .models import DecisionModel


@admin.register(DecisionModel)
class DecisionModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "schema_version",
        "is_public",
        "is_valid",
        "updated_at",
        "created_at",
    )
    list_filter = ("is_public", "is_valid", "schema_version", "created_at")
    search_fields = ("name", "description", "notes", "id")
    readonly_fields = ("id", "is_valid", "validation_errors", "created_at", "updated_at")
    raw_id_fields = ("owner",)
    ordering = ("-updated_at",)

    fieldsets = (
        (None, {"fields": ("id", "name", "description", "notes", "owner")}),
        ("Schema", {"fields": ("schema", "schema_version")}),
        ("Status", {"fields": ("is_public", "is_valid", "validation_errors", "tags")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
