"""
URL configuration for MakeDecision project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", include("apps.common.urls")),
    path("api/models/", include("apps.decision_models.urls")),
    path("api/methods/", include("apps.methods.urls")),
    path("api/calculations/", include("apps.calculations.urls")),
    # Future:
    # path("api/auth/", include("apps.users.urls")),
    # path("api/datasets/", include("apps.datasets.urls")),
]
