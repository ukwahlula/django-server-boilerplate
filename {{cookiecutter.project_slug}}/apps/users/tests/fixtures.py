import pytest

from .factories import UserFactory


@pytest.fixture
def user():
    user = UserFactory(username="test", email="test@test.com", is_active=True)
    return user


@pytest.fixture
def user_2():
    user = UserFactory(username="test_2", email="test_2@test.com", is_active=True)
    return user


@pytest.fixture
def user_signup():
    user = UserFactory(
        username="test", email="test@test.com", is_active=False, email_verification_code="email_verification_code"
    )
    return user
