from functools import wraps
from unittest import mock

from django.test import override_settings

from apps.email.backends import EmailDatabaseBackend
from apps.email.tasks import send_email_task


def send_email_task_sync(*args, **kwargs):
    kwargs["connection"] = EmailDatabaseBackend()
    return send_email_task(*args, **kwargs)


@override_settings(EMAIL_BACKEND="apps.email.backends.EmailDatabaseBackend")
def patch_email(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with mock.patch("apps.email.tasks.send_email_task.delay", side_effect=send_email_task_sync):
            return func(*args, **kwargs)

    return wrapper
