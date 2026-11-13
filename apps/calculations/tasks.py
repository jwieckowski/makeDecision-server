"""
Celery tasks for asynchronous calculation runs.
"""
from __future__ import annotations

import logging

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, name="calculations.run_calculation")
def run_calculation_task(self, calculation_run_id: str) -> dict:
    from .engine import run_decision_model
    from .models import CalculationRun

    try:
        run = CalculationRun.objects.get(id=calculation_run_id)
    except CalculationRun.DoesNotExist:
        logger.error("CalculationRun %s not found", calculation_run_id)
        return {"success": False, "error": "Run not found"}

    run.status = CalculationRun.Status.RUNNING
    run.started_at = timezone.now()
    run.celery_task_id = self.request.id or ""
    run.save(update_fields=["status", "started_at", "celery_task_id"])

    try:
        schema = run.input_schema
        if not schema and run.decision_model_id:
            schema = run.decision_model.schema

        result = run_decision_model(schema or {})

        run.result = result
        run.status = (
            CalculationRun.Status.SUCCESS
            if result.get("success")
            else CalculationRun.Status.FAILED
        )
        if not result.get("success"):
            run.error_message = result.get("error") or "Calculation failed"
        run.finished_at = timezone.now()
        run.save(
            update_fields=["result", "status", "error_message", "finished_at"]
        )
        return result
    except Exception as exc:
        logger.exception("Calculation run %s failed", calculation_run_id)
        run.status = CalculationRun.Status.FAILED
        run.error_message = str(exc)
        run.finished_at = timezone.now()
        run.result = {"success": False, "error": str(exc), "nodes": [], "order": []}
        run.save(
            update_fields=["status", "error_message", "finished_at", "result"]
        )
        return {"success": False, "error": str(exc)}
