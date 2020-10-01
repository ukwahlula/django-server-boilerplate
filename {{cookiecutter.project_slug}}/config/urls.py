from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

from apps.generic.views import HealthCheckView

admin.site.site_title = "{{cookiecutter.project_name}}"
admin.site.site_header = "{{cookiecutter.project_name}}"
admin.site.index_title = "{{cookiecutter.project_name}}"

urlpatterns = [
    path("admin_tools/", include("admin_tools.urls")),
    path("admin/", admin.site.urls),
    path("api/healthcheck/", HealthCheckView.as_view(), name="healthcheck"),
]

v1_urlpatterns = [
    path("api/v1/users/", include("apps.users.urls", namespace="users")),
    path("api/v1/storage/", include("apps.storage.urls", namespace="storage")),
]

urlpatterns += v1_urlpatterns

if settings.DEBUG:
    urlpatterns += [
        path("", lambda request: redirect("api/doc/", permanent=False)),
        path("api/doc/", include_docs_urls(title="API documentation", public=True)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
