from .base import *  # noqa

CELERY_ALWAYS_EAGER = True
DEBUG = False
TEMPLATES[0]["OPTIONS"]["debug"] = False  # noqa

DEFAULT_PASSWORD = "test_password"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
