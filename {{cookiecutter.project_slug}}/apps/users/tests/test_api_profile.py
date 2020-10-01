import pytest
from django.conf import settings
from django.urls import reverse

from apps.generic.choices import PrivacyChoices
from apps.sample.models import SampleSalivaTest
from apps.storage.models import Image
from apps.storage.tests.utils import generate_image_stub
from apps.users.models import User


@pytest.mark.django_db
def test_profile(user, api_client):
    url = reverse("users:profile")
    response = api_client.get(url)
    assert response.status_code == 403

    user.employee_id = "employee_id"
    user.passport_number = "passport_number"
    user.share_personal_info_data = PrivacyChoices.MY_ENTIRE_TEST_HISTORY
    user.save()

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["phone"] == user.phone
    assert response.data["email"] == user.email
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name
    assert response.data["employee_id"] == user.employee_id
    assert response.data["passport_number"] == user.passport_number
    assert response.data["share_personal_info_data"] == PrivacyChoices.MY_ENTIRE_TEST_HISTORY
    assert response.data["company_length"] == 3
    assert not response.data["is_passport_required"]
    assert response.data["is_profile_picture_required"]


@pytest.mark.django_db
def test_profile_company_length(user, company, api_client):
    url = reverse("users:profile")
    response = api_client.get(url)
    assert response.status_code == 403

    company.company_length = 5
    company.save()
    user.company = company
    user.save()

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["company_length"] == 5


@pytest.mark.django_db
def test_profile_is_passport_required(user, company, api_client):
    url = reverse("users:profile")
    response = api_client.get(url)
    assert response.status_code == 403

    company.is_passport_required = True
    company.save()
    user.company = company
    user.save()

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["is_passport_required"]


@pytest.mark.django_db
def test_profile_sample(user, company, api_client):
    url = reverse("users:profile")

    sample = SampleSalivaTest.objects.create(user=user)

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["sample"]["pk"] == str(sample.pk)

    sample_last = SampleSalivaTest.objects.create(user=user)

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["sample"]["pk"] == str(sample_last.pk)


@pytest.mark.django_db
def test_profile_password(user, api_client):
    url = reverse("users:profile-password")
    response = api_client.patch(url, {"password": "new_password", "repeat_password": "new_password_invalid"})
    assert response.status_code == 403

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)
    response = api_client.patch(url, {"password": "new_password", "repeat_password": ""})
    assert response.status_code == 400

    response = api_client.patch(url, {"password": "", "repeat_password": "new_password_invalid"})
    assert response.status_code == 400

    response = api_client.patch(url, {"password": "new_password", "repeat_password": "new_password"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_update(user, api_client):
    url = reverse("users:profile-update")
    response = api_client.patch(url, {})
    assert response.status_code == 403

    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.patch(
        url,
        {
            "first_name": "first_name",
            "last_name": "last_name",
            "share_personal_info": True,
            "share_personal_info_data": PrivacyChoices.MY_ENTIRE_TEST_HISTORY,
            "passport_number": "passport_number_test",
        },
    )
    assert response.status_code == 200
    assert response.data["first_name"] == "first_name"
    assert response.data["last_name"] == "last_name"
    assert response.data["passport_number"] == "passport_number_test"
    assert response.data["share_personal_info"]
    assert response.data["share_personal_info_data"] == PrivacyChoices.MY_ENTIRE_TEST_HISTORY
    user = User.objects.get(pk=user.pk)
    assert user.first_name == "first_name"
    assert user.last_name == "last_name"
    assert user.passport_number == "passport_number_test"
    assert user.share_personal_info
    assert user.share_personal_info_data == PrivacyChoices.MY_ENTIRE_TEST_HISTORY

    response = api_client.patch(
        url, {"first_name": "first_name", "last_name": "last_name", "share_personal_info": True}
    )
    assert response.status_code == 200
    assert response.data["first_name"] == "first_name"
    assert response.data["last_name"] == "last_name"
    assert response.data["share_personal_info"]
    user = User.objects.get(pk=user.pk)
    assert user.first_name == "first_name"
    assert user.last_name == "last_name"
    assert user.share_personal_info


@pytest.mark.django_db
def test_profile_avatar(user, api_client):
    url = reverse("users:profile-update")
    storage_url = reverse("storage:image-create")
    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    response = api_client.post(storage_url, {"image": generate_image_stub()})
    assert response.status_code == 201

    image_pk = response.data["pk"]
    image = Image.objects.filter(creator=user, pk=image_pk).first()
    assert image is not None

    response = api_client.patch(url, {"avatar": image.pk})
    assert response.status_code == 200
    assert response.data["avatar"] == image.pk
    image_pk = User.objects.get(pk=user.pk).avatar.pk
    assert image_pk == image.pk


@pytest.mark.django_db
def test_destroy_profile(user, api_client):
    api_client.login(username=user.username, password=settings.DEFAULT_PASSWORD)

    url = reverse("users:profile-destroy")
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_destroy_profile_view_permissions(user, api_client):
    url = reverse("users:profile-destroy")
    response = api_client.delete(url)
    assert response.status_code == 403
