import pytest
from django.conf import settings
from django.urls import reverse

from apps.users.models import User


@pytest.mark.django_db
def test_profile_update_backward_compatibility(user, api_client):
    url = reverse("users:profile-password")
    response = api_client.patch(url, {})
    assert response.status_code == 403

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.patch(url, {"password": "test", "repeat_password": "test_diff"})
    assert response.status_code == 400

    response = api_client.patch(url, {"password": "test", "repeat_password": "test"})
    assert response.status_code == 200

    user = User.objects.get(pk=user.pk)
    assert not user.check_password(settings.DEFAULT_PASSWORD)
    assert user.check_password("test")


@pytest.mark.django_db
def test_profile_update(user, api_client):
    url = reverse("users:profile-password")
    response = api_client.patch(url, {})
    assert response.status_code == 403

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.patch(url, {"current_password": "invalid", "password": "test", "repeat_password": "test"})
    assert response.status_code == 400

    response = api_client.patch(
        url, {"current_password": settings.DEFAULT_PASSWORD, "password": "test", "repeat_password": "test_diff"}
    )
    assert response.status_code == 400

    response = api_client.patch(
        url, {"current_password": settings.DEFAULT_PASSWORD, "password": "test", "repeat_password": "test"}
    )
    assert response.status_code == 200

    user = User.objects.get(pk=user.pk)
    assert not user.check_password(settings.DEFAULT_PASSWORD)
    assert user.check_password("test")
