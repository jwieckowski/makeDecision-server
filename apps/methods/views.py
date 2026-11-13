from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MethodMetaSerializer, MethodRunSerializer
from .services import list_available_methods, run_method


class MethodListView(APIView):
    """
    GET /api/methods/
    Query params (optional):
      - category: mcda | weights | ranking | correlation | sensitivity | ...
      - extension: crisp | fuzzy | intuitionistic
      - source_package: pymcdm | pyfdm | custom | ...
    """

    permission_classes = [AllowAny]

    def get(self, request):
        category = request.query_params.get("category")
        extension = request.query_params.get("extension")
        source = request.query_params.get("source_package")

        methods = list_available_methods(
            category=category,
            extension=extension,
            source_package=source,
        )
        serializer = MethodMetaSerializer(methods, many=True)
        return Response(
            {
                "count": len(methods),
                "results": serializer.data,
            }
        )


class MethodRunView(APIView):
    """
    POST /api/methods/run/
    Run a single method (useful for testing / simple calls).
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = MethodRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = run_method(
            name=data["name"],
            extension=data.get("extension", "crisp"),
            matrix=data.get("matrix"),
            criteria_types=data.get("criteria_types"),
            weights=data.get("weights"),
            params=data.get("params") or {},
            extras=data.get("extras") or {},
        )

        payload = {
            "success": result.success,
            "preference": result.preference,
            "ranking": result.ranking,
            "weights": result.weights,
            "correlation": result.correlation,
            "sensitivity": result.sensitivity,
            "extras": result.extras,
            "error": result.error,
            "meta": result.meta,
        }
        http_status = status.HTTP_200_OK if result.success else status.HTTP_400_BAD_REQUEST
        return Response(payload, status=http_status)
