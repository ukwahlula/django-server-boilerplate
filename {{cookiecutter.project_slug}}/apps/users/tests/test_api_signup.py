import pytest
from django.conf import settings
from django.urls import reverse

from apps.email.models import Email
from apps.email.tests.utils import patch_email
from apps.push.tests.utils import patch_push
from apps.sms.models import Sms
from apps.sms.tests.utils import patch_sms
from apps.storage.models import Image
from apps.storage.tests.utils import generate_image_stub
from apps.users.models import User


@pytest.mark.django_db
def test_status(user_signup, api_client):
    url = reverse("users:signup-status", kwargs={"email_verification_code": "invalid"})
    response = api_client.get(url)
    assert response.status_code == 404

    url = reverse("users:signup-status", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["phone"] == user_signup.phone
    assert response.data["email"] == user_signup.email
    assert response.data["first_name"] == user_signup.first_name
    assert response.data["last_name"] == user_signup.last_name
    assert response.data["birthday"] == user_signup.birthday
    assert response.data["passport_number"] == user_signup.passport_number
    assert not response.data["is_passport_required"]
    assert response.data["is_profile_picture_required"]


@pytest.mark.django_db
def test_status_is_passport_required(user_signup, company, api_client):
    url = reverse("users:profile")
    response = api_client.get(url)
    assert response.status_code == 403

    company.is_passport_required = True
    company.save()
    user_signup.company = company
    user_signup.save()

    url = reverse("users:signup-status", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["is_passport_required"]


@pytest.mark.django_db
def test_status_is_profile_picture_required(user_signup, company, api_client):
    url = reverse("users:profile")
    response = api_client.get(url)
    assert response.status_code == 403

    company.is_profile_picture_required = False
    company.save()
    user_signup.company = company
    user_signup.save()

    url = reverse("users:signup-status", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.get(url)
    assert response.status_code == 200
    assert not response.data["is_profile_picture_required"]


@pytest.mark.django_db
@patch_sms
def test_signup_send_code(user_signup, api_client):
    url = reverse("users:signup-send-code", kwargs={"email_verification_code": "invalid"})
    response = api_client.patch(url, {})
    assert response.status_code == 404

    url = reverse("users:signup-send-code", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {})
    assert response.status_code == 200
    assert len(response.data) == 1

    assert Sms.objects.all().count() == 1

    phone_verification_code = User.objects.get(pk=user_signup.pk).phone_verification_code
    assert phone_verification_code is not None


@pytest.mark.django_db
@patch_sms
def test_signup_send_code_again(user_signup, api_client):
    url = reverse("users:signup-send-code", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {})
    assert response.status_code == 200
    assert len(response.data) == 1

    assert Sms.objects.all().count() == 1

    url = reverse("users:signup-send-code", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {})
    assert response.status_code == 200
    assert len(response.data) == 1

    assert Sms.objects.all().count() == 2

    phone_verification_code = User.objects.get(pk=user_signup.pk).phone_verification_code
    assert phone_verification_code is not None


@pytest.mark.django_db
def test_signup_verify_code(user_signup, api_client):
    user_signup.phone_verification_code = "123456"
    user_signup.save(update_fields=("phone_verification_code",))

    phone_verification_code = user_signup.phone_verification_code

    url = reverse("users:signup-verify-phone", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {"phone_verification_code": "000000"})
    assert response.status_code == 400

    user = User.objects.get(pk=user_signup.pk)
    assert not user.is_phone_verified
    assert user.phone_verification_code

    url = reverse("users:signup-verify-phone", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {"phone_verification_code": phone_verification_code})
    assert response.status_code == 200

    user = User.objects.get(pk=user_signup.pk)
    assert user.is_phone_verified
    assert user.phone_verification_code


@pytest.mark.django_db
@patch_email
def test_signup_send_email_400(company, api_client):
    signin_url = reverse("users:signup-send-email")
    response = api_client.post(
        signin_url, {"company_name": company.name, "company_password": "invalid", "email": "test@test.com"}
    )
    assert response.status_code == 400

    response = api_client.post(
        signin_url, {"company_name": "invalid", "password": settings.DEFAULT_PASSWORD, "email": "test@test.com"}
    )
    assert response.status_code == 400

    response = api_client.post(
        signin_url, {"company_name": "invalid", "password": settings.DEFAULT_PASSWORD, "email": "test@test.com"}
    )
    assert response.status_code == 400

    response = api_client.post(
        signin_url, {"company_name": company.name, "company_password": settings.DEFAULT_PASSWORD}
    )
    assert response.status_code == 400


@pytest.mark.django_db
@patch_email
def test_signup_send_email(user_signup, company, api_client):
    signup_url = reverse("users:signup-send-email")
    company.pin = "1234"
    company.save()
    response = api_client.post(
        signup_url, {"company_name": company.name, "company_password": "1234", "email": "email@test.com"}
    )
    assert response.status_code == 200
    user = User.objects.filter(email="email@test.com").first()
    assert user
    assert not user.is_email_verified
    assert user.email_verification_code
    assert Email.objects.filter(to_emails="email@test.com").exists()

    response = api_client.post(
        signup_url, {"company_name": company.name, "company_password": "1234", "email": user_signup.email}
    )
    assert response.status_code == 200
    user = User.objects.filter(pk=user_signup.pk).first()
    assert user
    assert not user.is_email_verified
    assert user.email_verification_code
    assert Email.objects.filter(to_emails=user.email).exists()


@pytest.mark.django_db
@patch_email
def test_signup_send_email_user_exists(user_signup, company, api_client):
    signup_url = reverse("users:signup-send-email")
    company.pin = "1234"
    company.save()
    User.objects.create(email="email_active@test.com", is_active=True)
    response = api_client.post(
        signup_url, {"company_name": company.name, "company_password": "1234", "email": "email_active@test.com"}
    )
    assert response.status_code == 400

    response = api_client.post(signup_url, {"company_password": "1234", "email": "email_active@test.com"})
    assert response.status_code == 400

    response = api_client.post(signup_url, {"company_password": "1234", "email": "email_active@test.com"})
    assert response.status_code == 400

    response = api_client.post(signup_url, {"email": "email_active@test.com"})
    assert response.status_code == 400

    response = api_client.post(signup_url, {})
    assert response.status_code == 400


@pytest.mark.django_db
@patch_email
def test_signup_send_email_email_case_sensitive(company, api_client):
    signin_url = reverse("users:signup-send-email")
    company.pin = "1234"
    company.save()
    response = api_client.post(
        signin_url, {"company_name": company.name, "company_password": "1234", "email": "Email@test.com"}
    )
    assert response.status_code == 200
    user = User.objects.filter(email="email@test.com").first()
    assert user
    assert not user.is_email_verified
    assert user.email_verification_code
    assert Email.objects.filter(to_emails="email@test.com").exists()

    signin_url = reverse("users:signup-send-email")
    response = api_client.post(
        signin_url, {"company_name": company.name, "company_password": "1234", "email": "Email@Test.com"}
    )
    assert response.status_code == 200
    user_2 = User.objects.filter(email="email@test.com").first()
    assert user.pk == user_2.pk


@pytest.mark.django_db
@patch_email
def test_signup_send_email_pin_case_sensitive(company, api_client):
    signin_url = reverse("users:signup-send-email")
    company.name = "Test"
    company.pin = "1234"
    company.save()
    response = api_client.post(
        signin_url, {"company_name": "test", "company_password": "1234", "email": "email@test.com"}
    )
    assert response.status_code == 200
    user = User.objects.filter(email="email@test.com").first()
    assert user
    assert not user.is_email_verified
    assert user.email_verification_code
    assert Email.objects.filter(to_emails="email@test.com").exists()

    response = api_client.post(
        signin_url, {"company_name": "test1", "company_password": "1234", "email": "email@test.com"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_verify_email(user_signup, api_client):
    user_signup.email_verification_code = "123456"
    user_signup.is_email_verified = False
    user_signup.save(update_fields=("email_verification_code", "is_email_verified"))

    email_verification_code = user_signup.email_verification_code

    url = reverse("users:signup-verify-email", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {"email_verification_code": "000000"})
    assert response.status_code == 400

    user = User.objects.get(pk=user_signup.pk)
    assert not user.is_email_verified
    assert user.email_verification_code

    url = reverse("users:signup-verify-email", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {"email_verification_code": email_verification_code})
    assert response.status_code == 200

    user = User.objects.get(pk=user_signup.pk)
    assert user.is_email_verified
    assert user.email_verification_code


@pytest.mark.django_db
def test_signup_password(user_signup, api_client):
    url = reverse("users:signup-password", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {"password": "new_password", "repeat_password": "new_password_invalid"})
    assert response.status_code == 400

    response = api_client.patch(url, {"password": "new_password", "repeat_password": ""})
    assert response.status_code == 400

    response = api_client.patch(url, {"password": "", "repeat_password": "new_password_invalid"})
    assert response.status_code == 400

    invalid_url = reverse("users:signup-password", kwargs={"email_verification_code": "invalid"})
    response = api_client.patch(invalid_url, {"password": "new_password", "repeat_password": "new_password"})
    assert response.status_code == 404

    response = api_client.patch(url, {"password": "new_password", "repeat_password": "new_password"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_avatar(user_signup, api_client):
    storage_url = reverse("storage:image-create-signup", kwargs={"email_verification_code": "invalid"})
    response = api_client.post(storage_url)
    assert response.status_code == 404

    storage_url = reverse(
        "storage:image-create-signup", kwargs={"email_verification_code": user_signup.email_verification_code}
    )
    response = api_client.post(storage_url, {"image": generate_image_stub()})
    assert response.status_code == 201

    image_pk = response.data["pk"]
    image = Image.objects.filter(creator=user_signup, pk=image_pk).first()
    assert image is not None

    url = reverse("users:signup-profile", kwargs={"email_verification_code": "invalid"})
    response = api_client.patch(url, {"avatar": image.pk})
    assert response.status_code == 404

    url = reverse("users:signup-profile", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {"avatar": image.pk})
    assert response.status_code == 200
    assert response.data["avatar"] == image.pk
    image_pk = User.objects.get(pk=user_signup.pk).avatar.pk
    assert image_pk == image.pk


@pytest.mark.django_db
@patch_push
def test_signup_contact_details(user_signup, api_client):
    url = reverse("users:signup-profile", kwargs={"email_verification_code": "invalid"})
    response = api_client.patch(url, {})
    assert response.status_code == 404

    email_verification_code = user_signup.email_verification_code

    url = reverse("users:signup-profile", kwargs={"email_verification_code": email_verification_code})
    response = api_client.patch(url, {"first_name": "first_name", "last_name": "last_name"})

    assert response.status_code == 200
    assert response.data["first_name"] == "first_name"
    assert response.data["last_name"] == "last_name"
    user = User.objects.get(pk=user_signup.pk)
    assert user.first_name == "first_name"
    assert user.last_name == "last_name"


@pytest.mark.django_db
def test_signup_finish(user_signup, api_client):
    url = reverse("users:signup-finish", kwargs={"email_verification_code": "invalid"})
    response = api_client.patch(url, {})
    assert response.status_code == 404

    user_signup.is_active = True
    user_signup.email_verification_code = "test"
    user_signup.phone_verification_code = "test"
    user_signup.save()
    url = reverse("users:signup-finish", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {})
    assert response.status_code == 404

    user_signup.is_active = False
    user_signup.save()
    url = reverse("users:signup-finish", kwargs={"email_verification_code": user_signup.email_verification_code})
    response = api_client.patch(url, {})
    assert response.status_code == 200
    user = User.objects.get(pk=user_signup.pk)
    assert user.is_active
    assert not user.email_verification_code
    assert not user.phone_verification_code
