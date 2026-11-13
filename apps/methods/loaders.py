"""
Load methods from external packages into the registry.
Each loader is optional – missing packages are skipped gracefully.
"""
from __future__ import annotations

import logging
from typing import Callable

from .adapters import register_callable
from .base import Extension, MethodCategory

logger = logging.getLogger(__name__)


def _safe_import(module_path: str):
    try:
        parts = module_path.split(".")
        mod = __import__(module_path)
        for part in parts[1:]:
            mod = getattr(mod, part)
        return mod
    except Exception as exc:
        logger.debug("Could not import %s: %s", module_path, exc)
        return None


# ===== pymcdm (crisp) =====

def load_pymcdm() -> int:
    """Register crisp MCDA + weights methods from pymcdm."""
    count = 0

    methods_mod = _safe_import("pymcdm.methods")
    weights_mod = _safe_import("pymcdm.weights")

    if methods_mod is None:
        logger.info("pymcdm not available – skipping crisp MCDA methods")
        return 0

    # Map: registry name → attribute name on pymcdm.methods
    MCDA_MAP = {
        "ARAS": "ARAS",
        "COCOSO": "COCOSO",
        "CODAS": "CODAS",
        "COMET": "COMET",
        "COPRAS": "COPRAS",
        "EDAS": "EDAS",
        "MABAC": "MABAC",
        "MAIRCA": "MAIRCA",
        "MARCOS": "MARCOS",
        "MOORA": "MOORA",
        "OCRA": "OCRA",
        "PROMETHEE": "PROMETHEE_II",
        "SPOTIS": "SPOTIS",
        "TOPSIS": "TOPSIS",
        "VIKOR": "VIKOR",
        "WASPAS": "WASPAS",
        "WPM": "WPM",
        "WSM": "WSM",
        "PROBID": "PROBID",
        "RIM": "RIM",
        "ERVD": "ERVD",
    }

    for name, attr in MCDA_MAP.items():
        cls = getattr(methods_mod, attr, None)
        if cls is None:
            continue
        register_callable(
            name=name,
            extension=Extension.CRISP,
            func=cls,
            category=MethodCategory.MCDA,
            source_package="pymcdm",
            label=name,
        )
        count += 1

    if weights_mod is not None:
        WEIGHTS_MAP = {
            "EQUAL": "equal_weights",
            "ENTROPY": "entropy_weights",
            "CRITIC": "critic_weights",
            "STANDARD_DEVIATION": "standard_deviation_weights",
            "VARIANCE": "variance_weights",
            "GINI": "gini_weights",
            "ANGLE": "angle_weights",
            "CILOS": "cilos_weights",
            "IDOCRIW": "idocriw_weights",
            "MEREC": "merec_weights",
        }
        for name, attr in WEIGHTS_MAP.items():
            func = getattr(weights_mod, attr, None)
            if func is None:
                continue
            register_callable(
                name=name,
                extension=Extension.CRISP,
                func=func,
                category=MethodCategory.WEIGHTS,
                source_package="pymcdm",
                label=name.replace("_", " "),
                result_key="weights",
            )
            count += 1

    logger.info("Loaded %d methods from pymcdm", count)
    return count


# ===== pyfdm (fuzzy / TFN) =====

def load_pyfdm() -> int:
    count = 0
    methods_mod = _safe_import("pyfdm.methods")
    weights_mod = _safe_import("pyfdm.weights")

    if methods_mod is None:
        logger.info("pyfdm not available – skipping fuzzy methods")
        return 0

    FUZZY_MCDA = {
        "ARAS": "fARAS",
        "COCOSO": "fCOCOSO",
        "CODAS": "fCODAS",
        "COPRAS": "fCOPRAS",
        "EDAS": "fEDAS",
        "MABAC": "fMABAC",
        "MAIRCA": "fMAIRCA",
        "MOORA": "fMOORA",
        "OCRA": "fOCRA",
        "SPOTIS": "fSPOTIS",
        "TOPSIS": "fTOPSIS",
        "VIKOR": "fVIKOR",
        "WASPAS": "fWASPAS",
        "WPM": "fWPM",
        "WSM": "fWSM",
    }

    for name, attr in FUZZY_MCDA.items():
        cls = getattr(methods_mod, attr, None)
        if cls is None:
            continue
        register_callable(
            name=name,
            extension=Extension.FUZZY,
            func=cls,
            category=MethodCategory.MCDA,
            source_package="pyfdm",
            label=f"f{name}",
        )
        count += 1

    if weights_mod is not None:
        FUZZY_WEIGHTS = {
            "EQUAL": "equal_weights",
            "ENTROPY": "shannon_entropy_weights",
            "STANDARD_DEVIATION": "standard_deviation_weights",
            "VARIANCE": "variance_weights",
        }
        for name, attr in FUZZY_WEIGHTS.items():
            func = getattr(weights_mod, attr, None)
            if func is None:
                continue
            register_callable(
                name=name,
                extension=Extension.FUZZY,
                func=func,
                category=MethodCategory.WEIGHTS,
                source_package="pyfdm",
                label=name.replace("_", " "),
                result_key="weights",
            )
            count += 1

    logger.info("Loaded %d methods from pyfdm", count)
    return count


# ===== pyifdm (intuitionistic) – optional =====

def load_pyifdm() -> int:
    count = 0
    methods_mod = _safe_import("pyifdm.methods")
    if methods_mod is None:
        logger.debug("pyifdm not available")
        return 0

    # Register whatever public callables we find (best-effort)
    for attr in dir(methods_mod):
        if attr.startswith("_"):
            continue
        obj = getattr(methods_mod, attr)
        if callable(obj):
            name = attr.lstrip("f").lstrip("i").upper()
            try:
                register_callable(
                    name=name,
                    extension=Extension.INTUITIONISTIC,
                    func=obj,
                    category=MethodCategory.MCDA,
                    source_package="pyifdm",
                    label=attr,
                )
                count += 1
            except Exception:
                continue

    logger.info("Loaded %d methods from pyifdm", count)
    return count


# ===== pysensmcda (sensitivity) – optional =====

def load_pysensmcda() -> int:
    """Best-effort registration of sensitivity helpers."""
    count = 0
    mod = _safe_import("pysensmcda")
    if mod is None:
        logger.debug("pysensmcda not available")
        return 0

    # pysensmcda API may evolve – register known entry points if present
    for attr in ("sensitivity_analysis", "weights_sensitivity", "rank_sensitivity"):
        func = getattr(mod, attr, None)
        if func and callable(func):
            register_callable(
                name=attr.upper(),
                extension=Extension.CRISP,
                func=func,
                category=MethodCategory.SENSITIVITY,
                source_package="pysensmcda",
                label=attr.replace("_", " ").title(),
                result_key="sensitivity",
            )
            count += 1

    logger.info("Loaded %d methods from pysensmcda", count)
    return count


def load_all() -> dict[str, int]:
    """Load every known source. Returns counts per package."""
    return {
        "pymcdm": load_pymcdm(),
        "pyfdm": load_pyfdm(),
        "pyifdm": load_pyifdm(),
        "pysensmcda": load_pysensmcda(),
    }
