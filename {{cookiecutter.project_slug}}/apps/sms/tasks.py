from celery import shared_task
from django.conf import settings
from django.core.mail import get_connection


@shared_task
def task_send_sms(sms_data):
    connection = get_connection(settings.SMS_BACKEND)
    for phone in sms_data:
        sms = sms_data[phone]
        connection.send(phone, sms)
