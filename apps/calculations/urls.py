from django.urls import path

from .views import (
    CalculationRunDetailView,
    CalculationRunListCreateView,
    CalculationRunSyncView,
)

urlpatterns = [
    path("", CalculationRunListCreateView.as_view(), name="calculation-run-list-create"),
    path("sync/", CalculationRunSyncView.as_view(), name="calculation-run-sync"),
    path("<uuid:id>/", CalculationRunDetailView.as_view(), name="calculation-run-detail"),
]
