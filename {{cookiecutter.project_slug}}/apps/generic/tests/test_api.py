import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_healthcheck(api_client):
    url = reverse("healthcheck")
    response = api_client.get(url)
    assert response.status_code == 404
