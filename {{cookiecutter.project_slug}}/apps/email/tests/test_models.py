import pytest
from django.utils.safestring import mark_safe

from apps.email.models import Email


@pytest.mark.django_db
def test_email_model_name():
    email = Email.objects.create(sender="test@test.com", recipients="test@test.com", subject="test")
    validation_str = f'Email from "{email.sender}" to "{email.recipients}" sent at %s about "{email.subject}"'
    assert str(email) == validation_str


@pytest.mark.django_db
def test_email_body_html():
    email = Email.objects.create(sender="test@test.com", recipients="test@test.com", subject="test", body="test<br/>")
    assert email.body_html == mark_safe(email.body)
