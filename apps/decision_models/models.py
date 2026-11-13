"""
Django models for Decision Models.
"""
from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .connection_rules import validate_connections
from .schemas import DecisionModelSchema


class DecisionModel(models.Model):
    """
    Stored decision model built from blocks on the frontend.
    The full graph (nodes, edges, annotations, canvas state) is kept
    in the `schema` JSONField and validated with Pydantic + connection rules.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="decision_models",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    notes = models.TextField(blank=True, default="")

    # Full Decision Model Schema (v1.1)
    schema = models.JSONField(default=dict, blank=True)

    schema_version = models.CharField(max_length=10, default="1.1")

    is_public = models.BooleanField(default=False)
    is_valid = models.BooleanField(
        default=False,
        help_text="Result of the last structural / connection validation",
    )
    validation_errors = models.JSONField(
        default=list,
        blank=True,
        help_text="List of validation errors from the last check",
    )

    tags = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["owner", "-updated_at"]),
            models.Index(fields=["is_public", "-updated_at"]),
            models.Index(fields=["schema_version"]),
        ]
        verbose_name = "Decision Model"
        verbose_name_plural = "Decision Models"

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    # ===== Validation helpers =====

    def get_parsed_schema(self) -> DecisionModelSchema:
        """Parse and validate the raw JSON against the Pydantic schema."""
        return DecisionModelSchema.model_validate(self.schema)

    def validate_schema_structure(self) -> DecisionModelSchema:
        """
        Validate JSON structure (Pydantic).
        Raises pydantic.ValidationError on failure.
        """
        return self.get_parsed_schema()

    def validate_connections(self) -> list[dict]:
        """
        Run connection / graph rules.
        Returns a list of error dicts (empty when valid).
        """
        try:
            parsed = self.get_parsed_schema()
        except Exception as exc:
            return [
                {
                    "code": "SCHEMA_PARSE_ERROR",
                    "message": str(exc),
                }
            ]

        result = validate_connections(parsed)
        return [
            {
                "code": err.code,
                "message": err.message,
                "edge_id": str(err.edge_id) if err.edge_id else None,
                "source_node": str(err.source_node) if err.source_node else None,
                "target_node": str(err.target_node) if err.target_node else None,
                "details": err.details,
            }
            for err in result.errors
        ]

    def run_full_validation(self, *, save: bool = False) -> bool:
        """
        Run both structural (Pydantic) and connection validation.
        Updates is_valid and validation_errors.
        Returns True when the model is fully valid.
        """
        errors: list[dict] = []

        # 1. Structural
        try:
            self.validate_schema_structure()
        except Exception as exc:
            errors.append(
                {
                    "code": "SCHEMA_PARSE_ERROR",
                    "message": str(exc),
                }
            )
            self.is_valid = False
            self.validation_errors = errors
            if save:
                self.save(update_fields=["is_valid", "validation_errors", "updated_at"])
            return False

        # 2. Connections & graph
        conn_errors = self.validate_connections()
        errors.extend(conn_errors)

        self.is_valid = len(errors) == 0
        self.validation_errors = errors

        if save:
            self.save(update_fields=["is_valid", "validation_errors", "updated_at"])

        return self.is_valid

    def clean(self):
        """Called by Django admin / full_clean()."""
        super().clean()
        try:
            self.validate_schema_structure()
        except Exception as exc:
            raise ValidationError({"schema": f"Invalid schema: {exc}"}) from exc

    def save(self, *args, **kwargs):
        # Keep denormalised fields in sync with schema metadata when possible
        if self.schema and isinstance(self.schema, dict):
            meta = self.schema.get("metadata") or {}
            if not self.name and meta.get("name"):
                self.name = meta["name"]
            if meta.get("description") and not self.description:
                self.description = meta["description"]
            if "is_public" in meta:
                self.is_public = bool(meta["is_public"])
            if "tags" in meta and isinstance(meta["tags"], list):
                self.tags = meta["tags"]
            if meta.get("notes") and not self.notes:
                self.notes = meta["notes"]
            self.schema_version = self.schema.get("schema_version", self.schema_version)

        super().save(*args, **kwargs)
