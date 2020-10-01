import pytest
from django.contrib.admin.sites import AdminSite

from apps.sms.admin import SmsAdmin
from apps.sms.models import Sms


@pytest.mark.django_db
def test_sms_admin_qs(request, sms, user):
    admin = SmsAdmin(model=Sms, admin_site=AdminSite())
    request.user = user

    request.user.is_superuser = True
    assert admin.get_queryset(request).count() == 1

    request.user.is_superuser = False
    assert admin.get_queryset(request).count() == 1
