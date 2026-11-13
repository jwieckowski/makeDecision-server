"""
Models for calculation runs.
"""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class CalculationRun(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    decision_model = models.ForeignKey(
        "decision_models.DecisionModel",
        on_delete=models.CASCADE,
        related_name="calculation_runs",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calculation_runs",
    )

    # Snapshot of the schema used for this run (so results stay reproducible)
    input_schema = models.JSONField(default=dict, blank=True)

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    result = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True, default="")

    celery_task_id = models.CharField(max_length=255, blank=True, default="")

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]
        verbose_name = "Calculation Run"
        verbose_name_plural = "Calculation Runs"

    def __str__(self) -> str:
        return f"Run {self.id} [{self.status}]"
