"""
Method Registry + Factory.
Patterns: Registry, Factory Method, Singleton (module-level).
"""
from __future__ import annotations

from typing import Iterable, Type

from .base import BaseMethod, Extension, MethodCategory, MethodMeta


class MethodRegistry:
    """
    Central registry of all available methods.
    Key: (name_upper, extension_value) → method class or factory callable.
    """

    _registry: dict[tuple[str, str], Type[BaseMethod]] = {}
    _instances: dict[tuple[str, str], BaseMethod] = {}

    @classmethod
    def register(
        cls,
        name: str,
        extension: Extension | str,
        *,
        category: MethodCategory | None = None,
        label: str = "",
        description: str = "",
        source_package: str = "",
        params_schema: dict | None = None,
        tags: list[str] | None = None,
    ):
        """
        Decorator to register a BaseMethod subclass.

        Usage:
            @MethodRegistry.register("TOPSIS", Extension.CRISP, source_package="pymcdm")
            class TopsisCrisp(BaseMethod):
                ...
        """
        ext = extension.value if isinstance(extension, Extension) else extension

        def decorator(method_cls: Type[BaseMethod]) -> Type[BaseMethod]:
            # Attach / enrich meta if not already set on the class
            if not hasattr(method_cls, "meta") or method_cls.meta is None:
                method_cls.meta = MethodMeta(
                    name=name.upper(),
                    category=category or MethodCategory.MCDA,
                    extension=Extension(ext),
                    label=label or name.upper(),
                    description=description,
                    source_package=source_package,
                    params_schema=params_schema or {},
                    tags=tags or [],
                )
            else:
                # Ensure name/extension match
                method_cls.meta.name = name.upper()
                method_cls.meta.extension = Extension(ext)

            key = (name.upper(), ext)
            cls._registry[key] = method_cls
            # Invalidate cached instance
            cls._instances.pop(key, None)
            return method_cls

        return decorator

    @classmethod
    def register_instance(cls, method: BaseMethod) -> None:
        """Register an already constructed instance (useful for adapters)."""
        key = (method.meta.name.upper(), method.meta.extension.value)
        cls._registry[key] = type(method)  # type only for consistency
        cls._instances[key] = method

    @classmethod
    def get(
        cls,
        name: str,
        extension: Extension | str = Extension.CRISP,
        **params,
    ) -> BaseMethod:
        """
        Factory method – returns a ready-to-use method instance.
        """
        ext = extension.value if isinstance(extension, Extension) else extension
        key = (name.upper(), ext)

        if key in cls._instances and not params:
            return cls._instances[key]

        if key not in cls._registry:
            available = [f"{n}/{e}" for n, e in sorted(cls._registry.keys())]
            raise KeyError(
                f"Method '{name}' ({ext}) is not registered. "
                f"Available: {available}"
            )

        method_cls = cls._registry[key]
        instance = method_cls(**params)
        if not params:
            cls._instances[key] = instance
        return instance

    @classmethod
    def exists(cls, name: str, extension: Extension | str = Extension.CRISP) -> bool:
        ext = extension.value if isinstance(extension, Extension) else extension
        return (name.upper(), ext) in cls._registry

    @classmethod
    def list_methods(
        cls,
        category: MethodCategory | None = None,
        extension: Extension | str | None = None,
        source_package: str | None = None,
    ) -> list[MethodMeta]:
        """Return metadata of registered methods, optionally filtered."""
        results: list[MethodMeta] = []
        ext_filter = (
            extension.value if isinstance(extension, Extension) else extension
        )

        for (name, ext), method_cls in cls._registry.items():
            meta: MethodMeta = getattr(method_cls, "meta", None)
            if meta is None and (name, ext) in cls._instances:
                meta = cls._instances[(name, ext)].meta
            if meta is None:
                continue
            if category and meta.category != category:
                continue
            if ext_filter and meta.extension.value != ext_filter:
                continue
            if source_package and meta.source_package != source_package:
                continue
            results.append(meta)

        return sorted(results, key=lambda m: (m.category.value, m.name))

    @classmethod
    def list_names(cls) -> list[str]:
        return sorted({name for name, _ in cls._registry.keys()})

    @classmethod
    def clear(cls) -> None:
        """Mostly for tests."""
        cls._registry.clear()
        cls._instances.clear()


def get_method(name: str, extension: str | Extension = "crisp", **params) -> BaseMethod:
    """Shortcut factory function."""
    return MethodRegistry.get(name, extension, **params)
