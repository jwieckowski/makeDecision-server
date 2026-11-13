from django.contrib import admin

from .models import CalculationRun


@admin.register(CalculationRun)
class CalculationRunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "decision_model",
        "owner",
        "status",
        "created_at",
        "started_at",
        "finished_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("id", "celery_task_id", "error_message")
    readonly_fields = (
        "id",
        "result",
        "error_message",
        "celery_task_id",
        "started_at",
        "finished_at",
        "created_at",
    )
    raw_id_fields = ("decision_model", "owner")
