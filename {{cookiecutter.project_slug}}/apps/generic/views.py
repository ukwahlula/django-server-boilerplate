from django.conf import settings
from django.core.cache import cache
from django.db import connections as db_connections
from redis import from_url
from rest_framework import generics
from rest_framework.response import Response


class HealthCheckView(generics.GenericAPIView):
    def _healthcheck_db(self):
        try:
            conn = db_connections["default"]
            conn.cursor()
        except Exception:
            return False
        else:
            return True

    def _healthcheck_cache(self):
        try:
            cache.set("healthcheck", "itworks", 1)
            if not cache.get("healthcheck") == "itworks":
                return False
        except Exception:
            return False
        else:
            return True

    def _healthcheck_redis(self):
        redis_url = settings.CACHE_REDIS_LOCATION
        try:
            with from_url(redis_url) as conn:
                conn.ping()
        except Exception:
            return False
        else:
            return True

    def get(self, request, *args, **kwargs):
        status = 200
        response = {}
        response["db"] = self._healthcheck_db()
        response["cache"] = self._healthcheck_cache()
        response["redis"] = self._healthcheck_redis()
        if not response["db"] or not response["cache"] or not response["redis"]:
            status = 404
        return Response(response, status=status)
