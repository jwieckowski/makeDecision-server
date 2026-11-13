from rest_framework import serializers


class MethodMetaSerializer(serializers.Serializer):
    name = serializers.CharField()
    label = serializers.CharField()
    category = serializers.CharField()
    extension = serializers.CharField()
    source_package = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    params_schema = serializers.DictField()
    tags = serializers.ListField(child=serializers.CharField(), required=False)


class MethodRunSerializer(serializers.Serializer):
    name = serializers.CharField()
    extension = serializers.CharField(default="crisp")
    matrix = serializers.JSONField(required=False, allow_null=True)
    criteria_types = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_null=True
    )
    weights = serializers.JSONField(required=False, allow_null=True)
    params = serializers.DictField(required=False, default=dict)
    extras = serializers.DictField(required=False, default=dict)
