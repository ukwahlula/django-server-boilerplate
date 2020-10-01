import pytest
from django.contrib.admin.sites import AdminSite

from apps.cms.admin import ContentAdmin
from apps.cms.models import Content


@pytest.mark.django_db
def test_cms_admin_qs(request, content):
    admin = ContentAdmin(model=Content, admin_site=AdminSite())

    assert admin.get_queryset(request).count() == 1
