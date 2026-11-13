"""
Place for first-party / custom method implementations.
Example: a simple custom ranking helper and a placeholder sensitivity method.
"""
from __future__ import annotations

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


@MethodRegistry.register(
    "RANK_DESC",
    Extension.CRISP,
    category=MethodCategory.RANKING,
    source_package="custom",
    label="Rank (descending)",
    description="Convert preference vector to ranking (1 = best).",
)
class RankDescending(BaseMethod):
    meta = MethodMeta(
        name="RANK_DESC",
        category=MethodCategory.RANKING,
        extension=Extension.CRISP,
        source_package="custom",
        label="Rank (descending)",
    )

    def validate_input(self, data: MethodInput) -> None:
        if data.extras.get("preference") is None and data.matrix is None:
            # preference can come via extras or we accept precomputed preference in params
            pref = (data.params or {}).get("preference")
            if pref is None:
                raise ValueError("RANK_DESC requires preference vector")

    def _compute(self, data: MethodInput) -> MethodResult:
        pref = data.extras.get("preference") or (data.params or {}).get("preference")
        pref = np.asarray(pref, dtype=float).ravel()
        ranking = (np.argsort(-pref) + 1).tolist()
        return MethodResult(success=True, ranking=ranking, preference=pref.tolist())


@MethodRegistry.register(
    "WEIGHTS_PERTURBATION",
    Extension.CRISP,
    category=MethodCategory.SENSITIVITY,
    source_package="custom",
    label="Weights perturbation",
    description="One-at-a-time relative perturbation of weights.",
    params_schema={
        "range": {"type": "float", "default": 0.1, "min": 0.01, "max": 0.5},
        "steps": {"type": "int", "default": 10, "min": 2, "max": 100},
    },
)
class WeightsPerturbation(BaseMethod):
    """
    Simple OAT sensitivity on weights.
    Expects in extras:
      - mcda_method: name of registered MCDA method
      - mcda_extension: crisp/fuzzy
    """

    meta = MethodMeta(
        name="WEIGHTS_PERTURBATION",
        category=MethodCategory.SENSITIVITY,
        extension=Extension.CRISP,
        source_package="custom",
        label="Weights perturbation",
        params_schema={
            "range": {"type": "float", "default": 0.1},
            "steps": {"type": "int", "default": 10},
        },
    )

    def _compute(self, data: MethodInput) -> MethodResult:
        from .registry import MethodRegistry

        matrix = np.asarray(data.matrix, dtype=float)
        base_weights = np.asarray(data.weights, dtype=float).ravel()
        types = np.asarray(data.criteria_types, dtype=int) if data.criteria_types else None

        rng = float(data.params.get("range", 0.1))
        steps = int(data.params.get("steps", 10))
        method_name = data.extras.get("mcda_method", "TOPSIS")
        method_ext = data.extras.get("mcda_extension", "crisp")

        mcda = MethodRegistry.get(method_name, method_ext)
        n_crit = len(base_weights)
        results = []

        for c in range(n_crit):
            series = []
            for s in range(steps + 1):
                factor = 1.0 - rng + (2 * rng * s / steps)
                w = base_weights.copy()
                w[c] *= factor
                w = w / w.sum()
                out = mcda.calculate(
                    MethodInput(
                        matrix=matrix,
                        weights=w,
                        criteria_types=types.tolist() if types is not None else None,
                    )
                )
                series.append(
                    {
                        "factor": factor,
                        "weights": w.tolist(),
                        "preference": out.preference,
                        "ranking": out.ranking,
                    }
                )
            results.append({"criterion": c, "series": series})

        return MethodResult(
            success=True,
            sensitivity={"type": "weights_perturbation", "criteria": results},
        )
