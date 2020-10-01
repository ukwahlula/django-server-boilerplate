import pytest
from django.conf import settings
from django.urls import reverse

from .utils import generate_image_stub


@pytest.mark.django_db
def test_create_image_view_without_image(user, api_client):
    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)
    url = reverse("storage:image-create")
    response = api_client.post(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_image_view_permissions(api_client):
    url = reverse("storage:image-create")
    response = api_client.post(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_image_view(user, api_client):
    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)
    url = reverse("storage:image-create")
    response = api_client.post(url, {"image": generate_image_stub()})
    assert response.status_code == 201
