"""
DRF serializers for Decision Models.
"""
from __future__ import annotations

from rest_framework import serializers

from .connection_rules import validate_connections
from .models import DecisionModel
from .schemas import DecisionModelSchema


class DecisionModelListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""

    owner_username = serializers.CharField(source="owner.username", read_only=True, default=None)

    class Meta:
        model = DecisionModel
        fields = (
            "id",
            "name",
            "description",
            "schema_version",
            "is_public",
            "is_valid",
            "tags",
            "owner",
            "owner_username",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class DecisionModelSerializer(serializers.ModelSerializer):
    """Full serializer – includes schema and validation state."""

    owner_username = serializers.CharField(source="owner.username", read_only=True, default=None)
    validation_errors = serializers.JSONField(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = DecisionModel
        fields = (
            "id",
            "name",
            "description",
            "notes",
            "schema",
            "schema_version",
            "is_public",
            "is_valid",
            "validation_errors",
            "tags",
            "owner",
            "owner_username",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "is_valid",
            "validation_errors",
            "owner",
            "created_at",
            "updated_at",
        )

    def validate_schema(self, value: dict) -> dict:
        """Structural validation via Pydantic."""
        if not value:
            return value
        try:
            DecisionModelSchema.model_validate(value)
        except Exception as exc:
            raise serializers.ValidationError(f"Invalid schema: {exc}") from exc
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["owner"] = request.user
        instance = super().create(validated_data)
        instance.run_full_validation(save=True)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.run_full_validation(save=True)
        return instance


class DecisionModelValidateSerializer(serializers.Serializer):
    """Accepts a raw schema and returns validation result (no save)."""

    schema = serializers.JSONField()

    def validate_schema(self, value: dict) -> dict:
        try:
            DecisionModelSchema.model_validate(value)
        except Exception as exc:
            raise serializers.ValidationError(f"Invalid schema structure: {exc}") from exc
        return value

    def validate(self, attrs):
        schema_data = attrs["schema"]
        parsed = DecisionModelSchema.model_validate(schema_data)
        result = validate_connections(parsed)
        attrs["is_valid"] = result.is_valid
        attrs["errors"] = [
            {
                "code": e.code,
                "message": e.message,
                "edge_id": str(e.edge_id) if e.edge_id else None,
                "source_node": str(e.source_node) if e.source_node else None,
                "target_node": str(e.target_node) if e.target_node else None,
                "details": e.details,
            }
            for e in result.errors
        ]
        return attrs


class CanConnectSerializer(serializers.Serializer):
    """Check if a single connection is allowed."""

    schema = serializers.JSONField()
    source_node_id = serializers.UUIDField()
    source_port_id = serializers.CharField()
    target_node_id = serializers.UUIDField()
    target_port_id = serializers.CharField()
