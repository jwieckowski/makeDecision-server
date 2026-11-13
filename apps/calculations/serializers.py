from rest_framework import serializers

from .models import CalculationRun


class CalculationRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationRun
        fields = (
            "id",
            "decision_model",
            "owner",
            "status",
            "input_schema",
            "result",
            "error_message",
            "celery_task_id",
            "started_at",
            "finished_at",
            "created_at",
        )
        read_only_fields = (
            "id",
            "owner",
            "status",
            "result",
            "error_message",
            "celery_task_id",
            "started_at",
            "finished_at",
            "created_at",
        )


class CalculationRunCreateSerializer(serializers.Serializer):
    """
    Create a run from a stored DecisionModel and/or inline schema.
    """

    decision_model_id = serializers.UUIDField(required=False, allow_null=True)
    schema = serializers.JSONField(required=False, allow_null=True)
    async_mode = serializers.BooleanField(default=True)

    def validate(self, attrs):
        if not attrs.get("decision_model_id") and not attrs.get("schema"):
            raise serializers.ValidationError(
                "Provide decision_model_id or schema (or both)."
            )
        return attrs
