from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.decision_models.models import DecisionModel

from .engine import run_decision_model
from .models import CalculationRun
from .serializers import CalculationRunCreateSerializer, CalculationRunSerializer
from .tasks import run_calculation_task


class CalculationRunListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/calculations/     – list own runs
    POST /api/calculations/     – start a new run
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CalculationRunCreateSerializer
        return CalculationRunSerializer

    def get_queryset(self):
        return CalculationRun.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        ser = CalculationRunCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        decision_model = None
        schema = data.get("schema")

        if data.get("decision_model_id"):
            try:
                decision_model = DecisionModel.objects.get(id=data["decision_model_id"])
            except DecisionModel.DoesNotExist:
                return Response(
                    {"detail": "Decision model not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if decision_model.owner != request.user and not decision_model.is_public:
                return Response(
                    {"detail": "Permission denied."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if not schema:
                schema = decision_model.schema

        run = CalculationRun.objects.create(
            decision_model=decision_model,
            owner=request.user,
            input_schema=schema or {},
            status=CalculationRun.Status.PENDING,
        )

        async_mode = data.get("async_mode", True)

        if async_mode:
            task = run_calculation_task.delay(str(run.id))
            run.celery_task_id = task.id
            run.save(update_fields=["celery_task_id"])
            return Response(
                CalculationRunSerializer(run).data,
                status=status.HTTP_202_ACCEPTED,
            )

        # Synchronous path
        result = run_decision_model(schema or {})
        run.result = result
        run.status = (
            CalculationRun.Status.SUCCESS
            if result.get("success")
            else CalculationRun.Status.FAILED
        )
        if not result.get("success"):
            run.error_message = result.get("error") or "Calculation failed"
        from django.utils import timezone

        run.started_at = timezone.now()
        run.finished_at = timezone.now()
        run.save()

        return Response(
            CalculationRunSerializer(run).data,
            status=status.HTTP_200_OK,
        )


class CalculationRunDetailView(generics.RetrieveAPIView):
    """GET /api/calculations/{id}/"""

    serializer_class = CalculationRunSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return CalculationRun.objects.filter(
            Q(owner=self.request.user) | Q(decision_model__is_public=True)
        )


class CalculationRunSyncView(APIView):
    """
    POST /api/calculations/sync/
    Run calculation immediately from inline schema (no DB run record required).
    Useful for interactive frontend previews.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        schema = request.data.get("schema")
        if not schema:
            return Response(
                {"detail": "schema is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = run_decision_model(schema)
        http_status = (
            status.HTTP_200_OK if result.get("success") else status.HTTP_400_BAD_REQUEST
        )
        return Response(result, status=http_status)
