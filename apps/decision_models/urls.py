from django.urls import path

from .views import (
    CanConnectView,
    DecisionModelDetailView,
    DecisionModelListCreateView,
    DecisionModelRunValidationView,
    DecisionModelValidateView,
)

urlpatterns = [
    path("", DecisionModelListCreateView.as_view(), name="decision-model-list-create"),
    path("validate/", DecisionModelValidateView.as_view(), name="decision-model-validate"),
    path("can-connect/", CanConnectView.as_view(), name="decision-model-can-connect"),
    path("<uuid:id>/", DecisionModelDetailView.as_view(), name="decision-model-detail"),
    path("<uuid:id>/validate/", DecisionModelRunValidationView.as_view(), name="decision-model-run-validation"),
]
