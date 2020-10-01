import pytest
from django.conf import settings
from django.urls import reverse

from apps.sms.models import Sms
from apps.sms.tests.utils import patch_sms
from apps.users.models import User


@pytest.mark.django_db
def test_sign_in_email(api_client, user):
    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)


@pytest.mark.django_db
def test_sign_in_url(api_client, user):
    sign_in_url = reverse("users:signin")

    body = {"email": user.email, "password": "invalid"}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data

    body = {"email": "invalid", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data

    assert Sms.objects.all().count() == 0

    body = {"email": user.email, "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    assert Sms.objects.all().count() == 0


@pytest.mark.django_db
def test_sign_in_url_case(api_client, user):
    sign_in_url = reverse("users:signin")
    user.email = "case@case.com"
    user.save()

    body = {"email": user.email, "password": "invalid"}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data

    body = {"email": "invalid", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data

    assert Sms.objects.all().count() == 0

    body = {"email": "CaSe@CaSe.Com", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    assert Sms.objects.all().count() == 0


@pytest.mark.django_db
def test_sign_in_url_jwt_case(api_client, user):
    sign_in_url = reverse("users:signin-jwt-obtain")
    user.email = "case@case.com"
    user.save()

    body = {"username": user.email, "password": "invalid"}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 401, response.data

    body = {"username": "invalid", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 401, response.data

    assert Sms.objects.all().count() == 0

    body = {"username": "CaSe@CaSe.Com", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    assert Sms.objects.all().count() == 0


@pytest.mark.django_db
@patch_sms
def test_sign_in_url_2fa_admin_portal(api_client, user):
    sign_in_url = reverse("users:signin") + "?is_admin_portal=true"
    sign_in_url_2fa = reverse("users:signin-2fa")
    user.is_superuser = True
    user.is_2fa_enabled = True
    user.is_staff_of_admin_portal = True
    user.save()

    body = {"email": user.email, "password": "invalid"}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data

    body = {"email": "invalid", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.datas

    assert Sms.objects.all().count() == 0
    assert not user.phone_verification_code_2fa

    body = {"email": user.email, "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    assert Sms.objects.all().count() == 1
    user = User.objects.get(pk=user.pk)
    assert user.phone_verification_code_2fa

    response = api_client.post(sign_in_url_2fa, {"code": "invalid"})
    assert response.status_code == 400, response.data

    response = api_client.post(sign_in_url_2fa, {"code": user.phone_verification_code_2fa})
    assert response.status_code == 200, response.data


@pytest.mark.django_db
def test_sign_out(api_client, user):
    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)
    sign_out_url = reverse("users:signout")

    body = {}
    response = api_client.post(sign_out_url, body)
    assert response.status_code == 200, response.data
