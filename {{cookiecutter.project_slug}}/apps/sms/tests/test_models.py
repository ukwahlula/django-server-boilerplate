import pytest


@pytest.mark.django_db
def test_sms_model_name(sms):
    assert str(sms) == f"Sms {sms.phone}: {sms.sms}"
