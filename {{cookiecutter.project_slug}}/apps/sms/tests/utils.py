from functools import wraps
from unittest import mock

from django.test import override_settings

from apps.sms.tasks import send_sms_task


def send_sms_task_sync(*args, **kwargs):
    return send_sms_task(*args, **kwargs)


@override_settings(SMS_BACKEND="apps.sms.backends.SmsDatabaseBackend")
def patch_sms(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with mock.patch("apps.sms.tasks.send_sms_task.delay", side_effect=send_sms_task_sync):
            return func(*args, **kwargs)

    return wrapper
