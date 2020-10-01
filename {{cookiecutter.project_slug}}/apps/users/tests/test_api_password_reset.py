import pytest
from django.conf import settings
from django.urls import reverse

from apps.email.models import Email
from apps.email.tests.utils import patch_email
from apps.users.models import User


@pytest.mark.django_db
def test_password_reset_empty_email(user, api_client):
    password_reset_url = reverse("users:reset-password")
    email_qs = Email.objects.filter(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email)
    data = {"email": ""}
    response = api_client.post(password_reset_url, data)
    assert response.status_code == 400, response.data
    assert not email_qs.exists()


@pytest.mark.django_db
@patch_email
def test_password_reset_invalid_email(user, api_client):
    password_reset_url = reverse("users:reset-password")
    email_qs = Email.objects.filter(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email)
    data = {"email": "invalid@email.com"}
    response = api_client.post(password_reset_url, data)
    assert response.status_code == 200, response.data
    assert not email_qs.exists()


@pytest.mark.django_db
@patch_email
def test_password_reset(user, api_client):
    password_reset_url = reverse("users:reset-password")
    data = {"email": user.email}
    response = api_client.post(password_reset_url, data)
    assert response.status_code == 200, response.data
    assert Email.objects.filter(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email).exists()

    user = User.objects.filter(pk=user.pk).first()
    assert user is not None
    assert user.reset_password_code is not None


@pytest.mark.django_db
def test_password_reset_verify_invalid_code(user, api_client):
    data = {"new_password": "new12345", "repeat_new_password": "new12345"}
    response = api_client.put(reverse("users:reset-password-verify", kwargs={"reset_password_code": "invalid"}), data)
    assert response.status_code == 404, response.data
    assert not api_client.login(username=user.email, password="new12345")


@pytest.mark.django_db
def test_password_reset_verify_empty_repeate_pass(user, api_client):
    user.reset_password_code = "reset_password_code"
    user.save(update_fields=("reset_password_code",))
    password_reset_verify_url = reverse(
        "users:reset-password-verify", kwargs={"reset_password_code": user.reset_password_code}
    )

    data = {"password": "new12345", "repeat_password": ""}
    response = api_client.put(password_reset_verify_url, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")


@pytest.mark.django_db
def test_password_reset_verify_empty_pass(user, api_client):
    user.reset_password_code = "reset_password_code"
    user.save(update_fields=("reset_password_code",))
    password_reset_verify_url = reverse(
        "users:reset-password-verify", kwargs={"reset_password_code": user.reset_password_code}
    )

    data = {"password": "", "repeat_password": "new12345"}
    response = api_client.put(password_reset_verify_url, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")


@pytest.mark.django_db
def test_password_reset_verify_diff_pass(user, api_client):
    user.reset_password_code = "reset_password_code"
    user.save(update_fields=("reset_password_code",))
    password_reset_verify_url = reverse(
        "users:reset-password-verify", kwargs={"reset_password_code": user.reset_password_code}
    )

    data = {"password": "new12345", "repeat_password": "new123456"}
    response = api_client.put(password_reset_verify_url, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")


@pytest.mark.django_db
def test_password_reset_verify(user, api_client):
    user.reset_password_code = "reset_password_code"
    user.save(update_fields=("reset_password_code",))
    password_reset_verify_url = reverse(
        "users:reset-password-verify", kwargs={"reset_password_code": user.reset_password_code}
    )

    data = {"password": "new12345", "repeat_password": "new12345"}
    response = api_client.put(password_reset_verify_url, data)
    assert response.status_code == 200, response.data
    assert api_client.login(username=user.email, password="new12345")
