from django.apps import AppConfig


class MethodsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.methods"
    label = "methods"
    verbose_name = "MCDA Methods & Block Catalog"

    def ready(self):
        # Load external + custom methods when Django starts
        try:
            from .services import ensure_methods_loaded

            ensure_methods_loaded()
        except Exception:
            # Avoid crashing startup if optional scientific deps are missing
            pass
