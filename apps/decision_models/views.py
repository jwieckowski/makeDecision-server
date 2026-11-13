"""
API views for Decision Models.
"""
from __future__ import annotations

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .connection_rules import can_connect, validate_connections
from .models import DecisionModel
from .schemas import DecisionModelSchema
from .serializers import (
    CanConnectSerializer,
    DecisionModelListSerializer,
    DecisionModelSerializer,
    DecisionModelValidateSerializer,
)


class DecisionModelListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/models/          – list own + public models
    POST /api/models/          – create new model
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DecisionModelListSerializer
        return DecisionModelSerializer

    def get_queryset(self):
        user = self.request.user
        qs = DecisionModel.objects.all()
        if user.is_authenticated:
            return qs.filter(Q(owner=user) | Q(is_public=True))
        return qs.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DecisionModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/models/{id}/
    PUT    /api/models/{id}/
    PATCH  /api/models/{id}/
    DELETE /api/models/{id}/
    """

    serializer_class = DecisionModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        qs = DecisionModel.objects.all()
        if user.is_authenticated:
            return qs.filter(Q(owner=user) | Q(is_public=True))
        return qs.filter(is_public=True)

    def perform_update(self, serializer):
        # Only owner can update
        obj = self.get_object()
        if obj.owner != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request, message="Only the owner can edit this model.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request, message="Only the owner can delete this model.")
        instance.delete()


class DecisionModelValidateView(APIView):
    """
    POST /api/models/validate/
    Body: { "schema": { ... } }
    Returns validation result without saving.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = DecisionModelValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "is_valid": serializer.validated_data["is_valid"],
                "errors": serializer.validated_data["errors"],
            },
            status=status.HTTP_200_OK,
        )


class CanConnectView(APIView):
    """
    POST /api/models/can-connect/
    Check whether a single edge would be valid in the given schema.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = CanConnectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            parsed = DecisionModelSchema.model_validate(data["schema"])
        except Exception as exc:
            return Response(
                {"is_valid": False, "errors": [{"code": "SCHEMA_PARSE_ERROR", "message": str(exc)}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = can_connect(
            parsed,
            source_node_id=data["source_node_id"],
            source_port_id=data["source_port_id"],
            target_node_id=data["target_node_id"],
            target_port_id=data["target_port_id"],
        )

        return Response(
            {
                "is_valid": result.is_valid,
                "errors": [
                    {
                        "code": e.code,
                        "message": e.message,
                        "edge_id": str(e.edge_id) if e.edge_id else None,
                        "source_node": str(e.source_node) if e.source_node else None,
                        "target_node": str(e.target_node) if e.target_node else None,
                        "details": e.details,
                    }
                    for e in result.errors
                ],
            },
            status=status.HTTP_200_OK,
        )


class DecisionModelRunValidationView(APIView):
    """
    POST /api/models/{id}/validate/
    Re-run validation on a stored model and persist the result.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            model = DecisionModel.objects.get(id=id)
        except DecisionModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if model.owner != request.user and not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        is_valid = model.run_full_validation(save=True)
        return Response(
            {
                "is_valid": is_valid,
                "errors": model.validation_errors,
            },
            status=status.HTTP_200_OK,
        )
