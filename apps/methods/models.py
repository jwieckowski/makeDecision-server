"""
Catalog of block types, their ports and allowed connections.
Editable from Django Admin – controls 1:1 vs many relations.
"""
from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models


class BlockType(models.Model):
    """
    Definition of a block category available on the canvas
    (matrix, weights, mcda, sensitivity, …).
    """

    class Extension(models.TextChoices):
        CRISP = "crisp", "Crisp"
        FUZZY = "fuzzy", "Fuzzy"
        BOTH = "both", "Both"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.SlugField(
        max_length=64,
        unique=True,
        help_text="Stable code used in schema, e.g. 'matrix', 'mcda', 'sensitivity'",
    )
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default="")
    extension = models.CharField(
        max_length=16,
        choices=Extension.choices,
        default=Extension.BOTH,
    )
    # Optional default method name (e.g. TOPSIS for mcda blocks)
    default_method = models.CharField(max_length=64, blank=True, default="")
    color = models.CharField(max_length=32, blank=True, default="#607D8B")
    icon = models.CharField(max_length=64, blank=True, default="")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Block Type"
        verbose_name_plural = "Block Types"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class PortDefinition(models.Model):
    """
    Port belonging to a BlockType.
    Controls whether the port accepts one or many connections.
    """

    class Direction(models.TextChoices):
        INPUT = "input", "Input"
        OUTPUT = "output", "Output"

    class DataType(models.TextChoices):
        MATRIX = "matrix", "Matrix"
        CRITERIA_TYPES = "criteria_types", "Criteria types"
        WEIGHTS = "weights", "Weights"
        PREFERENCE = "preference", "Preference"
        RANKING = "ranking", "Ranking"
        RANKING_SET = "ranking_set", "Ranking set"
        CORRELATION = "correlation_matrix", "Correlation matrix"
        SENSITIVITY = "sensitivity", "Sensitivity results"
        MCDA_CONFIG = "mcda_config", "MCDA config"
        REFERENCE_POINTS = "reference_points", "Reference points"
        ANY = "any", "Any"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    block_type = models.ForeignKey(
        BlockType,
        on_delete=models.CASCADE,
        related_name="ports",
    )
    code = models.SlugField(
        max_length=64,
        help_text="Port code used in schema edges, e.g. 'in-matrix', 'out-preference'",
    )
    name = models.CharField(max_length=64, help_text="Internal name, e.g. 'matrix'")
    label = models.CharField(max_length=128, blank=True, default="")
    direction = models.CharField(max_length=8, choices=Direction.choices)
    data_type = models.CharField(max_length=32, choices=DataType.choices)

    required = models.BooleanField(
        default=False,
        help_text="Must be connected before calculation can run",
    )
    multiple = models.BooleanField(
        default=False,
        help_text="If False → 1:1 relation. If True → many connections allowed",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["block_type", "direction", "order", "name"]
        unique_together = [("block_type", "code")]
        verbose_name = "Port Definition"
        verbose_name_plural = "Port Definitions"

    def __str__(self) -> str:
        mult = "many" if self.multiple else "1:1"
        return f"{self.block_type.code}.{self.code} [{self.direction}, {mult}]"


class AllowedConnection(models.Model):
    """
    Explicit rule: which output port may connect to which input port.
    Managed from Admin – overrides/extends default data_type matching.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_port = models.ForeignKey(
        PortDefinition,
        on_delete=models.CASCADE,
        related_name="outgoing_rules",
        limit_choices_to={"direction": PortDefinition.Direction.OUTPUT},
    )
    target_port = models.ForeignKey(
        PortDefinition,
        on_delete=models.CASCADE,
        related_name="incoming_rules",
        limit_choices_to={"direction": PortDefinition.Direction.INPUT},
    )
    # Optional: require same extension
    require_same_extension = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        unique_together = [("source_port", "target_port")]
        verbose_name = "Allowed Connection"
        verbose_name_plural = "Allowed Connections"

    def __str__(self) -> str:
        return (
            f"{self.source_port.block_type.code}.{self.source_port.code} "
            f"→ {self.target_port.block_type.code}.{self.target_port.code}"
        )

    def clean(self):
        super().clean()
        if self.source_port_id and self.source_port.direction != PortDefinition.Direction.OUTPUT:
            raise ValidationError({"source_port": "Source must be an output port."})
        if self.target_port_id and self.target_port.direction != PortDefinition.Direction.INPUT:
            raise ValidationError({"target_port": "Target must be an input port."})
