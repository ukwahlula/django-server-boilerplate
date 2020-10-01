import pytest
from django.db.utils import IntegrityError

from apps.users.models import User


@pytest.mark.django_db
def test_user_model_name(user):
    assert str(user) == user.full_name


@pytest.mark.django_db
def test_user_same_email(user):
    User.objects.create(email="test1@test.com")
    with pytest.raises(IntegrityError):
        User.objects.create(email="test1@test.com")
