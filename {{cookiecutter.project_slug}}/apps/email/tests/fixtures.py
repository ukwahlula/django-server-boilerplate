import pytest

from apps.email.tests import factories


@pytest.fixture
def email():
    return factories.EmailFactory()
