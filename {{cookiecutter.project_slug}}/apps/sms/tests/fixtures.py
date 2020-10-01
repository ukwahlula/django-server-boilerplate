import pytest

from apps.sms.tests import factories


@pytest.fixture
def sms():
    return factories.SmsFactory()
