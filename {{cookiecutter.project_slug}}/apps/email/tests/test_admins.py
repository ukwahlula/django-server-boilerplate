import pytest
from django.contrib.admin.sites import AdminSite

from apps.email.admin import EmailAdmin
from apps.email.models import Email


@pytest.mark.django_db
def test_email_admin_qs(request, email, user):
    admin = EmailAdmin(model=Email, admin_site=AdminSite())
    request.user = user

    request.user.is_superuser = True
    assert admin.get_queryset(request).count() == 1

    request.user.is_superuser = False
    assert admin.get_queryset(request).count() == 1
