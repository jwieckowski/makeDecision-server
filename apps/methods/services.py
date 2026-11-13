"""
High-level service API used by views / calculation engine.
"""
from __future__ import annotations

from .base import Extension, MethodCategory, MethodInput, MethodResult
from .loaders import load_all
from .registry import MethodRegistry, get_method

_loaded = False


def ensure_methods_loaded() -> dict[str, int]:
    """Idempotent load of all external + custom methods."""
    global _loaded
    if _loaded:
        return {}
    # Custom methods are registered via import side-effects
    from . import custom  # noqa: F401

    counts = load_all()
    _loaded = True
    return counts


def list_available_methods(
    category: str | None = None,
    extension: str | None = None,
    source_package: str | None = None,
) -> list[dict]:
    ensure_methods_loaded()
    cat = MethodCategory(category) if category else None
    ext = Extension(extension) if extension else None
    metas = MethodRegistry.list_methods(
        category=cat, extension=ext, source_package=source_package
    )
    return [
        {
            "name": m.name,
            "label": m.label,
            "category": m.category.value,
            "extension": m.extension.value,
            "source_package": m.source_package,
            "description": m.description,
            "params_schema": m.params_schema,
            "tags": m.tags,
        }
        for m in metas
    ]


def run_method(
    name: str,
    extension: str = "crisp",
    *,
    matrix=None,
    criteria_types=None,
    weights=None,
    params: dict | None = None,
    extras: dict | None = None,
) -> MethodResult:
    """
    Convenience entry point for the calculation engine.
    """
    ensure_methods_loaded()
    method = get_method(name, extension)
    data = MethodInput(
        matrix=matrix,
        criteria_types=criteria_types,
        weights=weights,
        params=params or {},
        extras=extras or {},
    )
    return method.calculate(data)
