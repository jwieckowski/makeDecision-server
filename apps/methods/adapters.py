"""
Adapters that wrap external libraries (pymcdm, pyfdm, …) into BaseMethod.
Pattern: Adapter.
"""
from __future__ import annotations

from typing import Any, Callable

import numpy as np

from .base import (
    BaseMethod,
    Extension,
    MethodCategory,
    MethodInput,
    MethodMeta,
    MethodResult,
)
from .registry import MethodRegistry


def _to_numpy(data: Any):
    if data is None:
        return None
    if isinstance(data, np.ndarray):
        return data
    return np.asarray(data, dtype=float)


class CallableAdapter(BaseMethod):
    """
    Generic adapter: wraps a plain callable
    (matrix, weights, types, **params) → preference / weights / …
    """

    def __init__(
        self,
        func: Callable,
        meta: MethodMeta,
        *,
        result_key: str = "preference",
        **default_params,
    ):
        super().__init__(**default_params)
        self._func = func
        self.meta = meta
        self._result_key = result_key

    def _compute(self, data: MethodInput) -> MethodResult:
        matrix = _to_numpy(data.matrix)
        weights = _to_numpy(data.weights)
        types = _to_numpy(data.criteria_types) if data.criteria_types is not None else None

        # Build kwargs expected by most pymcdm/pyfdm signatures
        kwargs = dict(data.params or {})

        # Common calling conventions
        try:
            if self.meta.category == MethodCategory.WEIGHTS:
                # weights methods: usually (matrix) or (matrix, types)
                if types is not None:
                    try:
                        raw = self._func(matrix, types, **kwargs)
                    except TypeError:
                        raw = self._func(matrix, **kwargs)
                else:
                    raw = self._func(matrix, **kwargs)
                values = np.asarray(raw, dtype=float).tolist()
                return MethodResult(success=True, weights=values)

            # MCDA methods
            # Many libraries use: method(matrix, weights, types) or object.__call__
            if callable(self._func) and not isinstance(self._func, type):
                raw = self._func(matrix, weights, types, **kwargs)
            else:
                # Class-based (pymcdm style): instance = Cls(**params); instance(matrix, weights, types)
                instance = self._func(**kwargs)
                raw = instance(matrix, weights, types)

            preference = np.asarray(raw, dtype=float).ravel().tolist()
            ranking = (
                (np.argsort(-np.asarray(preference)) + 1).tolist()
                if preference
                else None
            )
            return MethodResult(
                success=True,
                preference=preference,
                ranking=ranking,
            )
        except Exception as exc:
            return MethodResult(success=False, error=str(exc))


def register_callable(
    name: str,
    extension: Extension,
    func: Callable,
    *,
    category: MethodCategory = MethodCategory.MCDA,
    source_package: str = "",
    label: str = "",
    description: str = "",
    params_schema: dict | None = None,
    result_key: str = "preference",
    tags: list[str] | None = None,
    **default_params,
) -> None:
    """
    Helper to quickly register an external callable as a method.
    """
    meta = MethodMeta(
        name=name.upper(),
        category=category,
        extension=extension,
        label=label or name.upper(),
        description=description,
        source_package=source_package,
        params_schema=params_schema or {},
        tags=tags or [],
    )
    adapter = CallableAdapter(
        func=func,
        meta=meta,
        result_key=result_key,
        **default_params,
    )
    MethodRegistry.register_instance(adapter)
