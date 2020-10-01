import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group

from apps.company.tests.factories import CompanyFactory
from apps.users.admin import UserAdmin
from apps.users.models import User
from apps.users.presets import GROUP_MANAGER_JUNIOR, GROUP_MANAGER_SENIOR

from .factories import UserFactory


@pytest.mark.django_db
def test_user_admin_qs(request, user):
    company = CompanyFactory()
    user.company = company
    user.save(update_fields=("company",))
    UserFactory(company=company)
    UserFactory()

    admin = UserAdmin(model=User, admin_site=AdminSite())
    request.user = user
    request.user.company = company

    request.user.is_superuser = True
    assert admin.get_queryset(request).count() == 3

    request.user.is_superuser = False
    assert admin.get_queryset(request).count() == 1

    request.user.is_superuser = False
    request.user.is_staff = True
    request.user.groups.set([Group.objects.create(name=GROUP_MANAGER_JUNIOR)])
    assert request.user.has_group(GROUP_MANAGER_JUNIOR)
    assert admin.get_queryset(request).count() == 3

    request.user.groups.set([Group.objects.create(name=GROUP_MANAGER_SENIOR)])
    assert request.user.has_group(GROUP_MANAGER_SENIOR)
    assert admin.get_queryset(request).count() == 3
