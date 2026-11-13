"""
Base abstractions for MCDA methods.
Design patterns: Strategy + Template Method + Adapter.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Extension(str, Enum):
    CRISP = "crisp"
    FUZZY = "fuzzy"
    INTUITIONISTIC = "intuitionistic"
    INTERVAL = "interval"


class MethodCategory(str, Enum):
    WEIGHTS = "weights"
    MCDA = "mcda"
    RANKING = "ranking"
    CORRELATION = "correlation"
    SENSITIVITY = "sensitivity"
    NORMALIZATION = "normalization"
    DISTANCE = "distance"
    DEFUZZIFICATION = "defuzzification"
    VISUALIZATION = "visualization"


@dataclass
class MethodMeta:
    """Static description of a method – used by registry and API."""

    name: str
    category: MethodCategory
    extension: Extension
    label: str = ""
    description: str = ""
    source_package: str = ""  # e.g. "pymcdm", "pyfdm", "custom"
    version: str = ""
    params_schema: dict[str, Any] = field(default_factory=dict)
    # Example:
    # {
    #   "normalization_function": {
    #       "type": "select", "default": "minmax",
    #       "options": ["minmax", "sum", "vector", "max"]
    #   },
    #   "lambda": {"type": "float", "default": 0.5, "min": 0, "max": 1}
    # }
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.label:
            self.label = self.name


@dataclass
class MethodInput:
    """Standardised input passed to every method."""

    matrix: Any = None  # 2D crisp or 3D fuzzy
    criteria_types: list[int] | None = None  # 1 = profit, -1 = cost
    weights: Any = None
    params: dict[str, Any] = field(default_factory=dict)
    # Extra context (e.g. other rankings for correlation)
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class MethodResult:
    """Standardised output from every method."""

    success: bool = True
    preference: list[float] | None = None
    ranking: list[int] | None = None
    weights: list[float] | None = None
    correlation: list[list[float]] | None = None
    sensitivity: dict[str, Any] | None = None
    extras: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    meta: dict[str, Any] = field(default_factory=dict)


class BaseMethod(ABC):
    """
    Abstract Strategy for a single MCDA (or related) method.
    Subclasses implement `_compute`. The public `calculate` adds
    validation and error handling (Template Method).
    """

    meta: MethodMeta

    def __init__(self, **default_params: Any):
        self.default_params = default_params

    def calculate(self, data: MethodInput) -> MethodResult:
        """Template method – do not override unless necessary."""
        try:
            self.validate_input(data)
            params = {**self.default_params, **(data.params or {})}
            data.params = params
            return self._compute(data)
        except Exception as exc:
            return MethodResult(success=False, error=str(exc))

    def validate_input(self, data: MethodInput) -> None:
        """Override to add method-specific checks."""
        if self.meta.category in {MethodCategory.MCDA, MethodCategory.WEIGHTS}:
            if data.matrix is None:
                raise ValueError(f"{self.meta.name}: matrix is required")

    @abstractmethod
    def _compute(self, data: MethodInput) -> MethodResult:
        """Actual computation – must be implemented by subclasses."""
        ...

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"name={self.meta.name} ext={self.meta.extension.value} "
            f"src={self.meta.source_package}>"
        )
