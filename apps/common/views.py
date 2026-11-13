from django.db import connection
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Simple health endpoint used by Docker healthcheck and load balancers.
    Checks database connectivity.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        status = "ok"
        db_ok = False

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_ok = True
        except Exception:
            status = "degraded"

        payload = {
            "status": status,
            "database": "ok" if db_ok else "unavailable",
            "service": "makedecision-backend",
        }

        http_status = 200 if db_ok else 503
        return JsonResponse(payload, status=http_status)
