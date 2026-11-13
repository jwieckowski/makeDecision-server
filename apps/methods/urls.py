from django.urls import path

from .views import MethodListView, MethodRunView

urlpatterns = [
    path("", MethodListView.as_view(), name="method-list"),
    path("run/", MethodRunView.as_view(), name="method-run"),
]
